import { NavLink } from 'react-router-dom';
import { supabase } from "../../supabaseClient"
import { useState, useEffect } from 'react';

export default function OffersNav() {
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
        <div className="text-[#011627] space-x-6 hidden md:flex">
          <h1 className="font-bold text-lg"> Job Offers</h1>
        </div>
    </nav>
    </div>
  );
}