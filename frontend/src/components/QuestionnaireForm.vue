<script setup>
import { computed, ref } from "vue";
import { store } from "../store.js";

const daysSick = ref();
const errs = ref("");
const canPostData = computed(() => store.addedSymptoms.length === 0);

async function submitSymptomForm(e) {
  e.preventDefault();
  if (store.age < 0 || store.age > 120) {
    errs.value = "Age needs to be between 1 and 120.";
    return;
  } else if (store.sex !== "M" && store.sex !== "F") {
    errs.value = "Sex should be Male or Female.";
    return;
  } else if (store.addedSymptoms.length === 0) {
    errs.value = "Start by adding a symptom.";
    return;
  }

  errs.value = "";
  store.changeStep(3);
  store.runDiagnosis();

  document
    .getElementById("site-header")
    .scrollIntoView({ behavior: "smooth" });
}
</script>

<template>
  <div class="personal-form-container">
    <form>
      <div class="full-sect days">
        <label for="sick">How long have you been sick? (optional)</label>
        <div class="day-input">
          <input type="number" v-model="daysSick" id="sick" min="0" />
          <div class="day-container">Days</div>
        </div>
      </div>

      <div class="errors">{{ errs }}</div>

      <div class="full-sect submit-container">
        <input
          :disabled="canPostData"
          type="submit"
          value="Continue"
          @click="submitSymptomForm"
        />
      </div>
    </form>
  </div>
</template>

<style scoped>
.errors {
  width: 100%;
  font-size: 12px;
  margin: 0 0 10px 0;
  color: red;
}

.personal-form-container {
  width: 100%;
  margin: 40px 0 0 0;
}

form {
  margin: 20px 0 0 0;
  width: 100%;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}

form label {
  font-size: 13px;
  color: black;
}

form input:focus,
form select:focus {
  outline: none;
}

form input,
form select {
  width: 100%;
  padding: 6px 15px 6px 15px;
  color: #4c4c4c;
  margin: 7px 0 0 0;
  border-radius: 4px;
  height: 36px;
  font-size: 13px;
  border: 1px solid #d9d9d9;
}

form .full-sect {
  width: 100%;
  margin: 0 0 20px 0;
}

form .days .day-input {
  width: 100%;
  margin: 7px 0 0 0;
  display: flex;
}

form .days input {
  width: 80%;
  margin: 0;
  border-top-left-radius: 4px;
  border-top-right-radius: 0px;
  border-bottom-left-radius: 4px;
  border-bottom-right-radius: 0px;
}

form .days .day-container {
  width: 20%;
  border: 1px solid #d9d9d9;
  background: #f6f6f6;
  color: #676767;
  border-top-left-radius: 0px;
  border-top-right-radius: 4px;
  border-bottom-left-radius: 0px;
  border-bottom-right-radius: 4px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 13px;
}

form .submit-container {
  display: flex;
  justify-content: end;
  margin: 20px 0 0 0;
}

form input[type="submit"] {
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

form input[type="submit"]:disabled {
  cursor: not-allowed;
  opacity: 0.7;
}
</style>
