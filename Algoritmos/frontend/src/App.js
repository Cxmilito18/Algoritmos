import React, { useState, useEffect } from "react";  // ← quitado useRef
import { Bar, Line } from "react-chartjs-2";
import "chart.js/auto";  // ← quitado ChartJS que no se usaba
import "./App.css";

import MergeTree from "./MergeTree";
import RadixBuckets from "./RadixBuckets";
import BucketBoxes from "./BucketBoxes";

// ===== DATOS DE ALGORITMOS =====
const INFO_ALGORITMOS = {
  merge: {
    nombre: "Merge Sort",
    emoji: "🌳",
    descripcion:
      "Merge Sort es un algoritmo de ordenamiento basado en el paradigma Divide y Vencerás. Divide el arreglo en dos mitades, las ordena de forma recursiva y luego las fusiona (merge) en un solo arreglo ordenado.",
    pasos: [
      "Divide el arreglo en dos mitades iguales.",
      "Llama recursivamente a Merge Sort en cada mitad.",
      "Fusiona las dos mitades ordenadas comparando elemento por elemento.",
      "Repite hasta que todo el arreglo esté ordenado.",
    ],
    mejorCaso:    "O(n log n)",
    casoPromedio: "O(n log n)",
    peorCaso:     "O(n log n)",
    espacio:      "O(n)",
    estable:      true,
    color: "#3b82f6",
  },
  radix: {
    nombre: "Radix Sort",
    emoji: "🔢",
    descripcion:
      "Radix Sort ordena los números dígito por dígito, desde el menos significativo (unidades) hasta el más significativo. En cada pasada distribuye los elementos en 10 cubetas (0-9) según el dígito actual y las concatena de nuevo.",
    pasos: [
      "Encuentra el número máximo para saber cuántos dígitos hay.",
      "Toma el dígito de las unidades de cada número.",
      "Distribuye en cubetas 0-9 según ese dígito.",
      "Concatena las cubetas en orden.",
      "Repite para decenas, centenas, etc.",
    ],
    mejorCaso:    "O(nk)",
    casoPromedio: "O(nk)",
    peorCaso:     "O(nk)",
    espacio:      "O(n + k)",
    estable:      true,
    color: "#a855f7",
  },
  bucket: {
    nombre: "Bucket Sort",
    emoji: "🪣",
    descripcion:
      "Bucket Sort distribuye los elementos en cubetas según su rango, ordena cada cubeta individualmente (con otro algoritmo o recursivamente) y luego las concatena. Es muy eficiente cuando los datos están distribuidos uniformemente.",
    pasos: [
      "Calcula el rango de los valores (mínimo y máximo).",
      "Crea N cubetas que cubren intervalos iguales del rango.",
      "Distribuye cada elemento en su cubeta correspondiente.",
      "Ordena individualmente cada cubeta.",
      "Concatena todas las cubetas en orden.",
    ],
    mejorCaso:    "O(n + k)",
    casoPromedio: "O(n + k)",
    peorCaso:     "O(n²)",
    espacio:      "O(n + k)",
    estable:      true,
    color: "#22c55e",
  },
};

// ===== BIG-O DATA =====
const BIG_O_NS = [1, 5, 10, 20, 50, 100, 200, 500];
function nlogn(n)  { return n * Math.log2(n); }
function nk(n)     { return n * 3; }
function nplusk(n) { return n + 10; }
function ncuad(n)  { return n * n; }

// ===== MERGE TREE =====
function buildMergeTree(arr) {
  if (!arr || arr.length === 0) return null;
  if (arr.length === 1) return { valor: arr, izquierda: null, derecha: null };
  const mid = Math.floor(arr.length / 2);
  return {
    valor: arr,
    izquierda: buildMergeTree(arr.slice(0, mid)),
    derecha:   buildMergeTree(arr.slice(mid)),
  };
}

// ===== MODAL EXPLICACIÓN =====
function ModalExplicacion({ info, onClose }) {
  useEffect(() => {
    const handler = (e) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  return (
    <div
      onClick={onClose}
      style={{
        position: "fixed", inset: 0, zIndex: 1000,
        background: "rgba(0,0,0,0.65)",
        display: "flex", alignItems: "center", justifyContent: "center",
        padding: "1rem",
        backdropFilter: "blur(4px)",
      }}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        style={{
          background: "#0f172a",
          border: `1.5px solid ${info.color}55`,
          borderRadius: "16px",
          padding: "2rem",
          maxWidth: "540px",
          width: "100%",
          boxShadow: `0 0 40px ${info.color}33`,
          animation: "modalIn 0.25s cubic-bezier(0.34,1.56,0.64,1)",
          maxHeight: "90vh",
          overflowY: "auto",
        }}
      >
        <style>{`
          @keyframes modalIn {
            from { opacity: 0; transform: scale(0.88) translateY(20px); }
            to   { opacity: 1; transform: scale(1)    translateY(0); }
          }
        `}</style>

        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1rem" }}>
          <h2 style={{ margin: 0, fontSize: "1.3rem", color: info.color }}>
            {info.emoji} {info.nombre}
          </h2>
          <button
            onClick={onClose}
            style={{
              background: "transparent", border: "none", color: "#94a3b8",
              fontSize: "1.4rem", cursor: "pointer", lineHeight: 1,
            }}
          >×</button>
        </div>

        <p style={{ color: "#cbd5e1", fontSize: "0.9rem", lineHeight: 1.7, marginBottom: "1.25rem" }}>
          {info.descripcion}
        </p>

        <div style={{ marginBottom: "1.25rem" }}>
          <p style={{ color: "#94a3b8", fontSize: "0.75rem", fontWeight: 700, letterSpacing: "0.08em", marginBottom: "0.5rem" }}>
            ¿CÓMO FUNCIONA?
          </p>
          <ol style={{ margin: 0, paddingLeft: "1.25rem" }}>
            {info.pasos.map((paso, i) => (
              <li key={i} style={{ color: "#e2e8f0", fontSize: "0.875rem", lineHeight: 1.7, marginBottom: "0.25rem" }}>
                {paso}
              </li>
            ))}
          </ol>
        </div>

        <div style={{ marginBottom: "1rem" }}>
          <p style={{ color: "#94a3b8", fontSize: "0.75rem", fontWeight: 700, letterSpacing: "0.08em", marginBottom: "0.5rem" }}>
            COMPLEJIDAD
          </p>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: "8px" }}>
            {[
              { label: "Mejor caso",    val: info.mejorCaso },
              { label: "Caso promedio", val: info.casoPromedio },
              { label: "Peor caso",     val: info.peorCaso },
            ].map(({ label, val }) => (
              <div key={label} style={{
                background: "#1e293b", borderRadius: "8px", padding: "0.6rem 0.75rem",
                border: `1px solid ${info.color}33`,
              }}>
                <div style={{ color: "#64748b", fontSize: "0.7rem", marginBottom: "2px" }}>{label}</div>
                <div style={{ color: info.color, fontSize: "0.95rem", fontWeight: 700, fontFamily: "monospace" }}>{val}</div>
              </div>
            ))}
          </div>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "8px", marginTop: "8px" }}>
            {[
              { label: "Espacio", val: info.espacio },
              { label: "Estable", val: info.estable ? "✅ Sí" : "❌ No" },
            ].map(({ label, val }) => (
              <div key={label} style={{
                background: "#1e293b", borderRadius: "8px", padding: "0.6rem 0.75rem",
                border: `1px solid ${info.color}33`,
              }}>
                <div style={{ color: "#64748b", fontSize: "0.7rem", marginBottom: "2px" }}>{label}</div>
                <div style={{ color: "#e2e8f0", fontSize: "0.9rem", fontWeight: 600 }}>{val}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

// ===== MODAL BIG-O =====
function ModalBigO({ onClose }) {
  useEffect(() => {
    const handler = (e) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  const labels = BIG_O_NS.map(String);
  const data = {
    labels,
    datasets: [
      {
        label: "Merge Sort — O(n log n)",
        data: BIG_O_NS.map(nlogn),
        borderColor: "#3b82f6",
        backgroundColor: "#3b82f622",
        tension: 0.4,
        pointRadius: 4,
        borderWidth: 2.5,
      },
      {
        label: "Radix Sort — O(nk)",
        data: BIG_O_NS.map(nk),
        borderColor: "#a855f7",
        backgroundColor: "#a855f722",
        tension: 0.4,
        pointRadius: 4,
        borderWidth: 2.5,
      },
      {
        label: "Bucket Sort mejor — O(n+k)",
        data: BIG_O_NS.map(nplusk),
        borderColor: "#22c55e",
        backgroundColor: "#22c55e22",
        tension: 0.4,
        pointRadius: 4,
        borderWidth: 2.5,
      },
      {
        label: "Bucket Sort peor — O(n²)",
        data: BIG_O_NS.map(ncuad),
        borderColor: "#ef4444",
        backgroundColor: "#ef444422",
        tension: 0.4,
        pointRadius: 4,
        borderWidth: 2,
        borderDash: [6, 3],
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        labels: { color: "#94a3b8", font: { size: 12 }, boxWidth: 20 },
      },
    },
    scales: {
      x: {
        title: { display: true, text: "n (tamaño del arreglo)", color: "#64748b" },
        ticks: { color: "#94a3b8" },
        grid:  { color: "#1e293b" },
      },
      y: {
        title: { display: true, text: "Operaciones (relativo)", color: "#64748b" },
        ticks: { color: "#94a3b8" },
        grid:  { color: "#1e293b" },
      },
    },
  };

  return (
    <div
      onClick={onClose}
      style={{
        position: "fixed", inset: 0, zIndex: 1000,
        background: "rgba(0,0,0,0.65)",
        display: "flex", alignItems: "center", justifyContent: "center",
        padding: "1rem",
        backdropFilter: "blur(4px)",
      }}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        style={{
          background: "#0f172a",
          border: "1.5px solid #334155",
          borderRadius: "16px",
          padding: "2rem",
          maxWidth: "680px",
          width: "100%",
          boxShadow: "0 0 40px rgba(0,0,0,0.5)",
          animation: "modalIn 0.25s cubic-bezier(0.34,1.56,0.64,1)",
        }}
      >
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1.25rem" }}>
          <h2 style={{ margin: 0, fontSize: "1.2rem", color: "#f1f5f9" }}>
            📈 Complejidad Big-O comparativa
          </h2>
          <button
            onClick={onClose}
            style={{
              background: "transparent", border: "none", color: "#94a3b8",
              fontSize: "1.4rem", cursor: "pointer", lineHeight: 1,
            }}
          >×</button>
        </div>

        <Line data={data} options={options} />

        <p style={{ color: "#475569", fontSize: "0.78rem", marginTop: "1rem", textAlign: "center" }}>
          Radix usa k = 3 dígitos promedio · Bucket asume k = 10 cubetas
        </p>
      </div>
    </div>
  );
}

// ===== APP =====
function App() {
  const [datos, setDatos]               = useState("");
  const [pasosBarra, setPasosBarra]     = useState([]);
  const [pasosCubetas, setPasosCubetas] = useState([]);
  const [mergeArbol, setMergeArbol]     = useState(null);
  const [algoritmo, setAlgoritmo]       = useState("merge");
  const [tamanio, setTamanio]           = useState(10);
  const [pasoActual, setPasoActual]     = useState(0);
  const [jugando, setJugando]           = useState(false);
  const [velocidad, setVelocidad]       = useState(1000);
  const [modalInfo, setModalInfo]       = useState(false);
  const [modalBigO, setModalBigO]       = useState(false);
  const [cargando, setCargando]         = useState(false);

  const generarAleatorios = () => {
    const aleatorios = Array.from({ length: tamanio }, () =>
      Math.floor(Math.random() * 100)
    );
    setDatos(aleatorios.join(" "));
  };

  const ordenar = async () => {
    const arr = datos.trim().split(/\s+/).map(Number).filter((n) => !isNaN(n));
    if (arr.length === 0) { alert("Ingresa números válidos"); return; }

    setCargando(true);
    try {
      const res = await fetch("https://algoritmos-backend.onrender.com/ordenar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ valores: arr, algoritmo }),
      });

      if (!res.ok) throw new Error(`Backend respondió ${res.status}`);

      const data = await res.json();

      if (algoritmo === "merge") {
        setPasosBarra(data.pasos);
        setPasosCubetas([]);
        setMergeArbol(buildMergeTree([...arr]));
      } else {
        setPasosBarra([arr, ...data.pasos.map((p) => p.flat())]);
        setPasosCubetas(data.pasos);
        setMergeArbol(null);
      }

      setPasoActual(0);
      setJugando(false);

    } catch (err) {
      alert("❌ No se pudo conectar al backend.\n¿Está corriendo FastAPI en el puerto 8000?\n\nComando: uvicorn app:app --reload");
    } finally {
      setCargando(false);
    }
  };

  useEffect(() => {
    let intervalo;
    if (jugando && pasosBarra.length > 0 && pasoActual < pasosBarra.length - 1) {
      intervalo = setInterval(() => setPasoActual((p) => p + 1), velocidad);
    }
    return () => clearInterval(intervalo);
  }, [jugando, pasoActual, pasosBarra, velocidad]);

  const pasoActualData = Array.isArray(pasosBarra[pasoActual]) ? pasosBarra[pasoActual] : [];
  const indiceCubeta   = pasoActual - 1;
  const infoActual     = INFO_ALGORITMOS[algoritmo];

  const getBarraColors = (data) => {
    if (pasoActual === pasosBarra.length - 1) return data.map(() => "#22c55e");
    return data.map((_, i) => ["#3b82f6", "#ef4444", "#22c55e"][i % 3]);
  };

  return (
    <div className="app-container">
      {modalInfo && <ModalExplicacion info={infoActual} onClose={() => setModalInfo(false)} />}
      {modalBigO && <ModalBigO onClose={() => setModalBigO(false)} />}

      <h1 className="titulo">Visualizador de Algoritmos</h1>
      <p className="subtitulo">Simulador interactivo paso a paso</p>

      <div className="panel-superior">
        <select value={algoritmo} onChange={(e) => setAlgoritmo(e.target.value)}>
          <option value="merge">Merge Sort</option>
          <option value="radix">Radix Sort</option>
          <option value="bucket">Bucket Sort</option>
        </select>

        <input
          type="number"
          value={tamanio}
          onChange={(e) => setTamanio(Number(e.target.value))}
        />

        <button onClick={generarAleatorios}>🎲 Aleatorios</button>

        <input
          type="text"
          value={datos}
          onChange={(e) => setDatos(e.target.value)}
          placeholder="Ej: 64 25 12 22 11"
        />

        <button onClick={ordenar} disabled={cargando}>
          {cargando ? "⏳ Calculando..." : "🚀 Ordenar"}
        </button>

        <button onClick={() => setModalInfo(true)} title="Ver explicación del algoritmo">
          ℹ️ ¿Cómo funciona?
        </button>
        <button onClick={() => setModalBigO(true)} title="Ver gráfica Big-O">
          📈 Big-O
        </button>
      </div>

      {pasosBarra.length > 0 && (
        <div className="visualizador-card">
          <h3>Paso {pasoActual + 1} de {pasosBarra.length}</h3>

          {pasoActualData.length > 0 && (
            <div className="barras-principal">
              <Bar
                key={`bar-${pasoActual}`}
                data={{
                  labels: pasoActualData.map((_, i) => i),
                  datasets: [{
                    label: "Estado del arreglo",
                    data: pasoActualData,
                    backgroundColor: getBarraColors(pasoActualData),
                    borderRadius: 5,
                    borderWidth: 2,
                    borderColor: "rgba(255,255,255,0.1)",
                  }],
                }}
                options={{
                  plugins: { legend: { display: false } },
                  scales: {
                    x: { ticks: { color: "#f1f5f9" } },
                    y: { ticks: { color: "#f1f5f9" } },
                  },
                  animation: { duration: 300, easing: "easeInOutQuart" },
                }}
              />
            </div>
          )}

          {algoritmo === "merge" && (
            <MergeTree arbol={mergeArbol} pasos={pasosBarra} pasoActual={pasoActual} />
          )}
          {algoritmo === "radix" && pasosCubetas.length > 0 && indiceCubeta >= 0 && (
            <RadixBuckets
              pasos={pasosCubetas}
              pasoActual={Math.min(indiceCubeta, pasosCubetas.length - 1)}
            />
          )}
          {algoritmo === "bucket" && pasosCubetas.length > 0 && indiceCubeta >= 0 && (
            <BucketBoxes
              pasos={pasosCubetas}
              pasoActual={Math.min(indiceCubeta, pasosCubetas.length - 1)}
            />
          )}

          <div className="controles">
            <button onClick={() => { setPasoActual(0); setJugando(false); }}>⏮️ Reiniciar</button>
            <button onClick={() => setJugando(!jugando)}>
              {jugando ? "⏸️ Pausar" : "▶️ Reproducir"}
            </button>
            <button onClick={() => setPasoActual((p) => Math.min(p + 1, pasosBarra.length - 1))}>
              ⏭️ Siguiente
            </button>
            <label>Velocidad:</label>
            <input
              type="range" min="200" max="2000" step="200"
              value={velocidad}
              onChange={(e) => setVelocidad(Number(e.target.value))}
            />
          </div>
        </div>
      )}
    </div>
  );
}

export default App;