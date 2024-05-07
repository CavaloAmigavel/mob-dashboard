<template>
  <div class="card text-center" style="width: 200px">
    <div class="card-body">
      <h4 class="card-title">{{ ae_ri }}</h4>
    </div>
  </div>
</template>

<script>
export default {
  name: "ConContainer",
  props: {
    ae: {
      type: String,
      required: true,
    },
    con: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      cins: null,
    };
  },
  computed: {
    //AE Resource Indentifier
    ae_ri() {
      return this.ae.split("/")[1];
    },
    conArray() {
      return this.cons["m2m:uril"].map((uri) => uri.split("/").pop());
    },
  },

  methods: {
    fetchCIN() {
      const options = {
        method: "GET",
        headers: {
          "X-M2M-Origin": "CAdmin",
          "X-M2M-RI": "123",
          "X-M2M-RVI": "3",
        },
      };
      fetch(`/acme${this.ae}?fu=1&ty=3`, options)
        .then((response) => response.json())
        .then((response) => {
          console.log(response);
          this.cons = response;
        })
        .catch((err) => console.error(err));
    },
  },
  mounted() {
    //this.fetchCIN();
  },
};
</script>
