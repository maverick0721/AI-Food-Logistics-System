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

    <div>

      <h2>Restaurants</h2>

      <ul>

        {restaurants.map((r, i) => (

          <li key={i}>{r.name} ({r.cuisine})</li>

        ))}

      </ul>

    </div>

  );

}

export default RestaurantList;