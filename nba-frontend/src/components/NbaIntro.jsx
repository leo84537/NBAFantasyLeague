import { useEffect, useState } from "react";

export default function NbaIntro({ onComplete }) {
  const [stage, setStage] = useState(0);

  useEffect(() => {
    const steps = [800, 800, 800, 500]; // duration for each letter + pause
    let step = 0;

    const interval = setInterval(() => {
      step++;
      setStage(step);
      if (step > steps.length - 1) {
        clearInterval(interval);
        onComplete?.(); // Notify parent to show main content
      }
    }, steps[step]);

    return () => clearInterval(interval);
  }, [onComplete]);

  return (
    <div className="fixed inset-0 bg-black text-white flex justify-center items-center z-50">
      <div className="text-7xl sm:text-9xl font-extrabold tracking-widest flex space-x-4">
        <span className={`transition duration-500 ${stage >= 1 ? "opacity-100" : "opacity-0 translate-y-4"}`}>N</span>
        <span className={`transition duration-500 ${stage >= 2 ? "opacity-100" : "opacity-0 translate-y-4"}`}>B</span>
        <span className={`transition duration-500 ${stage >= 3 ? "opacity-100" : "opacity-0 translate-y-4"}`}>A</span>
      </div>
    </div>
  );
}
