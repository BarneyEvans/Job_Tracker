import StageColumn from "./StageColumn";

export default function Board({ stages, loading, onDelete }) {
  // Toggle to revert if needed
  const USE_NEW_HEADERS = true;

  const NEW_LABELS = {
    applied: "Applied",
    action_required: "Action Required",
    interview: "Interview",
    assessment: "Assessment",
  };

  // Old mapping kept for easy rollback (same labels, previously had emojis)
  const OLD_LABELS = {
    applied: "Applied",
    action_required: "Action Required",
    interview: "Interview",
    assessment: "Assessment",
  };

  const ACCENTS = {
    applied: "#2563eb", // blue-600
    action_required: "#d97706", // amber-600
    interview: "#4f46e5", // indigo-600
    assessment: "#16a34a", // green-600
  };

  const labelMap = USE_NEW_HEADERS ? NEW_LABELS : OLD_LABELS;

  const stagesWithDefaults = Object.entries(labelMap).map(([dbName, label]) => {
    const stage = stages.find((s) => s.name === dbName);
    return {
      dbName,
      name: label,
      accent: ACCENTS[dbName],
      applications: stage ? stage.applications : [],
    };
  });

  return (
    <div className="flex flex-1">
      {stagesWithDefaults.map((stage) => (
        <StageColumn
          key={stage.dbName}
          stageName={stage.name}
          applications={stage.applications}
          loading={loading}
          accentColor={stage.accent}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
}
