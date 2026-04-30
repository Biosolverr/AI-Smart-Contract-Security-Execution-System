export default function GraphEdgesBuilder({ traces = [] }) {

  const edges = traces.map(t => ({
    from: t.intent,
    to: t.executor,
    type: "exploit_flow"
  }));

  return (
    <div>
      <h3>Graph Edges</h3>
      {edges.map((e, i) => (
        <div key={i}>
          {e.from} → {e.to}
        </div>
      ))}
    </div>
  );
}
