import { supabase } from "../supabaseClient";

export async function triggerSync() {
  const session = await supabase.auth.getSession();
  const accessToken = session.data.session?.access_token;

  const response = await fetch("http://localhost:8000/api/data", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${accessToken}`,
    },
    body: JSON.stringify({ message: "Start Gmail sync" }),
  });

  // Always check if response is OK
  if (!response.ok) {
    throw new Error(`Server responded with ${response.status}`);
  }

  const result = await response.json();
  console.log("triggerSync result:", result);
  return result; // ✅ important!
}
