<script setup>
import MobileSearchSymptoms from "./Search/MobileSearchSymptoms.vue";
import { store } from "../store.js";
</script>

<template>
  <div class="wrap">
    <div class="inner">
      <MobileSearchSymptoms />
    </div>
    <div @click="() => (store.displayStepTwoOverlay = false)" class="remove">
      <svg
        width="17"
        height="17"
        viewBox="0 0 17 17"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M1 16L16 1M1 1L16 16"
          stroke="black"
          stroke-width="1.5"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
      </svg>
    </div>
  </div>
</template>

<style scoped>
.wrap {
  height: 100vh;
  width: 100vw;
  /* outline: 1px solid black; */
  background: white;
  display: flex;
  justify-content: center;
  align-items: center;
}

.inner {
  width: 80%;
  /* outline: 1px solid red; */
}

.wrap .remove {
  position: absolute;
  top: 20px;
  right: 20px;
  cursor: pointer;
}
</style>
