import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { getJobs, getCategories } from "../services/api";

const JOB_TYPE_LABELS = {
  full_time: "Full Time",
  part_time: "Part Time",
  contract: "Contract",
  remote: "Remote",
  internship: "Internship",
};

const JOB_TYPE_COLORS = {
  full_time: "bg-emerald-500/15 text-emerald-400",
  part_time: "bg-blue-500/15 text-blue-400",
  contract: "bg-amber-500/15 text-amber-400",
  remote: "bg-purple-500/15 text-purple-400",
  internship: "bg-pink-500/15 text-pink-400",
};

export default function Home() {
  const [jobs, setJobs] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    search: "",
    category: "",
    job_type: "",
    ordering: "-created_at",
  });
  const [totalJobs, setTotalJobs] = useState(0);

  useEffect(() => {
    getCategories()
      .then((res) => setCategories(res.data.results || res.data))
      .catch(() => {});
  }, []);

  useEffect(() => {
    setLoading(true);
    const params = {};
    if (filters.search) params.search = filters.search;
    if (filters.category) params.category = filters.category;
    if (filters.job_type) params.job_type = filters.job_type;
    if (filters.ordering) params.ordering = filters.ordering;

    getJobs(params)
      .then((res) => {
        setJobs(res.data.results || []);
        setTotalJobs(res.data.count || 0);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [filters]);

  const formatSalary = (min, max) => {
    if (!min && !max) return null;
    const fmt = (n) => Number(n).toLocaleString();
    if (min && max) return `$${fmt(min)} — $${fmt(max)}`;
    if (min) return `From $${fmt(min)}`;
    return `Up to $${fmt(max)}`;
  };

  return (
    <div>
      {/* Hero */}
      <section className="relative pt-32 pb-20 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-slate-900 via-indigo-950/50 to-slate-900" />
        <div className="absolute inset-0">
          <div className="absolute top-1/2 left-1/5 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl" />
          <div className="absolute top-1/3 right-1/5 w-80 h-80 bg-purple-500/8 rounded-full blur-3xl" />
        </div>
        <div className="relative max-w-7xl mx-auto px-6 text-center">
          <h1 className="text-5xl font-extrabold tracking-tight mb-4">
            Find Your{" "}
            <span className="bg-gradient-to-r from-indigo-400 via-purple-400 to-amber-400 bg-clip-text text-transparent">
              Dream Job
            </span>{" "}
            Today
          </h1>
          <p className="text-lg text-slate-400 max-w-xl mx-auto mb-10">
            Discover job opportunities from top companies. Start your career
            journey now.
          </p>

          {/* Search Bar */}
          <div className="flex gap-3 max-w-2xl mx-auto bg-slate-800 p-2 rounded-2xl border border-slate-700 shadow-xl shadow-indigo-500/5">
            <div className="flex-1 flex items-center gap-2 px-3">
              <span>🔍</span>
              <input
                type="text"
                placeholder="Job title, keyword..."
                className="flex-1 bg-transparent text-white text-sm outline-none placeholder-slate-500"
                value={filters.search}
                onChange={(e) =>
                  setFilters({ ...filters, search: e.target.value })
                }
              />
            </div>
            <button
              onClick={() => setFilters({ ...filters })}
              className="px-6 py-3 bg-indigo-500 text-white font-semibold rounded-xl hover:bg-indigo-600 transition-all shadow-lg shadow-indigo-500/30"
            >
              Search
            </button>
          </div>

          {/* Stats */}
          <div className="flex justify-center gap-16 mt-12">
            <div className="text-center">
              <div className="text-3xl font-extrabold text-indigo-400">
                {totalJobs}
              </div>
              <div className="text-sm text-slate-500 mt-1">Active Jobs</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-extrabold text-indigo-400">
                {categories.length}
              </div>
              <div className="text-sm text-slate-500 mt-1">Categories</div>
            </div>
          </div>
        </div>
      </section>

      {/* Filters & Jobs */}
      <section className="max-w-7xl mx-auto px-6 py-8">
        <div className="flex flex-wrap gap-4 items-end mb-8 p-5 bg-slate-800 rounded-xl border border-slate-700">
          <div className="flex flex-col gap-1.5 min-w-[160px]">
            <label className="text-xs font-semibold uppercase tracking-wider text-slate-500">
              Category
            </label>
            <select
              className="px-3 py-2 bg-slate-900 border border-slate-700 rounded-lg text-sm text-white outline-none focus:border-indigo-500 transition"
              value={filters.category}
              onChange={(e) =>
                setFilters({ ...filters, category: e.target.value })
              }
            >
              <option value="">All Categories</option>
              {categories.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.name}
                </option>
              ))}
            </select>
          </div>
          <div className="flex flex-col gap-1.5 min-w-[160px]">
            <label className="text-xs font-semibold uppercase tracking-wider text-slate-500">
              Job Type
            </label>
            <select
              className="px-3 py-2 bg-slate-900 border border-slate-700 rounded-lg text-sm text-white outline-none focus:border-indigo-500 transition"
              value={filters.job_type}
              onChange={(e) =>
                setFilters({ ...filters, job_type: e.target.value })
              }
            >
              <option value="">All Types</option>
              {Object.entries(JOB_TYPE_LABELS).map(([k, v]) => (
                <option key={k} value={k}>
                  {v}
                </option>
              ))}
            </select>
          </div>
          <div className="flex flex-col gap-1.5 min-w-[160px]">
            <label className="text-xs font-semibold uppercase tracking-wider text-slate-500">
              Sort By
            </label>
            <select
              className="px-3 py-2 bg-slate-900 border border-slate-700 rounded-lg text-sm text-white outline-none focus:border-indigo-500 transition"
              value={filters.ordering}
              onChange={(e) =>
                setFilters({ ...filters, ordering: e.target.value })
              }
            >
              <option value="-created_at">Newest First</option>
              <option value="created_at">Oldest First</option>
              <option value="-salary_min">Highest Salary</option>
              <option value="title">Title (A-Z)</option>
            </select>
          </div>
          <button
            onClick={() =>
              setFilters({
                search: "",
                category: "",
                job_type: "",
                ordering: "-created_at",
              })
            }
            className="px-4 py-2 text-sm border border-slate-600 text-slate-400 rounded-lg hover:border-indigo-500 hover:text-indigo-400 transition"
          >
            Clear Filters
          </button>
        </div>

        {/* Job Cards */}
        {loading ? (
          <div className="text-center py-16">
            <div className="w-10 h-10 border-3 border-slate-700 border-t-indigo-500 rounded-full animate-spin mx-auto mb-4" />
            <p className="text-slate-500">Loading jobs...</p>
          </div>
        ) : jobs.length === 0 ? (
          <div className="text-center py-16">
            <div className="text-5xl mb-4">🔍</div>
            <h3 className="text-xl font-bold text-white mb-2">No Jobs Found</h3>
            <p className="text-slate-500">
              Try adjusting your filters or search terms.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {jobs.map((job) => (
              <Link
                key={job.id}
                to={`/jobs/${job.id}`}
                className="group bg-slate-800 border border-slate-700 rounded-xl p-6 transition-all hover:border-indigo-500 hover:-translate-y-0.5 hover:shadow-xl hover:shadow-indigo-500/5 relative overflow-hidden"
              >
                <div className="absolute top-0 left-0 right-0 h-0.5 bg-gradient-to-r from-indigo-500 to-purple-500 opacity-0 group-hover:opacity-100 transition-opacity" />
                <div className="flex justify-between items-start mb-3">
                  <h3 className="font-bold text-white text-lg leading-snug pr-2">
                    {job.title}
                  </h3>
                  <span
                    className={`px-2.5 py-1 rounded-full text-xs font-semibold whitespace-nowrap ${JOB_TYPE_COLORS[job.job_type] || "bg-slate-700 text-slate-300"}`}
                  >
                    {JOB_TYPE_LABELS[job.job_type] || job.job_type}
                  </span>
                </div>
                <p className="text-slate-400 text-sm mb-3">
                  {job.company_name || "Company"}
                </p>
                <div className="flex flex-wrap gap-4 text-xs text-slate-500">
                  <span>📍 {job.location}</span>
                  {job.category_name && <span>📂 {job.category_name}</span>}
                  <span>
                    🕐 {new Date(job.created_at).toLocaleDateString()}
                  </span>
                </div>
                {formatSalary(job.salary_min, job.salary_max) && (
                  <div className="mt-4 pt-4 border-t border-slate-700 text-emerald-400 font-bold">
                    {formatSalary(job.salary_min, job.salary_max)}
                  </div>
                )}
              </Link>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
