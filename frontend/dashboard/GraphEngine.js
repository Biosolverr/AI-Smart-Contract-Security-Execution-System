export default function GraphEngine({ edges = [] }) {
  return (
    <div>
      <h3>Graph Engine</h3>
      {edges.map((e, i) => (
        <div key={i}>
          {e.from} → {e.to} ({e.type})
        </div>
      ))}
    </div>
  );
}
