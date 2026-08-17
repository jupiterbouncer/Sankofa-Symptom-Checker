<script setup>
import { store } from "../../store.js";
</script>

<template>
  <p @click="store.resetSearchFilters()">Reset Filters</p>
</template>

<style scoped>
p {
  cursor: pointer;
  width: 100%;
  text-align: right;
  margin: 7px 0 0 0;
  font-size: 12px;
}
</style>
