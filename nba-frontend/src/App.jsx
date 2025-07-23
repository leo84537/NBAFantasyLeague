import { Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import PlayerPage from "./pages/PlayerPage";
import TeamPage from "./pages/TeamPage";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/player/:name" element={<PlayerPage />} />
      <Route path="/team/:name" element={<TeamPage />} />
    </Routes>
  );
}
