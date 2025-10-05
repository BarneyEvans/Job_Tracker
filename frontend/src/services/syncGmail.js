import { supabase } from "../supabaseClient";

export async function triggerSync() {
  // Get the current logged-in user's ID
  const {
    data: { user },
    error: userError,
  } = await supabase.auth.getUser();

  if (userError || !user) {
    throw new Error("User not logged in");
  }

  const response = await fetch("http://localhost:8000/api/data", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      message: "Start Gmail sync",
      user_id: user.id, // send the user ID instead of the token
    }),
  });

  if (!response.ok) {
    throw new Error(`Server responded with ${response.status}`);
  }

  const result = await response.json();
  console.log("triggerSync result:", result);
  return result;
}

