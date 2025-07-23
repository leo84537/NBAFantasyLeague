import { useEffect, useState } from "react";
import api from "../main";
const API_URL = import.meta.env.VITE_API_URL;


export default function Last10Games({ playerId }) {
  const [games, setGames] = useState([]);

  useEffect(() => {
    const fetchGames = async () => {
      try {
        const res = await api.get(`/players/${playerId}/last10`);
        setGames(res.data);
      } catch (err) {
        console.error("Failed to fetch last 10 games", err);
      }
    };
    fetchGames();
  }, [playerId]);

  if (games.length === 0) return <p className="text-gray-500">No recent games available.</p>;

  return (
    <div className="mt-6">
      <h2 className="text-xl font-bold mb-2">Last 10 Games</h2>
      <table className="w-full table-auto border">
        <thead>
          <tr className="bg-gray-100 text-sm">
            <th className="px-2 py-1">Date</th>
            <th className="px-2 py-1">PTS</th>
            <th className="px-2 py-1">REB</th>
            <th className="px-2 py-1">AST</th>
            <th className="px-2 py-1">FG%</th>
            <th className="px-2 py-1">Opponent</th>
          </tr>
        </thead>
        <tbody>
          {games.map((game) => (
            <tr key={game.game_id} className="text-center text-sm hover:bg-gray-50">
              <td className="px-2 py-1">{game.game_date}</td>
              <td className="px-2 py-1">{game.pts}</td>
              <td className="px-2 py-1">{game.reb}</td>
              <td className="px-2 py-1">{game.ast}</td>
              <td className="px-2 py-1">
                {game.fga > 0 ? `${((game.fgm / game.fga) * 100).toFixed(1)}%` : "0.0%"}
              </td>
              <td className="px-2 py-1">{game.opponent}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
