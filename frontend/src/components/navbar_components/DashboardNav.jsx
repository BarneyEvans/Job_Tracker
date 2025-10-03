import { NavLink, useNavigate } from "react-router-dom";
import { supabase } from "../../supabaseClient"
import { useState, useEffect } from 'react';

export default function DashboardNav() {
  const [user, setUser] = useState(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [showDropdown, setShowDropdown] = useState(false);
  const navigate = useNavigate();

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

  // Fetch applications matching search query
  useEffect(() => {
    if (!searchQuery || !user) {
      setSearchResults([]);
      return;
    }

  const fetchApplications = async () => {
    const { data, error } = await supabase
      .from("job_applications")
      .select("application_id, job_title, company")
      .or(
        `job_title.ilike.%${searchQuery}%,company.ilike.%${searchQuery}%`
      ) // search both job_title and company
      .eq("user", user.id)
      .limit(5); // limit results for dropdown


    console.log(data);
    console.log(data, error);
    if (!error) {
      setSearchResults(data);
    }
  };


    fetchApplications();
  }, [searchQuery, user]);

  const handleSelect = (appId) => {
    setSearchQuery("");
    setSearchResults([]);
    navigate(`/dashboard/application/${appId}`);
  };

  return (
    <div className="flex top-0 right-0 z-9">
    <nav className="bg-[#FDFFFC] text-white w-full px-4 py-2 border-b-1 border-[#b7c2c5b0] min-h-14 flex items-center justify-between">
        <div className="text-[#011627] space-x-6 hidden md:flex">
          <h1 className="font-bold text-lg"> Dashboard</h1>
        </div>
        {/* Middle: Search Bar */}
          <div className="absolute left-1/2 transform -translate-x-1/2 w-full max-w-md">
            <input
              type="text"
              className="w-full border border-gray-300 rounded-md px-3 py-1 text-gray-700 focus:outline-none focus:ring-1 focus:ring-blue-500"
              placeholder="Search applications..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onFocus={() => setShowDropdown(true)}
              onBlur={() => setTimeout(() => setShowDropdown(false), 150)} // delay to allow click
            />
            {showDropdown && searchResults.length > 0 && (
              <ul className="absolute z-20 w-full bg-white border border-gray-300 rounded-md mt-1 max-h-60 overflow-y-auto shadow-md">
                {searchResults.map((app) => (
                  <li
                    key={app.application_id}
                    className="px-3 py-2 cursor-pointer hover:bg-gray-100 text-gray-700"
                    onMouseDown={() => handleSelect(app.application_id)}
                  >
                    <div className="font-medium">{app.company}</div>
                    <div className="text-sm text-gray-500">{app.job_title}</div>
                  </li>
                ))}
              </ul>
            )}
          </div>
    </nav>
    </div>
  );
}
