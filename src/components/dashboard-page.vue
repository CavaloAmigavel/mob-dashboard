<template>
	<div id="grad" class="container-fluid p-5 text-white text-center">
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
				<div class="card w-100">
					<div class="card-body">
						<h5 class="card-title">{{ card.title }}</h5>
						<p class="card-text">{{ card.content }}</p>
						<div
							class="card text-center bg-light"
							style="width: 268px; margin-bottom: 10px"
						>
							<div class="card-body">
								<h5 class="card-title">{{ con }}</h5>
								<div class="card text-center" style="width: 232px">
									<div class="card-body">
										<h6 class="card-title">{{ cinValue }}</h6>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>

	<div class="container mt-4">
		<div class="row gx-4 gy-4">
			<div class="col-12 col-sm-6 col-md-4 col-lg-3">
				<AEContainer v-for="(ae, index) in aesArray" :key="index" :ae="ae" />
			</div>
		</div>
	</div>
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
