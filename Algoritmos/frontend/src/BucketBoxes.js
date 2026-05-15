import React, { useMemo } from "react";

// ── Constantes ────────────────────────────────────────────────────
const BUCKET_COLORS = ["#3b82f6", "#ef4444", "#22c55e", "#f59e0b", "#a855f7"];
const ANIM_STAGGER  = 60;

// ── Utilidades ────────────────────────────────────────────────────

/** Garantiza que cualquier cosa se convierta en array de números */
function normalizeBucket(raw) {
  if (!raw) return [];
  if (Array.isArray(raw)) return raw.map(Number);
  if (typeof raw === "string") {
    const trimmed = raw.trim();
    if (!trimmed || trimmed === "[]") return [];
    return trimmed
      .replace(/[[\]]/g, "")
      .split(",")
      .map((s) => Number(s.trim()))
      .filter((n) => !isNaN(n));
  }
  if (typeof raw === "object") return Object.values(raw).map(Number);
  return [];
}

/** Normaliza el paso: puede ser array de buckets u objeto {buckets, ...} */
function normalizeStep(step) {
  if (!step) return [];
  if (Array.isArray(step)) return step.map(normalizeBucket);
  if (typeof step === "object" && step.buckets) {
    return step.buckets.map(normalizeBucket);
  }
  return [];
}

function getRange(pasos) {
  let min = Infinity, max = -Infinity;
  pasos.forEach((step) =>
    normalizeStep(step).forEach((bucket) =>
      bucket.forEach((v) => {
        if (v < min) min = v;
        if (v > max) max = v;
      })
    )
  );
  if (!isFinite(min)) return { min: 0, max: 1 };
  return { min, max: max === min ? max + 1 : max };
}

// ── Componente ────────────────────────────────────────────────────
export default function BucketBoxes({ pasos, pasoActual }) {
  const buckets = useMemo(
    () => normalizeStep(pasos?.[pasoActual]),
    [pasos, pasoActual]
  );

  const { min, max } = useMemo(() => {
    if (!pasos?.length) return { min: 0, max: 1 };
    return getRange(pasos);
  }, [pasos]);

  const totalItems    = useMemo(() => buckets.reduce((s, b) => s + b.length, 0), [buckets]);
  const maxBucketSize = useMemo(() => Math.max(...buckets.map((b) => b.length), 1), [buckets]);
  const filledCount   = buckets.filter((b) => b.length > 0).length;

  const totalPasos = Math.max((pasos?.length ?? 1) - 1, 1);
  const progress   = pasoActual / totalPasos;

  if (!buckets.length) return null;

  return (
    <div className="merge-container">
      <style>{`
        @keyframes bucketDrop {
          from { opacity: 0; transform: translateY(-18px) scale(0.85); }
          to   { opacity: 1; transform: translateY(0) scale(1); }
        }
        @keyframes chipIn {
          from { opacity: 0; transform: scale(0.5); }
          to   { opacity: 1; transform: scale(1); }
        }
        .bucket-wrap {
          display: flex; flex-direction: column; align-items: center; gap: 6px;
          animation: bucketDrop 0.4s cubic-bezier(0.34,1.56,0.64,1) both;
        }
        .bucket-body {
          display: flex; flex-direction: column-reverse; gap: 4px;
          padding: 8px 8px 0; border: 2px solid; border-top: none;
          border-radius: 0 0 10px 10px; min-width: 64px; min-height: 90px;
          justify-content: flex-start; align-items: center; position: relative;
          transition: border-color 0.3s;
        }
        .bucket-bar-fill {
          position: absolute; bottom: 0; left: 0; right: 0;
          border-radius: 0 0 8px 8px; transition: height 0.5s ease; pointer-events: none;
        }
        .value-chip {
          font-size: 11px; font-weight: 700; font-family: 'Segoe UI', monospace;
          padding: 2px 7px; border-radius: 99px; color: #f1f5f9;
          position: relative; z-index: 1; white-space: nowrap;
          animation: chipIn 0.3s cubic-bezier(0.34,1.56,0.64,1) both;
        }
        .bucket-label {
          font-size: 12px; font-weight: 700; font-family: 'Segoe UI', monospace; color: #94a3b8;
        }
        .bucket-count-badge {
          font-size: 10px; padding: 1px 6px; border-radius: 99px;
          font-weight: 700; background: rgba(255,255,255,0.07);
        }
      `}</style>

      <h3>🪣 Cubetas — Bucket Sort</h3>
      <p style={{ color: "#94a3b8", fontSize: "0.85rem", marginTop: 0 }}>
        Cada valor cae a su cubeta según su rango numérico
      </p>

      <div style={{
        display: "flex", flexWrap: "wrap", gap: "12px",
        justifyContent: "center", padding: "0.5rem 0", overflowX: "auto",
      }}>
        {buckets.map((bucket, i) => {
          const color   = BUCKET_COLORS[i % BUCKET_COLORS.length];
          const fillPct = (bucket.length / maxBucketSize) * 72;
          const isEmpty = bucket.length === 0;

          return (
            <div key={i} className="bucket-wrap" style={{ animationDelay: `${i * ANIM_STAGGER}ms` }}>
              <div
                className="bucket-body"
                style={{
                  borderColor: isEmpty ? "rgba(255,255,255,0.1)" : color,
                  boxShadow: isEmpty ? "none" : `0 0 12px ${color}33`,
                }}
              >
                <div className="bucket-bar-fill" style={{ height: `${fillPct}px`, background: `${color}22` }} />

                {bucket.map((val, j) => {
                  const norm  = max > min ? (val - min) / (max - min) : 0.5;
                  const alpha = Math.round((0.55 + norm * 0.45) * 255).toString(16).padStart(2, "0");
                  return (
                    <span
                      key={j}
                      className="value-chip"
                      style={{ background: `${color}${alpha}`, animationDelay: `${i * ANIM_STAGGER + j * 40}ms` }}
                    >
                      {val}
                    </span>
                  );
                })}

                {isEmpty && <span style={{ fontSize: "18px", opacity: 0.18, marginBottom: "8px" }}>∅</span>}
              </div>

              <span className="bucket-label">B{i}</span>
              {bucket.length > 0 && (
                <span className="bucket-count-badge" style={{ color }}>{bucket.length}</span>
              )}
            </div>
          );
        })}
      </div>

      <div style={{ marginTop: "1rem", display: "flex", alignItems: "center", gap: "0.75rem", padding: "0 0.5rem" }}>
        <span style={{ color: "#94a3b8", fontSize: "0.8rem", whiteSpace: "nowrap" }}>
          Elementos: {totalItems} · Cubetas usadas: {filledCount}/{buckets.length}
        </span>
        <div style={{ flex: 1, height: "5px", background: "#1e293b", borderRadius: "9999px", overflow: "hidden" }}>
          <div style={{
            height: "100%", width: `${progress * 100}%`,
            background: "linear-gradient(90deg, #3b82f6, #f59e0b)",
            borderRadius: "9999px", transition: "width 0.4s ease",
          }} />
        </div>
      </div>
    </div>
  );
}