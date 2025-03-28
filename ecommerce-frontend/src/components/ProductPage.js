import React, { useState } from "react";
import { db } from "./firebaseConfig"; // Import Firestore instance
import { collection, addDoc } from "firebase/firestore";

const ProductPage = () => {
  const [productName, setProductName] = useState("");
  const [productPrice, setProductPrice] = useState("");

  const addProduct = async () => {
    if (!productName || !productPrice) {
      alert("Please enter product details!");
      return;
    }

    try {
      await addDoc(collection(db, "products"), {
        name: productName,
        price: parseFloat(productPrice),
      });
      alert("Product added successfully!");
      setProductName("");
      setProductPrice("");
    } catch (error) {
      console.error("Error adding product: ", error);
    }
  };

  return (
    <div>
      <h2>Add Product</h2>
      <input
        type="text"
        placeholder="Product Name"
        value={productName}
        onChange={(e) => setProductName(e.target.value)}
      />
      <input
        type="number"
        placeholder="Price"
        value={productPrice}
        onChange={(e) => setProductPrice(e.target.value)}
      />
      <button onClick={addProduct}>Add Product</button>
    </div>
  );
};

export default ProductPage;
