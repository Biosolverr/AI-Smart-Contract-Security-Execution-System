import { useMemo, useState } from "react";

// Если у вас нет shadcn/ui, используем стандартные HTML элементы с классами Tailwind
// Для работы этого кода убедитесь, что Tailwind CSS подключен в index.html

const EXECUTORS = [
  "financial_executor",
  "audit_executor",
  "social_executor",
  "consensus_executor",
];

// Конфигурация API
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function GenRouteUI() {
  const [input, setInput] = useState("");
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [lastResult, setLastResult] = useState(null);
  
  const graphData = useMemo(() => {
    const counts = {};
    EXECUTORS.forEach((e) => (counts[e] = 0));
    logs.forEach((l) => {
      if (counts[l.executor] !== undefined) counts[l.executor]++;
    });
    return counts;
  }, [logs]);

  const runSimulation = async () => {
    if (!input.trim()) return;
    setLoading(true);
    
    try {
      const response = await fetch(`${API_URL}/api/route`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ input }),
      });
      
      if (!response.ok) throw new Error("Network response was not ok");
      
      const data = await response.json();
      
      const newLog = {
        input,
        executor: data.executor,
        score: data.attack_score,
        confidence: data.confidence,
        time: Date.now(),
      };
      
      setLogs((prev) => [newLog, ...prev]);
      setLastResult(data);
      setInput("");
    } catch (error) {
      console.error("Error:", error);
      alert("Failed to connect to GenRoute API. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (score) => {
    if (score > 70) return "text-red-500 bg-red-900/20 border-red-500";
    if (score > 30) return "text-yellow-500 bg-yellow-900/20 border-yellow-500";
    return "text-green-500 bg-green-900/20 border-green-500";
  };

  return (
    <div className="min-h-screen bg-slate-900 text-white p-6 font-sans">
      <header className="mb-8 text-center">
        <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
          🛡 GenRoute AI Firewall
        </h1>
        <p className="text-slate-400 mt-2">Real-time Transaction Routing & Security Analysis</p>
      </header>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-7xl mx-auto">
        
        {/* CONTROL PANEL */}
        <div className="md:col-span-1 space-y-6">
          <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-lg">
            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
              <span>🎮</span> Control Panel
            </h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm text-slate-400 mb-1">Input Payload</label>
                <textarea
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg p-3 text-sm focus:ring-2 focus:ring-blue-500 outline-none transition-all"
                  rows="4"
                  placeholder="Simulate attack or normal transaction..."
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && runSimulation()}
                />
              </div>
              
              <button 
                onClick={runSimulation} 
                disabled={loading}
                className={`w-full py-3 rounded-lg font-medium transition-all ${
                  loading 
                    ? "bg-slate-700 cursor-not-allowed" 
                    : "bg-blue-600 hover:bg-blue-500 active:scale-95"
                }`}
              >
                {loading ? "Analyzing..." : "Simulate Route"}
              </button>
              
              {lastResult && (
                <div className={`mt-4 p-4 rounded-lg border ${getStatusColor(lastResult.attack_score)}`}>
                  <div className="flex justify-between items-center mb-2">
                    <span className="font-bold">Status:</span>
                    <span className="uppercase font-bold">{lastResult.attack_score > 70 ? "BLOCKED" : "ALLOWED"}</span>
                  </div>
                  <div className="text-sm space-y-1 opacity-90">
                    <div>Executor: {lastResult.executor}</div>
                    <div>Threat Score: {lastResult.attack_score}/100</div>
                    <div>Confidence: {(lastResult.confidence * 100).toFixed(1)}%</div>
                  </div>
                </div>
              )}
            </div>
          </div>
          
          {/* Executors Legend */}
          <div className="bg-slate-800 p-6 rounded-xl border border-slate-700">
            <h3 className="font-semibold mb-3 text-sm text-slate-400">ACTIVE EXECUTORS</h3>
            <div className="flex flex-wrap gap-2">
              {EXECUTORS.map((e) => (
                <span key={e} className="px-3 py-1 bg-slate-700 rounded-full text-xs font-mono border border-slate-600">
                  {e.replace('_executor', '')}
                </span>
              ))}
            </div>
          </div>
        </div>
        
        {/* GRAPH VISUALIZATION */}
        <div className="md:col-span-1 bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-lg">
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <span>📊</span> Routing Distribution
          </h2>
          <div className="space-y-4">
            {Object.entries(graphData).map(([key, value]) => {
              const total = logs.length || 1;
              const percent = Math.round((value / total) * 100);
              const colorClass = key.includes('consensus') ? 'bg-red-500' : 
                                  key.includes('audit') ? 'bg-yellow-500' : 'bg-blue-500';
              
              return (
                <div key={key}>
                  <div className="flex justify-between text-xs mb-1 text-slate-300">
                    <span>{key.replace('_executor', '')}</span>
                    <span>{value} ({percent}%)</span>
                  </div>
                  <div className="h-3 bg-slate-900 rounded-full overflow-hidden">
                    <div 
                      className={`h-full ${colorClass} transition-all duration-500`}
                      style={{ width: `${percent}%` }}
                    />
                  </div>
                </div>
              );
            })}
            {logs.length === 0 && (
              <div className="text-center text-slate-500 text-sm py-8">
                No data yet. Run a simulation.
              </div>
            )}
          </div>
        </div>
        
        {/* LOGS / HEATMAP */}
        <div className="md:col-span-1 bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-lg flex flex-col">
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <span>🔥</span> Live Threat Feed
          </h2>
          <div className="flex-1 overflow-y-auto space-y-3 pr-2 max-h-[500px] custom-scrollbar">
            {logs.map((log, i) => (
              <div 
                key={i} 
                className={`p-3 rounded-lg border text-xs animate-in fade-in slide-in-from-bottom-2 duration-300 ${
                  log.score > 70 ? 'bg-red-900/10 border-red-500/30' : 
                  log.score > 30 ? 'bg-yellow-900/10 border-yellow-500/30' : 
                  'bg-green-900/10 border-green-500/30'
                }`}
              >
                <div className="flex justify-between items-start mb-1">
                  <span className={`font-bold uppercase ${
                    log.score > 70 ? 'text-red-400' : 
                    log.score > 30 ? 'text-yellow-400' : 'text-green-400'
                  }`}>
                    {log.executor.replace('_', ' ')}
                  </span>
                  <span className="opacity-70">⚠ {log.score}</span>
                </div>
                <div className="text-slate-300 truncate font-mono mb-1" title={log.input}>
                  {log.input}
                </div>
                <div className="flex justify-between text-slate-500 text-[10px]">
                  <span>Conf: {(log.confidence * 100).toFixed(0)}%</span>
                  <span>{new Date(log.time).toLocaleTimeString()}</span>
                </div>
              </div>
            ))}
            {logs.length === 0 && (
              <div className="text-center text-slate-500 text-sm py-8">
                Waiting for incoming traffic...
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
