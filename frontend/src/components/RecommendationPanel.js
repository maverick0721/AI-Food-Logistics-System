import React, { useState } from "react";

import { getRecommendation } from "../api";


function RecommendationPanel() {

  const [user, setUser] = useState("");
  const [restaurant, setRestaurant] = useState("");

  const [score, setScore] = useState(null);

  const check = async () => {

    const res = await getRecommendation(user, restaurant);

    setScore(res.data.score);

  };

  return (

    <div>

      <h2>Recommendation Score</h2>

      <input placeholder="User ID" onChange={e => setUser(e.target.value)} />

      <input placeholder="Restaurant ID" onChange={e => setRestaurant(e.target.value)} />

      <button onClick={check}>Check</button>

      {score && <p>Score: {score}</p>}

    </div>

  );

}

export default RecommendationPanel;