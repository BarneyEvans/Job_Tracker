import { useState, useEffect } from "react";
import CalendarNav from "../components/navbar_components/CalendarNav";
import Sidebar from "../components/Sidebar";
import CalendarEvent from "../components/calendar_components/CalendarEvent";
import { supabase } from "../supabaseClient";

export default function Calendar() {
  const weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
  const hours = Array.from({ length: 24 }, (_, i) => `${i}:00`);
  const today = new Date();

  // Compute start of the week (Monday)
  const getStartOfWeek = (date) => {
    const d = new Date(date);
    const day = d.getDay();
    const diff = d.getDate() - ((day + 6) % 7); // Monday = 0
    return new Date(d.setDate(diff));
  };

  const [currentWeekStart, setCurrentWeekStart] = useState(getStartOfWeek(today));
  const [events, setEvents] = useState([]);

  const handlePrevWeek = () => {
    const prev = new Date(currentWeekStart);
    prev.setDate(prev.getDate() - 7);
    setCurrentWeekStart(prev);
  };

  const handleNextWeek = () => {
    const next = new Date(currentWeekStart);
    next.setDate(next.getDate() + 7);
    setCurrentWeekStart(next);
  };

  const weekDates = weekdays.map((_, i) => {
    const d = new Date(currentWeekStart);
    d.setDate(d.getDate() + i);
    return d;
  });

  // Fetch events for current week
  useEffect(() => {
    const fetchEvents = async () => {
      const start = weekDates[0].toISOString();
      const end = weekDates[6].toISOString();

      const { data, error } = await supabase
        .from("calendar")
        .select("*, application_id(job_title, company, stage)")
        .gte("date", start)
        .lte("date", end);

      if (!error) setEvents(data);
      else console.error(error);
    };

    fetchEvents();
  }, [currentWeekStart]);

  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar className="w-64 flex-shrink-0" />
      <div className="flex-1 flex flex-col">
        <CalendarNav
          currentWeekStart={currentWeekStart}
          onPrevWeek={handlePrevWeek}
          onNextWeek={handleNextWeek}
        />

        {/* Weekly Calendar Area */}
        <div className="flex-1 overflow-auto bg-gray-50">
          {/* Weekday headers (sticky) */}
          <div className="grid grid-cols-8 text-center border-b border-gray-300 bg-gray-50 sticky top-0 z-10">
            <div className="w-16 bg-gray-50"></div> {/* empty corner for hours */}
            {weekDates.map((date, i) => {
              const isToday = date.toDateString() === today.toDateString();
              return (
                <div
                  key={i}
                  className={`py-2 font-semibold border-l border-gray-300 ${
                    isToday ? "text-blue-600" : "text-gray-700"
                  }`}
                >
                  {weekdays[i]} <br />
                  <span
                    className={`text-sm font-normal px-2 py-1 rounded-full ${
                      isToday ? "bg-blue-600 text-white" : "text-gray-500"
                    }`}
                  >
                    {date.getDate()}
                  </span>
                </div>
              );
            })}
          </div>

          {/* Calendar grid */}
          <div className="grid grid-cols-8">
            {/* Hour labels column */}
            <div className="flex flex-col border-gray-300">
              {hours.map((hour) => (
                <div
                  key={hour}
                  className="h-16 border-b border-gray-200 text-xs text-gray-500 flex items-start justify-end pr-1"
                >
                  {hour}
                </div>
              ))}
            </div>

            {/* Days columns */}
            {weekdays.map((_, i) => (
              <div key={i} className="flex flex-col border-l border-gray-300 relative">
                {hours.map((_, hourIndex) => (
                  <div
                    key={hourIndex}
                    className="h-16 border-b border-gray-200 hover:bg-gray-100 cursor-pointer relative"
                  >
                    {/* Render events for this day and hour */}
                    {events
                      .filter((event) => {
                        const eventDate = new Date(event.date);

                        const [hours, minutes, seconds] = event.time.split(":").map(Number);

                        // Combine date + time
                        eventDate.setHours(hours);
                        eventDate.setMinutes(minutes);
                        eventDate.setSeconds(seconds || 0);
                        const eventDay = (eventDate.getDay() + 6) % 7; // Monday = 0
                        return eventDay === i && eventDate.getHours() === hourIndex;
                      })
                      .map((event) => (
                        <CalendarEvent key={event.event_id} event={event} />
                      ))}
                  </div>
                ))}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
