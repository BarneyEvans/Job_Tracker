import { useState } from "react";
import Application from "./Application";
import Filler from "./Filler";
import { ChevronDown } from "lucide-react";

export default function StageColumn({ stageName, applications, loading, onDelete, accentColor }) {
  const [showHidden, setShowHidden] = useState(false);

  if (loading) {
    return <Filler stageName={stageName} />;
  }

  // --- Separate applications by substate ---
  const upcoming = "upcoming";
  const deadline = "deadline";
  const actionRequired = "action_required";
  const passiveStates = ["applied", "completed"];
  const rejectedState = "rejected";

  // Calculate age (in days)
  const today = new Date();
  const daysOld = (date) => Math.floor((today - new Date(date)) / (1000 * 60 * 60 * 24));

  const upcomingApps = applications
    .filter((app) => app.state === upcoming && daysOld(app.date) <= 60)
    .sort((a, b) => new Date(a.date) - new Date(b.date));

  const deadlineApps = applications
    .filter((app) => app.state === deadline && daysOld(app.date) <= 60)
    .sort((a, b) => new Date(a.date) - new Date(b.date));

  const actionApps = applications
    .filter((app) => app.state === actionRequired && daysOld(app.date) <= 60)
    .sort((a, b) => new Date(a.date) - new Date(b.date));

  const passiveApps = applications
    .filter((app) => passiveStates.includes(app.state) && daysOld(app.date) <= 60)
    .sort((a, b) => new Date(a.date) - new Date(b.date));

  // Hidden apps (rejected OR older than 60 days)
  const hiddenApps = applications.filter(
    (app) => app.state === rejectedState || daysOld(app.date) > 60
  );

  return (
    <div className="flex-1 bg-[#EDF6F9] border-r border-[#b7c2c5b0] flex flex-col">
      {/* Sticky header with accent dot */}
      <h2 className="font-semibold text-lg text-center sticky top-0 bg-[#EDF6F9] z-10 m-6">
        <span style={{ color: accentColor || "#1f2937" }}>{stageName}</span>
      </h2>

      {/* Scrollable content area */}
      <div
        className="flex-1 overflow-y-auto px-4 pb-50 scroll-overlay"
        style={{ maxHeight: "calc(109vh - 40px)", minHeight: "calc(100vh - 40px)" }}
      >
        {/* Upcoming */}
        {upcomingApps.map((app, index) => (
          <Application
            key={`upcoming-${index}`}
            id={app.id}
            company={app.company}
            role={app.role}
            date={app.date}
            isUpcoming
            onDelete={onDelete}
            accentColor={accentColor}
          />
        ))}

        {/* Deadline */}
        {deadlineApps.map((app, index) => (
          <Application
            key={`deadline-${index}`}
            id={app.id}
            company={app.company}
            role={app.role}
            date={app.date}
            isDeadline
            onDelete={onDelete}
            accentColor={accentColor}
          />
        ))}

        {/* Action Required */}
        {actionApps.map((app, index) => (
          <Application
            key={`action-${index}`}
            id={app.id}
            company={app.company}
            role={app.role}
            date={app.date}
            isAction
            onDelete={onDelete}
            accentColor={accentColor}
          />
        ))}

        {/* Passive */}
        {passiveApps.map((app, index) => (
          <Application
            key={`passive-${index}`}
            id={app.id}
            company={app.company}
            role={app.role}
            date={app.date}
            isPassive
            onDelete={onDelete}
            accentColor={accentColor}
          />
        ))}

        {/* Hidden dropdown */}
        {hiddenApps.length > 0 && (
          <div className="mt-4">
            <button
              onClick={() => setShowHidden(!showHidden)}
              className="flex w-full justify-between items-center text-sm text-gray-600 hover:text-gray-800"
            >
              <span>Hidden ({hiddenApps.length})</span>
              <ChevronDown
                size={16}
                className={`transform transition-transform ${showHidden ? "rotate-180" : "rotate-0"}`}
              />
            </button>

            {hiddenApps.length > 0 && (
              <hr className="border-t border-[#b7c2c5b0] mt-2 mb-4" />
            )}

            {showHidden && (
              <div className="mt-2">
                {hiddenApps.map((app, index) => (
                  <Application
                    key={`hidden-${index}`}
                    id={app.id}
                    company={app.company}
                    role={app.role}
                    date={app.date}
                    isRejected={app.state === rejectedState}
                    onDelete={onDelete}
                    accentColor={accentColor}
                  />
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
