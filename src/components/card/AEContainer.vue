<template>
	<div class="card w-100">
		<div class="card-body">
			<h4 class="card-title">{{ ae_ri }}</h4>
			<div v-if="cons">
				<ConContainer
					v-for="(con, index) in conArray"
					:key="index"
					:con="con"
					:ae="ae"
				/>
			</div>
		</div>
	</div>
</template>

<script>
import ConContainer from "./ConContainer.vue";
export default {
	name: "AEContainer",
	components: {
		ConContainer,
	},
	props: {
		ae: {
			type: String,
			required: true,
		},
	},
	data() {
		return {
			cons: null,
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
		fetchCON() {
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
		this.fetchCON();
	},
};
</script>
