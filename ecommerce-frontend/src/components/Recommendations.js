import React, { useState } from 'react';
import axios from 'axios';
import { Spinner } from 'react-bootstrap';
import { toast } from 'react-toastify';

const Recommendations = () => {
  const [itemId, setItemId] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchRecommendations = async () => {
    if (!itemId.trim()) {
      toast.warn("Please enter a valid Product ID! ⚠️"); // Warning toast
      return;
    }

    setLoading(true);
    try {
      const res = await axios.get(`http://localhost:8000/recommendations?item_id=${itemId}`);
      setResults(res.data);
      toast.success("Recommendations fetched successfully! ✅"); // Success toast
    } catch (err) {
      console.error('Error:', err);
      toast.error("Failed to fetch recommendations. ❌"); // Error toast
    }
    setLoading(false);
  };

  return (
    <div className="card p-3">
      <h3>Product Recommendations</h3>
      <div className="input-group mb-3">
        <input
          type="text"
          className="form-control"
          placeholder="Enter Product ID"
          value={itemId}
          onChange={(e) => setItemId(e.target.value)}
          disabled={loading}
        />
        <button className="btn btn-success" onClick={fetchRecommendations} disabled={loading}>
          {loading ? "Fetching..." : "Get Recommendations"}
        </button>
      </div>

      {loading && (
        <div className="text-center">
          <Spinner animation="border" variant="success" />
        </div>
      )}

      {results.length > 0 && !loading && (
        <ul className="list-group">
          {results.map((item, index) => (
            <li key={index} className="list-group-item">
              <strong>{item.product_name}</strong> <br />
              Category: {item.main_category} <br />
              Product ID: {item.item_id}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Recommendations;
