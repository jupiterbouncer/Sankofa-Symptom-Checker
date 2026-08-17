import { reactive } from "vue";

export const store = reactive({
  name: "",
  sex: "NB",
  age: null,
  bmi: null,
  email: "",
  meds: "",
  existingConditions: "",

  fetchingSymptoms: false,
  fetchingConditions: false,

  api_base: "/api/v1",

  showStepOne: true,
  showStepTwo: false,
  showStepThree: false,

  changeStep(step) {
    switch (step) {
      case 1:
        this.showStepOne = true;
        this.showStepTwo = false;
        this.showStepThree = false;
        break;
      case 2:
        this.showStepOne = false;
        this.showStepTwo = true;
        this.showStepThree = false;
        break;
      case 3:
        this.showStepOne = false;
        this.showStepTwo = false;
        this.showStepThree = true;
        break;
      default:
        return `The step ${step} was not found`;
    }
  },

  displayStepTwoOverlay: false,
  displayStepThreeOverlay: false,

  heading: "Search",

  allowed_headings: [
    "Scalp",
    "Forehead",
    "Eyes",
    "Nose",
    "Ears",
    "Face",
    "Mouth",
    "Jaw",
    "Neck",
    "Breast",
    "Chest",
    "Shoulder",
    "Armpit",
    "Upperarm",
    "Elbow",
    "Forearm",
    "Wrist",
    "Hand",
    "Finger",
    "Abdomen",
    "Pelvis",
    "Buttock",
    "Hip",
    "Groin",
    "Genital",
    "Back",
    "Lowerback",
    "Flank",
    "Hip",
    "Rectum",
    "Thigh",
    "Hamstring",
    "Knee",
    "Shin",
    "Calf",
    "Ankle",
    "Foot",
    "Toes",
  ],

  // semantic search results from GET /api/v1/symptoms/search
  searchSymptoms: [],

  // mobile staging before commit to addedSymptoms
  stagedSymptoms: [],

  // selected symptom feature_id strings sent to POST /api/v1/diagnose
  addedSymptoms: [],

  // feature_id -> display_name for UI labels
  symptomDisplayNames: {},

  possible_conditions: [],
  focused_condition: {},
  diagnosisDisclaimer: "",

  searchText: "",

  getSymptomDisplayName(featureId) {
    return this.symptomDisplayNames[featureId] || featureId;
  },

  addSymptom({ feature_id, display_name }) {
    if (!this.addedSymptoms.includes(feature_id)) {
      this.addedSymptoms.push(feature_id);
      this.symptomDisplayNames[feature_id] = display_name;
    }
  },

  removeSymptom(featureId) {
    const idx = this.addedSymptoms.indexOf(featureId);
    if (idx !== -1) {
      this.addedSymptoms.splice(idx, 1);
      delete this.symptomDisplayNames[featureId];
    }
  },

  addStagedSymptom({ feature_id, display_name }) {
    if (!this.stagedSymptoms.some((s) => s.feature_id === feature_id)) {
      this.stagedSymptoms.push({ feature_id, display_name });
    }
  },

  removeStagedSymptom(featureId) {
    const idx = this.stagedSymptoms.findIndex((s) => s.feature_id === featureId);
    if (idx !== -1) {
      this.stagedSymptoms.splice(idx, 1);
    }
  },

  async fetchRegionSymptoms(region) {
    if (!region || region === "Search") {
      this.searchSymptoms = [];
      return;
    }
    this.fetchingSymptoms = true;
    try {
      const res = await fetch(`${this.api_base}/symptoms/by-region/${region.toLowerCase()}`);
      if (!res.ok) {
        throw new Error(`Failed to fetch region symptoms: ${res.status}`);
      }
      const data = await res.json();
      this.searchSymptoms = (data.symptoms || []).map((sym) => {
        const display = sym
          .split(" ")
          .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
          .join(" ");
        return {
          feature_id: sym,
          display_name: display,
        };
      });
    } catch (error) {
      console.error("Error fetching region symptoms:", error);
      this.searchSymptoms = [];
    } finally {
      this.fetchingSymptoms = false;
    }
  },

  async fetchSearchResults() {
    if (this.searchText.trim().length > 0 && this.heading !== "Search") {
      this.heading = "Search";
    }

    if (this.heading !== "Search") {
      await this.fetchRegionSymptoms(this.heading);
      return;
    }

    const query = this.searchText.trim();
    if (query.length < 2) {
      this.searchSymptoms = [];
      this.fetchingSymptoms = false;
      return;
    }

    this.fetchingSymptoms = true;
    try {
      const params = new URLSearchParams({ q: query, limit: "5" });
      const res = await fetch(`${this.api_base}/symptoms/search?${params}`);
      if (!res.ok) {
        throw new Error(`Search failed: ${res.status}`);
      }
      const data = await res.json();
      this.searchSymptoms = data.matches || [];
    } catch (error) {
      console.error("Search error:", error);
      this.searchSymptoms = [];
    } finally {
      this.fetchingSymptoms = false;
    }
  },

  resetSearchFilters() {
    this.heading = "Search";
    if (this.searchText.trim().length >= 2) {
      this.fetchSearchResults();
    } else {
      this.searchSymptoms = [];
    }
  },

  async runDiagnosis() {
    this.fetchingConditions = true;
    try {
      const payload = {
        symptoms: [...this.addedSymptoms],
        metadata: {
          age: this.age != null ? Number(this.age) : null,
          sex: this.sex === "F" ? "F" : "M",
          bmi: this.bmi != null ? Number(this.bmi) : null,
        },
      };

      const res = await fetch(`${this.api_base}/diagnose`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        throw new Error(`Diagnosis failed: ${res.status}`);
      }

      const data = await res.json();
      this.possible_conditions = (data.predictions || []).map((p) => ({
        title: p.disease,
        probability: p.probability,
        urgency: p.urgency,
        serious: p.urgency === "Urgent",
        summary: p.recommendation,
        treatment: p.recommendation,
      }));
      this.diagnosisDisclaimer = data.disclaimer || "";
    } catch (error) {
      console.error("Diagnosis error:", error);
      this.possible_conditions = [];
      this.diagnosisDisclaimer = "";
    } finally {
      this.fetchingConditions = false;
    }
  },
});
