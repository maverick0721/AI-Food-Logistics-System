import React, { useEffect, useRef, useState } from "react";
import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";

import { getMapboxToken } from "../api";

const MAPBOX_TOKEN = (process.env.REACT_APP_MAPBOX_TOKEN || "").trim();

function DeliveryMap() {
  const mapNodeRef = useRef(null);
  const [mapError, setMapError] = useState("");
  const [token, setToken] = useState(MAPBOX_TOKEN);
  const [loadingToken, setLoadingToken] = useState(MAPBOX_TOKEN.length === 0);

  useEffect(() => {
    let cancelled = false;

    if (token) {
      setLoadingToken(false);
      return () => {
        cancelled = true;
      };
    }

    const fetchToken = async () => {
      setLoadingToken(true);
      try {
        const res = await getMapboxToken();
        const backendToken = (res?.data?.token || "").trim();
        if (!cancelled && backendToken) {
          setToken(backendToken);
          setMapError("");
        }
      } catch {
        if (!cancelled) {
          setMapError("Map disabled: missing REACT_APP_MAPBOX_TOKEN in project .env.");
        }
      } finally {
        if (!cancelled) {
          setLoadingToken(false);
        }
      }
    };

    fetchToken();

    return () => {
      cancelled = true;
    };
  }, [token]);

  useEffect(() => {
    if (!token) {
      return undefined;
    }

    mapboxgl.accessToken = token;

    if (!mapboxgl.supported()) {
      setMapError("WebGL is not available in this browser.");
      return undefined;
    }

    if (!mapNodeRef.current) {
      return undefined;
    }

    let map;
    try {
      map = new mapboxgl.Map({
        container: mapNodeRef.current,
        style: "mapbox://styles/mapbox/streets-v11",
        center: [77.89, 29.86],
        zoom: 12
      });
    } catch {
      setMapError("Map could not be loaded.");
      return undefined;
    }

    return () => {
      if (map) map.remove();
    };
  }, [token]);

  return (
    <div className="module">
      <h2>Delivery Map</h2>
      <p className="module-subtitle">City-level dispatch view for routing awareness.</p>
      {mapError ? <p className="status-text error-text">{mapError}</p> : null}

      {!token ? (
        <div className="map-fallback" role="note" aria-label="Map setup instructions">
          <p className="muted-text">
            {loadingToken
              ? "Loading map token from backend..."
              : "Add a token in project .env and restart backend + frontend:"}
          </p>
          <pre className="map-env-snippet">REACT_APP_MAPBOX_TOKEN=your_public_mapbox_token</pre>
        </div>
      ) : (
        <div ref={mapNodeRef} className="map-view" />
      )}
    </div>
  );
}

export default DeliveryMap;