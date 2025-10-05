import { useEffect, useState } from "react";
import { api } from "./lib/api";

export default function App() {
  const [status, setStatus] = useState("checking...");
  const [file, setFile] = useState<File | null>(null);
  const [docId, setDocId] = useState<string | null>(null);
  const [fields, setFields] = useState<any[]>([]);

  useEffect(() => {
    api<{ok:boolean; time:string}>("/api/health")
      .then(d => setStatus(`API OK • ${new Date(d.time).toLocaleString()}`))
      .catch(() => setStatus("API unreachable"));
  }, []);

  const upload = async () => {
    if (!file) return;
    const fd = new FormData();           // standard way to send files with fetch
    fd.append("file", file);
    const res = await fetch(`${API_BASE}/api/documents`, { method:"POST", body: fd });
    const data = await res.json();
    setDocId(data.id);
    setFields(await api<any[]>(`/api/documents/${data.id}/fields`));
  };

  return (
    <div className="min-h-screen p-8 space-y-6">
      <h1 className="text-2xl font-bold">Kill me asap pls (MVP)</h1>
      <div className="text-sm px-3 py-2 rounded bg-gray-100 inline-block">{status}</div>

      <div className="space-y-2">
        <input type="file" onChange={e => setFile(e.target.files?.[0] || null)} />
        <button onClick={upload} className="px-4 py-2 rounded bg-black text-white disabled:opacity-40" disabled={!file}>
          Upload & Process (mock)
        </button>
      </div>

      {docId && (
        <div className="space-y-2">
          <h2 className="text-xl font-semibold">Fields for doc: {docId}</h2>
          <ul className="list-disc pl-6">
            {fields.map(f => (
              <li key={f.id}>
                <span className={f.conf < 0.8 ? "text-red-600" : "text-green-700"}>
                  {f.key}: <b>{f.value}</b> (conf {Math.round(f.conf*100)}%)
                </span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

const API_BASE = "http://localhost:5000";
