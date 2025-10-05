import { NavLink } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import { X, Calendar, AlarmClock, MessageSquare, AlertCircle } from "lucide-react";
import { deleteApplication } from "../../services/deleteApplication";

export default function Application({
  id,
  company,
  role,
  date,
  isUpcoming = false,
  isAction = false,
  isPassive = false,
  isRejected = false,
  isDeadline = false,
  onDelete,
}) {
  const today = new Date();
  const appDate = date ? new Date(date) : null;
  const daysSince = appDate ? Math.floor((today - appDate) / (1000 * 60 * 60 * 24)) : null;

  const navigate = useNavigate();

  async function handleDelete(e) {
    e.preventDefault();
    e.stopPropagation();
    const confirmed = window.confirm(
      `Delete "${company} - ${role}"? This removes its timeline and calendar. This action cannot be undone.`
    );
    if (!confirmed) return;
    try {
      await deleteApplication(id);
      if (typeof onDelete === "function") onDelete(id);
    } catch (err) {
      console.error("Delete failed", err);
      alert("Failed to delete application. Please try again.");
    }
  }

  let daysLabel = "";
  if (daysSince === 0) daysLabel = "Today";
  else if (daysSince === 1) daysLabel = "Yesterday";
  else if (daysSince !== null) daysLabel = `${daysSince}d ago`;

  return (
    <NavLink
      to={`/dashboard/application/${id}`}
      className={({ isActive }) =>
        `block w-full bg-white p-4 mb-2 rounded text-left border ${
          isActive
            ? "bg-gray-100 border-[#011627]"
            : "hover:bg-gray-50 border-[#b7c2c5b0] hover:border-[#011627]"
        } relative`
      }
    >
      {/* X delete button */}
      <button
        aria-label="Delete application"
        className="absolute top-2 right-2 p-1 rounded text-gray-400 hover:text-red-600 hover:bg-red-50"
        onClick={handleDelete}
      >
        <X size={16} />
      </button>

      {/* Header: company (with right padding so it doesn't sit under the X) */}
      <div className="flex justify-between items-start pr-6">
        <div className="font-bold text-blue-500">{company}</div>
      </div>

      {/* Role */}
      <div className="mt-1">{role}</div>

      {/* Status pills */}
      <div className="mt-2 flex items-center gap-2 flex-wrap">
        {isAction && (
          <span className="inline-flex items-center gap-1 rounded-full bg-gray-100 px-2 py-0.5 text-xs text-gray-600">
            <AlertCircle size={14} /> Action Required
          </span>
        )}
        {isPassive && (
          <span className="inline-flex items-center gap-1 rounded-full bg-gray-100 px-2 py-0.5 text-xs text-gray-600">
            <MessageSquare size={14} /> Awaiting response
          </span>
        )}
        {isUpcoming && (
          <button
            onClick={(e) => {
              e.preventDefault();
              navigate("/calendar");
            }}
            className="inline-flex items-center gap-1 rounded-full bg-gray-100 px-2 py-0.5 text-xs text-gray-600 hover:bg-gray-200"
          >
            <Calendar size={14} /> Scheduled
          </button>
        )}
        {isDeadline && (
          <span className="inline-flex items-center gap-1 rounded-full bg-gray-100 px-2 py-0.5 text-xs text-gray-600">
            <AlarmClock size={14} /> Deadline
          </span>
        )}
        {isRejected && (
          <span className="inline-flex items-center gap-1 rounded-full bg-gray-100 px-2 py-0.5 text-xs text-gray-600">
            <AlertCircle size={14} /> Rejected
          </span>
        )}
      </div>

      {/* Footer: relative age */}
      {daysLabel && (
        <div className="text-xs text-gray-500 text-right mt-2">{daysLabel}</div>
      )}
    </NavLink>
  );
}

