import React, { useState } from "react";

import { createOrder } from "../api";


function OrderForm() {

  const [user, setUser] = useState("");
  const [restaurant, setRestaurant] = useState("");
  const [item, setItem] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState("");

  const submit = async () => {
    if (!user || !restaurant || !item) {
      setMessage("Fill all fields before creating the order.");
      return;
    }

    setSubmitting(true);
    setMessage("");
    try {
      await createOrder({
        user_id: parseInt(user, 10),
        restaurant_id: parseInt(restaurant, 10),
        item: item
      });
      setMessage("Order created successfully.");
      setItem("");
    } catch {
      setMessage("Could not create order. Please try again.");
    } finally {
      setSubmitting(false);
    }

  };

  return (

    <div className="module">
      <h2>Create Order</h2>
      <p className="module-subtitle">Trigger a new order and publish it to the dispatch stream.</p>

      <div className="form-grid">
        <label>
          User ID
          <input value={user} placeholder="e.g. 7" onChange={e => setUser(e.target.value)} />
        </label>

        <label>
          Restaurant ID
          <input value={restaurant} placeholder="e.g. 2" onChange={e => setRestaurant(e.target.value)} />
        </label>

        <label className="label-wide">
          Item
          <input value={item} placeholder="e.g. Pasta Alfredo" onChange={e => setItem(e.target.value)} />
        </label>
      </div>

      <button className="btn-primary" onClick={submit} disabled={submitting}>
        {submitting ? "Creating..." : "Create Order"}
      </button>

      {message ? <p className="status-text">{message}</p> : null}
    </div>

  );

}

export default OrderForm;