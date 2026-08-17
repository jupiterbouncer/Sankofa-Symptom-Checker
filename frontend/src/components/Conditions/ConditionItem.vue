<script setup>
import RightArrowIcon from "../icons/RightArrowIcon.vue";
import { store } from "../../store.js";

const props = defineProps({
  condition: {
    type: Object,
    required: true,
  },
});

function showConditionDetail() {
  store.focused_condition = props.condition;
  store.displayStepThreeOverlay = true;
}

function borderLeftStyle() {
  return {
    borderLeft:
      props.condition.serious === true
        ? `3px solid #DC0000`
        : `3px solid #12104a`,
  };
}

function formatProbability(probability) {
  return `${Math.round(probability * 100)}%`;
}
</script>

<template>
  <div
    @click="showConditionDetail"
    class="condition-container"
    :style="borderLeftStyle()"
  >
    <div class="condition-info">
      <p>{{ condition.title }}</p>
      <small class="meta">
        {{ formatProbability(condition.probability) }} · {{ condition.urgency }}
      </small>
    </div>
    <div class="icon"><RightArrowIcon /></div>
  </div>
</template>

<style scoped>
.condition-container {
  width: 100%;
  height: 40px;
  border-left: 3px solid #12104a;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-radius: 5px;
  background: #fafafa;
  font-size: 13px;
  cursor: pointer;
  margin: 15px 0 15px 0;
}

.condition-info {
  display: flex;
  flex-direction: column;
  padding: 0 0 0 29px;
}

.condition-container p {
  font-size: 13px;
  margin: 0;
}

.meta {
  font-size: 11px;
  color: #909090;
}

.condition-container .icon {
  padding: 0 45px 0 0;
}
</style>
