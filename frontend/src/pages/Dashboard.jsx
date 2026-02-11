import { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import {
  getMyApplications,
  getJobs,
  getJobApplications,
  updateApplicationStatus,
} from "../services/api";
import { useAuth } from "../context/AuthContext";

const STATUS_COLORS = {
  pending: "bg-amber-500/15 text-amber-400",
  reviewed: "bg-blue-500/15 text-blue-400",
  accepted: "bg-emerald-500/15 text-emerald-400",
  rejected: "bg-red-500/15 text-red-400",
};

export default function Dashboard() {
  const { user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!user) navigate("/login");
  }, [user, navigate]);

  if (!user) return null;

  return user.role === "job_seeker" ? (
    <JobSeekerDashboard />
  ) : (
    <EmployerDashboard />
  );
}

function JobSeekerDashboard() {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getMyApplications()
      .then((res) => setApplications(res.data.results || res.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="max-w-5xl mx-auto px-6 pt-24 pb-16">
      <h2 className="text-2xl font-extrabold text-white mb-1">
        My Applications
      </h2>
      <p className="text-slate-500 mb-8">
        Track the status of your job applications
      </p>

      {loading ? (
        <div className="text-center py-16">
          <div className="w-10 h-10 border-3 border-slate-700 border-t-indigo-500 rounded-full animate-spin mx-auto" />
        </div>
      ) : applications.length === 0 ? (
        <div className="text-center py-16 bg-slate-800 rounded-xl border border-slate-700">
          <div className="text-5xl mb-4">📋</div>
          <h3 className="text-xl font-bold text-white mb-2">
            No Applications Yet
          </h3>
          <p className="text-slate-500 mb-4">
            Start by browsing available jobs.
          </p>
          <Link
            to="/"
            className="px-6 py-3 bg-indigo-500 text-white font-semibold rounded-lg hover:bg-indigo-600 transition-all inline-block"
          >
            Browse Jobs
          </Link>
        </div>
      ) : (
        <div className="grid gap-4">
          {applications.map((app) => (
            <div
              key={app.id}
              className="bg-slate-800 border border-slate-700 rounded-xl p-5 hover:border-indigo-500/50 transition"
            >
              <div className="flex justify-between items-start">
                <div>
                  <Link
                    to={`/jobs/${app.job}`}
                    className="text-lg font-bold text-white hover:text-indigo-400 transition"
                  >
                    {app.job_title || `Job #${app.job}`}
                  </Link>
                  <p className="text-sm text-slate-500 mt-1">
                    Applied{" "}
                    {new Date(app.applied_at).toLocaleDateString("en-US", {
                      year: "numeric",
                      month: "short",
                      day: "numeric",
                    })}
                  </p>
                </div>
                <span
                  className={`px-3 py-1 rounded-full text-xs font-semibold uppercase ${STATUS_COLORS[app.status] || "bg-slate-700 text-slate-300"}`}
                >
                  {app.status}
                </span>
              </div>
              {app.cover_letter && (
                <p className="text-sm text-slate-400 mt-3 line-clamp-2">
                  {app.cover_letter}
                </p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function EmployerDashboard() {
  const [myJobs, setMyJobs] = useState([]);
  const [selectedJob, setSelectedJob] = useState(null);
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loadingApps, setLoadingApps] = useState(false);

  useEffect(() => {
    getJobs({})
      .then((res) => {
        const jobs = res.data.results || [];
        setMyJobs(jobs);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const viewApplications = async (jobId) => {
    setSelectedJob(jobId);
    setLoadingApps(true);
    try {
      const res = await getJobApplications(jobId);
      setApplications(res.data.results || res.data);
    } catch {
      setApplications([]);
    } finally {
      setLoadingApps(false);
    }
  };

  const handleStatusUpdate = async (appId, status) => {
    try {
      await updateApplicationStatus(appId, status);
      setApplications((prev) =>
        prev.map((a) => (a.id === appId ? { ...a, status } : a)),
      );
    } catch {
      // silent fail
    }
  };

  return (
    <div className="max-w-5xl mx-auto px-6 pt-24 pb-16">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h2 className="text-2xl font-extrabold text-white">
            Employer Dashboard
          </h2>
          <p className="text-slate-500">
            Manage your job postings and applications
          </p>
        </div>
        <Link
          to="/post-job"
          className="px-5 py-2.5 bg-indigo-500 text-white font-semibold rounded-lg hover:bg-indigo-600 transition-all shadow-lg shadow-indigo-500/25"
        >
          + Post Job
        </Link>
      </div>

      {loading ? (
        <div className="text-center py-16">
          <div className="w-10 h-10 border-3 border-slate-700 border-t-indigo-500 rounded-full animate-spin mx-auto" />
        </div>
      ) : myJobs.length === 0 ? (
        <div className="text-center py-16 bg-slate-800 rounded-xl border border-slate-700">
          <div className="text-5xl mb-4">📝</div>
          <h3 className="text-xl font-bold text-white mb-2">
            No Job Postings Yet
          </h3>
          <p className="text-slate-500 mb-4">Create your first job posting.</p>
          <Link
            to="/post-job"
            className="px-6 py-3 bg-indigo-500 text-white font-semibold rounded-lg hover:bg-indigo-600 transition-all inline-block"
          >
            Post a Job
          </Link>
        </div>
      ) : (
        <div className="grid gap-4">
          {myJobs.map((job) => (
            <div
              key={job.id}
              className={`bg-slate-800 border rounded-xl p-5 transition ${selectedJob === job.id ? "border-indigo-500" : "border-slate-700 hover:border-slate-600"}`}
            >
              <div className="flex justify-between items-start">
                <div>
                  <Link
                    to={`/jobs/${job.id}`}
                    className="text-lg font-bold text-white hover:text-indigo-400 transition"
                  >
                    {job.title}
                  </Link>
                  <p className="text-sm text-slate-500 mt-1">
                    📍 {job.location} •{" "}
                    {new Date(job.created_at).toLocaleDateString()}
                    {job.application_count !== undefined &&
                      ` • ${job.application_count} applications`}
                  </p>
                </div>
                <button
                  onClick={() => viewApplications(job.id)}
                  className="px-4 py-2 text-sm border border-slate-600 text-slate-400 rounded-lg hover:border-indigo-500 hover:text-indigo-400 transition"
                >
                  View Applications
                </button>
              </div>

              {/* Applications for this job */}
              {selectedJob === job.id && (
                <div className="mt-5 pt-5 border-t border-slate-700">
                  {loadingApps ? (
                    <p className="text-slate-500 text-sm">
                      Loading applications...
                    </p>
                  ) : applications.length === 0 ? (
                    <p className="text-slate-500 text-sm">
                      No applications received yet.
                    </p>
                  ) : (
                    <div className="space-y-3">
                      {applications.map((app) => (
                        <div
                          key={app.id}
                          className="bg-slate-900 rounded-lg p-4"
                        >
                          <div className="flex justify-between items-center">
                            <div>
                              <p className="font-semibold text-white">
                                {app.applicant_name ||
                                  app.applicant_email ||
                                  `Applicant #${app.applicant}`}
                              </p>
                              <p className="text-xs text-slate-500 mt-1">
                                Applied{" "}
                                {new Date(app.applied_at).toLocaleDateString()}
                              </p>
                              {app.cover_letter && (
                                <p className="text-sm text-slate-400 mt-2">
                                  {app.cover_letter}
                                </p>
                              )}
                            </div>
                            <div className="flex items-center gap-2">
                              <span
                                className={`px-2.5 py-1 rounded-full text-xs font-semibold uppercase ${STATUS_COLORS[app.status]}`}
                              >
                                {app.status}
                              </span>
                              <select
                                value={app.status}
                                onChange={(e) =>
                                  handleStatusUpdate(app.id, e.target.value)
                                }
                                className="px-2 py-1 bg-slate-800 border border-slate-700 rounded text-xs text-white outline-none"
                              >
                                <option value="pending">Pending</option>
                                <option value="reviewed">Reviewed</option>
                                <option value="accepted">Accepted</option>
                                <option value="rejected">Rejected</option>
                              </select>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
