import { defineStore } from "pinia";

export const useMessageStore = defineStore("message", {
  state: () => ({
    messages: [],
    piToConMap: {},
  }),
  actions: {
    addMessage(message) {
      this.messages.push(message);
      // Extract pi and con values and save them in piToConMap
      const { pi, con } = message;
      this.piToConMap[pi] = con;
    },
  },
  getters: {
    getMessages: (state) => state.messages,
    getPiToConMap: (state) => state.piToConMap,
  },
});
