<script setup>
import { defineProps } from "vue";

const props = defineProps({
  title: {
    type: String,
    default: "默认",
  },
});
</script>

<template>
  <div>{{ props.title }}组件</div>
</template>

<style lang="less" scoped></style>
