// src/api.js
const API_BASE_URL =
  process.env.REACT_APP_API_BASE_URL || "http://localhost:8000";

/**
 * Call the FastAPI /grade endpoint.
 * payload shape must match GradeRequest:
 * {
 *   github_link: string,
 *   rubric: object,
 *   test_results?: string
 * }
 */
export async function gradeSubmission(payload) {
  const res = await fetch(`${API_BASE_URL}/grade`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  let data;
  try {
    data = await res.json();
  } catch {
    data = null;
  }

  if (!res.ok) {
    // FastAPI often returns {"detail": "..."} on errors
    const message =
      (data && typeof data.detail === "string" && data.detail) ||
      res.statusText ||
      "Request failed";
    throw new Error(message);
  }

  return data; // This should match GradeResponse from your backend.
}
