import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { user, logoutUser } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logoutUser();
    navigate("/");
  };

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-slate-900/85 backdrop-blur-xl border-b border-slate-700/50">
      <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
        <Link
          to="/"
          className="flex items-center gap-2 text-xl font-bold text-white"
        >
          <span className="text-2xl">💼</span>
          <span>
            Job<span className="text-indigo-400">Board</span>
          </span>
        </Link>

        <div className="flex items-center gap-3">
          <Link
            to="/"
            className="px-4 py-2 text-sm font-medium text-slate-300 hover:text-white hover:bg-indigo-500/10 rounded-lg transition-all"
          >
            Browse Jobs
          </Link>

          {!user ? (
            <>
              <Link
                to="/login"
                className="px-4 py-2 text-sm font-medium text-slate-300 hover:text-white hover:bg-indigo-500/10 rounded-lg transition-all"
              >
                Login
              </Link>
              <Link
                to="/register"
                className="px-5 py-2 text-sm font-semibold bg-indigo-500 text-white rounded-lg hover:bg-indigo-600 transition-all shadow-lg shadow-indigo-500/25"
              >
                Sign Up
              </Link>
            </>
          ) : (
            <>
              <Link
                to="/dashboard"
                className="px-4 py-2 text-sm font-medium text-slate-300 hover:text-white hover:bg-indigo-500/10 rounded-lg transition-all"
              >
                Dashboard
              </Link>
              {(user.role === "employer" || user.role === "admin") && (
                <Link
                  to="/post-job"
                  className="px-4 py-2 text-sm font-medium text-slate-300 hover:text-white hover:bg-indigo-500/10 rounded-lg transition-all"
                >
                  Post Job
                </Link>
              )}
              <div className="flex items-center gap-3 ml-2 pl-4 border-l border-slate-700">
                <div className="w-8 h-8 rounded-full bg-indigo-500 flex items-center justify-center text-sm font-bold text-white">
                  {user.first_name?.[0] || user.email[0].toUpperCase()}
                </div>
                <span className="text-sm font-medium text-slate-300">
                  {user.first_name || user.email}
                </span>
                <button
                  onClick={handleLogout}
                  className="px-3 py-1.5 text-xs font-semibold border border-slate-600 text-slate-400 rounded-lg hover:border-indigo-500 hover:text-indigo-400 transition-all"
                >
                  Logout
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}
