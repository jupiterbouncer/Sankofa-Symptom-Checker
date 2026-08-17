<script setup>
// nav
import Navbar from "./components/NavigationMenu.vue";

// first page → init user form
import StartForm from "./components/StartForm.vue";

// second page → components collecting symptom data
import SearchSymptoms from "./components/Search/SearchSymptoms.vue";
import AddSymptoms from "./components/Add/AddSymptoms.vue";
import PersonalForm from "./components/QuestionnaireForm.vue";

// interactive models
import InteractiveMaleModel from "./components/InteractiveModels/InteractiveMaleModel.vue";
import InteractiveFemaleModel from "./components/InteractiveModels/InteractiveFemaleModel.vue";

// third page → displaying user conditions
import PatientInfo from "./components/PatientInfo.vue";
import ConditionsViewer from "./components/Conditions/ConditionsViewer.vue";

// overlay
import MobileOverlay from "./components/MobileOverlay.vue";
import ConditionsOverlay from "./components/Conditions/ConditionsOverlay.vue";

// store state data
import { store } from "./store.js";

import MobileSearchSymptoms from "./components/Search/MobileSearchSymptoms.vue";

function closeOverlay(e) {
  if (e.target.classList[0] === "conditions-overlay-block") {
    store.focused_condition = [];
    store.displayStepThreeOverlay = false;
  }
}
</script>

<template>
  <div class="step-1" v-if="store.showStepOne">
    <div class="start-wrapper">
      <StartForm />
    </div>
  </div>

  <div class="step-2" v-if="store.showStepTwo">
    <header id="site-header">
      <Navbar />
    </header>
    <div class="container">
      <div class="wrapper">
        <div class="left"><SearchSymptoms /></div>
        <div class="model">
          <InteractiveMaleModel
            v-if="store.sex === 'M'"
          /><InteractiveFemaleModel v-if="store.sex === 'F'" />
        </div>
        <div class="mobile-search">
          <MobileSearchSymptoms />
        </div>
        <div id="personal-form" class="right">
          <AddSymptoms /><PersonalForm />
        </div>
      </div>
    </div>
    <transition name="slide">
      <div v-if="store.displayStepTwoOverlay" class="overlay">
        <MobileOverlay />
      </div>
    </transition>
  </div>

  <div class="step-3" v-if="store.showStepThree">
    <header>
      <Navbar />
    </header>

    <div class="container">
      <div class="wrapper">
        <div class="conditions"><ConditionsViewer /></div>
        <div class="personal-info">
          <PatientInfo />
        </div>
      </div>
    </div>

    <transition name="slide">
      <div
        v-if="store.displayStepThreeOverlay"
        class="conditions-overlay-block"
        @click="(e) => closeOverlay(e)"
      >
        <div v-if="store.displayStepThreeOverlay" class="conditions-overlay">
          <ConditionsOverlay />
        </div>
      </div>
    </transition>
  </div>
</template>

<style scoped>
.conditions-overlay-block {
  position: fixed;
  top: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.219);
  display: flex;
  justify-content: flex-end;
}

div.step-3 {
  width: 100%;
  min-height: 100vh;
  margin: 0 0 70px 0;
}

div.step-3 .container {
  width: 100%;
  /* background: red; */
  display: flex;
  justify-content: center;
}
div.step-3 .container .wrapper {
  width: 80%;
  /* background: blue; */
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  margin: 50px 0 0 0;
}

div.step-3 .container .wrapper .personal-info {
  width: 30%;
  /* background: green; */
  display: flex;
  justify-content: flex-end;
}

div.step-3 .container .wrapper .conditions {
  width: 60%;
  /* border: 1px solid purple; */
  /* background: purple; */
}

.overlay {
  position: fixed;
  top: 0;
  z-index: 1000;
  transition: transform 0.3s ease;
}

.conditions-overlay {
  width: 415px;
  position: fixed;
  top: 0;
  transition: transform 0.3s ease;
  z-index: 1000;
}

header {
  width: 100%;
  display: flex;
  justify-content: center;
  /* outline: 1px solid black; */
}

div.step-1 {
  display: flex;
  justify-content: center;
  width: 100%;
  align-items: center;
  min-height: 100vh;
  /* outline: 1px solid blue; */
}

div.step-1 .start-wrapper {
  width: 450px;
  /*outline: 1px solid red; */
}

div.step-2 {
  width: 100%;
  /* display: flex; */
  justify-content: center;
  /* background: aqua; */
  margin: 0 0 100px 0;
  /* outline: 1px solid black; */
}

div.step-2 .container {
  width: 100%;
  display: flex;
  justify-content: center;
}

div.step-2 .wrapper {
  width: 80%;
  /* background-color: pink; */
  display: flex;

  flex-wrap: wrap;
  justify-content: center;
}

div.step-2 .wrapper .left {
  width: 28%;
  /* outline: 3px solid aquamarine; */
  background: white;
  padding: 80px 0 0 0;
}

div.step-2 .wrapper .model {
  display: flex;
  justify-content: center;
  /* background-color: blueviolet; */
  width: 44%;
}

div.step-2 .wrapper .mobile-search {
  display: none;
}

div.step-2 .wrapper .right {
  /* background-color: chartreuse; */
  width: 28%;
  padding: 80px 0 0 0;
}
@media screen and (max-width: 550px) {
  div.step-1 .start-wrapper {
    width: 90%;
  }
}
@media screen and (max-width: 1300px) {
  div.step-2 .wrapper {
    width: 90%;
  }

  div.step-3 .container .wrapper {
    width: 90%;
  }
}
@media screen and (max-width: 1200px) {
  div.step-2 .wrapper {
    width: 95%;
  }

  div.step-3 .container .wrapper {
    width: 95%;
  }

  div.step-3 .container .wrapper .personal-info {
    width: 35%;
  }
}

@media screen and (max-width: 1050px) {
  div.step-2 .wrapper .left,
  div.step-2 .wrapper .model,
  div.step-2 .wrapper .right,
  div.step-2 .wrapper .mobile-search {
    width: 80%;
    padding: 20px 0 0 0;
    /* outline: 1px solid black; */
  }

  div.step-2 .wrapper .left {
    display: none;
  }

  div.step-2 .wrapper .model {
    display: none;
  }

  div.step-2 .wrapper .mobile-search {
    display: block;
    padding: 80px 0 25px 0;
    /* outline: 1px solid red; */
  }

  div.step-3 .container .wrapper {
    width: 80%;
    justify-content: center;
  }

  div.step-3 .container .wrapper .personal-info {
    width: 90%;
  }

  div.step-3 .container .wrapper .conditions {
    width: 90%;
  }
}

@media screen and (max-width: 750px) {
  div.step-2 .wrapper .model,
  div.step-2 .wrapper .right,
  div.step-2 .wrapper .mobile-search {
    width: 90%;
  }

  div.step-3 .container .wrapper {
    width: 90%;
  }
}

@media screen and (max-width: 500px) {
  div.step-2 .wrapper .model,
  div.step-2 .wrapper .right,
  div.step-2 .wrapper .mobile-search {
    width: 95%;
  }

  div.step-3 .container .wrapper .personal-info {
    width: 100%;
  }

  div.step-3 .container .wrapper .conditions {
    width: 100%;
  }

  div.step-3 .container .wrapper {
    width: 95%;
  }

  .conditions-overlay {
    width: 100vw;
  }

  @media screen and (max-width: 480px) {
    div.step-2 .wrapper .model {
      padding: 0;
    }
  }
}

/* Slide-in transition classes */
.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s ease;
}

.slide-enter-from {
  transform: translateX(100%); /* Start off-screen to the right */
}

.slide-enter-to {
  transform: translateX(0); /* Slide in to original position */
}

.slide-leave-from {
  transform: translateX(0); /* Start at the original position */
}

.slide-leave-to {
  transform: translateX(100%); /* Slide out to the right */
}
</style>
