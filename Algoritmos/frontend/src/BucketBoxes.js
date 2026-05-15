import React from "react";

export default function BucketBoxes({ pasos, pasoActual }) {
  const buckets = pasos[pasoActual]; // backend debe devolver array de buckets
  return (
    <div className="visualizador-card">
      <h3>Buckets de Bucket Sort</h3>
      <div className="cubetas">
        {buckets.map((bucket, i) => (
          <div key={i} className="cubeta">
            <h4>Bucket {i}</h4>
            <div className="valores">{bucket.join(" ")}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
