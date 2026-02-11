import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { createJob, getCategories } from "../services/api";
import { useAuth } from "../context/AuthContext";

export default function PostJob() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [form, setForm] = useState({
    title: "",
    category: "",
    job_type: "full_time",
    location: "",
    salary_min: "",
    salary_max: "",
    description: "",
    requirements: "",
  });

  useEffect(() => {
    if (!user || (user.role !== "employer" && user.role !== "admin")) {
      navigate("/");
    }
    getCategories()
      .then((res) => setCategories(res.data.results || res.data))
      .catch(() => {});
  }, [user, navigate]);

  const update = (field) => (e) =>
    setForm({ ...form, [field]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const payload = { ...form };
      if (!payload.category) delete payload.category;
      if (!payload.salary_min) delete payload.salary_min;
      if (!payload.salary_max) delete payload.salary_max;
      if (!payload.requirements) delete payload.requirements;
      const { data } = await createJob(payload);
      navigate(`/jobs/${data.id}`);
    } catch (err) {
      const d = err.response?.data;
      if (d) {
        const msgs = [];
        for (const [k, v] of Object.entries(d)) {
          msgs.push(`${k}: ${Array.isArray(v) ? v.join(", ") : v}`);
        }
        setError(msgs.join("\n"));
      } else {
        setError("Failed to create job posting.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto px-6 pt-24 pb-16">
      <div className="bg-slate-800 border border-slate-700 rounded-2xl p-10">
        <h2 className="text-2xl font-extrabold text-white mb-1">
          Post a New Job
        </h2>
        <p className="text-slate-500 mb-8">
          Fill in the details to create a job posting
        </p>

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-sm font-semibold text-slate-400 mb-1.5">
              Job Title *
            </label>
            <input
              type="text"
              required
              value={form.title}
              onChange={update("title")}
              placeholder="e.g. Senior Python Developer"
              className="w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg text-white text-sm outline-none focus:border-indigo-500 transition"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-semibold text-slate-400 mb-1.5">
                Category
              </label>
              <select
                value={form.category}
                onChange={update("category")}
                className="w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg text-white text-sm outline-none focus:border-indigo-500 transition"
              >
                <option value="">Select Category</option>
                {categories.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.name}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-semibold text-slate-400 mb-1.5">
                Job Type *
              </label>
              <select
                value={form.job_type}
                onChange={update("job_type")}
                className="w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg text-white text-sm outline-none focus:border-indigo-500 transition"
              >
                <option value="full_time">Full Time</option>
                <option value="part_time">Part Time</option>
                <option value="contract">Contract</option>
                <option value="remote">Remote</option>
                <option value="internship">Internship</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-sm font-semibold text-slate-400 mb-1.5">
              Location *
            </label>
            <input
              type="text"
              required
              value={form.location}
              onChange={update("location")}
              placeholder="e.g. Addis Ababa, Ethiopia"
              className="w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg text-white text-sm outline-none focus:border-indigo-500 transition"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-semibold text-slate-400 mb-1.5">
                Min Salary
              </label>
              <input
                type="number"
                value={form.salary_min}
                onChange={update("salary_min")}
                placeholder="e.g. 50000"
                className="w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg text-white text-sm outline-none focus:border-indigo-500 transition"
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-slate-400 mb-1.5">
                Max Salary
              </label>
              <input
                type="number"
                value={form.salary_max}
                onChange={update("salary_max")}
                placeholder="e.g. 80000"
                className="w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg text-white text-sm outline-none focus:border-indigo-500 transition"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-semibold text-slate-400 mb-1.5">
              Description *
            </label>
            <textarea
              required
              value={form.description}
              onChange={update("description")}
              rows={5}
              placeholder="Describe the role, responsibilities..."
              className="w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg text-white text-sm outline-none focus:border-indigo-500 transition resize-y"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-slate-400 mb-1.5">
              Requirements
            </label>
            <textarea
              value={form.requirements}
              onChange={update("requirements")}
              rows={4}
              placeholder="List qualifications, skills needed..."
              className="w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg text-white text-sm outline-none focus:border-indigo-500 transition resize-y"
            />
          </div>

          {error && (
            <p className="text-red-400 text-sm whitespace-pre-line">{error}</p>
          )}

          <button
            type="submit"
            disabled={loading}
            className="px-8 py-3 bg-indigo-500 text-white font-semibold rounded-lg hover:bg-indigo-600 transition-all shadow-lg shadow-indigo-500/25 disabled:opacity-50"
          >
            {loading ? "Publishing..." : "Publish Job"}
          </button>
        </form>
      </div>
    </div>
  );
}
