import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Spinner } from 'react-bootstrap';
import { toast } from 'react-toastify';
import { db } from "./firebaseConfig"; // Import Firestore config
import { collection, addDoc, serverTimestamp, onSnapshot } from "firebase/firestore";

const BargainChat = () => {
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Real-time listener for Firestore chat history
    const unsubscribe = onSnapshot(collection(db, "customer_chats"), (snapshot) => {
      const chats = snapshot.docs.map(doc => doc.data());
      setChatHistory(chats);
    });

    return () => unsubscribe(); // Cleanup listener on unmount
  }, []);

  const sendMessage = async () => {
    if (!message.trim()) {
      toast.warn("Please enter a message! ⚠️");
      return;
    }

    setLoading(true);
    try {
      // Save user message to Firestore
      await addDoc(collection(db, "customer_chats"), {
        user: "Customer",
        message,
        timestamp: serverTimestamp(),
      });

      // Send message to chatbot API
      const res = await axios.get(`http://localhost:8000/chat?message=${message}`);

      // Save bot response to Firestore
      await addDoc(collection(db, "customer_chats"), {
        user: "Salesperson",
        message: res.data.response,
        timestamp: serverTimestamp(),
      });

      toast.success("Response received! ✅");
    } catch (err) {
      console.error('Error:', err);
      toast.error("Failed to send message. ❌");
    }

    setMessage('');
    setLoading(false);
  };

  return (
    <div className="card p-3">
      <h3>Bargain Chat</h3>
      <div className="chat-box border rounded p-2 mb-3" style={{ height: '300px', overflowY: 'auto' }}>
        {chatHistory.map((chat, index) => (
          <div key={index}>
            <p><strong>{chat.user}:</strong> {chat.message}</p>
            <hr />
          </div>
        ))}
      </div>

      {loading && (
        <div className="text-center">
          <Spinner animation="border" variant="primary" />
        </div>
      )}

      <div className="input-group">
        <input
          type="text"
          className="form-control"
          placeholder="Type your message..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          disabled={loading}
        />
        <button className="btn btn-primary" onClick={sendMessage} disabled={loading}>
          {loading ? "Sending..." : "Send"}
        </button>
      </div>
    </div>
  );
};

export default BargainChat;
