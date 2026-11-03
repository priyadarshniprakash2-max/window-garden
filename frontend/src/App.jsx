import { useEffect, useState } from "react";

function daysSince(iso) {
  if (!iso) return null;
  const ms = Date.now() - new Date(iso + "T00:00:00").getTime();
  return Math.floor(ms / 86400000);
}

function status(plant) {
  const since = daysSince(plant.last_watered);
  if (since === null) return { text: "Never watered", due: true };
  const left = plant.water_every_days - since;
  if (left <= 0) return { text: "Needs water today", due: true };
  return { text: `Water in ${left} day${left === 1 ? "" : "s"}`, due: false };
}

export default function App() {
  const [plants, setPlants] = useState([]);
  const [name, setName] = useState("");
  const [days, setDays] = useState(7);
  const [error, setError] = useState("");

  async function load() {
    try {
      const res = await fetch("/api/plants");
      if (!res.ok) throw new Error();
      setPlants(await res.json());
      setError("");
    } catch {
      setError("Can't reach the server. Start the FastAPI backend on port 8000.");
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function addPlant(e) {
    e.preventDefault();
    if (!name.trim()) return;
    await fetch("/api/plants", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: name.trim(), water_every_days: Number(days) }),
    });
    setName("");
    load();
  }

  async function water(id) {
    await fetch(`/api/plants/${id}/water`, { method: "POST" });
    load();
  }

  async function remove(id) {
    await fetch(`/api/plants/${id}`, { method: "DELETE" });
    load();
  }

  return (
    <main className="page">
      <header>
        <h1>Window Garden</h1>
        <p className="lede">Keep track of which plants need water today.</p>
      </header>

      {error && <p className="error" role="alert">{error}</p>}

      <ul className="plants">
        {plants.map((p) => {
          const s = status(p);
          return (
            <li key={p.id} className={s.due ? "plant due" : "plant"}>
              <div>
                <h2>{p.name}</h2>
                <p>{s.text} · every {p.water_every_days} days</p>
              </div>
              <div className="actions">
                <button onClick={() => water(p.id)}>Mark watered</button>
                <button className="ghost" onClick={() => remove(p.id)} aria-label={`Remove ${p.name}`}>
                  Remove
                </button>
              </div>
            </li>
          );
        })}
        {!error && plants.length === 0 && (
          <li className="empty">No plants yet. Add your first one below.</li>
        )}
      </ul>

      <form className="add" onSubmit={addPlant}>
        <label>
          Plant name
          <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Fiddle leaf fig" />
        </label>
        <label>
          Water every (days)
          <input type="number" min="1" max="60" value={days} onChange={(e) => setDays(e.target.value)} />
        </label>
        <button type="submit">Add plant</button>
      </form>
    </main>
  );
}
