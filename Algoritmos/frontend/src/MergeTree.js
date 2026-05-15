import React from "react";
import { Bar } from "react-chartjs-2";

function renderNode(nodo) {
  if (!nodo || !nodo.valor) return null;

  return (
    <li>
      <div className="nodo">{JSON.stringify(nodo.valor)}</div>
      {(nodo.izquierda || nodo.derecha) && (
        <ul>
          {nodo.izquierda && renderNode(nodo.izquierda)}
          {nodo.derecha && renderNode(nodo.derecha)}
        </ul>
      )}
    </li>
  );
}

export default function MergeTree({ pasos, pasoActual }) {
  const arbol = pasos[pasoActual];

  return (
    <div className="merge-container">
      <h3>Árbol de Merge Sort</h3>
      <ul className="arbol">{renderNode(arbol)}</ul>

      {/* Barras sincronizadas */}
      {Array.isArray(arbol?.valor) && (
        <div className="barras-extra">
          <Bar
            data={{
              labels: arbol.valor.map((_, i) => i),
              datasets: [
                {
                  label: "Estado del arreglo",
                  data: arbol.valor,
                  backgroundColor: arbol.valor.map((val, idx) => {
                    if (pasoActual === pasos.length - 1) return "#22c55e"; // verde final
                    if (idx % 3 === 0) return "#3b82f6"; // azul
                    if (idx % 3 === 1) return "#ef4444"; // rojo
                    return "#22c55e"; // verde
                  }),
                  borderRadius: 5,
                },
              ],
            }}
            options={{
              plugins: { legend: { display: false } },
              scales: {
                x: { ticks: { color: "#f1f5f9" } },
                y: { ticks: { color: "#f1f5f9" } },
              },
              animation: { duration: 500, easing: "easeInOutQuart" },
            }}
          />
        </div>
      )}
    </div>
  );
}