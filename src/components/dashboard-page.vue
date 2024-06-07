<template>

	<div id="grad" class="container-fluid p-5 text-white text-center">
		<h1>Smart Display</h1>
		<p>Showing what is Connected</p>
	</div>


  <div class="container mt-4">
    <div class="row gx-4 gy-4">
      <div
        v-for="(ae, index) in aesArray"
        :key="index"
        class="col-12 col-sm-6 col-md-4 col-lg-3"
      >
        <AEContainer :ae="ae" />
      </div>
    </div>
  </div>
</template>

<script>
import AEContainer from "./card/AEContainer.vue"; // Import the AeContainer component
import { useMessageStore } from "../stores/messageStore";

export default {
  components: {
    AEContainer, // Register the AeContainer component
  },
  name: "DashboardPage",
  data() {
    return {
      aes: null,
      cards: [
        { title: "Card 1", content: "Some content for card 1." },
        { title: "Card 2", content: "Some content for card 2." },
        { title: "Card 3", content: "Some content for card 3." },
        { title: "Card 4", content: "Some content for card 4." },
        { title: "Card 5", content: "Some content for card 5." },
        // Add more cards as needed
      ],
    };
  },
  computed: {
    aesArray() {
      if (this.aes && Array.isArray(this.aes["m2m:uril"])) {
        return this.aes["m2m:uril"];
      }
      return [];
    },
  },
  methods: {
    fetchAE() {
      const options = {
        method: "GET",
        headers: {
          "X-M2M-Origin": "CAdmin",
          "X-M2M-RI": "123",
          "X-M2M-RVI": "3",
        },
      };
      fetch(`/acme${process.env.VUE_APP_ACME_CSE}?fu=1&ty=2`, options)
        .then((response) => response.json())
        .then((response) => {
          this.aes = response;
        })
        .catch((err) => console.error(err));
    },
    connectWebSocket() {
      this.ws = new WebSocket(
        `ws://${process.env.VUE_APP_MQTT_IP}:${process.env.VUE_APP_MQTT_PORT}`
      );

      this.ws.onopen = () => {
        console.log("WebSocket connection opened.");
        this.subscribeToChannel("m2m");
      };

      this.ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data);
          console.log("message", message);
          const messageStore = useMessageStore();
          messageStore.addMessage(message);
        } catch (error) {
          console.error("Failed to parse WebSocket message", error);
        }
      };

      this.ws.onclose = () => {
        console.log("WebSocket connection closed.");
      };

      this.ws.onerror = (error) => {
        console.error("WebSocket error:", error);
      };
    },
    subscribeToChannel(channel) {
      const message = { action: "subscribe", channel: channel };
      this.ws.send(JSON.stringify(message));
      console.log(`Subscribed to channel: ${channel}`);
    },
  },
  mounted() {
    this.fetchAE();
    this.connectWebSocket();
  },
  beforeUnmount() {
    if (this.ws) {
      this.ws.close();
    }
  },

};
</script>

<style scoped>
#grad {
  background: linear-gradient(to right, #00b16a, #009358);
}

.card {
  display: block;
  margin-bottom: 20px;
  line-height: 1.42857143;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 5px 0 rgba(0, 0, 0, 0.16), 0 2px 10px 0 rgba(0, 0, 0, 0.12);
  transition: box-shadow 0.25s;
}

.card:hover {
  box-shadow: 0 8px 17px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
}

.card-title {
  margin-top: 0px;
  font-weight: 700;
  font-size: 1.4em;
}

h1 {
	font-family: "Brush Script MT", cursive;
}
</style>
