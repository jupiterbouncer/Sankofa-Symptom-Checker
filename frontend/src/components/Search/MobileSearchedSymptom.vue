<script setup>
import AddIcon from "../icons/AddIcon.vue";
import { store } from "../../store.js";
import { ref } from "vue";

const props = defineProps({
  symptom: {
    type: Object,
    required: true,
  },
});

const staged = ref(false);

function toggleStageItem() {
  if (staged.value) {
    store.removeStagedSymptom(props.symptom.feature_id);
  } else {
    store.addStagedSymptom(props.symptom);
  }
  staged.value = !staged.value;
}

function formatScore(score) {
  return `${Math.round(score * 100)}%`;
}
</script>

<template>
  <button
    :style="[
      staged
        ? { border: '2px solid #f397f3' }
        : { border: '1px solid #d9d9d9' },
    ]"
    @click="toggleStageItem"
  >
    <span>{{ symptom.display_name }}</span>
    <small class="score">{{ formatScore(symptom.similarity_score) }}</small>
    <AddIcon />
  </button>
</template>

<style scoped>
button {
  display: flex;
  align-items: center;
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
