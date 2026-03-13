import React, { useState } from "react";

import { getRecommendation } from "../api";


function RecommendationPanel() {

  const [user, setUser] = useState("");
  const [restaurant, setRestaurant] = useState("");

  const [score, setScore] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const check = async () => {
    if (!user || !restaurant) {
      setError("Provide user and restaurant IDs.");
      return;
    }

    setLoading(true);
    setError("");
    try {
      const res = await getRecommendation(user, restaurant);
      setScore(res.data.score);
    } catch {
      setError("Could not fetch recommendation score.");
    } finally {
      setLoading(false);
    }

  };

  return (

    <div className="module">
      <h2>Recommendation Score</h2>
      <p className="module-subtitle">Estimate user affinity before assignment.</p>

      <div className="form-grid">
        <label>
          User ID
          <input placeholder="e.g. 7" onChange={e => setUser(e.target.value)} />
        </label>

        <label>
          Restaurant ID
          <input placeholder="e.g. 2" onChange={e => setRestaurant(e.target.value)} />
        </label>
      </div>

      <button className="btn-primary" onClick={check} disabled={loading}>
        {loading ? "Checking..." : "Check Score"}
      </button>

      {error ? <p className="status-text error-text">{error}</p> : null}
      {score !== null ? (
        <div className="score-block">
          <span>Predicted score</span>
          <strong>{Number(score).toFixed(4)}</strong>
        </div>
      ) : null}
    </div>

  );

}

export default RecommendationPanel;