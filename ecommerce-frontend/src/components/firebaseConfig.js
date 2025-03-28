// Import required Firebase modules
import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";

// Firebase config
const firebaseConfig = {
  apiKey: "AIzaSyBKRd84KfDCEYd-47HIojtxBbGQTYHvp_o",
  authDomain: "funku1990-faff1.firebaseapp.com",
  projectId: "funku1990-faff1",
  storageBucket: "funku1990-faff1.appspot.com",
  messagingSenderId: "861049018336",
  appId: "1:861049018336:web:786b644d3a5e93cc06bd85",
  measurementId: "G-VQ7N526DPW"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firestore
const db = getFirestore(app);

export { db };
