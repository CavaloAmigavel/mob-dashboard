<template>
  <div class="card text-center bg-light w-100" style="margin-bottom: 10px">
    <div class="card-body">
      <h5 class="card-title">{{ con }}</h5>

      <div v-if="hasPi === null">
        <div v-if="cin">
          <CinContainer :key="index" :cin="cin" :ae="ae" />
        </div>
      </div>
      <div v-else-if="hasPi !== null">
        <SubContainer :value="hasPi" />
      </div>
    </div>
  </div>
</template>

<script>
import { useMessageStore } from "../../stores/messageStore";
import CinContainer from "./CinContainer.vue";
import SubContainer from "./SubContainer.vue";
export default {
  name: "ConContainer",
  components: {
    CinContainer,
    SubContainer,
  },
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
      cin: null,
    };
  },
  computed: {
    piValue() {
      return this.cin ? this.cin["m2m:cin"].pi : null;
    },
    hasPi() {
      const store = useMessageStore();
      const piToConMap = store.getPiToConMap;
      return piToConMap[this.piValue] || null;
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
      fetch(`/acme${this.ae}/${this.con}/la?fu=1&ty=4`, options)
        .then((response) => response.json())
        .then((response) => {
          if (response["m2m:cin"] !== undefined) {
            this.cin = response;
          } else {
            console.log(this.ae, "/", this.con);
            console.log(response);
          }
        })
        .catch((err) => {
          console.log(this.ae, "/", this.con);
          console.error(err);
        });
    },
  },
  mounted() {
    this.fetchCIN();
  },
};
</script>
