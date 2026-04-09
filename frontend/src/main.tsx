import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import { AppProviders } from "./app/providers/AppProviders";
import { AppRouter } from "./app/router/AppRouter";

ReactDOM.createRoot(document.getElementById("app")!).render(
  <React.StrictMode>
    <AppProviders>
      <AppRouter />
    </AppProviders>
  </React.StrictMode>
);
