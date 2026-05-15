import React from "react";

export default function RadixBuckets({ pasos, pasoActual }) {
  const buckets = pasos[pasoActual]; // backend debe devolver array de 10 buckets
  return (
    <div className="visualizador-card">
      <h3>Cubetas de Radix Sort</h3>
      <div className="cubetas">
        {buckets.map((bucket, i) => (
          <div key={i} className="cubeta">
            <h4>{i}</h4>
            <div className="valores">{bucket.join(" ")}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
