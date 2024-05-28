<template>
	<div class="card text-center w-100">
		<div class="card-body">
			<h6 class="card-title">{{ cinValue }}</h6>
		</div>
	</div>
</template>

<script>
export default {
	name: "CinContainer",
	props: {
		ae: {
			type: String,
			required: true,
		},
		cin: {
			type: Object,
			required: true,
		},
	},
	computed: {
		cinValue() {
			return this.cin["m2m:cin"].con;
		},
	},
};
</script>
