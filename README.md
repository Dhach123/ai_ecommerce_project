# Funku Online Store

## Overview
Funku is an AI-powered e-commerce platform that integrates a **recommendation system**, a **bargaining system**, and a **chatbot**, providing users with a unique shopping experience. The backend is built using **Flask**, while the frontend is developed with **React.js**. Firebase is used as a real-time database to store customer chats.

## Features
- **AI-Powered Recommendation System**: Suggests products based on user behavior and preferences.
- **Bargaining System**: Allows users to negotiate prices with an AI chatbot.
- **Chatbot Integration**: Provides customer support and assists users in making purchases.
- **Firebase Integration**: Stores user chats and transaction data in Firestore.
- **Flask Backend**: Handles API requests, recommendations, and chatbot responses.
- **React.js Frontend**: Provides a smooth and interactive user experience.

## Technologies Used
- **Frontend**: React.js, Bootstrap, React-Toastify
- **Backend**: Flask, Flask-CORS, Flask-RESTful
- **Database**: Firebase Firestore
- **AI Models**: NLP-based chatbot and recommendation algorithms
- **Hosting**: Localhost (development) / Firebase Hosting (optional for deployment)

---

## Setup Instructions

### Prerequisites
Ensure you have the following installed:
- **Node.js** (for frontend) - [Download](https://nodejs.org/)
- **Python 3.8+** (for backend) - [Download](https://www.python.org/)
- **Firebase Account** (for chat storage) - [Sign up](https://firebase.google.com/)

### 1️⃣ Clone the Repository
```sh
$ git clone https://github.com/Dhach123/ai_ecommerce_project
$ cd funku-online-store
```

### 2️⃣ Backend Setup (Flask)
#### Install dependencies
```sh
$ cd backend
$ pip install -r requirements.txt
```

#### Run Flask Server
```sh
$ python app.py
```
By default, Flask runs on **http://localhost:8000**

### 3️⃣ Frontend Setup (React.js)
#### Install dependencies
```sh
$ cd frontend
$ npm install
```

#### Run the React App
```sh
$ npm start
```
The frontend runs on **http://localhost:3000**

### 4️⃣ Firebase Setup
- Create a **Firebase Project** at [Firebase Console](https://console.firebase.google.com/)
- Get your Firebase configuration and replace it in `src/components/firebaseConfig.js`:
```js
import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";

const firebaseConfig = {
  apiKey: "your-api-key",
  authDomain: "your-auth-domain",
  projectId: "your-project-id",
  storageBucket: "your-storage-bucket",
  messagingSenderId: "your-messaging-sender-id",
  appId: "your-app-id"
};

const app = initializeApp(firebaseConfig);
export const db = getFirestore(app);
```

---

## API Endpoints (Backend)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/chat?message=your_message` | GET | Handles bargaining chatbot queries |
| `/recommendations?user_id=123` | GET | Fetches personalized product recommendations |

---

## Future Enhancements
- Deploy the backend on **Google Cloud Run** or **AWS Lambda**.
- Improve chatbot AI with **GPT-4** for better bargaining interactions.
- Implement a **secure authentication system** using Firebase Auth.

---

## Contributors
- **Your Name** - [GitHub Profile]https://github.com/Dhach123/ai_ecommerce_project)

---

### 🎉 Happy Coding & Shopping with Funku! 🛍️

