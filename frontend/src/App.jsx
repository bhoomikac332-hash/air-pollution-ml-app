import { useState } from "react";

function App() {
  const [city, setCity] = useState("");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const getData = async () => {
    setLoading(true);
    const res = await fetch(`http://127.0.0.1:5000/predict/${city}`);
    const result = await res.json();
    setData(result);
    setLoading(false);
  };

  const getColor = () => {
    if (!data) return "#333";
    if (data.risk.includes("Low")) return "green";
    if (data.risk.includes("Medium")) return "orange";
    return "red";
  };

  const getBgColor = () => {
    if (!data) return "#f0f2f5";
    if (data.risk.includes("Low")) return "#d4edda";
    if (data.risk.includes("Medium")) return "#fff3cd";
    return "#f8d7da";
  };

  return (
    <div
      style={{
        backgroundColor: getBgColor(),
        minHeight: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        fontFamily: "Arial",
      }}
    >
      <div
        style={{
          background: "white",
          padding: "30px",
          borderRadius: "15px",
          boxShadow: "0 0 15px rgba(0,0,0,0.2)",
          textAlign: "center",
          width: "350px",
        }}
      >
        <h1>🌍 Air Pollution</h1>

        <input
          placeholder="Enter City"
          value={city}
          onChange={(e) => setCity(e.target.value)}
          style={{
            padding: "10px",
            width: "100%",
            marginBottom: "10px",
            borderRadius: "5px",
            border: "1px solid gray",
          }}
        />

        <button
          onClick={getData}
          style={{
            padding: "10px",
            width: "100%",
            background: "#007bff",
            color: "white",
            border: "none",
            borderRadius: "5px",
            cursor: "pointer",
          }}
        >
          Check
        </button>

        {loading && <p>Loading...</p>}

        {data && (
          <div style={{ marginTop: "20px" }}>
            <h2>{data.city}</h2>
            <h3>AQI: {data.aqi}</h3>

            <h2 style={{ color: getColor() }}>{data.risk}</h2>

            <p>
              {data.risk.includes("High") && "⚠️ Avoid going outside"}
              {data.risk.includes("Medium") && "😷 Wear mask"}
              {data.risk.includes("Low") && "✅ Safe air"}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;