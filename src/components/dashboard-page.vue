<template>
	<div class="container-fluid p-5 bg-success text-white text-center">
		<h1>ACME Monitor</h1>
		<p>Showing what is Connected</p>
	</div>
	<div class="container mt-4">
		<div class="row gx-4 gy-4">
			<div
				class="col-12 col-sm-6 col-md-4 col-lg-3"
				v-for="(card, index) in cards"
				:key="index"
			>
				<div class="card h-100">
					<div class="card-body">
						<h5 class="card-title">{{ card.title }}</h5>
						<p class="card-text">{{ card.content }}</p>
					</div>
				</div>
			</div>
		</div>
	</div>

	<AEContainer v-for="(ae, index) in aesArray" :key="index" :ae="ae" />
</template>

<script>
import AEContainer from "./card/AEContainer.vue"; // Import the AeContainer component

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
	},
	mounted() {
		this.fetchAE();
	},
};
</script>
