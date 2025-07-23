import { Link, useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import HeaderWithSearch from "../components/HeaderWithSearch";
import api from "../main"; 

export default function TeamPage() {
  const { name } = useParams(); // Example: "Los-Angeles-Lakers"
  const [team, setTeam] = useState(null);
  const [sortKey, setSortKey] = useState("ppg");

  const teamColorMap = {
    ATL: "hover:border-red-600",
    BOS: "hover:border-green-700",
    CHA: "hover:border-purple-600",
    CHI: "hover:border-red-700",
    CLE: "hover:border-yellow-700",
    DAL: "hover:border-blue-800",
    DEN: "hover:border-blue-600",
    DET: "hover:border-red-800",
    GSW: "hover:border-yellow-500",
    HOU: "hover:border-red-500",
    IND: "hover:border-blue-700",
    LAC: "hover:border-red-500",
    LAL: "hover:border-yellow-600",
    MEM: "hover:border-blue-500",
    MIA: "hover:border-red-600",
    MIL: "hover:border-green-600",
    MIN: "hover:border-blue-600",
    NOP: "hover:border-navy-600",
    NYK: "hover:border-orange-600",
    OKC: "hover:border-blue-500",
    ORL: "hover:border-blue-700",
    PHI: "hover:border-blue-800",
    PHX: "hover:border-orange-700",
    POR: "hover:border-red-600",
    SAC: "hover:border-purple-700",
    SAS: "hover:border-gray-600",
    TOR: "hover:border-red-700",
    UTA: "hover:border-green-700",
    WSH: "hover:border-blue-600",
  };
  
  

  useEffect(() => {
    const fetchTeam = async () => {
      try {
        // Replace hyphens with spaces so backend matches "Los Angeles Lakers"
        const formattedName = name.replace(/-/g, " "); // Los-Angeles -> Los Angeles
        console.log("📦 Fetching team:", formattedName);
        const res = await api.get(`/teams/${formattedName}`);
        console.log("✅ Team response:", res.data);
        
        //Sort based on keys
        res.data.players.sort((a, b) => (b[sortKey] || 0) - (a[sortKey] || 0));
        setTeam(res.data);
        
      } catch (err) {
        console.error("Team fetch error:", err);
      }
    };
    fetchTeam();
  }, [name, sortKey]);

  if (!team) return <div className="p-4">Loading...</div>;

  return (
    <div className="p-4 max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-2">{team.name}</h1>
      <HeaderWithSearch />
      <p className="text-gray-600 mb-2 text-sm">Season: {team.season}</p>
      <p className="text-gray-600 mb-2 text-sm">
        Wins: {team.wins} | Losses: {team.losses} | Win %: {team.win_pct}
      </p>

      <img
        src={`https://cdn.nba.com/logos/nba/${team.team_id}/primary/L/logo.svg`}
        alt={`${team.name} logo`}
        className="w-24 h-24 my-4"
        onError={(e) => {
          e.target.src = "https://via.placeholder.com/100";
        }}
      />
      <div className="flex justify-between items-center mt-6 mb-2">
    <h2 className="text-2xl font-semibold">Roster & Stats</h2>
    <select
        value={sortKey}
        onChange={(e) => setSortKey(e.target.value)}
        className="border border-gray-300 rounded px-2 py-1 text-sm"
    >
        <option value="ppg">Sort by PPG</option>
        <option value="rpg">Sort by RPG</option>
        <option value="apg">Sort by APG</option>
        <option value="stl">Sort by STL</option>
        <option value="blk">Sort by BLK</option>
        <option value="tov">Sort by TOV</option>
    </select>
    </div>


      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {team.players && team.players.length > 0 ? (
          team.players.map((player) => {
            const hoverClass = teamColorMap[team.abbreviation] || "hover:border-gray-300";
            return (
                <Link to={`/player/${encodeURIComponent(player.name)}`} className="block">
              <div
                key={player.player_id}
                className={`flex gap-3 items-center p-3 rounded-xl border shadow-sm bg-white transition transform duration-200 border-gray-200 ${hoverClass} hover:scale-105`}
              >
                <img
                  src={`https://cdn.nba.com/headshots/nba/latest/260x190/${player.player_id}.png`}
                  alt={`${player.name} headshot`}
                  onError={(e) => (e.target.src = "/fallback.png")}
                  className="w-14 h-14 rounded-full object-cover flex-shrink-0"
                />

                <div className="w-full overflow-hidden">
                  <h3 className="text-sm font-bold truncate">{player.name}</h3>
                  <p className="text-xs text-gray-500 truncate">
                    {player.position} | {player.height} | {player.weight} lbs
                  </p>
                  <div className="grid grid-cols-3 gap-y-1 gap-x-4 mt-2 text-center text-xs">
                    <div>
                      <div className="font-bold">{player.ppg}</div>
                      <div className="text-gray-400">PPG</div>
                    </div>
                    <div>
                      <div className="font-bold">{player.rpg}</div>
                      <div className="text-gray-400">RPG</div>
                    </div>
                    <div>
                      <div className="font-bold">{player.apg}</div>
                      <div className="text-gray-400">APG</div>
                    </div>
                    <div>
                      <div className="font-bold">{player.stl}</div>
                      <div className="text-gray-400">STL</div>
                    </div>
                    <div>
                      <div className="font-bold">{player.blk}</div>
                      <div className="text-gray-400">BLK</div>
                    </div>
                    <div>
                      <div className="font-bold">{player.tov}</div>
                      <div className="text-gray-400">TOV</div>
                    </div>
                  </div>
                </div>
              </div>
              </Link>
            );
          })
        ) : (
          <p className="text-gray-500">No roster data available.</p>
        )}
      </div>
    </div>
  );
}