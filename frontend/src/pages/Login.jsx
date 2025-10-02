import { useState } from "react";
import { supabase } from "../supabaseClient";
import { NavLink } from "react-router-dom";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage("");

    const { error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });

    if (error) {
      setMessage(error.message);
    } else {
      setMessage("✅ Successfully logged in!");
      // Optionally redirect after login
    }

    setLoading(false);
  };

  const handleGoogleLogin = async () => {
    await supabase.auth.signInWithOAuth({ provider: "google" });
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="w-full max-w-md bg-white rounded-2xl shadow-lg p-8">
        <h2 className="text-2xl font-bold text-center text-[#011627] mb-6">
          Login to Your Account
        </h2>
        <form onSubmit={handleLogin} className="space-y-5">
          <div>
            <label className="block text-gray-700 text-sm mb-2">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none"
              placeholder="johndoe@example.com"
            />
          </div>
          <div className="relative">
            <label className="block text-gray-700 text-sm mb-2">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none"
              placeholder="••••••••"
            />
            <NavLink
              to="/forgot-password"
              className="absolute right-0 top-0 text-sm text-[#011627] hover:underline mt-2 mr-2"
            >
              Forgot password?
            </NavLink>
          </div>
          <button
            type="submit"
            disabled={loading}
            className="w-full py-2 bg-[#011627] text-white font-semibold rounded-lg hover:bg-[#052F51] transition"
          >
            {loading ? "Logging in..." : "Login"}
          </button>
        </form>

        {/* OR separator */}
        <div className="flex items-center my-4">
          <hr className="flex-grow border-gray-300" />
          <span className="px-2 text-gray-500">or</span>
          <hr className="flex-grow border-gray-300" />
        </div>

        {/* Continue with Google */}
        <button
            type="button"
            onClick={async () => {
                const { error } = await supabase.auth.signInWithOAuth({
                provider: "google",
                options: {
                    // Optional: redirect after login
                    // redirectTo: window.location.origin
                },
                });
                if (error) console.error("Error signing in with Google:", error.message);
            }}
            className="w-full flex items-center justify-center py-2 px-4 border border-gray-300 rounded-lg shadow-sm hover:bg-gray-100 transition"
            >
            <svg
                className="w-5 h-5 mr-2"
                viewBox="0 0 48 48"
                xmlns="http://www.w3.org/2000/svg"
            >
                <path
                fill="#EA4335"
                d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"
                />
                <path
                fill="#4285F4"
                d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"
                />
                <path
                fill="#FBBC05"
                d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"
                />
                <path
                fill="#34A853"
                d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"
                />
                <path fill="none" d="M0 0h48v48H0z" />
            </svg>

            <span className="text-sm font-medium text-gray-700">
                Login with Google
            </span>
        </button>

        {/* Create account & Passkey */}
        <p className="mt-6 text-center text-sm text-gray-600">
          New here?{" "}
          <NavLink to="/register" className="text-[#011627] hover:underline">
            Create an account
          </NavLink>
        </p>
        <p className="mt-2 text-center text-sm text-[#011627] hover:underline cursor-pointer">
          Sign in with a passkey
        </p>

        {message && (
          <p className="mt-4 text-center text-sm text-gray-600">{message}</p>
        )}
      </div>
    </div>
  );
}
