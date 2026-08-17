<script setup>
import ConditionItem from "./ConditionItem.vue";
import { store } from "../../store.js";
import FetchingIcon from "../icons/FetchingIcon.vue";
</script>

<template>
  <div v-if="store.fetchingConditions === false" class="conditions-container">
    <h1>Possible conditions</h1>
    <p class="explain">
      Conditions highlighted in red may require emergency attention. The listed
      conditions reflect your symptoms, not your diagnosis. You may consult our
      <a target="_blank" href="https://sankofa.me">doctors</a>
      for any questions or concerns. Sankofa is an academic prototype and not a certified diagnostic device.
    </p>
    
    <hr />

    <div v-if="store.possible_conditions.length > 0" class="conditions-list">
      <ConditionItem
        v-for="condition in store.possible_conditions"
        :condition="condition"
        :key="condition.title"
      />
    </div>
    <div v-else class="no-conditions">
      <span>No matching conditions found.</span>
    </div>
  </div>

  <div v-if="store.fetchingConditions === true" class="no-conditions">
    <FetchingIcon />
    <span>Fetching conditions </span>
  </div>
</template>

<style scoped>
.no-conditions {
  margin: 40px 0 0 0;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #676767;
  font-size: 13px;
  border: 1px solid #d9d9d9;
  border-radius: 5px;
  background-color: #fafafa;
  height: 200px;
}

.no-conditions span {
  padding: 0 0 0 10px;
}

.conditions-container {
  width: 100%;
}

p {
  font-size: 13px;
  color: #808080;
}

.disclaimer {
  font-size: 12px;
  color: #676767;
  border: 1px solid #d9d9d9;
  border-radius: 5px;
  background-color: #fafafa;
  padding: 10px 15px;
}

hr {
  width: 100%;
  color: #e7e7e7;
  margin: 20px 0 30px 0;
}

p.explain a {
  color: black;
}
</style>
