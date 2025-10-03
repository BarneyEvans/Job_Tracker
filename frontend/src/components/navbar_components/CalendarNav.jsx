import { useState, useEffect } from "react";
import { supabase } from "../../supabaseClient";
import { ChevronLeft, ChevronRight } from "lucide-react"; // arrow icons

export default function CalendarNav({ currentWeekStart, onPrevWeek, onNextWeek }) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const fetchUser = async () => {
      const {
        data: { user },
      } = await supabase.auth.getUser();
      setUser(user);
    };

    fetchUser();

    const { data: listener } = supabase.auth.onAuthStateChange(
      (event, session) => {
        setUser(session?.user ?? null);
      }
    );

    return () => listener.subscription.unsubscribe();
  }, []);

  // Compute month range (e.g., "September 2025" or "Sep–Oct 2025")
  const getMonthLabel = () => {
    const start = new Date(currentWeekStart);
    const end = new Date(start);
    end.setDate(end.getDate() + 6);

    const sameMonth = start.getMonth() === end.getMonth();
    const sameYear = start.getFullYear() === end.getFullYear();

    if (sameMonth && sameYear) {
      return `${start.toLocaleString("default", { month: "long" })} ${start.getFullYear()}`;
    } else if (!sameMonth && sameYear) {
      return `${start.toLocaleString("default", { month: "short" })} – ${end.toLocaleString(
        "default",
        { month: "short" }
      )} ${start.getFullYear()}`;
    } else {
      return `${start.toLocaleString("default", { month: "short" })} ${start.getFullYear()} – ${end.toLocaleString(
        "default",
        { month: "short" }
      )} ${end.getFullYear()}`;
    }
  };

  return (
    <div className="flex top-0 right-0 z-9">
    <nav className="bg-[#FDFFFC] text-white w-full px-4 p-2 border-b-1 border-[#b7c2c5b0] min-h-14 flex items-center justify-between">
        <div className="text-[#011627] space-x-6 hidden md:flex">
          <h1 className="font-bold text-lg"> Calendar</h1>
        </div>
        <div className="flex items-center space-x-3 text-[#011627]">
            <h1 className="font-bold text-lg">{getMonthLabel()}</h1>
          <button
            onClick={onPrevWeek}
            className="p-1 rounded hover:bg-gray-200 transition"
          >
            <ChevronLeft size={15} />
          </button>
          <button
            onClick={onNextWeek}
            className="p-1 rounded hover:bg-gray-200 transition"
          >
            <ChevronRight size={15} />
          </button>
          
          
        </div>
      </nav>
    </div>
  );
}
