import React, { useMemo } from "react";

// ── Constantes ────────────────────────────────────────────────────
const DIGIT_COUNT = 10;
const DIGIT_COLORS = [
  "#6366f1", "#3b82f6", "#06b6d4", "#22c55e", "#84cc16",
  "#eab308", "#f97316", "#ef4444", "#ec4899", "#a855f7",
];
const STAGGER = 45;

// ── Utilidades ────────────────────────────────────────────────────

/** Convierte cualquier cosa en array de números */
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

/** Normaliza el paso completo y extrae metadata */
function normalizeStep(step) {
  if (!step) return { buckets: Array.from({ length: DIGIT_COUNT }, () => []), digitActual: null, isSorted: false };

  let raw, digitActual = null, isSorted = false;

  if (Array.isArray(step)) {
    raw = step;
  } else if (typeof step === "object") {
    raw         = step.buckets ?? step;
    digitActual = step.digit   ?? null;
    isSorted    = step.sorted  ?? false;
  } else {
    raw = [];
  }

  // Asegura exactamente 10 cubetas para radix
  const buckets = Array.from({ length: DIGIT_COUNT }, (_, i) =>
    normalizeBucket(Array.isArray(raw) ? raw[i] : null)
  );

  return { buckets, digitActual, isSorted };
}

// ── Componente ────────────────────────────────────────────────────
export default function RadixBuckets({ pasos, pasoActual }) {
  const { buckets, digitActual, isSorted } = useMemo(
    () => normalizeStep(pasos?.[pasoActual]),
    [pasos, pasoActual]
  );

  const totalItems    = useMemo(() => buckets.reduce((s, b) => s + b.length, 0), [buckets]);
  const maxBucketSize = useMemo(() => Math.max(...buckets.map((b) => b.length), 1), [buckets]);

  const totalPasos = Math.max((pasos?.length ?? 1) - 1, 1);
  const progress   = pasoActual / totalPasos;

  const digitLabel = digitActual !== null
    ? (["unidades", "decenas", "centenas", "millares"][digitActual] ?? `posición ${digitActual}`)
    : null;

  return (
    <div className="merge-container">
      <style>{`
        @keyframes radixDrop {
          from { opacity: 0; transform: translateY(-14px) scale(0.88); }
          to   { opacity: 1; transform: translateY(0) scale(1); }
        }
        @keyframes chipSlide {
          from { opacity: 0; transform: translateX(-10px); }
          to   { opacity: 1; transform: translateX(0); }
        }
        @keyframes pulseDigit {
          0%,100% { box-shadow: 0 0 0 0 transparent; }
          50%     { box-shadow: 0 0 14px 3px var(--d-color); }
        }
        .rdx-bucket-col {
          display: flex; flex-direction: column; align-items: center; gap: 5px;
          animation: radixDrop 0.38s cubic-bezier(0.34,1.56,0.64,1) both;
        }
        .rdx-bucket-body {
          display: flex; flex-direction: column-reverse; gap: 3px;
          padding: 6px 6px 0; border: 2px solid; border-top: none;
          border-radius: 0 0 9px 9px; min-width: 52px; min-height: 80px;
          align-items: center; position: relative; transition: border-color 0.3s, box-shadow 0.3s;
        }
        .rdx-bucket-body.active { animation: pulseDigit 1.4s ease-in-out infinite; }
        .rdx-fill-bar {
          position: absolute; bottom: 0; left: 0; right: 0;
          border-radius: 0 0 7px 7px; transition: height 0.5s ease; pointer-events: none;
        }
        .rdx-chip {
          font-size: 10px; font-weight: 700; font-family: 'Segoe UI', monospace;
          padding: 2px 6px; border-radius: 99px; color: #f1f5f9;
          position: relative; z-index: 1; white-space: nowrap;
          animation: chipSlide 0.28s ease both;
        }
        .rdx-digit-label {
          font-size: 13px; font-weight: 800; font-family: 'Segoe UI', monospace;
          width: 24px; height: 24px; border-radius: 50%; display: flex;
          align-items: center; justify-content: center; border: 2px solid;
          transition: background 0.3s, border-color 0.3s;
        }
        .rdx-count-badge {
          font-size: 10px; padding: 1px 5px; border-radius: 99px;
          font-weight: 700; background: rgba(255,255,255,0.07);
        }
        .rdx-sorted-list {
          display: flex; flex-wrap: wrap; gap: 6px; margin-top: 8px;
          animation: radixDrop 0.4s ease both;
        }
        .rdx-sorted-chip {
          font-size: 12px; font-weight: 700; font-family: 'Segoe UI', monospace;
          padding: 3px 10px; border-radius: 99px; color: #f1f5f9;
          background: #22c55e88; border: 1.5px solid #22c55e;
        }
      `}</style>

      <h3>🔢 Cubetas — Radix Sort</h3>
      <p style={{ color: "#94a3b8", fontSize: "0.85rem", marginTop: 0 }}>
        {digitLabel
          ? `Clasificando por dígito de ${digitLabel} (pasada ${digitActual + 1})`
          : "Distribuyendo valores en cubetas por dígito"}
      </p>

      {/* Indicador de posición */}
      {digitActual !== null && (
        <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "12px", fontSize: "0.8rem", color: "#94a3b8" }}>
          <span>Posición:</span>
          {["centenas", "decenas", "unidades"].map((name, idx) => {
            const pos    = 2 - idx;
            const active = pos === digitActual;
            return (
              <span key={pos} style={{
                padding: "2px 10px", borderRadius: "99px", fontSize: "0.75rem",
                fontWeight: active ? 700 : 400,
                background: active ? "#3b82f622" : "transparent",
                border: `1.5px solid ${active ? "#3b82f6" : "rgba(255,255,255,0.1)"}`,
                color: active ? "#3b82f6" : "#475569",
                transition: "all 0.3s",
              }}>
                {name}
              </span>
            );
          })}
        </div>
      )}

      {/* Vista de ordenado final */}
      {isSorted ? (
        <div>
          <p style={{ color: "#22c55e", fontSize: "0.85rem", marginBottom: "6px" }}>✅ Array ordenado</p>
          <div className="rdx-sorted-list">
            {buckets.flat().map((val, i) => (
              <span key={i} className="rdx-sorted-chip" style={{ animationDelay: `${i * 40}ms` }}>
                {val}
              </span>
            ))}
          </div>
        </div>
      ) : (
        <div style={{
          display: "flex", flexWrap: "wrap", gap: "8px",
          justifyContent: "center", padding: "0.5rem 0", overflowX: "auto",
        }}>
          {buckets.map((bucket, digit) => {
            const color    = DIGIT_COLORS[digit];
            const isEmpty  = bucket.length === 0;
            const fillH    = (bucket.length / maxBucketSize) * 68;
            const isActive = digitActual !== null && !isEmpty;

            return (
              <div
                key={digit}
                className="rdx-bucket-col"
                style={{ animationDelay: `${digit * STAGGER}ms`, "--d-color": color }}
              >
                <div
                  className={`rdx-bucket-body${isActive ? " active" : ""}`}
                  style={{
                    borderColor: isEmpty ? "rgba(255,255,255,0.08)" : color,
                    boxShadow: isEmpty ? "none" : `0 0 8px ${color}30`,
                  }}
                >
                  <div className="rdx-fill-bar" style={{ height: `${fillH}px`, background: `${color}1a` }} />

                  {bucket.map((val, j) => (
                    <span
                      key={j}
                      className="rdx-chip"
                      style={{ background: `${color}cc`, animationDelay: `${digit * STAGGER + j * 35}ms` }}
                    >
                      {val}
                    </span>
                  ))}

                  {isEmpty && <span style={{ fontSize: "16px", opacity: 0.15, marginBottom: "6px" }}>∅</span>}
                </div>

                <div className="rdx-digit-label" style={{
                  color: isEmpty ? "#334155" : color,
                  borderColor: isEmpty ? "#1e293b" : color,
                  background: isEmpty ? "transparent" : `${color}18`,
                }}>
                  {digit}
                </div>

                {!isEmpty && (
                  <span className="rdx-count-badge" style={{ color }}>{bucket.length}</span>
                )}
              </div>
            );
          })}
        </div>
      )}

      {/* Barra de progreso */}
      <div style={{ marginTop: "1rem", display: "flex", alignItems: "center", gap: "0.75rem", padding: "0 0.5rem" }}>
        <span style={{ color: "#94a3b8", fontSize: "0.8rem", whiteSpace: "nowrap" }}>
          Elementos: {totalItems}
        </span>
        <div style={{ flex: 1, height: "5px", background: "#1e293b", borderRadius: "9999px", overflow: "hidden" }}>
          <div style={{
            height: "100%", width: `${progress * 100}%`,
            background: "linear-gradient(90deg, #6366f1, #22c55e, #ef4444)",
            borderRadius: "9999px", transition: "width 0.4s ease",
          }} />
        </div>
      </div>
    </div>
  );
}