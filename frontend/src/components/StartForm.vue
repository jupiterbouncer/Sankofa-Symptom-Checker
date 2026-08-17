<script setup>
import { ref } from "vue";
import { store } from "../store.js";
import WarningIcon from "./icons/WarningIcon.vue";

const inputAge = ref();
const inputSex = ref("");
const errs = ref("");

function submitFormData(e) {
  e.preventDefault();
  if (inputAge.value == null || inputSex.value == "") {
    errs.value = "Please fill in all form fields";
    return;
  } else if (inputAge.value < 0 || inputAge.value > 120) {
    errs.value = "Please select an age between 1 and 120";
    return;
  }

  store.sex = inputSex.value;
  store.age = Number(inputAge.value);
  errs.value = "";
  store.changeStep(2);
}
</script>

<template>
  <div class="personal-form-container">
    <div class="heading">
      <img src="../assets/img/site-logo.png" alt="Onkhida Health" />
      <div class="text">
        <h1>Onkhida Health</h1>
        <small>Symptom Checker</small>
      </div>
    </div>

    <form>
      <div class="full-sect">
        <p>
          You are about to fill out a form to learn about potential causes of
          your symptoms and next steps. Our tool offers guidance based on
          available data; for serious health concerns, consult a
          <a class="contact-link" href="https://onkhida.me" target="_blank"
            >qualified medical professional</a
          >.
        </p>
      </div>

      <div class="hlf-sect">
        <label for="age">Age</label>
        <input
          type="number"
          v-model="inputAge"
          id="age"
          required
          placeholder="e.g. 52"
          min="0"
        />
      </div>

      <div class="hlf-sect">
        <label for="sex">Sex</label>
        <select v-model="inputSex" id="sex" required>
          <option value="" disabled selected>Select your option</option>
          <option value="M">Male</option>
          <option value="F">Female</option>
        </select>
      </div>

      <div class="disclaimer">
        <WarningIcon />
        <span>This tool is not a substitute for medical advice. </span>
      </div>

      <div class="errors">{{ errs }}</div>

      <div class="full-sect">
        <input type="submit" value="Get Started" @click="submitFormData" />
      </div>
    </form>
  </div>
</template>

<style scoped>
.personal-form-container {
  width: 100%;
  margin: 40px 0 0 0;
}

.personal-form-container .heading {
  width: 100%;
  display: flex;
  justify-content: center;
}

.personal-form-container .heading img {
  width: 41px;
  margin: 0 10px 0 0;
  height: 42px;
}

.personal-form-container .heading .text h1 {
  font-size: 21px;
  line-height: 21px;
}

.personal-form-container .heading .text small {
  font-size: 12px;
  color: #808080;
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

form .hlf-sect {
  width: 45%;
  margin: 0 0 20px 0;
}

form input[type="submit"] {
  cursor: pointer;
  padding: 10px 50px 10px 50px;
  color: white;
  background: black;
  margin: 0;
  border-radius: 5px;
  height: fit-content;
  font-size: 13px;
  border: 0;
}

.disclaimer {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #676767;
  font-size: 13px;
  border: 1px solid #d9d9d9;
  border-radius: 5px;
  background-color: #fafafa;
  padding: 11px 0 11px 0;
  margin: 10px 0 20px 0;
}

.disclaimer span {
  padding: 0 0 0 10px;
}

.errors {
  width: 100%;
  font-size: 12px;
  margin: 0 0 10px 0;
  color: red;
}

.full-sect p {
  font-size: 13px;
  margin: 15px 0 0 0;
  text-align: center;
}

a.contact-link {
  color: black;
}
</style>
