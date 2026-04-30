export default function RiskScoreCard({ logs = [] }) {

  const score = logs.reduce((a, b) => a + (b.severity || 0), 0);

  return (
    <div>
      <h3>Risk Score</h3>
      <div>{score}</div>
    </div>
  );
}
