import { useEffect, useState } from "react";
import DashboardNav from "../components/navbar_components/DashboardNav";
import Sidebar from "../components/Sidebar";
import Board from "../components/application_board/Board";
import { getApplicationsByStage } from "../services/fetch_applications";

export default function Home() {
  const [stages, setStages] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      const data = await getApplicationsByStage();
      setStages(data);
      setLoading(false);
    }
    fetchData();
  }, []);
  
  return (
    <div className="h-screen flex overflow-hidden">
      <Sidebar />
      <div className="flex-1 flex flex-col ">
        <DashboardNav />
        <main className="flex z-0 bg-[#EDF6F9] overflow-hidden">
          <Board stages={stages} loading={loading} />
        </main>
      </div>
    </div>
  );
}


