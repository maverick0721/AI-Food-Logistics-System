import React from "react";

import OrderForm from "./components/orderForm";
import RestaurantList from "./components/RestaurantList";
import RecommendationPanel from "./components/RecommendationPanel";
import DeliveryMap from "./components/DeliveryMap";


function App() {

  return (

    <div>

      <h1>AI Food Delivery Platform</h1>

      <RestaurantList />

      <OrderForm />

      <RecommendationPanel />

      <DeliveryMap />

    </div>

  );

}

export default App;