import React from "react";
import axios from "axios";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "./App";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>
);

// baseURL "http://localhost:8000"
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL 
});

export default api;
