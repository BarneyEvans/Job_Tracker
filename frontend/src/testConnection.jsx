import { useEffect } from "react"
import { supabase } from "./supabaseClient"

export default function TestConnection() {
  useEffect(() => {
    const testConnection = async () => {
      const { data, error } = await supabase
        .from("job_applications") // 👈 replace with any table you already have
        .select("*")
        .limit(5)

      if (error) {
        console.error("❌ Supabase connection failed:", error.message)
      } else {
        console.log("✅ Supabase connected! Data:", data)
      }
    }

    testConnection()
  }, [])

  return <p>Check the console for Supabase connection test results.</p>
}