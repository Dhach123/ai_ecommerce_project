import React, { useState } from 'react';
import axios from 'axios';
import { Spinner } from 'react-bootstrap';
import { toast } from 'react-toastify';

const BargainChat = () => {
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!message.trim()) {
      toast.warn("Please enter a message! ⚠️");
      return;
    }

    setLoading(true);
    try {
      const res = await axios.get(`http://localhost:8000/chat?message=${message}`);
      setChatHistory([...chatHistory, { user: message, bot: res.data.response }]);
      toast.success("Response received! ✅");
    } catch (err) {
      console.error('Error:', err);
      toast.error("Failed to fetch chatbot response. ❌");
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
            <p><strong>You:</strong> {chat.user}</p>
            <p><strong>Salesperson:</strong> {chat.bot}</p>
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
