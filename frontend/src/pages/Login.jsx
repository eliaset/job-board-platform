import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { login as loginApi, getProfile } from "../services/api";
import { useAuth } from "../context/AuthContext";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { loginUser } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const { data: tokens } = await loginApi(email, password);
      localStorage.setItem("access_token", tokens.access);
      localStorage.setItem("refresh_token", tokens.refresh);
      const { data: profile } = await getProfile();
      loginUser(tokens, profile);
      navigate("/dashboard");
    } catch (err) {
      setError(
        err.response?.data?.detail || "Invalid credentials. Please try again.",
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex justify-center items-center px-6 pt-20">
      <div className="w-full max-w-md bg-slate-800 border border-slate-700 rounded-2xl p-10 shadow-xl shadow-indigo-500/5">
        <div className="text-center mb-8">
          <h2 className="text-2xl font-extrabold text-white">Welcome Back</h2>
          <p className="text-slate-500 mt-1">Sign in to your account</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-sm font-semibold text-slate-400 mb-1.5">
              Email
            </label>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="your@email.com"
              className="w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg text-white text-sm outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition"
            />
          </div>
          <div>
            <label className="block text-sm font-semibold text-slate-400 mb-1.5">
              Password
            </label>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              className="w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg text-white text-sm outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition"
            />
          </div>

          {error && <p className="text-red-400 text-sm">{error}</p>}

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 bg-indigo-500 text-white font-semibold rounded-lg hover:bg-indigo-600 transition-all shadow-lg shadow-indigo-500/25 disabled:opacity-50"
          >
            {loading ? "Signing in..." : "Sign In"}
          </button>
        </form>

        <p className="text-center mt-6 text-sm text-slate-500">
          Don't have an account?{" "}
          <Link
            to="/register"
            className="text-indigo-400 hover:text-indigo-300"
          >
            Sign Up
          </Link>
        </p>
      </div>
    </div>
  );
}
