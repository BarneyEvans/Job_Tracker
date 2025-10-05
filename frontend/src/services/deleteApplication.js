import { supabase } from "../supabaseClient";

export async function deleteApplication(applicationId) {
  const {
    data: { user },
    error: userError,
  } = await supabase.auth.getUser();

  if (userError || !user) {
    throw new Error("User not logged in");
  }

  const resp = await fetch(
    `http://localhost:8000/api/applications/${applicationId}?user_id=${encodeURIComponent(
      user.id
    )}`,
    {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
    }
  );

  if (!resp.ok) {
    const text = await resp.text().catch(() => "");
    throw new Error(`Delete failed (${resp.status}): ${text}`);
  }

  return resp.json();
}

