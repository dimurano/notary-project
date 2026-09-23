// src/api.js
const API_BASE_URL = "https://run.app";

/**
 * Core wrapper to handle secure network fetches automatically adding JWT headers
 */
async function apiRequest(endpoint, options = {}) {
  const token = localStorage.getItem("notary_token");
  
  // Set up standard headers required by FastAPI
  const headers = {
    ...options.headers,
  };

  // If a JWT token exists in the browser, inject it into the Authorization header
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  // Ensure JSON requests have the proper content type (skip if uploading a file/FormData)
  if (options.body && !(options.body instanceof FormData) && !headers["Content-Type"]) {
    headers["Content-Type"] = "application/json";
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || "Network request failed");
  }

  return response.json();
}

export const api = {
  // Authentication endpoint (sends URL-encoded form data as required by FastAPI OAuth2)
  login: async (email, password) => {
    const formData = new URLSearchParams();
    formData.append("username", email); // FastAPI OAuth2 expects 'username'
    formData.append("password", password);

    const data = await apiRequest("/auth/token", {
      method: "POST",
      body: formData,
    });
    
    // Save token securely on success
    localStorage.setItem("notary_token", data.access_token);
    return data;
  },

  // Secure data endpoint example
  getDashboard: () => apiRequest("/notary/secure-dashboard-data", { method: "GET" }),

  // Document upload initialization endpoint
  createSession: (clientEmail, docName, fileObject) => {
    const formData = new FormData();
    formData.append("client_email", clientEmail);
    formData.append("document_name", docName);
    formData.append("file", fileObject);

    return apiRequest("/notary/create-session", {
      method: "POST",
      body: formData,
    });
  },

  logout: () => {
    localStorage.removeItem("notary_token");
  }
};
