import { supabase } from "../supabaseClient"
import Navbar from "../components/navbar_components/DashboardNav"
import Sidebar from "../components/side_bar/Sidebar"

export default function Account() {
  const handleSignOut = async () => {
    const { error } = await supabase.auth.signOut()
    if (error) {
      console.error("Error signing out:", error.message)
    } else {
      // Optionally redirect to home or login page
      window.location.href = "/"
    }
  }

  return (
        <div className="flex h-screen overflow-hidden">
              {/* Sidebar always full height */}
              <Sidebar />
        
              {/* Main content area */}
              <div className="flex-1 flex flex-col">
                {/* Navbar aligned next to sidebar */}
                <Navbar />
                <h1 className="text-2xl font-bold mb-4">Account Page</h1>
                <button
                    onClick={handleSignOut}
                    className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition"
                >
                    Sign Out
                </button>
                
              </div>
            </div>
  )
}
