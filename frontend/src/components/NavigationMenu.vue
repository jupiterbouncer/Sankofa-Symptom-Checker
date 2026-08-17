<script setup>
import { store } from "../store.js";

function restartApp() {
  store.name = "";
  store.sex = "NB";
  store.age = null;
  store.bmi = null;
  store.email = "";

  store.displayStepTwoOverlay = false;
  store.displayStepThreeOverlay = false;

  store.heading = "Search";
  store.searchText = "";
  store.searchSymptoms = [];
  store.stagedSymptoms = [];
  store.addedSymptoms = [];
  store.symptomDisplayNames = {};

  store.possible_conditions = [];
  store.diagnosisDisclaimer = "";
  store.focused_condition = {};

  store.changeStep(1);
}
</script>

<template>
  <nav>
    <div class="logo">
      <img src="../assets/img/site-logo.png" alt="Onkhida Health" />
      <div class="text">
        <h1>Onkhida Health</h1>
        <small>Symptom Checker</small>
      </div>
    </div>

    <div @click="restartApp" class="restart-btn">
      <span>Restart</span>
      <svg
        width="16"
        height="15"
        viewBox="0 0 16 15"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M4.24957 7.49913L1 10.7504M1 10.7504L4.24957 14M1 10.7504H15.2981V1"
          stroke="white"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
      </svg>
    </div>
  </nav>
</template>

<style scoped>
nav {
  width: 80%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 30px 0 30px 0;
  border-bottom: 1px solid black;
}

nav .logo {
  display: flex;
  align-items: center;
  justify-content: center;
}

nav .logo img {
  width: 34px;
  height: 35px;
  margin: 0 10px 0 0;
}

nav .logo .text h1 {
  font-size: 21px;
  line-height: 21px;
}

nav .logo .text small {
  font-size: 12px;
  color: #808080;
}

nav .restart-btn {
  width: 120px;
  display: flex;
  justify-content: center;
  padding: 10px 0 10px 0;
  cursor: pointer;
  border-radius: 5px;
  background: black;
  color: white;
}

nav .restart-btn span {
  font-size: 13px;
  margin: 0 15px 0 0;
  padding: 0;
}

@media screen and (max-width: 1300px) {
  nav {
    width: 90%;
  }
}

@media screen and (max-width: 1200px) {
  nav {
    width: 95%;
  }
}

@media screen and (max-width: 1050px) {
  nav {
    width: 80%;
  }
}

@media screen and (max-width: 750px) {
  nav {
    width: 90%;
  }

  nav .logo .text {
    display: none;
  }
}

@media screen and (max-width: 500px) {
  nav {
    width: 95%;
  }
}
</style>
