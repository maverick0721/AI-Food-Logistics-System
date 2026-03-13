import React, { useEffect, useRef, useState } from "react";

import OrderForm from "./components/orderForm";
import RestaurantList from "./components/RestaurantList";
import RecommendationPanel from "./components/RecommendationPanel";
import DeliveryMap from "./components/DeliveryMap";
import { getDashboardMetrics } from "./api";
import "./App.css";


function App() {
  const [theme, setTheme] = useState("light");
  const [apiStatus, setApiStatus] = useState("Syncing");
  const [kpiValues, setKpiValues] = useState({
    uptime: 0,
    zones: 0,
    eta: 0,
    lag: 0
  });
  const [kpiTargets, setKpiTargets] = useState({
    uptime: 0,
    zones: 0,
    eta: 0,
    lag: 0
  });
  const valuesRef = useRef(kpiValues);

  useEffect(() => {
    valuesRef.current = kpiValues;
  }, [kpiValues]);

  const kpis = [
    { key: "uptime", label: "API Uptime", suffix: "%", decimals: 1, note: apiStatus },
    { key: "zones", label: "Active Zones", suffix: "", decimals: 0, note: "from restaurants" },
    { key: "eta", label: "Avg ETA", suffix: "m", decimals: 1, note: "live estimate" },
    { key: "lag", label: "Stream Lag", suffix: "ms", decimals: 0, note: "live stream" }
  ];

  useEffect(() => {
    const pullMetrics = async () => {
      try {
        const res = await getDashboardMetrics();
        const data = res?.data || {};
        setApiStatus("Live");
        setKpiTargets({
          uptime: Number(data.uptime_pct ?? 0),
          zones: Number(data.active_zones ?? 0),
          eta: Number(data.avg_eta_minutes ?? 0),
          lag: Number(data.stream_lag_ms ?? 0)
        });
      } catch {
        setApiStatus("Offline");
        setKpiTargets(prev => ({ ...prev, uptime: 0, lag: 0 }));
      }
    };

    pullMetrics();
    const intervalId = window.setInterval(pullMetrics, 20000);

    return () => {
      window.clearInterval(intervalId);
    };
  }, []);

  useEffect(() => {
    const duration = 700;
    let start = null;
    let rafId = null;
    const from = valuesRef.current;

    const animate = timestamp => {
      if (!start) start = timestamp;
      const progress = Math.min((timestamp - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);

      setKpiValues({
        uptime: from.uptime + (kpiTargets.uptime - from.uptime) * eased,
        zones: from.zones + (kpiTargets.zones - from.zones) * eased,
        eta: from.eta + (kpiTargets.eta - from.eta) * eased,
        lag: from.lag + (kpiTargets.lag - from.lag) * eased
      });

      if (progress < 1) {
        rafId = window.requestAnimationFrame(animate);
      }
    };

    rafId = window.requestAnimationFrame(animate);
    return () => {
      if (rafId) window.cancelAnimationFrame(rafId);
    };
  }, [kpiTargets]);

  const toggleTheme = () => {
    setTheme(current => (current === "light" ? "night" : "light"));
  };

  const handlePanelMove = e => {
    const rect = e.currentTarget.getBoundingClientRect();
    const x = (e.clientX - rect.left) / rect.width;
    const y = (e.clientY - rect.top) / rect.height;

    const rotateY = (x - 0.5) * 5;
    const rotateX = (0.5 - y) * 5;

    e.currentTarget.style.setProperty("--tilt-x", `${rotateY.toFixed(2)}deg`);
    e.currentTarget.style.setProperty("--tilt-y", `${rotateX.toFixed(2)}deg`);
  };

  const resetPanelTilt = e => {
    e.currentTarget.style.setProperty("--tilt-x", "0deg");
    e.currentTarget.style.setProperty("--tilt-y", "0deg");
  };

  const formatKpiValue = ({ key, decimals, suffix }) => {
    const value = kpiValues[key] ?? 0;
    return `${value.toFixed(decimals)}${suffix}`;
  };

  return (

    <div className="app-shell" data-theme={theme}>
      <div className="ambient ambient-left" />
      <div className="ambient ambient-right" />

      <div className="dashboard-shell">
        <aside className="left-rail" aria-label="Sections">
          <div className="rail-brand">AFLS</div>
          <a href="#map" className="rail-link">Map</a>
          <a href="#restaurants" className="rail-link">Restaurants</a>
          <a href="#orders" className="rail-link">Orders</a>
          <a href="#recommend" className="rail-link">Recommend</a>
        </aside>

        <div className="main-column">
          <header className="hero">
            <div className="hero-topline">
              <p className="eyebrow">Smart Dispatch Console</p>
              <button className="theme-toggle" onClick={toggleTheme}>
                {theme === "light" ? "Switch to Night" : "Switch to Day"}
              </button>
            </div>
            <h1>AI Food Delivery Platform</h1>
            <p className="hero-subtitle">
              Optimize restaurant operations, order creation, and dispatch decisions from one minimalist control surface.
            </p>

            <div className="kpi-row" role="status" aria-live="polite">
              {kpis.map(item => (
                <article key={item.key} className="kpi-card">
                  <span>{item.label}</span>
                  <strong>{formatKpiValue(item)}</strong>
                  <small>{item.note}</small>
                </article>
              ))}
            </div>
          </header>

          <main className="content-grid">
            <section
              id="map"
              className="panel panel-map tilt-panel"
              onMouseMove={handlePanelMove}
              onMouseLeave={resetPanelTilt}
            >
              <DeliveryMap />
            </section>

            <section
              id="restaurants"
              className="panel tilt-panel"
              onMouseMove={handlePanelMove}
              onMouseLeave={resetPanelTilt}
            >
              <RestaurantList />
            </section>

            <section
              id="orders"
              className="panel tilt-panel"
              onMouseMove={handlePanelMove}
              onMouseLeave={resetPanelTilt}
            >
              <OrderForm />
            </section>

            <section
              id="recommend"
              className="panel tilt-panel"
              onMouseMove={handlePanelMove}
              onMouseLeave={resetPanelTilt}
            >
              <RecommendationPanel />
            </section>
          </main>
        </div>
      </div>
    </div>

  );

}

export default App;