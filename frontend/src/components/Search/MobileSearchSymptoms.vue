<script setup>
import { computed } from "vue";
import MobileSearchedSymptoms from "./MobileSearchedSymptom.vue";
import NoSymptom from "../icons/NoSymptoms.vue";
import FetchingIcon from "../icons/FetchingIcon.vue";
import ResetIcon from "../icons/ResetIcon.vue";
import { store } from "../../store.js";
import debounce from "lodash/debounce";

const displaySearchSymptoms = computed(() => store.searchSymptoms);

const showNoResults = computed(
  () =>
    !store.fetchingSymptoms &&
    store.searchText.trim().length >= 2 &&
    displaySearchSymptoms.value.length === 0
);

const debouncedSearch = debounce(() => store.fetchSearchResults(), 250);

function pushStagedSymptoms() {
  for (const symptom of store.stagedSymptoms) {
    store.addSymptom(symptom);
  }
  store.stagedSymptoms = [];

  document
    .getElementById("personal-form")
    .scrollIntoView({ behavior: "smooth" });
}
</script>

<template>
  <div>
    <div class="heading">
      <h1>{{ store.heading }} Symptoms</h1>
    </div>
    <small>Search for symptoms that describe how you feel. </small>

    <input
      @input="debouncedSearch"
      v-model="store.searchText"
      placeholder="search symptoms..."
    />
    <ResetIcon v-if="store.heading !== 'Search'" />

    <div v-if="store.fetchingSymptoms">
      <div class="no-items">
        <FetchingIcon />
        <span>Fetching symptoms </span>
      </div>
    </div>
    <div v-else-if="displaySearchSymptoms.length > 0">
      <div class="searched-symptoms">
        <MobileSearchedSymptoms
          v-for="symptom in displaySearchSymptoms"
          :symptom="symptom"
          :key="symptom.feature_id"
        />
      </div>
    </div>
    <div v-else-if="showNoResults">
      <div class="no-items">
        <NoSymptom />
        <span> No Symptoms Found. </span>
      </div>
    </div>

    <div class="btn-wrap-container">
      <button
        @click="pushStagedSymptoms"
        v-show="store.stagedSymptoms.length > 0"
        class="add-staged-symptoms"
      >
        Add {{ store.stagedSymptoms.length }} Symptom<span
          v-if="store.stagedSymptoms.length > 1"
          >s</span
        >
      </button>
    </div>
  </div>
</template>

<style scoped>
input {
  width: 100%;
  font-size: 12px;
  padding: 10px 15px 10px 15px;
  border: 0;
  margin: 15px 0 0 0;
  color: #909090;
  border-bottom: 2px solid #d9d9d9;
  border-radius: 4px;
}
input:focus {
  outline: none;
}

.searched-symptoms {
  margin: 15px 0 0 0;
  max-height: 350px;
  min-height: 50px;
  overflow-y: scroll;
  padding: 5px;
  width: 100%;
  display: flex;
  flex-wrap: wrap;
  outline: 1px solid #909090;
  border-radius: 5px;
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

.heading {
  display: flex;
  align-items: center;
}

.heading h1 {
  margin: 0 10px 0 0;
}

.btn-wrap-container {
  width: 100%;
  display: flex;
  justify-content: flex-end;
  margin: 20px 0 0 0;
  min-height: 50px;
}

button.add-staged-symptoms {
  cursor: pointer;
  padding: 10px 40px 10px 40px;
  color: white;
  background: black;
  margin: 0;
  width: fit-content;
  border-radius: 5px;
  height: fit-content;
  font-size: 13px;
  border: 0;
}
</style>
