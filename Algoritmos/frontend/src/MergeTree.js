import React, { useMemo, useRef } from "react";

// ── Constantes de layout ──────────────────────────────────────────
const LEVEL_H   = 110;
const LEAF_W    = 95;
const NODE_R    = 30;
const PADDING_X = 55;
const PADDING_Y = 55;

const DEPTH_COLORS = ["#3b82f6", "#ef4444", "#22c55e"];

// ── Utilidades ────────────────────────────────────────────────────

function leafCount(node) {
  if (!node) return 0;
  if (!node.izquierda && !node.derecha) return 1;
  return leafCount(node.izquierda) + leafCount(node.derecha);
}

function computeLayout(node, depth = 0, xStart = 0) {
  if (!node) return null;
  const lw    = leafCount(node.izquierda);
  const left  = computeLayout(node.izquierda, depth + 1, xStart);
  const right = computeLayout(node.derecha,   depth + 1, xStart + lw);

  let nodeX;
  if (left && right)   nodeX = (left.x + right.x) / 2;
  else if (left)       nodeX = left.x;
  else if (right)      nodeX = right.x;
  else                 nodeX = xStart + 0.5;

  return { valor: node.valor, x: nodeX, y: depth, izquierda: left, derecha: right };
}

/** BFS: devuelve los nodos en orden nivel por nivel */
function collectBFS(root) {
  if (!root) return [];
  const result = [];
  const queue  = [root];
  while (queue.length) {
    const node = queue.shift();
    result.push(node);
    if (node.izquierda) queue.push(node.izquierda);
    if (node.derecha)   queue.push(node.derecha);
  }
  return result;
}

function collectEdges(node, edges = []) {
  if (!node) return edges;
  if (node.izquierda) {
    edges.push({ from: node, to: node.izquierda });
    collectEdges(node.izquierda, edges);
  }
  if (node.derecha) {
    edges.push({ from: node, to: node.derecha });
    collectEdges(node.derecha, edges);
  }
  return edges;
}

function makeLabel(valor) {
  if (!Array.isArray(valor)) return String(valor);
  if (valor.length === 1)    return String(valor[0]);
  if (valor.length <= 4)     return valor.join(",");
  return `${valor[0]}…${valor[valor.length - 1]}`;
}

function nodeRadius(valor) {
  return Math.max(NODE_R, makeLabel(valor).length * 7);
}

// ── Componente ────────────────────────────────────────────────────

export default function MergeTree({ arbol, pasos, pasoActual }) {
  // Ref para animar los nodos con CSS al montarse/cambiar
  const svgRef = useRef(null);

  const computed = useMemo(() => {
    if (!arbol) return null;

    const layout      = computeLayout(arbol);
    const bfsNodes    = collectBFS(layout);   // orden BFS = orden de aparición
    const allEdges    = collectEdges(layout);
    const totalLeaves = leafCount(arbol);
    const maxDepth    = Math.max(...bfsNodes.map((n) => n.y));

    const svgW = totalLeaves * LEAF_W + PADDING_X * 2;
    const svgH = (maxDepth + 1) * LEVEL_H + PADDING_Y * 2;

    const toX = (x) => x * LEAF_W + LEAF_W / 2 + PADDING_X;
    const toY = (y) => y * LEVEL_H + PADDING_Y;

    return { bfsNodes, allEdges, svgW, svgH, toX, toY };
  }, [arbol]);

  if (!computed) return null;

  const { bfsNodes, allEdges, svgW, svgH, toX, toY } = computed;

  // ── Cuántos nodos mostrar según el progreso ──────────────────────
  // Al inicio (paso 0) solo la raíz; al final todos visibles.
  const totalNodes   = bfsNodes.length;
  const totalPasos   = Math.max(pasos.length - 1, 1);
  const progress     = pasoActual / totalPasos;               // 0 → 1
  const visibleCount = Math.max(1, Math.round(progress * totalNodes));

  const visibleSet = new Set(bfsNodes.slice(0, visibleCount));

  // Arista visible solo si ambos extremos son visibles
  const visibleEdges = allEdges.filter(
    (e) => visibleSet.has(e.from) && visibleSet.has(e.to)
  );

  return (
    <div className="merge-container">
      {/* Inyectar keyframes de animación */}
      <style>{`
        @keyframes nodeIn {
          from { opacity: 0; transform: scale(0.3); }
          to   { opacity: 1; transform: scale(1); }
        }
        @keyframes edgeIn {
          from { opacity: 0; stroke-dashoffset: 200; }
          to   { opacity: 1; stroke-dashoffset: 0; }
        }
        .merge-node { transform-box: fill-box; transform-origin: center; }
      `}</style>

      <h3>🌳 Árbol de división — Merge Sort</h3>
      <p style={{ color: "#94a3b8", fontSize: "0.85rem", marginTop: 0 }}>
        El árbol se construye a medida que avanza el ordenamiento
      </p>

      <div style={{ overflowX: "auto" }}>
        <svg ref={svgRef} width={svgW} height={svgH}
          style={{ display: "block", margin: "0 auto" }}>

          {/* ── Puntas de flecha por color ── */}
          <defs>
            {DEPTH_COLORS.map((color, i) => (
              <marker key={i} id={`arrow-${i}`}
                markerWidth="10" markerHeight="7"
                refX="9" refY="3.5" orient="auto">
                <polygon points="0 0, 10 3.5, 0 7" fill={color} />
              </marker>
            ))}
          </defs>

          {/* ── Aristas animadas ── */}
          {visibleEdges.map((e, i) => {
            const x1  = toX(e.from.x);
            const y1  = toY(e.from.y);
            const x2  = toX(e.to.x);
            const y2  = toY(e.to.y);
            const r2  = nodeRadius(e.to.valor);
            const dx  = x2 - x1;
            const dy  = y2 - y1;
            const len = Math.sqrt(dx * dx + dy * dy);
            const ex  = x2 - (dx / len) * (r2 + 3);
            const ey  = y2 - (dy / len) * (r2 + 3);

            const colorIdx = e.to.y % DEPTH_COLORS.length;
            const color    = DEPTH_COLORS[colorIdx];

            // key único que incluye el índice visible para reiniciar la animación
            const edgeKey = `edge-${i}-${visibleCount}`;

            return (
              <line
                key={edgeKey}
                x1={x1} y1={y1} x2={ex} y2={ey}
                stroke={color}
                strokeWidth="2"
                strokeDasharray="200"
                markerEnd={`url(#arrow-${colorIdx})`}
                style={{
                  animation: "edgeIn 0.4s ease forwards",
                }}
              />
            );
          })}

          {/* ── Nodos animados ── */}
          {bfsNodes.map((node, i) => {
            if (!visibleSet.has(node)) return null;

            const cx    = toX(node.x);
            const cy    = toY(node.y);
            const r     = nodeRadius(node.valor);
            const color = DEPTH_COLORS[node.y % DEPTH_COLORS.length];
            const txt   = makeLabel(node.valor);

            // key que cambia cuando el nodo "aparece" para disparar la animación
            const isLastVisible = i === visibleCount - 1;
            const nodeKey = `node-${i}-${isLastVisible ? visibleCount : "stable"}`;

            return (
              <g
                key={nodeKey}
                className="merge-node"
                style={{
                  animation: isLastVisible
                    ? "nodeIn 0.35s cubic-bezier(0.34,1.56,0.64,1) forwards"
                    : "none",
                  opacity: 1,
                }}
              >
                {/* Sombra */}
                <circle cx={cx} cy={cy + 3} r={r} fill="rgba(0,0,0,0.35)" />

                {/* Círculo principal */}
                <circle
                  cx={cx} cy={cy} r={r}
                  fill="#1e293b"
                  stroke={color}
                  strokeWidth="2.5"
                />

                {/* Brillo interno sutil */}
                <circle
                  cx={cx - r * 0.25} cy={cy - r * 0.25}
                  r={r * 0.35}
                  fill="rgba(255,255,255,0.04)"
                />

                {/* Texto */}
                <text
                  x={cx} y={cy}
                  textAnchor="middle"
                  dominantBaseline="middle"
                  fill="#f1f5f9"
                  fontSize={r > NODE_R ? "11" : "13"}
                  fontWeight="bold"
                  fontFamily="'Segoe UI', monospace"
                >
                  {txt}
                </text>
              </g>
            );
          })}
        </svg>
      </div>

      {/* Indicador de progreso del árbol */}
      <div style={{
        marginTop: "0.75rem",
        display: "flex",
        alignItems: "center",
        gap: "0.75rem",
        padding: "0 0.5rem",
      }}>
        <span style={{ color: "#94a3b8", fontSize: "0.8rem", whiteSpace: "nowrap" }}>
          Nodos: {visibleCount}/{totalNodes}
        </span>
        <div style={{
          flex: 1,
          height: "5px",
          background: "#1e293b",
          borderRadius: "9999px",
          overflow: "hidden",
        }}>
          <div style={{
            height: "100%",
            width: `${(visibleCount / totalNodes) * 100}%`,
            background: "linear-gradient(90deg, #3b82f6, #22c55e)",
            borderRadius: "9999px",
            transition: "width 0.4s ease",
          }} />
        </div>
      </div>
    </div>
  );
}