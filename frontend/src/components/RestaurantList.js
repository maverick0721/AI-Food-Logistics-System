import React, { useEffect, useState } from "react";

import { createRestaurant, getRestaurants } from "../api";


function RestaurantList() {

  const [restaurants, setRestaurants] = useState([]);
  const [name, setName] = useState("");
  const [cuisine, setCuisine] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [status, setStatus] = useState("");

  const loadRestaurants = async () => {
    const res = await getRestaurants();
    setRestaurants(res.data || []);
  };

  useEffect(() => {
    loadRestaurants();
  }, []);

  const submitRestaurant = async () => {
    if (!name.trim() || !cuisine.trim()) {
      setStatus("Enter both restaurant name and cuisine.");
      return;
    }

    setSubmitting(true);
    setStatus("");
    try {
      await createRestaurant({ name: name.trim(), cuisine: cuisine.trim() });
      setName("");
      setCuisine("");
      setStatus("Restaurant added.");
      await loadRestaurants();
    } catch {
      setStatus("Could not add restaurant. Please try again.");
    } finally {
      setSubmitting(false);
    }
  };

  return (

    <div className="module">
      <h2>Restaurants</h2>
      <p className="module-subtitle">Live directory synced from your backend API.</p>

      <div className="form-grid" style={{ marginBottom: "14px" }}>
        <label>
          Restaurant Name
          <input
            value={name}
            placeholder="e.g. Riverfront Diner"
            onChange={e => setName(e.target.value)}
          />
        </label>
        <label>
          Cuisine
          <input
            value={cuisine}
            placeholder="e.g. Continental"
            onChange={e => setCuisine(e.target.value)}
          />
        </label>
      </div>

      <button className="btn-primary" onClick={submitRestaurant} disabled={submitting}>
        {submitting ? "Adding..." : "Add Restaurant"}
      </button>
      {status ? <p className="status-text">{status}</p> : null}

      {restaurants.length === 0 ? (
        <p className="muted-text">No restaurants yet.</p>
      ) : (
        <ul className="restaurant-list">
          {restaurants.map((r, i) => (
            <li key={i} className="restaurant-item">
              <span className="restaurant-name">{r.name}</span>
              <span className="restaurant-chip">{r.cuisine}</span>
            </li>
          ))}
        </ul>
      )}
    </div>

  );

}

export default RestaurantList;