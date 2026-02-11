import axios from "axios";

const API_BASE = import.meta.env.VITE_API_URL || "/api";

const API = axios.create({
  baseURL: API_BASE,
  headers: { "Content-Type": "application/json" },
});

// Attach JWT token to every request
API.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// Auto-refresh on 401
API.interceptors.response.use(
  (res) => res,
  async (error) => {
    const original = error.config;
    if (error.response?.status === 401 && !original._retry) {
      original._retry = true;
      const refresh = localStorage.getItem("refresh_token");
      if (refresh) {
        try {
          const { data } = await axios.post("/api/auth/token/refresh/", {
            refresh,
          });
          localStorage.setItem("access_token", data.access);
          original.headers.Authorization = `Bearer ${data.access}`;
          return API(original);
        } catch {
          localStorage.clear();
          window.location.href = "/login";
        }
      }
    }
    return Promise.reject(error);
  },
);

// Auth
export const register = (data) => API.post("/auth/register/", data);
export const login = (email, password) =>
  API.post("/auth/login/", { email, password });
export const getProfile = () => API.get("/auth/profile/");
export const updateProfile = (data) => API.put("/auth/profile/", data);

// Categories
export const getCategories = () => API.get("/categories/");
export const createCategory = (data) => API.post("/categories/", data);

// Jobs
export const getJobs = (params) => API.get("/jobs/", { params });
export const getJob = (id) => API.get(`/jobs/${id}/`);
export const createJob = (data) => API.post("/jobs/", data);
export const updateJob = (id, data) => API.put(`/jobs/${id}/`, data);
export const deleteJob = (id) => API.delete(`/jobs/${id}/`);

// Applications
export const applyToJob = (jobId, coverLetter) =>
  API.post("/applications/apply/", { job: jobId, cover_letter: coverLetter });
export const getMyApplications = () => API.get("/applications/my/");
export const getJobApplications = (jobId) =>
  API.get(`/applications/job/${jobId}/`);
export const updateApplicationStatus = (id, status) =>
  API.patch(`/applications/${id}/status/`, { status });

export default API;
