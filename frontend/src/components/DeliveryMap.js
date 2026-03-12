import React, { useEffect } from "react";
import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";

mapboxgl.accessToken = process.env.REACT_APP_MAPBOX_TOKEN;

function DeliveryMap() {
  useEffect(() => {
    const map = new mapboxgl.Map({
      container: "map",
      style: "mapbox://styles/mapbox/streets-v11",
      center: [77.89, 29.86],
      zoom: 12
    });

    return () => map.remove();
  }, []);

  return (
    <div>
      <h2>Delivery Map</h2>
      <div id="map" style={{ height: "400px" }}></div>
    </div>
  );
}

export default DeliveryMap;