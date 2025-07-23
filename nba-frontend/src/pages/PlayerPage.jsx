import { useParams, Link } from "react-router-dom";

import { useEffect, useState } from "react";
import api from "../main";
import { teamStyles } from "../teamStyles";
import HeaderWithSearch from "../components/HeaderWithSearch";
import {
  ResponsiveContainer,
  LineChart,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  Bar,
  Cell,
  ReferenceLine,
} from "recharts";
import { FaHeart, FaRegHeart } from "react-icons/fa";

const statOptions = [
  { label: "Points", key: "ppg", gameKey: "pts" },
  { label: "Rebounds", key: "rpg", gameKey: "reb" },
  { label: "Assists", key: "apg", gameKey: "ast" },
  { label: "Blocks", key: "blk", gameKey: "blk" },
  { label: "Steals", key: "stl", gameKey: "stl" },
  { label: "Turnovers", key: "tov", gameKey: "to" },
];

export default function PlayerPage() {
  const { name } = useParams();
  const [player, setPlayer] = useState(null);
  const [last10Games, setLast10Games] = useState([]);
  const [selectedStat, setSelectedStat] = useState("ppg");
  const [liked, setLiked] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [playerRes, gamesRes] = await Promise.all([
          api.get(`/players/${name}`),
          api.get(`/players/${name}/last10`),
        ]);
        setPlayer(playerRes.data);
        setLast10Games(gamesRes.data);
        setSelectedStat("ppg");
      } catch (err) {
        console.error("Fetch error:", err);
      }
    };
    fetchData();
  }, [name]);

  if (!player) return <div className="p-4">❌ I am not playing this season heee heee.</div>;

  const team = player.team;
  const style = teamStyles[team] || {
    color: "#1e3a8a",
    logo: "",
  };

  const selected = statOptions.find((s) => s.key === selectedStat);
  const gameKey = selected.gameKey;
  const statLabel = selected.label;
  const seasonAverage = player[selected.key];
  const chartData = [{ game_date: "", [gameKey]: null }, ...last10Games,{ game_date: "", [gameKey]: null } ];

  return (
    <div className="w-full min-h-screen">
      {/* Banner */}
      <div
        className="relative bg-[teamColor] w-full h-24 px-6 flex items-center justify-between"
        style={{ backgroundColor: style.color }}
      >
        {/* Left side: logo + name */}
        <div className="flex items-center gap-4 text-white">
        <Link to="/">
          <img
            src={style.logo}
            alt={team}
            className="w-14 h-14 bg-white rounded-full p-1"
          />
          </Link>
          <div>
            <p className="text-xs uppercase">{team} | {player.position?.toUpperCase()}</p>
            <h1 className="text-3xl font-bold">{player.name}</h1>
          </div>
        </div>

        {/* Center: search bar */}
        <div className="absolute left-1/2 top-1/2 transform -translate-x-1/2 -translate-y-1/2 w-full max-w-md z-50">
          <HeaderWithSearch />
        </div>

        {/* Right side: like button */}
        <button
          onClick={() => setLiked(!liked)}
          className="bg-white rounded-full p-2 text-lg text-red-500 shadow transition"
        >
          {liked ? <FaHeart /> : <FaRegHeart />}
        </button>
      </div>


      {/* Bio Section */}
      <div className="flex flex-col sm:flex-row items-center sm:items-start gap-6 mt-6 px-6">
        <img
          src={`https://cdn.nba.com/headshots/nba/latest/1040x760/${player.player_id}.png`}
          alt={player.name}
          className="w-36 h-36 rounded-full object-cover border"
        />
        <div className="text-sm text-gray-700">
          <p><strong>Team:</strong> {team}</p>
          <p><strong>Season:</strong> {player.season}</p>
          <p><strong>Position:</strong> {player.position}</p>
          <p><strong>Height:</strong> {player.height} ({player.height_inches} in)</p>
          <p><strong>Weight:</strong> {player.weight} lbs</p>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4 mt-6 px-6">
        {statOptions.map((s) => (
          <div
            key={s.key}
            className="bg-white rounded-lg p-4 shadow text-center border border-gray-200"
          >
            <div className="text-2xl font-bold">{player[s.key]}</div>
            <div className="text-sm text-gray-500 mt-1">{s.label}</div>
          </div>
        ))}
      </div>

      {/* Stat Selector */}
      <div className="mt-8 px-6">
        <label htmlFor="stat" className="text-sm font-medium text-gray-700 mr-2">
          Select Stat:
        </label>
        <select
          id="stat"
          value={selectedStat}
          onChange={(e) => setSelectedStat(e.target.value)}
          className="border rounded px-2 py-1 text-sm"
        >
          {statOptions.map((s) => (
            <option key={s.key} value={s.key}>
              {s.label}
            </option>
          ))}
        </select>
      </div>

      {/* Chart */}
      <div className="bg-white rounded-lg shadow p-4 mt-4 mx-6 mb-10">
        <h2 className="text-lg font-semibold mb-2">{statLabel} over Last 10 Games</h2>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart
            data={chartData}
            margin={{ top: 10, right: 60, left: 40, bottom: 40 }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis
              dataKey="game_date"
              tick={{ fontSize: 12 }}
              angle={-45}
              textAnchor="end"
              height={60}
            />
            <YAxis />
            <Tooltip
              content={({ active, payload, label }) => {
                if (!active || !payload || !payload.length) return null;
                const barPoint = payload.find(
                  (p) =>
                    p.dataKey === gameKey &&
                    p.payload[gameKey] !== null &&
                    p.payload[gameKey] !== undefined
                );
                if (!barPoint) return null;
                return (
                  <div className="bg-white p-2 border rounded shadow text-sm">
                    <div className="font-medium">Game Date: {label}</div>
                    <div>
                      {statLabel}: <strong>{barPoint.value}</strong>
                    </div>
                  </div>
                );
              }}
            />
            <Bar
              dataKey={gameKey}
              radius={[4, 4, 0, 0]}
              barCategoryGap={15}
              barGap={4}
              isAnimationActive={true}
            >
              {chartData.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={
                    entry[gameKey] == null
                      ? "#ffffff"
                      : entry[gameKey] < seasonAverage
                      ? "#f87171"
                      : "#4ade80"
                  }
                />
              ))}
            </Bar>
            <ReferenceLine
              y={seasonAverage}
              label={{
                value: `Season Avg (${seasonAverage})`,
                position: "insideRight",
                fill: "#1e3a8a",
                fontSize: 12,
                fontWeight: "bold",
                dx: -10,
                dy: -10,
              }}
              stroke="#1e3a8a"
              strokeWidth={3}
              strokeDasharray="4 4"
              ifOverflow="extendDomain"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
