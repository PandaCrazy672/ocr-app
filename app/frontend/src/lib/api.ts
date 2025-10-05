export const API_BASE = "http://localhost:5000";
export async function api<T>(path: string, opts: RequestInit = {}): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, opts);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}
