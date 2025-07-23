import HeaderWithSearch from "../components/HeaderWithSearch";
import HomeContent from "../components/HomeContent";
import NbaIntro from "../components/NbaIntro";

export default function HomePage() {
  return (
    <div className="relative w-full min-h-screen bg-gradient-to-br from-sky-100 to-white">
      {/* Background banner art or image */}
      <div className="absolute inset-0 bg-[url('/your-background.svg')] bg-no-repeat bg-top bg-cover opacity-10 pointer-events-none" />

      {/* Centered Hero content */}
      <div className="flex flex-col justify-center items-center text-center py-32 px-4 relative z-10">
        <h1 className="text-5xl font-bold mb-6 text-gray-900">NBA Insights</h1>
        <p className="text-lg text-gray-600 mb-10">Search players or teams to explore stats and trends</p>

        <div className="w-full max-w-xl">
          <HeaderWithSearch />
        </div>
      </div>
    </div>
  );
}
