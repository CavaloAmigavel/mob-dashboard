<template>
	<div class="card text-center" style="width: 200px">
		<div class="card-body">
			<h6 class="card-title">{{ cin }}</h6>
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
			type: String,
			required: true,
		},
	},
	mounted() {},
};
</script>
