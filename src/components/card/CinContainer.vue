<template>
	<div class="card text-center" style="width: 232px">
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
