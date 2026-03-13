import React, { useEffect, useRef, useState } from "react";
import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";

mapboxgl.accessToken = process.env.REACT_APP_MAPBOX_TOKEN;

function DeliveryMap() {
  const mapNodeRef = useRef(null);
  const [mapError, setMapError] = useState("");

  useEffect(() => {
    if (!mapboxgl.accessToken) {
      setMapError("Map token missing.");
      return undefined;
    }

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
  }, []);

  return (
    <div className="module">
      <h2>Delivery Map</h2>
      <p className="module-subtitle">City-level dispatch view for routing awareness.</p>
      {mapError ? <p className="status-text error-text">{mapError}</p> : null}
      <div ref={mapNodeRef} className="map-view" />
    </div>
  );
}

export default DeliveryMap;