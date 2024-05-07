<template>
	<div class="card text-center" style="width: 200px">
		<div class="card-body">
			<h5 class="card-title">{{ con }}</h5>
			<div v-if="cins">
				<CinContainer
					v-for="(cin, index) in cinArray"
					:key="index"
					:cin="cin"
					:ae="ae"
				/>
			</div>
		</div>
	</div>
</template>

<script>
import CinContainer from "./CinContainer.vue";
export default {
	name: "ConContainer",
	components: {
		CinContainer,
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
			cins: null,
		};
	},
	computed: {
		//AE Resource Indentifier
		cinArray() {
			return this.cins["m2m:uril"].map((uri) => uri.split("/").pop());
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
			fetch(`/acme${this.ae}/${this.con}?fu=1&ty=4`, options)
				.then((response) => response.json())
				.then((response) => {
					console.log(response);
					this.cins = response;
				})
				.catch((err) => console.error(err));
		},
	},
	mounted() {
		this.fetchCIN();
	},
};
</script>
