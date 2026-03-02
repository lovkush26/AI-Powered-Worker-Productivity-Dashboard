import React from "react";
import { useEffect, useState } from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";

const card = {
  padding:"20px",
  borderRadius:"10px",
  background:"#f4f6f8",
  boxShadow:"0 2px 8px rgba(0,0,0,0.1)",
  minWidth:"180px"
};

export default function Dashboard() {
  const [data, setData] = useState(null);

  const load = () =>
    fetch("http://localhost:8000/metrics")
      .then(r => r.json())
      .then(setData);

  useEffect(() => {
    load();
    const id = setInterval(load, 5000);
    return () => clearInterval(id);
  }, []);

  if (!data) return <div>Loading...</div>;

  return (
    <div style={{padding:20,fontFamily:"Arial"}}>
      <h1>Factory Productivity Dashboard</h1>
    
      <div style={{display:"flex",gap:"20px",marginBottom:"30px"}}>
  <div style={card}>
    <h3>Total Units</h3>
    <h2>{data.factory.total_units}</h2>
  </div>

  <div style={card}>
    <h3>Avg Utilization</h3>
    <h2>{data.factory.avg_utilization.toFixed(1)}%</h2>
  </div>

  <div style={card}>
    <h3>Production Rate</h3>
    <h2>{data.factory.production_rate.toFixed(1)}/hr</h2>
  </div>
</div>

      <h2>Worker Utilization</h2>
      <BarChart
  width={700}
  height={320}
  data={data.workers}
  margin={{ top: 20, right: 30, left: 10, bottom: 5 }}
>
  <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
  <XAxis dataKey="worker_id" />
  <YAxis />
  <Tooltip />
  <Bar
    dataKey="utilization_percent"
    fill="#3b82f6"
    radius={[6, 6, 0, 0]}
  />
</BarChart>
    </div>
  );
}