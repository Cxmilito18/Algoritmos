import React, { useState, useEffect } from "react";
import axios from "axios";
import { Bar } from "react-chartjs-2";
import { Chart as ChartJS } from "chart.js/auto";
import "./App.css";

import MergeTree from "./MergeTree";
import RadixBuckets from "./RadixBuckets";
import BucketBoxes from "./BucketBoxes";

function App() {
  const [datos, setDatos] = useState("");
  const [pasos, setPasos] = useState([]);
  const [algoritmo, setAlgoritmo] = useState("merge");
  const [tamanio, setTamanio] = useState(10);
  const [pasoActual, setPasoActual] = useState(0);
  const [jugando, setJugando] = useState(false);
  const [velocidad, setVelocidad] = useState(1000);

  const generarAleatorios = () => {
    const aleatorios = Array.from({ length: tamanio }, () =>
      Math.floor(Math.random() * 100)
    );
    setDatos(aleatorios.join(" "));
  };

  const ordenar = async () => {
    try {
      const arr = datos.split(" ").map(Number);
      const res = await axios.post("http://127.0.0.1:8000/ordenar", {
        valores: arr,
        algoritmo: algoritmo,
      });
      setPasos(res.data.pasos);
      setPasoActual(0);
      setJugando(false);
      console.log("Respuesta backend:", res.data);
    } catch (err) {
      console.error("Error al conectar con el backend:", err);
    }
  };

  useEffect(() => {
    let intervalo;
    if (jugando && pasos.length > 0 && pasoActual < pasos.length - 1) {
      intervalo = setInterval(() => {
        setPasoActual((prev) => prev + 1);
      }, velocidad);
    }
    return () => clearInterval(intervalo);
  }, [jugando, pasoActual, pasos, velocidad]);

  return (
    <div className="app-container">
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
          placeholder="Tamaño"
        />

        <button onClick={generarAleatorios}>🎲 Aleatorios</button>
        <input
          type="text"
          value={datos}
          onChange={(e) => setDatos(e.target.value)}
          placeholder="Ej: 64 25 12 22 11"
        />
        <button onClick={ordenar}>🚀 Ordenar</button>
      </div>

      {pasos.length > 0 && (
        <div className="visualizador-card">
          <h3>Paso {pasoActual + 1} de {pasos.length}</h3>

          {/* Barras solo si el paso actual es array */}
          {Array.isArray(pasos[pasoActual]) && (
            <Bar
              data={{
                labels: pasos[pasoActual].map((_, i) => i),
                datasets: [
                  {
                    label: "Estado del arreglo",
                    data: pasos[pasoActual],
                    backgroundColor: pasos[pasoActual].map((val, idx) => {
                      if (pasoActual === pasos.length - 1) return "#84cc16"; // verde final
                      if (idx <= pasoActual) return "#3b82f6"; // azul ordenándose
                      return "#64748b"; // gris pendiente
                    }),
                    borderRadius: 5,
                  },
                ],
              }}
              options={{
                plugins: { legend: { display: false } },
                scales: {
                  x: { ticks: { color: "#ccc" } },
                  y: { ticks: { color: "#ccc" } },
                },
                animation: { duration: 500, easing: "easeInOutQuart" },
              }}
            />
          )}

          {/* Visual extra */}
          {algoritmo === "merge" && <MergeTree pasos={pasos} pasoActual={pasoActual} />}
          {algoritmo === "radix" && <RadixBuckets pasos={pasos} pasoActual={pasoActual} />}
          {algoritmo === "bucket" && <BucketBoxes pasos={pasos} pasoActual={pasoActual} />}

          {/* Controles */}
          <div className="controles">
            <button onClick={() => setPasoActual(0)} className="btn-reiniciar">⏮️ Reiniciar</button>
            <button onClick={() => setJugando(!jugando)} className="btn-play">
              {jugando ? "⏸️ Pausar" : "▶️ Reproducir"}
            </button>
            <button
              onClick={() =>
                setPasoActual((prev) =>
                  prev < pasos.length - 1 ? prev + 1 : prev
                )
              }
              className="btn-siguiente"
            >
              ⏭️ Siguiente
            </button>
            <label>Velocidad:</label>
            <input
              type="range"
              min="200"
              max="2000"
              step="200"
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
