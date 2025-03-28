import React, { useState, useEffect } from "react";
import BargainChat from './components/BargainChat';
import Recommendations from './components/Recommendations';
import { db } from "./components/firebaseConfig";
import { collection, getDocs, addDoc } from "firebase/firestore";
import productData from "./products.json";

import "./App.css";

const App = () => {
  const [darkMode, setDarkMode] = useState(localStorage.getItem("darkMode") === "true");
  const [cart, setCart] = useState([]);
  const [products, setProducts] = useState([]);
  const [newProduct, setNewProduct] = useState({ name: "", price: "", discountedPrice: "", stock: "In Stock" });
  const [isMerchant, setIsMerchant] = useState(false);
  const [merchantCredentials, setMerchantCredentials] = useState({ username: "", password: "" });
  const [customer, setCustomer] = useState({ username: "", isNewUser: false, loggedIn: false });

  useEffect(() => {
    document.body.className = darkMode ? "dark-mode" : "";
    localStorage.setItem("darkMode", darkMode);
  }, [darkMode]);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const querySnapshot = await getDocs(collection(db, "products"));
        const productList = querySnapshot.docs.map((doc) => ({
          id: doc.id,
          ...doc.data(),
        }));
        setProducts([...productData, ...productList]); // Merge local and DB products
      } catch (error) {
        console.error("Error fetching products: ", error);
      }
    };

    fetchProducts();
  }, []);

  const handleCustomerLogin = () => {
    if (customer.username.trim()) {
      setCustomer({ ...customer, loggedIn: true });
      alert(`Welcome ${customer.isNewUser ? "new" : "back"}, ${customer.username}!`);
    } else {
      alert("Please enter a username to log in.");
    }
  };

  return (
    <div className="app-container">
      <nav className="navbar">
        <h2 className="funku-title">🛍️ FUNKU ONLINE STORE</h2>

        <div className="customer-support">
          <img src="/support-icon.png" alt="Support" className="support-logo" />
          <p>📞 Helpline: +1 (800) 987-6543</p>
        </div>

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

        {/* Customer Login */}
        {!customer.loggedIn && (
          <div className="customer-login">
            <h3>🔑 Customer Login</h3>
            <input
              type="text"
              placeholder="Enter Username"
              value={customer.username}
              onChange={(e) => setCustomer({ ...customer, username: e.target.value })}
            />
            <label>
              <input
                type="checkbox"
                checked={customer.isNewUser}
                onChange={() => setCustomer({ ...customer, isNewUser: !customer.isNewUser })}
              />
              New User
            </label>
            <button onClick={handleCustomerLogin}>Login</button>
          </div>
        )}

        {/* Product List */}
        <div className="product-list">
          {products.map((product) => (
            <div key={product.id} className="product-card">
              <h3>{product.name}</h3>
              <p>Retail Price: <span className="line-through">${product.price}</span></p>
              <p>Discounted Price: <span className="text-green">${product.discountedPrice}</span></p>
              <p>Stock: <span className={product.stock === "Out of Stock" ? "text-red" : "text-blue"}>{product.stock}</span></p>
              <p className="text-sm">ID: {product.id}</p>

              <button 
                className="cart-button"
                onClick={() => setCart([...cart, product])}
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
