import StageColumn from "./StageColumn";

export default function Board({ stages, loading, onDelete }) {
  // Mapping from DB values -> UI labels
  const stageMap = {
    applied: "Applied 📨",
    action_required: "Action Required 🔍",
    interview: "Interview 💬",
    assessment: "Assessment 💻",
  };

  // Ensure every stage exists in the final list
  const stagesWithDefaults = Object.entries(stageMap).map(([dbName, label]) => {
    const stage = stages.find((s) => s.name === dbName);
    return {
      dbName, // keep for internal use if needed
      name: label, // pretty label for rendering
      applications: stage ? stage.applications : [],
    };
  });

  return (
    <div className="flex flex-1">
      {stagesWithDefaults.map((stage) => (
        <StageColumn
          key={stage.dbName}
          stageName={stage.name} // pretty display
          applications={stage.applications}
          loading={loading}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
}

