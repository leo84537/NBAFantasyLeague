import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "../main";

export default function SearchOverlay({
  query,
  setQuery,
  highlightedIndex,
  setHighlightedIndex,
  onKeyDown,
  showOverlay,
}) {
  const [results, setResults] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchResults = async () => {
      if (!query.trim()) return setResults([]);
      try {
        const [playerRes, teamRes] = await Promise.all([
          axios.get(`/players/search/?query=${query}`),
          axios.get(`/teams/search/?query=${query}`),
        ]);

        const players = playerRes.data.map((p) => ({
          ...p,
          type: "player",
          player_id: p.player_id,
        }));

        const teams = teamRes.data.map((t) => ({
          ...t,
          type: "team",
          team_id: t.team_id,
        }));

        setResults([...players, ...teams]);
      } catch (err) {
        console.error("Search failed", err);
        setResults([]);
      }
    };

    fetchResults();
  }, [query]);

  if (!showOverlay) return null;

  const lowerQuery = query.toLowerCase();

  const startsWith = results.filter((item) =>
    item.name.toLowerCase().startsWith(lowerQuery)
  );
  const contains = results.filter(
    (item) =>
      item.name.toLowerCase().includes(lowerQuery) &&
      !item.name.toLowerCase().startsWith(lowerQuery)
  );

  const filtered = [...startsWith, ...contains];

  const formatTeamRoute = (name) => `/team/${name.replace(/\s+/g, "-")}`;
  const formatPlayerRoute = (name) => `/player/${encodeURIComponent(name)}`;

  return (
    <div className="w-full bg-white border border-gray-200 shadow-lg rounded-xl mt-2 max-h-96 overflow-y-auto animate-slide-down">
      {query && (
        filtered.length > 0 ? (
          filtered.map((item, i) => (
            <div
              key={i}
              className="flex items-center justify-between px-4 py-3 hover:bg-gray-100 cursor-pointer"
              onClick={() => {
                const route =
                  item.type === "team"
                    ? formatTeamRoute(item.name)
                    : formatPlayerRoute(item.name);
                navigate(route);
                setQuery("");
                setHighlightedIndex(-1);
              }}
            >
              <div className="flex items-center gap-3 text-left">
                <img
                  src={
                    item.type === "player"
                      ? `https://cdn.nba.com/headshots/nba/latest/1040x760/${item.player_id}.png`
                      : `https://cdn.nba.com/logos/nba/${item.team_id}/global/L/logo.svg`
                  }
                  onError={(e) => {
                    e.target.onerror = null;
                    e.target.src = "/fallback.png";
                  }}
                  alt={item.name}
                  className="w-10 h-10 rounded-full object-cover"
                />
                <div className="text-left">
                  <div className="text-sm font-semibold text-black">{item.name}</div>
                  <div className="text-xs text-gray-500">
                    {item.type === "player" ? item.team : "NBA Team"}
                  </div>
                </div>
              </div>
              <button className="text-sm px-3 py-1 border rounded font-medium hover:bg-gray-50">
                View
              </button>
            </div>
          ))
        ) : (
          <div className="p-4 text-sm text-gray-500">
            No results for "<span className="font-semibold">{query}</span>"
          </div>
        )
      )}
    </div>
  );
}
