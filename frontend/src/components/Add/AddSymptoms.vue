<script setup>
import { store } from "../../store.js";
import AddedSymptom from "./AddedSymptom.vue";
import AboutAdded from "../icons/AboutAdded.vue";
</script>

<template>
  <div class="add-symptom-container">
    <h1>Added Symptoms</h1>
    <small>Symptoms that you want factored into the result.</small>

    <div class="wrapper">
      <div v-if="store.addedSymptoms.length > 0" class="added-symptoms">
        <AddedSymptom
          v-for="symptom in store.addedSymptoms"
          :symptom="symptom"
          :key="symptom"
        />
      </div>

      <div v-if="store.addedSymptoms.length === 0">
        <div class="no-items">
          <AboutAdded />
          <span> Begin by adding a symptom. </span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.add-symptom-container {
  width: 100%;
}

.added-symptoms {
  margin: 5px 0 0 0;
  width: 100%;
  display: flex;
  flex-wrap: wrap;
}

.wrapper {
  width: 100%;
  /* min-height: 120px; */
}

.no-items {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #676767;
  font-size: 13px;
  border: 1px solid #d9d9d9;
  border-radius: 5px;
  background-color: #fafafa;
  padding: 13px 0 13px 0;
  margin: 10px 0 0 0;
}

.no-items span {
  padding: 0 0 0 10px;
}
</style>
