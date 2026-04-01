import React, { useEffect, useState } from "react";

import { createOrder, getRestaurants } from "../api";


function OrderForm() {

  const [user, setUser] = useState("");
  const [restaurantId, setRestaurantId] = useState("");
  const [item, setItem] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState("");
  const [restaurants, setRestaurants] = useState([]);

  useEffect(() => {
    let cancelled = false;

    const loadRestaurants = async () => {
      try {
        const res = await getRestaurants();
        const list = res?.data || [];
        if (!cancelled) {
          setRestaurants(list);
          if (list.length > 0) {
            setRestaurantId(String(list[0].id));
          }
        }
      } catch {
        if (!cancelled) {
          setRestaurants([]);
        }
      }
    };

    loadRestaurants();

    return () => {
      cancelled = true;
    };
  }, []);

  const submit = async () => {
    if (!user || !restaurantId || !item) {
      setMessage("Fill all fields before creating the order.");
      return;
    }

    setSubmitting(true);
    setMessage("");
    try {
      await createOrder({
        user_id: parseInt(user, 10),
        restaurant_id: parseInt(restaurantId, 10),
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
          Restaurant Name
          <select value={restaurantId} onChange={e => setRestaurantId(e.target.value)}>
            {restaurants.length === 0 ? (
              <option value="">No restaurants available</option>
            ) : (
              restaurants.map(r => (
                <option key={r.id} value={String(r.id)}>
                  {r.name}
                </option>
              ))
            )}
          </select>
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