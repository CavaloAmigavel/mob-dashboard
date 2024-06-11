# dashboard

## Project setup

```
git clone https://github.com/CavaloAmigavel/mob-dashboard
cd mob-dashboard
npm install
```

## Prepare Envirement Variables

```
cp .env.example .env
```

```
nano .env
```

```
#Exemple
VUE_APP_ACME_CSE=cse-mn
VUE_APP_ACME_URL=http://10.20.140.120:8000 #IP of ACME Server
VUE_APP_MQTT_URL=mqtt://10.20.140.120:1883 #IP of MQTT Server
VUE_APP_MQTT_IP=10.20.140.133 #Ip of the "monitor.py"
VUE_APP_MQTT_PORT=8088  #PORT of the "monitor.py" for WS
```

### Compiles and hot-reloads for development and testing

```
npm run serve
```

### Compiles and minifies for production

```
npm run build
```
