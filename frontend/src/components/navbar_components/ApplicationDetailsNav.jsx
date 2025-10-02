import { NavLink } from "react-router-dom";
import { supabase } from "../../supabaseClient";
import { useState, useEffect } from "react";
import { ChevronLeft } from "lucide-react"; // ⬅️ use Lucide instead of inline SVG

export default function ApplicationDetailsNav() {
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

  return (
    <div className="flex top-0 right-0 z-10">
    <nav className="bg-[#FDFFFC] text-white w-full px-4 py-2 border-b-1 border-[#b7c2c5b0] min-h-14 flex items-center justify-between">
        <div className="flex justify-between items-center">
          <NavLink
            to="/dashboard"
            className="flex items-center text-[#011627] font-bold hover:text-[#052F51] transition"
          >
            <ChevronLeft className="w-5 h-5 mr-2" /> {/* ⬅️ Lucide Arrow */}
            Dashboard
          </NavLink>
        </div>
      </nav>
    </div>
  );
}

