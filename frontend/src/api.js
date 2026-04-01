import axios from "axios";

const API = axios.create({

  baseURL: "http://localhost:8000"

});

export const createOrder = (data) => API.post("/orders", data);

export const createRestaurant = (data) => API.post("/restaurants", data);

export const getRestaurants = () => API.get("/restaurants");

export const getRecommendation = (user, restaurant) =>
  API.get(`/recommend?user_id=${user}&restaurant_id=${restaurant}`);

export const getDashboardMetrics = () => API.get("/metrics/dashboard");

export const getMapboxToken = () => API.get("/config/mapbox-token");