<script setup>
import RemoveIcon from "../icons/RemoveIcon.vue";
import { store } from "../../store.js";

defineProps({
  symptom: {
    type: String,
    required: true,
  },
});

function removeItem(featureId) {
  store.removeSymptom(featureId);
  if (store.searchText.trim().length >= 2) {
    store.fetchSearchResults();
  }
}
</script>

<template>
  <button @click="removeItem(symptom)">
    <span>{{ store.getSymptomDisplayName(symptom) }}</span>
    <RemoveIcon />
  </button>
</template>

<style scoped>
button {
  display: flex;
  align-items: center;
  border: 1px solid #d9d9d9;
  padding: 7px 16px 7px 16px;
  font-size: 13px;
  color: #676767;
  cursor: pointer;
  border-radius: 5px;
  margin: 5px 5px 0 0;
}

button span {
  padding: 0 7px 0 0;
}
</style>
