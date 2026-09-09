import { authorizedFetch } from "../lib/api";

const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

export async function submitSituation(text) {
  const response = await authorizedFetch(`${BASE_URL}/simt`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });
  if (!response.ok) throw new Error("request_failed");
  const data = await response.json();
  if (!data || typeof data !== "object") throw new Error("invalid_response");
  return data;
}
