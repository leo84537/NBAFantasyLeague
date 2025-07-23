import { useState } from "react";
import SearchOverlay from "./SearchOverlay";
import { X } from "lucide-react";

export default function HeaderWithSearch() {
  const [query, setQuery] = useState("");
  const [highlightedIndex, setHighlightedIndex] = useState(-1);
  const [showOverlay, setShowOverlay] = useState(false);

  const handleKeyDown = (e) => {
    if (e.key === "ArrowDown") {
      setHighlightedIndex((prev) => prev + 1);
    } else if (e.key === "ArrowUp") {
      setHighlightedIndex((prev) => Math.max(prev - 1, 0));
    } else if (e.key === "Enter") {
      // handle selection
    }
  };

  return (
    <div className="relative w-full max-w-xl mx-auto">
      {/* Search Input */}
      <div className="relative transition-all duration-300 bg-white border border-gray-300 rounded-xl shadow-md">
        <input
          type="text"
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            setShowOverlay(e.target.value.trim().length > 0);
          }}
          placeholder="Search players or teams"
          onKeyDown={handleKeyDown}
          className="w-full px-4 py-2 pr-10 text-sm rounded-xl border-none focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        {query && (
          <button
            onClick={() => {
              setQuery("");
              setShowOverlay(false);
            }}
            className="absolute top-1/2 right-3 -translate-y-1/2 text-gray-400 hover:text-white hover:bg-red-500 rounded-full p-1 transition"
          >
            <X size={16} />
          </button>
        )}
      </div>

      {/* Overlay Dropdown */}
      {showOverlay && (
        <div className="absolute left-0 top-full w-full z-50 mt-1">
          <SearchOverlay
            query={query}
            setQuery={setQuery}
            highlightedIndex={highlightedIndex}
            setHighlightedIndex={setHighlightedIndex}
            onKeyDown={handleKeyDown}
            showOverlay={showOverlay}
          />
        </div>
      )}
    </div>
  );
}
