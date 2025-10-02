import { useState, useEffect } from "react";
import { supabase } from "../../supabaseClient";

export default function EventTimeline({ applicationId }) {
  const [events, setEvents] = useState([]);
  const [selectedEmail, setSelectedEmail] = useState(null);

  useEffect(() => {
    const fetchEvents = async () => {
      if (!applicationId) return; // wait until id is available

      const { data, error } = await supabase
        .from("application_events")
        .select("*")
        .eq("application_id", applicationId) // 🔥 filter by URL id
        .order("event_date", { ascending: true });

      if (error) {
        console.error(error);
      } else {
        setEvents(data);
      }
    };

    fetchEvents();
  }, [applicationId]);

  return (
    <div className="relative flex">
      {/* Timeline */}
      <div className="relative border-l-2 border-gray-300 pl-8 ml-20 flex-1">
        {events.map((event) => (
          <TimelineEvent
            key={event.event_id}
            event={event}
            onShowEmail={() => setSelectedEmail(event.email_text)}
          />
        ))}
      </div>

      {/* Email panel */}
      {selectedEmail && (
        <div className="fixed right-0 top-0 bottom-0 w-2/5 bg-white p-10  mt-19 mr-10 mb-10 rounded border border-gray-200 overflow-y-auto">

          <button
            className="absolute top-3 right-3 pr-1 text-gray-600 hover:text-black text-xl"
            onClick={() => setSelectedEmail(null)}
          >
            ✕
          </button>
          <h2 className="font-bold text-lg mb-4">Email</h2>
          <div className="whitespace-pre-wrap text-sm text-gray-800">
            {selectedEmail}
          </div>
        </div>
      )}
    </div>
  );
}

function TimelineEvent({ event, onShowEmail }) {
  return (
    <div className="mb-8 relative flex items-center">
      {/* Date */}
      <div className="absolute -left-50 text-sm text-gray-500 top-1/2 -translate-y-1/2">
        {new Date(event.event_date).toLocaleDateString("en-GB", {
          weekday: "long", // full day name (e.g., Monday)
          day: "2-digit",
          month: "2-digit",
          year: "numeric",
        })}
      </div>

      {/* Timeline dot */}
      <div className="absolute -left-[41px] top-1/2 -translate-y-1/2 w-4 h-4 bg-[#011627] rounded-full border-2 border-white"></div>

      {/* Event content */}
      <div className="bg-white p-4 rounded border border-gray-200 w-3/7">
        <h3 className="font-bold text-lg">
          {event.event_summary || event.event_type}
        </h3>
        {event.notes && (
          <p className="text-sm text-gray-600 mt-1">{event.notes}</p>
        )}

        {/* Show email button */}
        {event.email_text && (
          <div className="mt-3">
            <button
              className="text-sm text-[#011627] font-semibold hover:underline"
              onClick={onShowEmail}
            >
              Show email
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
