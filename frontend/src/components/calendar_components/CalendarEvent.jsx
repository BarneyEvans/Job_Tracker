export default function CalendarEvent({ event }) {
  if (!event) return null;
    console.log(event);
  // Convert the event date into a JS Date object
  const eventDate = new Date(event.date);
  
  const [hours, minutes, seconds] = event.time.split(":").map(Number);

  // Combine date + time
  eventDate.setHours(hours);
  eventDate.setMinutes(minutes);
  eventDate.setSeconds(seconds || 0);

  // Duration fallback
  const duration = event.duration || 60; // default 1 hour

  // Height based on duration (1h = 4rem, since each cell is h-16)
  const height = (duration / 60) * 64; // 64px = h-16

  return (
    <div
      className="absolute left-1 right-1 bg-blue-500 text-white text-xs rounded-md shadow-md p-1 overflow-hidden"
      style={{
        top: `${(minutes / 60) * 64}px`, // offset inside the hour block
        height: `${height}px`,
      }}
    >
      <div className="font-semibold truncate">{event.application_id.stage.charAt(0).toUpperCase()  + event.application_id.stage.slice(1) || "Event"}</div>
      <div className="truncate">{event.application_id.company || "No Company"}</div>
      <div className="text-[10px] opacity-90">
        {eventDate.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
      </div>
    </div>
  );
}
