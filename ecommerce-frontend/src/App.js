import React, { useState, useEffect } from "react";
import BargainChat from './components/BargainChat';
import Recommendations from './components/Recommendations';
import productData from "./products.json";

import "./App.css";

const App = () => {
  const [darkMode, setDarkMode] = useState(
    localStorage.getItem("darkMode") === "true"
  );

  const [cart, setCart] = useState([]);

  useEffect(() => {
    document.body.className = darkMode ? "dark-mode" : "";
    localStorage.setItem("darkMode", darkMode);
  }, [darkMode]);

  // Function to add item to cart
  const addToCart = (product) => {
    setCart([...cart, product]);
    alert(`${product.name} added to cart!`);
  };

  return (
    <div className="app-container">
      <nav className="navbar">
        <h2 className="funku-title">🛍️ FUNKU ONLINE STORE</h2>
        <div className="toggle-container">
          <input
            type="checkbox"
            id="darkModeToggle"
            className="toggle-checkbox"
            checked={darkMode}
            onChange={() => setDarkMode(!darkMode)}
          />
          <label htmlFor="darkModeToggle" className="toggle-label"></label>
        </div>
      </nav>

      <div className="content">
        <Recommendations />
        <BargainChat />

        <div className="product-list">
          {productData.map((product) => (
            <div key={product.id} className="product-card">
              <h3>{product.name}</h3>
              <p>Retail Price: <span className="line-through">${product.price}</span></p>
              <p>Discounted Price: <span className="text-green">${product.discountedPrice}</span></p>
              <p>Stock: <span className={product.stock === "Out of Stock" ? "text-red" : "text-blue"}>{product.stock}</span></p>
              <p className="text-sm">ID: {product.id}</p>

              {/* Add to Cart Button */}
              <button 
                className="cart-button"
                onClick={() => addToCart(product)}
                disabled={product.stock === "Out of Stock"}
              >
                {product.stock === "Out of Stock" ? "Out of Stock" : "Add to Cart"}
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default App;
