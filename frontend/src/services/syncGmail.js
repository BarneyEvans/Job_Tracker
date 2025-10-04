import { supabase } from "../supabaseClient";

export async function triggerSync() {
  const session = await supabase.auth.getSession();
  const accessToken = session.data.session?.access_token;

  const response = await fetch("http://localhost:8000/sync-gmail", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${accessToken}`, // send the JWT
    },
    body: JSON.stringify({ /* maybe extra info if needed */ }),
  });

  const result = await response.json();
  console.log(result);
}