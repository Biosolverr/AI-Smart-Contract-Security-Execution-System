import { useMemo, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { motion } from "framer-motion";

// Mock executors
const EXECUTORS = [
  "financial_executor",
  "audit_executor",
  "social_executor",
  "consensus_executor",
];

function fakeAttackScore(input) {
  const lower = input.toLowerCase();
  let score = 0;
  if (lower.includes("ignore") || lower.includes("override")) score += 60;
  if (lower.includes("system") || lower.includes("executor")) score += 50;
  if (input.length > 120) score += 20;
  return Math.min(100, score + Math.floor(Math.random() * 20));
}

function fakeRoute(input) {
  const score = fakeAttackScore(input);
  let executor = EXECUTORS[Math.floor(Math.random() * EXECUTORS.length)];
  if (score > 70) executor = "consensus_executor";
  if (score < 30) executor = "audit_executor";
  const confidence = Math.max(30, 100 - score);
  return { executor, score, confidence };
}

export default function GenRouteUI() {
  const [input, setInput] = useState("");
  const [logs, setLogs] = useState([]);

  const graphData = useMemo(() => {
    const counts = {};
    EXECUTORS.forEach((e) => (counts[e] = 0));
    logs.forEach((l) => counts[l.executor]++);
    return counts;
  }, [logs]);

  const runSimulation = () => {
    const result = fakeRoute(input);
    setLogs((prev) => [
      { input, ...result, time: Date.now() },
      ...prev,
    ]);
    setInput("");
  };

  return (
    <div className="p-6 grid grid-cols-3 gap-4">
      {/* CONTROL PANEL */}
      <Card className="col-span-1">
        <CardContent className="p-4 space-y-3">
          <h2 className="text-lg font-bold">GenRoute Control</h2>

          <Input
            placeholder="simulate attack or prompt..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />

          <Button onClick={runSimulation} className="w-full">
            Simulate Route
          </Button>

          <div className="pt-2 space-y-1">
            <h3 className="font-semibold">Executors</h3>
            {EXECUTORS.map((e) => (
              <Badge key={e} className="mr-1">
                {e}
              </Badge>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* GRAPH */}
      <Card className="col-span-1">
        <CardContent className="p-4">
          <h2 className="font-bold mb-2">Routing Graph</h2>
          <div className="space-y-2">
            {Object.entries(graphData).map(([k, v]) => (
              <div key={k}>
                <div className="flex justify-between text-sm">
                  <span>{k}</span>
                  <span>{v}</span>
                </div>
                <div className="h-2 bg-gray-200 rounded">
                  <div
                    className="h-2 bg-black rounded"
                    style={{ width: `${v * 20}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* LOGS / HEATMAP */}
      <Card className="col-span-1">
        <CardContent className="p-4">
          <h2 className="font-bold mb-2">Attack Heatmap</h2>
          <div className="space-y-2 max-h-[400px] overflow-auto">
            {logs.map((l, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="p-2 border rounded text-xs"
              >
                <div className="flex justify-between">
                  <span>{l.executor}</span>
                  <span>⚠ {l.score}</span>
                </div>
                <div className="text-gray-500 truncate">
                  {l.input}
                </div>
                <div className="text-xs opacity-60">
                  conf: {l.confidence}
                </div>
              </motion.div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
