import { NavLink } from "react-router-dom";
import { useState, useEffect } from "react";
import { supabase } from "../supabaseClient";

export default function Sidebar() {
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
    <div className="flex h-screen left-0 top-0 bottom-0 z-10">
    <aside className="w-50 bg-[#FDFFFC] text-[#011627] border-r border-[#b7c2c5b0] min-h-screen p-1 flex flex-col ">
      {/* Logo */}
      <NavLink to="/" className="text-3xl font-bold mb-8 text-center mt-5 ">
        VestigoJobs
      </NavLink>

      {/* Navigation links */}
      <nav className="flex flex-col space-y-1 text-[#006D77]">
        <NavLink
          to="/dashboard"
          className={({ isActive }) =>
            isActive ? "text-sm bg-[#EDF6F9] box-border border rounded p-1 border-[#b7c2c5b0]" : "hover:bg-gray-100 rounded p-1 text-sm border border-transparent"
          }
        >
          📋 Application Dashboard     
        </NavLink>
        <NavLink
          to="/job-offers"
          className={({ isActive }) =>
            isActive ? "text-sm bg-[#EDF6F9] box-border border rounded p-1 border-[#b7c2c5b0]" : "hover:bg-gray-100 rounded p-1 text-sm border border-transparent"
          }
        >
          🤝 Job Offers
        </NavLink>
        <NavLink
          to="/calendar"
          className={({ isActive }) =>
            isActive ? "text-sm bg-[#EDF6F9] box-border border rounded p-1 border-[#b7c2c5b0]" : "hover:bg-gray-100 rounded p-1 text-sm border border-transparent"
          }
        >
          📅 Calendar
        </NavLink>
      </nav>
      <div className="flex flex-col gap-2 mb-1 px-1 mt-auto">
          {!user ? (
            <>
              <NavLink
                to="/login"
                className="text-[#011627] hover:underline transition"
              >
                Login
              </NavLink>
              <NavLink
                to="/register"
                className="bg-[#011627] text-[#FDFFFC] px-2 py-1 rounded-lg hover:bg-[#052F51] transition font-semibold"
              >
                Register
              </NavLink>
            </>
          ) : (
            <NavLink
              to="/account"
              className="bg-[#011627] text-[#FDFFFC] px-2 py-1 rounded-lg hover:bg-[#052F51] transition font-semibold"
            >
              Account
            </NavLink>
          )}
        </div>
    </aside>
    </div>
  );
}

