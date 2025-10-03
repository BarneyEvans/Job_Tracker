import { useParams } from "react-router-dom";
import ApplicationDetailsNav from "../components/navbar_components/ApplicationDetailsNav";
import Sidebar from "../components/side_bar/Sidebar";
import EventTimeline from "../components/details_components/EventTimeline";

export default function ApplicationDetails() {
  const { applicationId } = useParams(); // gets application_id from URL

  return (
    <div className="h-screen flex overflow-hidden">
          <Sidebar />
          <div className="flex-1 flex flex-col">
          <ApplicationDetailsNav />

        <main className="flex-1 overflow-y-auto bg-[#EDF6F9] pl-25 pt-5">
          <EventTimeline applicationId={applicationId} />
        </main>
      </div>
    </div>
  );
}


