import React, { useState } from "react";

import { createOrder } from "../api";


function OrderForm() {

  const [user, setUser] = useState("");
  const [restaurant, setRestaurant] = useState("");
  const [item, setItem] = useState("");

  const submit = async () => {

    await createOrder({

      user_id: parseInt(user),
      restaurant_id: parseInt(restaurant),
      item: item

    });

    alert("Order created");

  };

  return (

    <div>

      <h2>Create Order</h2>

      <input placeholder="User ID" onChange={e => setUser(e.target.value)} />

      <input placeholder="Restaurant ID" onChange={e => setRestaurant(e.target.value)} />

      <input placeholder="Item" onChange={e => setItem(e.target.value)} />

      <button onClick={submit}>Order</button>

    </div>

  );

}

export default OrderForm;