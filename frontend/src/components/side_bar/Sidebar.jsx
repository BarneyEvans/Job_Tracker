import { NavLink } from "react-router-dom";
import { useState, useEffect } from "react";
import { supabase } from "../../supabaseClient";
import GmailSyncButton from "./GmailSyncButton";

export default function Sidebar() {
    const [user, setUser] = useState(null);
    const [isOverlayOpen, setIsOverlayOpen] = useState(false);
    
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

        const handleOverlayToggle = () => {
    setIsOverlayOpen(prev => !prev);
  };
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
            <>
            <button
              type="button"
              onClick={handleOverlayToggle}
              className="w-full flex items-center justify-center py-2 px-4 border border-gray-300 rounded-lg shadow-sm hover:bg-gray-100 transition"
            >
              <svg
                className="w-5 h-5 mr-2"
                viewBox="0 0 48 48"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  fill="#EA4335"
                  d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"
                />
                <path
                  fill="#4285F4"
                  d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"
                />
                <path
                  fill="#FBBC05"
                  d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"
                />
                <path
                  fill="#34A853"
                  d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"
                />
                <path fill="none" d="M0 0h48v48H0z" />
              </svg>

              <span className="text-sm font-medium text-gray-700">
                Connect Gmail
              </span>
            </button>
            <NavLink
              to="/account"
              className="bg-[#011627] text-[#FDFFFC] px-2 py-1 rounded-lg hover:bg-[#052F51] transition font-semibold"
            >
              Account
            </NavLink>
            {isOverlayOpen && (
              <>
                {/* Subtle dimming layer */}
                <div
                  className="fixed inset-0 z-40"
                  style={{ backgroundColor: "rgba(0,0,0,0.1)" }} // 10% black
                  onClick={handleOverlayToggle} // click outside to close
                />

                {/* Modal content */}
                <div className="fixed inset-0 flex items-center justify-center z-50">
                  <div className="relative bg-white p-6 rounded-lg shadow-lg max-w-md w-full">
                    
                    {/* Cross button top-right */}
                    <button
                      className="absolute top-3 right-3 text-gray-500 hover:text-gray-700 text-lg font-bold"
                      onClick={handleOverlayToggle}
                    >
                      &times;
                    </button>

                    {/* Modal text */}
                    <h2 className="text-xl font-bold mb-2">Gmail Connections</h2>
                    <p className="mb-4 text-gray-700">
                      You may connect multiple Gmail accounts to VestigoJobs. Currently, we're only compatible with Gmail - so if you do not have an account please create a new Gmail account and come back.
                    </p>

                    {/* Gmail Sync Button */}
                    <GmailSyncButton />
                  </div>
                </div>
              </>
            )}

            </>
          )}
        </div>
    </aside>
    </div>
  );
}

