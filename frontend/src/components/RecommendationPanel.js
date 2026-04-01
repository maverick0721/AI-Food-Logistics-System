import React, { useEffect, useState } from "react";

import { getRecommendation, getRestaurants } from "../api";


function RecommendationPanel() {

  const [user, setUser] = useState("");
  const [restaurantId, setRestaurantId] = useState("");
  const [restaurants, setRestaurants] = useState([]);

  const [score, setScore] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

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

  const check = async () => {
    if (!user || !restaurantId) {
      setError("Provide user and restaurant details.");
      return;
    }

    setLoading(true);
    setError("");
    try {
      const res = await getRecommendation(user, restaurantId);
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