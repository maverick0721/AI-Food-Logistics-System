import React, { useEffect, useState } from "react";

import { getRestaurants } from "../api";


function RestaurantList() {

  const [restaurants, setRestaurants] = useState([]);

  useEffect(() => {

    getRestaurants().then(res => {

      setRestaurants(res.data);

    });

  }, []);

  return (

    <div className="module">
      <h2>Restaurants</h2>
      <p className="module-subtitle">Live directory synced from your backend API.</p>

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