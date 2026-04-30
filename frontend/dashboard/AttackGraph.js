export default function AttackGraph({ traces = [] }) {
  const map = {};

  traces.forEach(t => {
    map[t.executor] = (map[t.executor] || 0) + 1;
  });

  return (
    <div>
      <h3>Attack Graph</h3>
      {Object.entries(map).map(([k, v]) => (
        <div key={k}>
          {k}: {v}
        </div>
      ))}
    </div>
  );
}
