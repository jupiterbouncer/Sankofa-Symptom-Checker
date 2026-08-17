<script setup>
import { store } from "../../store.js";
import { computed } from "vue";
import RedWarningIcon from "../icons/RedWarningIcon.vue";
// import RemoveIcon from "../icons/RemoveIcon.vue";

const conditionDetails = computed(() => {
  return store.focused_condition;
});

function closeOverlay() {
  store.focused_condition = [];
  store.displayStepThreeOverlay = false;
}
</script>

<template>
  <div class="overlay-container">
    <div class="wrapper">
      <div @click="closeOverlay" class="remove">
        <svg
          width="14"
          height="14"
          viewBox="0 0 14 14"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M1 13L13 1M1 1L13 13"
            stroke="black"
            stroke-width="1.5"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>
      </div>
      <div class="content">
        <div v-if="store.focused_condition.serious === true" class="disclaimer">
          <RedWarningIcon />
          <span>This is a serious condition </span>
        </div>
        <h1>{{ conditionDetails.title }}</h1>
        <p v-if="conditionDetails.probability != null" class="probability">
          Match confidence: {{ Math.round(conditionDetails.probability * 100) }}%
          · {{ conditionDetails.urgency }}
        </p>
        <p>
          {{ conditionDetails.summary }}
        </p>

        <div class="treatment">
          <h5>Possible treatment options</h5>
          <p>{{ conditionDetails.treatment }}</p>
        </div>

        <div class="help-container">
          <button>
            <a target="_blank" href="https://sankofa.me">Get Help</a>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.overlay-container {
  position: relative;
  width: 100%;
  height: 100vh;
  border-left: 2px solid black;
  background: white;
  z-index: 1;
  display: flex;
  justify-content: center;
  overflow-y: auto;
}

.help-container {
  width: 100%;
  display: flex;
  justify-content: flex-end;
}

.help-container button {
  cursor: pointer;
  padding: 10px 50px 10px 50px;
  color: white;
  background: black;
  margin: 0;
  width: fit-content;
  border-radius: 5px;
  height: fit-content;
  font-size: 13px;
  border: 0;
}

.help-container a {
  text-decoration: none;
  color: white;
}

.remove {
  position: absolute;
  top: 30px;
  right: 30px;
  cursor: pointer;
}

.overlay-container .wrapper {
  width: 80%;
  height: fit-content;
  margin: 0 0 80px 0;
}

h1 {
  font-size: 22px;
  margin: 0 0 5px 0;
}

.probability {
  color: #676767;
  font-size: 12px;
  margin: 0 0 10px 0;
}

p {
  font-size: 13px;
}

.disclaimer {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #8d0000;
  font-size: 13px;
  border: 1px solid #8d0000;
  border-radius: 3px;
  background-color: #ffe3e3;
  padding: 11px 0 11px 0;
  margin: 10px 0 20px 0;
}

.content {
  margin: 90px 0 20px 0;
}

.disclaimer span {
  padding: 0 0 0 10px;
}

.symptoms-wrapper {
  margin: 10px 0 0 0;
  width: 100%;
  display: flex;
  flex-wrap: wrap;
}

button {
  display: flex;
  align-items: center;
  border: 1px solid #d9d9d9;
  padding: 7px 16px 7px 16px;
  font-size: 13px;
  color: #676767;
  border-radius: 5px;
  margin: 5px 5px 0 0;
}

.treatment {
  margin: 25px 0 0 0;
}

.treatment h5 {
  font-size: 15px;
  margin: 0 0 7px 0;
}

.treatment p,
.symptoms-wrapper p {
  font-size: 12px;
  /* color: #808080; */
  padding: 0 0 50px 0;
}
</style>
