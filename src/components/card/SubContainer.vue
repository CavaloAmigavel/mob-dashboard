<template>
  <div class="card text-center w-100">
    <div class="card-body">
      <h6 class="card-title">{{ value }}</h6>
    </div>
  </div>
</template>

<script>
export default {
  name: "SubContainer",
  props: {
    value: {
      type: String,
      required: true,
    },
  },
};
</script>
