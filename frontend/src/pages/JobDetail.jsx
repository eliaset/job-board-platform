import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getJob, applyToJob } from "../services/api";
import { useAuth } from "../context/AuthContext";

const JOB_TYPE_LABELS = {
  full_time: "Full Time",
  part_time: "Part Time",
  contract: "Contract",
  remote: "Remote",
  internship: "Internship",
};

export default function JobDetail() {
  const { id } = useParams();
  const { user } = useAuth();
  const navigate = useNavigate();
  const [job, setJob] = useState(null);
  const [loading, setLoading] = useState(true);
  const [coverLetter, setCoverLetter] = useState("");
  const [applying, setApplying] = useState(false);
  const [applied, setApplied] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    getJob(id)
      .then((res) => setJob(res.data))
      .catch(() => navigate("/"))
      .finally(() => setLoading(false));
  }, [id, navigate]);

  const handleApply = async () => {
    if (!user) return navigate("/login");
    setApplying(true);
    setError("");
    try {
      await applyToJob(id, coverLetter);
      setApplied(true);
    } catch (err) {
      const d = err.response?.data;
      if (d?.non_field_errors) setError(d.non_field_errors.join(", "));
      else if (d?.detail) setError(d.detail);
      else setError("Failed to apply. Please try again.");
    } finally {
      setApplying(false);
    }
  };

  const formatSalary = (min, max) => {
    if (!min && !max) return null;
    const fmt = (n) => Number(n).toLocaleString();
    if (min && max) return `$${fmt(min)} — $${fmt(max)}`;
    if (min) return `From $${fmt(min)}`;
    return `Up to $${fmt(max)}`;
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center pt-20">
        <div className="w-10 h-10 border-3 border-slate-700 border-t-indigo-500 rounded-full animate-spin" />
      </div>
    );
  }

  if (!job) return null;

  return (
    <div className="max-w-4xl mx-auto px-6 pt-24 pb-16">
      <button
        onClick={() => navigate("/")}
        className="mb-6 px-4 py-2 text-sm border border-slate-600 text-slate-400 rounded-lg hover:border-indigo-500 hover:text-indigo-400 transition"
      >
        ← Back to Jobs
      </button>

      <div className="bg-slate-800 border border-slate-700 rounded-2xl p-10">
        <h1 className="text-3xl font-extrabold text-white mb-2">{job.title}</h1>
        <p className="text-lg text-slate-400 mb-5">
          {job.company_name || "Company"}
        </p>

        <div className="flex flex-wrap gap-3 mb-6">
          <span className="px-3 py-1.5 bg-indigo-500/15 text-indigo-400 rounded-full text-xs font-semibold">
            {JOB_TYPE_LABELS[job.job_type] || job.job_type}
          </span>
          <span className="px-3 py-1.5 bg-slate-700 text-slate-300 rounded-full text-xs font-semibold">
            📍 {job.location}
          </span>
          {job.category_name && (
            <span className="px-3 py-1.5 bg-slate-700 text-slate-300 rounded-full text-xs font-semibold">
              📂 {job.category_name}
            </span>
          )}
          {formatSalary(job.salary_min, job.salary_max) && (
            <span className="px-3 py-1.5 bg-emerald-500/15 text-emerald-400 rounded-full text-xs font-semibold">
              💰 {formatSalary(job.salary_min, job.salary_max)}
            </span>
          )}
        </div>

        <div className="mt-8">
          <h3 className="text-lg font-bold text-indigo-400 mb-3">
            Description
          </h3>
          <p className="text-slate-400 leading-relaxed whitespace-pre-wrap">
            {job.description}
          </p>
        </div>

        {job.requirements && (
          <div className="mt-8">
            <h3 className="text-lg font-bold text-indigo-400 mb-3">
              Requirements
            </h3>
            <p className="text-slate-400 leading-relaxed whitespace-pre-wrap">
              {job.requirements}
            </p>
          </div>
        )}

        <div className="mt-6 text-sm text-slate-500">
          Posted on{" "}
          {new Date(job.created_at).toLocaleDateString("en-US", {
            year: "numeric",
            month: "long",
            day: "numeric",
          })}
          {job.posted_by &&
            ` by ${job.posted_by.first_name} ${job.posted_by.last_name}`}
        </div>

        {/* Apply Section — Job Seekers Only */}
        {user?.role === "job_seeker" && (
          <div className="mt-10 pt-8 border-t border-slate-700">
            {applied ? (
              <div className="text-center py-6">
                <div className="text-4xl mb-3">✅</div>
                <h3 className="text-xl font-bold text-emerald-400">
                  Application Submitted!
                </h3>
                <p className="text-slate-500 mt-1">
                  You will hear back from the employer soon.
                </p>
              </div>
            ) : (
              <>
                <h3 className="text-lg font-bold text-white mb-3">
                  Apply for this Position
                </h3>
                <textarea
                  value={coverLetter}
                  onChange={(e) => setCoverLetter(e.target.value)}
                  rows={4}
                  placeholder="Write a brief cover letter (optional)..."
                  className="w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg text-white text-sm outline-none focus:border-indigo-500 transition resize-y"
                />
                {error && <p className="text-red-400 text-sm mt-2">{error}</p>}
                <button
                  onClick={handleApply}
                  disabled={applying}
                  className="mt-4 px-8 py-3 bg-indigo-500 text-white font-semibold rounded-lg hover:bg-indigo-600 transition-all shadow-lg shadow-indigo-500/25 disabled:opacity-50"
                >
                  {applying ? "Submitting..." : "Submit Application"}
                </button>
              </>
            )}
          </div>
        )}

        {/* Prompt to login */}
        {!user && (
          <div className="mt-10 pt-8 border-t border-slate-700 text-center">
            <p className="text-slate-400 mb-4">
              Want to apply for this position?
            </p>
            <button
              onClick={() => navigate("/login")}
              className="px-8 py-3 bg-indigo-500 text-white font-semibold rounded-lg hover:bg-indigo-600 transition-all shadow-lg shadow-indigo-500/25"
            >
              Login to Apply
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
