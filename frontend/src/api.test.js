jest.mock("axios", () => ({
  __esModule: true,
  default: {
    create: jest.fn(() => ({ post: jest.fn(), get: jest.fn() }))
  }
}));

import axios from "axios";
import {
  createOrder,
  createRestaurant,
  getRestaurants,
  getRecommendation,
  getDashboardMetrics,
  getMapboxToken
} from "./api";

const apiClient = axios.create.mock.results[0].value;

describe("frontend api client", () => {
  beforeEach(() => {
    apiClient.post.mockReset();
    apiClient.get.mockReset();
  });

  test("createOrder sends POST /orders with payload", async () => {
    apiClient.post.mockResolvedValue({ data: { id: 1 } });
    const payload = { user_id: 1, restaurant_id: 2, item: "pizza" };

    await createOrder(payload);

    expect(apiClient.post).toHaveBeenCalledWith("/orders", payload);
  });

  test("getRestaurants sends GET /restaurants", async () => {
    apiClient.get.mockResolvedValue({ data: [] });

    await getRestaurants();

    expect(apiClient.get).toHaveBeenCalledWith("/restaurants");
  });

  test("createRestaurant sends POST /restaurants with payload", async () => {
    apiClient.post.mockResolvedValue({ data: { id: 1 } });
    const payload = { name: "Green Bowl", cuisine: "Healthy" };

    await createRestaurant(payload);

    expect(apiClient.post).toHaveBeenCalledWith("/restaurants", payload);
  });

  test("getRecommendation sends GET with query params", async () => {
    apiClient.get.mockResolvedValue({ data: { score: 0.5 } });

    await getRecommendation(5, 9);

    expect(apiClient.get).toHaveBeenCalledWith("/recommend?user_id=5&restaurant_id=9");
  });

  test("getDashboardMetrics sends GET /metrics/dashboard", async () => {
    apiClient.get.mockResolvedValue({ data: {} });

    await getDashboardMetrics();

    expect(apiClient.get).toHaveBeenCalledWith("/metrics/dashboard");
  });

  test("getMapboxToken sends GET /config/mapbox-token", async () => {
    apiClient.get.mockResolvedValue({ data: { token: "pk.test" } });

    await getMapboxToken();

    expect(apiClient.get).toHaveBeenCalledWith("/config/mapbox-token");
  });
});
