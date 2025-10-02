// src/services/applications.js
import { supabase } from "../supabaseClient";

export async function getApplicationsByStage() {
  // Example: fetch all applications and group by stage
  const { data, error } = await supabase
    .from("job_applications")
    .select("*");

  if (error) {
    console.error("Error fetching applications:", error);
    return [];
  }
  // Group applications by stage
  const stagesMap = {};
  data.forEach((app) => {
    if (!stagesMap[app.stage]) stagesMap[app.stage] = [];
    stagesMap[app.stage].push({ id: app.application_id, company: app.company, role: app.job_title, state: app.substate, date: app.latest_date});
  });

  // Convert to array of objects
  return Object.entries(stagesMap).map(([stage, applications]) => ({
    name: stage,
    applications,
  }));
}
