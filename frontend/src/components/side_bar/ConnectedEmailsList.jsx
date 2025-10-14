import { useState, useEffect, forwardRef, useImperativeHandle } from "react";
import { supabase } from "../../supabaseClient";

const ConnectedEmailsList = forwardRef(({ userId }, ref) => {
  const [emails, setEmails] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchEmails = async () => {
    if (!userId) return;
    setLoading(true);

    const { data, error } = await supabase
      .from("user_email")
      .select("id, connected_email")
      .eq("user_id", userId)
      .order("id", { ascending: true });

    if (error) console.error(error.message);
    else setEmails(data);

    setLoading(false);
  };

  // Expose fetchEmails to parent via ref
  useImperativeHandle(ref, () => ({
    refetchEmails: fetchEmails
  }));

  useEffect(() => {
    fetchEmails();
  }, [userId]);

  const handleDisconnect = async (id) => {
    const { error } = await supabase.from("user_email").delete().eq("id", id);
    if (!error) fetchEmails();
  };

  if (loading) return <p>Loading connected accounts...</p>;
  if (!emails.length) return <p className="text-gray-500">No connected accounts.</p>;

  return (
    <ul className="space-y-2">
      {emails.map(email => (
        <li key={email.id} className="flex justify-between items-center border p-2 rounded">
          <span>{email.connected_email}</span>
          <button
            className="text-red-500 hover:text-red-700 font-semibold"
            onClick={() => handleDisconnect(email.id)}
          >
            Disconnect
          </button>
        </li>
      ))}
    </ul>
  );
});

export default ConnectedEmailsList;
