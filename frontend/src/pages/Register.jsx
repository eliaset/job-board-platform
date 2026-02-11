import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { register as registerApi, getProfile } from "../services/api";
import { useAuth } from "../context/AuthContext";

export default function Register() {
  const [form, setForm] = useState({
    email: "",
    first_name: "",
    last_name: "",
    role: "job_seeker",
    company_name: "",
    phone: "",
    password: "",
    password_confirm: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { loginUser } = useAuth();
  const navigate = useNavigate();

  const update = (field) => (e) =>
    setForm({ ...form, [field]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    if (form.password !== form.password_confirm) {
      setError("Passwords do not match.");
      return;
    }
    setLoading(true);
    try {
      const { data } = await registerApi(form);
      // Auto-login after registration
      localStorage.setItem("access_token", data.tokens.access);
      localStorage.setItem("refresh_token", data.tokens.refresh);
      const { data: profile } = await getProfile();
      loginUser(data.tokens, profile);
      navigate("/dashboard");
    } catch (err) {
      const d = err.response?.data;
      if (d) {
        const msgs = [];
        for (const [k, v] of Object.entries(d)) {
          msgs.push(`${k}: ${Array.isArray(v) ? v.join(", ") : v}`);
        }
        setError(msgs.join("\n"));
      } else {
        setError("Registration failed. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex justify-center items-center px-6 pt-24 pb-12">
      <div className="w-full max-w-lg bg-slate-800 border border-slate-700 rounded-2xl p-10 shadow-xl shadow-indigo-500/5">
        <div className="text-center mb-8">
          <h2 className="text-2xl font-extrabold text-white">Create Account</h2>
          <p className="text-slate-500 mt-1">Join the JobBoard community</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-5">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-semibold text-slate-400 mb-1.5">
                First Name
              </label>
              <input
                type="text"
                required
                value={form.first_name}
                onChange={update("first_name")}
                placeholder="John"
                className="w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg text-white text-sm outline-none focus:border-indigo-500 transition"
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-slate-400 mb-1.5">
                Last Name
              </label>
              <input
                type="text"
                required
                value={form.last_name}
                onChange={update("last_name")}
                placeholder="Doe"
                className="w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg text-white text-sm outline-none focus:border-indigo-500 transition"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-semibold text-slate-400 mb-1.5">
              Email
            </label>
            <input
              type="email"
              required
              value={form.email}
              onChange={update("email")}
              placeholder="your@email.com"
              className="w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg text-white text-sm outline-none focus:border-indigo-500 transition"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-slate-400 mb-1.5">
              I am a
            </label>
            <select
              value={form.role}
              onChange={update("role")}
              className="w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg text-white text-sm outline-none focus:border-indigo-500 transition"
            >
              <option value="job_seeker">Job Seeker</option>
              <option value="employer">Employer</option>
            </select>
          </div>

          {form.role === "employer" && (
            <div>
              <label className="block text-sm font-semibold text-slate-400 mb-1.5">
                Company Name
              </label>
              <input
                type="text"
                value={form.company_name}
                onChange={update("company_name")}
                placeholder="Your Company"
                className="w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg text-white text-sm outline-none focus:border-indigo-500 transition"
              />
            </div>
          )}

          <div>
            <label className="block text-sm font-semibold text-slate-400 mb-1.5">
              Phone (optional)
            </label>
            <input
              type="text"
              value={form.phone}
              onChange={update("phone")}
              placeholder="+251..."
              className="w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg text-white text-sm outline-none focus:border-indigo-500 transition"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-semibold text-slate-400 mb-1.5">
                Password
              </label>
              <input
                type="password"
                required
                minLength={8}
                value={form.password}
                onChange={update("password")}
                placeholder="••••••••"
                className="w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg text-white text-sm outline-none focus:border-indigo-500 transition"
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-slate-400 mb-1.5">
                Confirm Password
              </label>
              <input
                type="password"
                required
                value={form.password_confirm}
                onChange={update("password_confirm")}
                placeholder="••••••••"
                className="w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg text-white text-sm outline-none focus:border-indigo-500 transition"
              />
            </div>
          </div>

          {error && (
            <p className="text-red-400 text-sm whitespace-pre-line">{error}</p>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 bg-indigo-500 text-white font-semibold rounded-lg hover:bg-indigo-600 transition-all shadow-lg shadow-indigo-500/25 disabled:opacity-50"
          >
            {loading ? "Creating Account..." : "Create Account"}
          </button>
        </form>

        <p className="text-center mt-6 text-sm text-slate-500">
          Already have an account?{" "}
          <Link to="/login" className="text-indigo-400 hover:text-indigo-300">
            Sign In
          </Link>
        </p>
      </div>
    </div>
  );
}
