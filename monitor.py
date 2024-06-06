from zeroconf import IPVersion, ServiceInfo, Zeroconf
import requests, socket, json, atexit, threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from time import sleep
import asyncio
import websockets

_isEnabled = False
_host = None
_callback = None
_notificationURI = None
_name = None
_portCSE = 8000
_portNoti = 3000

_wsPort = 8088
_wsServer = None
_wsServerTask = None
_wsServerThread = None



##vai buscar o ip da interface de rede certa (podia-se alterar o /etc/hosts mas meh! assim tb da)
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
    local_ip_address = s.getsockname()[0]
    return local_ip_address

def setupNotifications(callback=None, host='127.0.0.1', port=1400, flag = 0):

	
	# Initialize configuration, possible a new configuration

	if not host:
		print("error!")
	if port == -1:
		print("error!")
	_host = host
	_portNoti = port
	_callback = callback
	_notificationURI = 'http://' + _host + ':' + str(_portNoti)
	_startNotificationServer()
	enableNotifications()
	print("Notification server running on port {}".format(_portNoti))
	return True


def enableNotifications():
	"""
	Enable the notification handling again, after disabling them with the
	`onem2mlib.notifications.disableNotifications`() method.
	"""
	#print("estou a arrancar!")
	global _isEnabled
	if _isEnabled:
		return
	_isEnabled = True
	

def disableNotifications():
	"""
	Disable the notification handling for a short time. This does **not** shut down the
	http server or removes subscriptions from resources in the CSE. It just stops the 
	processing of notifications and the calling of the callback functions.
	Processing and callback can be re-enabled with the `onem2mlib.notifications.enableNotifications`()
	method.
	"""
	global _isEnabled
	if not _isEnabled:
		return
	_isEnabled = False


@atexit.register
def shutdownNotifications():
	""" 
	Shutdown the notification sub-module and the http server. It also removes subscriptions
	created through the `onem2mlib.ResourceBase.subscribe`() method. After this no more 
	notifications can be received through the sub-module.
	**Note**
	This function is automatically called when the parent program terminates.
	"""
	global _notificationURI

	if not _notificationURI:
		return
	disableNotifications()
	_notificationURI = None
	_stopNotificationServer()


def isNotificationEnabled():
	""" Boolean. Return the status whether notifications are currently enabled. """
	return _isEnabled


def getNotificationURI():
	""" String. Return the current notificationURI, or None when notifications are disabled. """
	return _notificationURI

###############################################################################
#
#	Notification callback server
#
#	This is actually a simple HTTP server
#

_server = None
_thread = None


# Start the notification server in a background thread
def _startNotificationServer():
	global _server, _thread
	if _thread:
		return
	# Start processing requests in a separate thread.
	# Listen on any interface/IP address.
	# TODO: Make this configurable
	_server = HTTPNotificationServer(('', _portNoti), HTTPNotificationHandler)
	_thread = threading.Thread(target=_server.run)
	_thread.start()


# Stop the thread/notification server
def _stopNotificationServer():
	global _server, _thread
	if not _server or not _thread:
		return
	# Shutdown server
	_server.shutdown()
	_thread.join()
	_server = None
	_thread = None



# This class implements the notification server that runs in the background.
class HTTPNotificationServer(HTTPServer):
	def run(self):
		try:
			self.serve_forever()
		finally:
			# Clean-up server (close socket, etc.)
			self.server_close()

def getALLSubElementsJSON(jsn, name):
	result = []
	for elemName in jsn:
		elem = jsn[elemName]
		if elemName == name:
			result.append(elem)
		elif isinstance(elem, dict):
			result.extend(getALLSubElementsJSON(elem, name))
		elif isinstance(elem, list):
			for e in elem:
				if isinstance(e, dict):
					result.extend(getALLSubElementsJSON(e, name))
	return result

# This class implements the handler that reseives the requests
class HTTPNotificationHandler(BaseHTTPRequestHandler):
	def get_ip():
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
		local_ip_address = s.getsockname()[0]
		return local_ip_address

	# Handle incoming notifications (POST requests)
	def do_POST(self):
			# Construct return header
			self.send_response(200)
			self.send_header('X-M2M-RSC', '2000')
			ri = self.headers['X-M2M-RI']
			self.send_header('X-M2M-RI', ri)
			self.end_headers()

			# Get headers and content data
			length = int(self.headers['Content-Length'])
			contentType = self.headers['Content-Type']
			post_data = self.rfile.read(length)
			#print("post data:",post_data)
			#print(self.headers['X-M2M-RI'])
			if _isEnabled:
				# Handle notification in the background when enabled
				threading.Thread(target=self._handleJSON, args=(post_data, get_ip())).start()
			

	# Catch and ignore all log messages
	def log_message(self, format, *args):
		return

	# Handle JSON notifications 
	def _handleJSON(self, data, host):
		jsn =  json.loads(data.decode('utf-8'))
		print("json", jsn)
		nev= getALLSubElementsJSON(jsn, 'nev')
		if len(nev) > 0:
			cin = nev[0].get('rep', {}).get('m2m:cin', {})
			if cin:
				#print("[CIN]", cin)
				# Check if WebSocket server is running and send data
				print("#1",host)
				asyncio.run(self.sendToWebSocket(cin, host))
		#check verification request
		vrq = getALLSubElementsJSON(jsn, 'vrq')
		if len(vrq) == 0:										# TODO remove later when om2m corrects this
			vrq = getALLSubElementsJSON(jsn, 'm2m:vrq')
		if len(vrq) > 0 and vrq[0] == True:
			return 	# do nothing

		#get the sur first
		sur = getALLSubElementsJSON(jsn, 'sur')
		if len(sur) == 0:										# TODO remove later when om2m corrects this
			sur = getALLSubElementsJSON(jsn, 'm2m:sur')
		if len(sur) > 0:
			sur = sur[0]
		else:
			return 	# must have a subscription ID
		
	async def sendToWebSocket(self, data, host, channel="m2m"):
		global _wsServerTask, _wsPort
		if _wsServerTask and not _wsServerTask.done():
			try:
				async with websockets.connect(f'ws://{host}:{_wsPort}') as websocket:
					message = {"action": "publish", "channel": channel, "data": data}
					await websocket.send(json.dumps(message))
					print("Sent m2m:cin data to WebSocket server")
			except Exception as e:
				print(f"Error sending data to WebSocket server: {e}")
		else:
			print("WebSocket server is not running")
		
		
# WebSocket setup function
def setupWebSocket(local_ip, port=8088):
    global _wsServer, _wsServerTask, _wsServerThread
    if _wsServer:
        return

    async def websocketHandler(websocket, path):
        async for message in websocket:
            print(f"Received message: {message}")
            await websocket.send(f"Echo: {message}")

    async def startServer():
        async with websockets.serve(websocketHandler, local_ip, port):
            await asyncio.Future()  # Run forever

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    _wsServerTask = loop.create_task(startServer())
    _wsServerThread = threading.Thread(target=loop.run_forever)
    _wsServerThread.start()
    print(f"WebSocket server running on {local_ip}:{port}")

def shutdownWebSocketServer():
    global _wsServerTask, _wsServerThread
    if _wsServerTask and _wsServerThread:
        _wsServerTask.cancel()
        _wsServerThread.join()
        _wsServerTask = None
        _wsServerThread = None
        print("WebSocket server shut down")

if __name__ == '__main__':

    local_ip = get_ip()
    print("Notification server running on ip {}".format(local_ip))    
    setupWebSocket(local_ip, _wsPort)
    setupNotifications(None, local_ip, _portNoti, 0)
    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        print("Unregistering...")
        Zeroconf.unregister_service(info)
        Zeroconf.close()
        shutdownWebSocketServer()
        shutdownNotifications()
  
