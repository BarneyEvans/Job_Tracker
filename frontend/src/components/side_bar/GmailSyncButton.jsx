import React, { useState } from "react";
import { triggerSync } from "../../services/syncGmail";
import { supabase } from "../../supabaseClient";

export default function GmailSyncButton() {
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState("");

  const handleSync = async () => {
    setLoading(true);
    setStatus("");

    try {
      const { data: emails, error: emailError } = await supabase
        .from("user_email")
        .select("*")

      if (emailError) throw emailError;
      console.log(emails);
      if (!emails || emails.length === 0) {
        // ❌ No connected emails
        alert("You must connect your email first.");
        setStatus("⚠️ No connected emails");
        return;
      }

      // ✅ Step 3: If emails exist, trigger the sync
      const result = await triggerSync();
      setStatus(`✅ ${result.message}`);
    } catch (error) {
      console.error("Sync failed:", error);
      setStatus("❌ Sync failed — check console");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full">
      <button
        type="button"
        onClick={handleSync}
        disabled={loading}
        className="w-full flex items-center justify-center py-2 px-4 border border-gray-300 rounded-lg shadow-sm hover:bg-gray-100 transition"
      >
        {/* 🔄 Sync Icon (SVG) */}
        <svg
          className={`w-5 h-5 mr-2 ${loading ? "animate-spin" : ""}`}
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M4 4v6h6M20 20v-6h-6M5 19a9 9 0 0114-8M19 5a9 9 0 01-14 8"
          />
        </svg>

        <span className="text-sm font-medium text-gray-700">
          {loading ? "Syncing..." : "Sync Gmail"}
        </span>
      </button>

      {status && (
        <p className="mt-2 text-xs text-gray-500 text-center">{status}</p>
      )}
    </div>
  );
}
