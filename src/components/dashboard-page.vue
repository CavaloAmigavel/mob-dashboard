<template>
  <div class="container-fluid p-5 bg-success text-white text-center">
    <h1>ACME Monitor</h1>
    <p>Showing what is Connected</p>
  </div>

  <div class="container-fluid d-flex mt-5 justify-content-center">
    <AEContainer v-for="(ae, index) in aesArray" :key="index" :ae="ae" />
  </div>
</template>

<script>
import "bootstrap/dist/css/bootstrap.css";
import AEContainer from "./card/AEContainer.vue"; // Import the AeContainer component

export default {
  components: {
    AEContainer, // Register the AeContainer component
  },
  name: "DashboardPage",
  data() {
    return {
      aes: null,
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
  },
  mounted() {
    this.fetchAE();
  },
};
</script>
