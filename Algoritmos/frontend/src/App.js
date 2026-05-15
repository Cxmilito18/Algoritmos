import React, { useState, useEffect } from "react";
import { Bar } from "react-chartjs-2";
import { Chart as ChartJS } from "chart.js/auto";
import "./App.css";

import MergeTree from "./MergeTree";
import RadixBuckets from "./RadixBuckets";
import BucketBoxes from "./BucketBoxes";

// ===== ALGORITMOS =====
function mergeSort(arr) {
  const pasos = [];
  pasos.push([...arr]);

  function merge(left, right) {
    let result = [];
    let i = 0, j = 0;
    while (i < left.length && j < right.length) {
      if (left[i] <= right[j]) result.push(left[i++]);
      else result.push(right[j++]);
      pasos.push([...result, ...left.slice(i), ...right.slice(j)]);
    }
    return [...result, ...left.slice(i), ...right.slice(j)];
  }

  function sort(arr) {
    if (arr.length <= 1) return arr;
    const mid = Math.floor(arr.length / 2);
    const left = sort(arr.slice(0, mid));
    const right = sort(arr.slice(mid));
    return merge(left, right);
  }

  sort([...arr]);
  return pasos;
}

// 🌳 Construye el árbol de división del merge sort
function buildMergeTree(arr) {
  if (!arr || arr.length === 0) return null;
  if (arr.length === 1) return { valor: arr, izquierda: null, derecha: null };
  const mid = Math.floor(arr.length / 2);
  return {
    valor: arr,
    izquierda: buildMergeTree(arr.slice(0, mid)),
    derecha: buildMergeTree(arr.slice(mid)),
  };
}

function bucketSort(arr) {
  const pasos = [];
  pasos.push([...arr]);
  const max = Math.max(...arr);
  const min = Math.min(...arr);
  const bucketCount = Math.min(5, arr.length);
  const buckets = Array.from({ length: bucketCount }, () => []);

  for (let num of arr) {
    const index = Math.floor(((num - min) / (max - min + 1)) * bucketCount);
    buckets[index].push(num);
    pasos.push([...arr]);
  }

  let result = [];
  for (let bucket of buckets) {
    bucket.sort((a, b) => a - b);
    result.push(...bucket);
    pasos.push([...result]);
  }
  return pasos;
}

function radixSort(arr) {
  const pasos = [];
  pasos.push([...arr]);
  if (arr.length === 0) return pasos;
  const max = Math.max(...arr);
  let exp = 1;

  while (Math.floor(max / exp) > 0) {
    const buckets = Array.from({ length: 10 }, () => []);
    for (let num of arr) {
      const digit = Math.floor((num / exp) % 10);
      buckets[digit].push(num);
    }
    arr = buckets.flat();
    pasos.push([...arr]);
    exp *= 10;
  }
  return pasos;
}

function App() {
  const [datos, setDatos] = useState("");
  const [pasos, setPasos] = useState([]);
  const [mergeArbol, setMergeArbol] = useState(null); // 🌳 árbol de merge
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

  const ordenar = () => {
    const arr = datos
      .trim()
      .split(/\s+/)
      .map(Number)
      .filter((n) => !isNaN(n));

    if (arr.length === 0) {
      alert("Ingresa números válidos");
      return;
    }

    let resultado = [];

    if (algoritmo === "merge") {
      resultado = mergeSort([...arr]);
      setMergeArbol(buildMergeTree([...arr])); // 🌳 construir árbol
    } else if (algoritmo === "bucket") {
      resultado = bucketSort([...arr]);
      setMergeArbol(null);
    } else if (algoritmo === "radix") {
      resultado = radixSort([...arr]);
      setMergeArbol(null);
    }

    setPasos(resultado);
    setPasoActual(0);
    setJugando(false);
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

  const pasoActualData = Array.isArray(pasos[pasoActual]) ? pasos[pasoActual] : [];

  // 🎨 Solo rojo, azul y verde
  const getBarraColors = (data) => {
    const isOrdenado = pasoActual === pasos.length - 1;

    // Verde completo al terminar
    if (isOrdenado) return data.map(() => "#22c55e");

    if (algoritmo === "merge") {
      return data.map((_, idx) => {
        if (idx % 3 === 0) return "#3b82f6"; // Azul
        if (idx % 3 === 1) return "#ef4444"; // Rojo
        return "#22c55e";                    // Verde
      });
    }

    if (algoritmo === "radix") {
      const colors = ["#3b82f6", "#ef4444", "#22c55e"];
      return data.map((_, idx) => colors[idx % 3]);
    }

    if (algoritmo === "bucket") {
      return data.map((val) => {
        const ratio = val / 100;
        if (ratio < 0.33) return "#3b82f6"; // Azul
        if (ratio < 0.66) return "#ef4444"; // Rojo
        return "#22c55e";                   // Verde
      });
    }

    return "#3b82f6";
  };

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

          {pasoActualData.length > 0 && (
            <div className="barras-principal">
              <Bar
                key={`bar-${pasoActual}`}
                data={{
                  labels: pasoActualData.map((_, i) => i),
                  datasets: [
                    {
                      label: "Estado del arreglo",
                      data: pasoActualData,
                      backgroundColor: getBarraColors(pasoActualData),
                      borderRadius: 5,
                      borderWidth: 2,
                      borderColor: "rgba(255, 255, 255, 0.1)",
                    },
                  ],
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
            <MergeTree arbol={mergeArbol} pasos={pasos} pasoActual={pasoActual} />
          )}
          {algoritmo === "radix" && (
            <RadixBuckets pasos={pasos} pasoActual={pasoActual} />
          )}
          {algoritmo === "bucket" && (
            <BucketBoxes pasos={pasos} pasoActual={pasoActual} />
          )}

          <div className="controles">
            <button onClick={() => setPasoActual(0)}>⏮️ Reiniciar</button>
            <button onClick={() => setJugando(!jugando)}>
              {jugando ? "⏸️ Pausar" : "▶️ Reproducir"}
            </button>
            <button
              onClick={() =>
                setPasoActual((prev) => (prev < pasos.length - 1 ? prev + 1 : prev))
              }
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