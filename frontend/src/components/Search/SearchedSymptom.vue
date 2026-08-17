<script setup>
import AddIcon from "../icons/AddIcon.vue";
import { store } from "../../store.js";
import { ref } from "vue";

defineProps({
  symptom: {
    type: Object,
    required: true,
  },
});

const showBtn = ref(true);

function addItem(symptom) {
  showBtn.value = false;
  store.addSymptom(symptom);
}

function formatScore(score) {
  return `${Math.round(score * 100)}%`;
}
</script>

<template>
  <button v-show="showBtn" @click="addItem(symptom)">
    <span>{{ symptom.display_name }}</span>
    <small class="score">{{ formatScore(symptom.similarity_score) }}</small>
    <AddIcon />
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

.score {
  color: #909090;
  font-size: 11px;
  margin-right: 7px;
}
</style>
