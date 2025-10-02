import { NavLink } from "react-router-dom";
import { useNavigate } from "react-router-dom";

export default function Application({
  id, // 👈 unique id for each application
  company,
  role,
  date,
  isUpcoming = false,
  isAction = false,
  isPassive = false,
  isRejected = false,
  isDeadline = false
}) {
  // Calculate days since
  const today = new Date();
  const appDate = date ? new Date(date) : null;
  const daysSince = appDate
    ? Math.floor((today - appDate) / (1000 * 60 * 60 * 24))
    : null;

  const navigate = useNavigate();

  let daysLabel = "";
  if (daysSince === 0) {
    daysLabel = "Today";
  } else if (daysSince === 1) {
    daysLabel = "Yesterday";
  } else if (daysSince !== null) {
    daysLabel = `${daysSince}d ago`;
  }

  return (
    <NavLink
  to={`/dashboard/application/${id}`}
  className={({ isActive }) =>
    `block w-full bg-white p-4 mb-2 rounded text-left border ${
      isActive
        ? "bg-gray-100 border-[#011627]" // 👈 active styling
        : "hover:bg-gray-50 border-[#b7c2c5b0] hover:border-[#011627]"
    }`
  }
>
  <div className="flex justify-between items-center">
    <div className="font-bold text-blue-500">{company}</div>

    {isAction && <div className="text-xs text-gray-500">Take action!</div>}
    {isPassive && <div className="text-xs text-gray-500">Awaiting response ⌛</div>}
    
    {isUpcoming && (
      <button
          onClick={(e) => {
            e.preventDefault(); // prevent outer link navigation
            navigate("/calendar");
          }}
          className="text-xs text-gray-500 hover:underline"
        >
          Scheduled 📅
        </button>
    )}
    {isDeadline && <div className="text-xs text-gray-500">Deadline ⏰</div>}

    {isRejected && <div className="text-xs text-gray-500">Rejected ❌</div>}
  </div>

  <div>{role}</div>

  {daysLabel && (
    <div className="text-xs text-gray-500 text-right mt-2">{daysLabel}</div>
  )}
</NavLink>
  );
}