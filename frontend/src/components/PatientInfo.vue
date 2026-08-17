<script setup>
import { store } from "../store.js";
</script>

<template>
  <div class="personal-form-container">
    <div class="heading">
      <h1>Your details</h1>
      <p>
        Your age and sex refine the accuracy of symptom analysis for more
        tailored health insights.
      </p>
    </div>
    <form>
      <div class="hlf-sect">
        <label for="age">Age</label>
        <input
          type="number"
          id="age"
          required
          placeholder="e.g. 20"
          :value="store.age"
          disabled
        />
      </div>

      <div class="hlf-sect">
        <label for="sex">Sex</label>
        <input
          type="text"
          id="sex"
          required
          :value="store.sex === 'M' ? 'Male' : store.sex === 'F' ? 'Female' : ''"
          disabled
        />
      </div>
    </form>

    <div class="heading">
      <h1>Your symptoms</h1>
      <p>
        Be thorough and honest for the most accurate results. Adding more
        symptoms may also enhance the checker's accuracy.
      </p>
    </div>

    <div class="symptoms-wrapper">
      <button :key="symptom" v-for="symptom in store.addedSymptoms">
        <span>{{ store.getSymptomDisplayName(symptom) }}</span>
      </button>
    </div>
  </div>
</template>

<style scoped>
.personal-form-container {
  width: 100%;
  padding: 10px 0 10px 10%;
  margin: 40px 0 0 0;
  border-left: 1px solid #e7e7e7;
}

.personal-form-container .heading {
  width: 100%;
}

.personal-form-container .heading h1 {
  font-size: 15px;
}

.personal-form-container .heading p {
  font-size: 13px;
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

form input {
  width: 100%;
  padding: 6px 15px 6px 15px;
  margin: 7px 0 0 0;
  border-radius: 4px;
  height: 36px;
  font-size: 13px;
  background: #e5e5e5;
  border: 1px solid #d9d9d9;
  color: #bfbfbf;
}

form .hlf-sect {
  width: 47%;
  margin: 0 0 20px 0;
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

@media screen and (max-width: 1050px) {
  .personal-form-container {
    padding: 10px 0 10px 0px;
    border: 0;
  }
}
</style>
