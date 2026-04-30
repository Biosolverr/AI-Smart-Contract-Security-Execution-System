export default function StepByStepSimulatorUI({ steps = [] }) {
  return (
    <div>
      <h3>Step Simulation</h3>
      {steps.map((s, i) => (
        <div key={i}>▶ {s}</div>
      ))}
    </div>
  );
}
