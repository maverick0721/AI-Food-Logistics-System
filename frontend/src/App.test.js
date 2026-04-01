import React from "react";
import ReactDOMServer from "react-dom/server";

jest.mock("./api", () => ({
  createOrder: jest.fn(),
  getRestaurants: jest.fn(() => Promise.resolve({ data: [] })),
  getRecommendation: jest.fn(() => Promise.resolve({ data: { score: 0 } })),
  getMapboxToken: jest.fn(() => Promise.resolve({ data: { token: "" } })),
  getDashboardMetrics: jest.fn(() =>
    Promise.resolve({
      data: {
        uptime_pct: 99.9,
        active_zones: 3,
        avg_eta_minutes: 16.4,
        stream_lag_ms: 28
      }
    })
  )
}));

jest.mock("mapbox-gl", () => ({
  __esModule: true,
  default: {
    accessToken: "",
    Map: function MockMap() {
      return { remove: jest.fn() };
    }
  }
}));

import App from "./App";

test("renders app title", () => {
  const html = ReactDOMServer.renderToString(<App />);
  expect(html).toContain("AI Food Delivery Platform");
});
