import { defineStore } from "pinia";
import { ref } from "vue";

export const useCounterStore = defineStore("counter", () => {
	const count = ref(0);
	const name = ref("Message");
	const doubleCount = computed(() => count.value * 2);

	function increment() {
		count.value++;
	}

	return { count, increment, name, doubleCount };
});
