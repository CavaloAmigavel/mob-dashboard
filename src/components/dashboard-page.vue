<template>
  <div id="grad" class="container-fluid p-5 text-white text-center">
    <h1>ACME Monitor</h1>
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
import mqtt from "mqtt"; // Import MQTT
import AEContainer from "./card/AEContainer.vue"; // Import the AeContainer component

export default {
  components: {
    AEContainer, // Register the AeContainer component
  },
  name: "DashboardPage",
  data() {
    return {
      connection: {
        protocol: "mqtt",
        host: process.env.VUE_APP_MQTT_IP,
        port: process.env.VUE_APP_MQTT_PORT,
        clean: true,
        connectTimeout: 30 * 1000, // ms
        reconnectPeriod: 4000, // ms
        clientId: "smart_display_agent", // Your client ID
      },
      subscription: {
        topic: "#", // Subscribe to all topics
        qos: 0, // Quality of Service (0, 1, or 2)
      },
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
    connectToMQTTBroker() {
      const client = mqtt.connect("mqtt://10.20.140.120:1883"); // Use mqtt:// protocol

      client.on("connect", () => {
        console.log("Connected to MQTT broker!");
        client.subscribe(this.subscription.topic, {
          qos: this.subscription.qos,
        });
      });

      client.on("message", (topic, message) => {
        console.log(
          `Received message on topic ${topic}: ${message.toString()}`
        );
      });

      client.on("error", (error) => {
        console.error("MQTT error:", error);
        // Handle errors gracefully
      });
    },
  },

  mounted() {
    this.fetchAE();
    this.connectToMQTTBroker();
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
</style>
