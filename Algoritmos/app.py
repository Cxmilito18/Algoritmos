import streamlit as st
import plotly.graph_objects as go
from controller import Controller
from utils import Utils
from merge_sort import MergeSort
import json

# ─────────────────────────────────────────────────────────────
# CONFIGURACIÓN STREAMLIT
# ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="AlgoSort - Visualizador de Algoritmos",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    :root {
        --accent-merge: #00d9ff;
        --accent-shell: #00ff88;
        --accent-radix: #ff006e;
        --bg-dark: #0a0e27;
        --bg-panel: #141829;
        --text-primary: #e0e6ff;
        --text-muted: #8892b0;
        --border: #1e2139;
    }
    
    body {
        background-color: var(--bg-dark);
        color: var(--text-primary);
    }
    
    .stApp {
        background-color: var(--bg-dark);
    }
    
    .algorithm-card {
        background: linear-gradient(135deg, #141829 0%, #1a2942 100%);
        border: 1px solid #1e2139;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
    }
    
    .metric-box {
        background: var(--bg-panel);
        border-left: 3px solid var(--accent-merge);
        border-radius: 8px;
        padding: 15px;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# ESTADO DE LA SESIÓN
# ─────────────────────────────────────────────────────────────

if "algoritmo_actual" not in st.session_state:
    st.session_state.algoritmo_actual = "merge_sort"
if "datos_ingresados" not in st.session_state:
    st.session_state.datos_ingresados = []
if "pasos_animacion" not in st.session_state:
    st.session_state.pasos_animacion = []
if "paso_actual" not in st.session_state:
    st.session_state.paso_actual = 0
if "animando" not in st.session_state:
    st.session_state.animando = False

# ─────────────────────────────────────────────────────────────
# BARRA LATERAL - NAVEGACIÓN
# ─────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 🎯 AlgoSort")
    st.markdown("---")
    
    # Selector de algoritmo
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔵 Merge Sort", use_container_width=True):
            st.session_state.algoritmo_actual = "merge_sort"
            st.session_state.paso_actual = 0
            st.rerun()
    with col2:
        if st.button("🟢 Shell Sort", use_container_width=True):
            st.session_state.algoritmo_actual = "shell_sort"
            st.session_state.paso_actual = 0
            st.rerun()
    with col3:
        if st.button("🔴 Radix Sort", use_container_width=True):
            st.session_state.algoritmo_actual = "radix_sort"
            st.session_state.paso_actual = 0
            st.rerun()
    
    st.markdown("---")
    
    # Información del algoritmo
    algoritmo_info = {
        "merge_sort": {
            "nombre": "MERGE SORT",
            "complejidad": "O(n log n)",
            "lema": "Divide y vencerás",
            "descripcion": "Divide el arreglo en mitades recursivamente, luego combina los subarreglos ordenados.",
            "color": "#00d9ff"
        },
        "shell_sort": {
            "nombre": "SHELL SORT",
            "complejidad": "O(n log² n)",
            "lema": "Inserción generalizada",
            "descripcion": "Generalización del ordenamiento por inserción que permite el intercambio de elementos lejanos.",
            "color": "#00ff88"
        },
        "radix_sort": {
            "nombre": "RADIX SORT",
            "complejidad": "O(nk)",
            "lema": "Ordena por dígitos",
            "descripcion": "Ordena los números dígito por dígito, comenzando desde el menos o más significativo.",
            "color": "#ff006e"
        }
    }
    
    info = algoritmo_info[st.session_state.algoritmo_actual]
    st.markdown(f"### {info['nombre']}")
    st.markdown(f"**{info['lema']}** · *{info['complejidad']}*")
    st.markdown(f"_{info['descripcion']}_")
    
    st.markdown("---")
    
    # Controles de entrada
    st.markdown("### ⚙️ Datos de Entrada")
    
    modo_entrada = st.radio("Modo", ["Manual", "Generar"], horizontal=True)
    
    if modo_entrada == "Manual":
        entrada_texto = st.text_input(
            "Array",
            value=" ".join(map(str, st.session_state.datos_ingresados)) if st.session_state.datos_ingresados else "",
            placeholder="Ej: 64 25 12 22 11"
        )
        if st.button("✔️ Cargar Array", use_container_width=True):
            try:
                datos = []
                for d in entrada_texto.split():
                    try:
                        datos.append(float(d))
                    except:
                        datos.append(d)
                st.session_state.datos_ingresados = datos
                st.session_state.paso_actual = 0
                st.success(f"✓ {len(datos)} elementos cargados")
            except Exception as e:
                st.error(f"Error al cargar datos: {e}")
    else:
        n = st.number_input("N elementos", min_value=1, max_value=100, value=10)
        if st.button("⟳ Generar Array", use_container_width=True):
            st.session_state.datos_ingresados = Utils.generar_datos(n)
            st.session_state.paso_actual = 0
            st.success(f"✓ {n} números aleatorios generados")
    
    st.markdown("---")
    
    # Control de velocidad
    velocidad = st.slider("Velocidad de animación", min_value=1, max_value=100, value=50)
    
    # Botones de control
    st.markdown("### ▶️ Animación")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ Ordenar", use_container_width=True):
            if st.session_state.datos_ingresados:
                pasos = Controller.obtener_pasos(st.session_state.datos_ingresados.copy())
                st.session_state.pasos_animacion = pasos
                st.session_state.paso_actual = 0
                st.rerun()
            else:
                st.error("Por favor ingresa o genera datos primero")
    
    with col2:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.paso_actual = 0
            st.session_state.pasos_animacion = []
            st.rerun()

# ─────────────────────────────────────────────────────────────
# ÁREA PRINCIPAL
# ─────────────────────────────────────────────────────────────

st.markdown("# 📊 AlgoSort - Visualizador de Algoritmos de Ordenamiento")

if not st.session_state.datos_ingresados:
    st.info("👈 Configura tus datos en la barra lateral para comenzar")
else:
    # Fila de información
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Elementos",
            value=len(st.session_state.datos_ingresados),
            delta="elementos cargados"
        )
    
    with col2:
        ordenado = Utils.esta_ordenado(st.session_state.datos_ingresados)
        st.metric(
            label="Estado",
            value="✓ Ordenado" if ordenado else "✗ Desordenado"
        )
    
    with col3:
        st.metric(
            label="Datos",
            value=", ".join(map(str, st.session_state.datos_ingresados[:5])) + 
                  ("..." if len(st.session_state.datos_ingresados) > 5 else "")
        )
    
    st.markdown("---")
    
    # Visualización principal
    col_visual, col_info = st.columns([3, 1])
    
    with col_visual:
        st.markdown("### 📈 Visualización de Barras")
        
        # Crear gráfico de barras interactivo
        fig = go.Figure()
        
        # Datos actuales a visualizar
        if st.session_state.pasos_animacion and st.session_state.paso_actual < len(st.session_state.pasos_animacion):
            tipo, data = st.session_state.pasos_animacion[st.session_state.paso_actual]
            datos_a_mostrar = data
        else:
            datos_a_mostrar = st.session_state.datos_ingresados
        
        # Convertir strings a números si es necesario para graficar
        valores = []
        etiquetas = []
        for i, d in enumerate(datos_a_mostrar):
            try:
                valores.append(float(d))
                etiquetas.append(str(d))
            except:
                valores.append(i)
                etiquetas.append(str(d))
        
        # Determinar color según algoritmo
        color_map = {
            "merge_sort": "#00d9ff",
            "shell_sort": "#00ff88",
            "radix_sort": "#ff006e"
        }
        color_actual = color_map.get(st.session_state.algoritmo_actual, "#00d9ff")
        
        fig.add_trace(go.Bar(
            x=list(range(len(valores))),
            y=valores,
            marker=dict(
                color=color_actual,
                line=dict(color="#1e2139", width=1)
            ),
            hovertemplate="<b>Posición: %{x}</b><br>Valor: %{y}<extra></extra>"
        ))
        
        fig.update_layout(
            title=None,
            xaxis_title="Posición",
            yaxis_title="Valor",
            hovermode="x unified",
            plot_bgcolor="#141829",
            paper_bgcolor="#0a0e27",
            font=dict(color="#e0e6ff"),
            height=400,
            showlegend=False,
            margin=dict(l=50, r=50, t=50, b=50)
        )
        
        fig.update_xaxes(gridcolor="#1e2139")
        fig.update_yaxes(gridcolor="#1e2139")
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col_info:
        st.markdown("### 📊 Información")
        
        if st.session_state.pasos_animacion:
            progreso = st.session_state.paso_actual / len(st.session_state.pasos_animacion)
            st.progress(progreso)
            st.caption(f"Paso {st.session_state.paso_actual + 1} / {len(st.session_state.pasos_animacion)}")
            
            if st.session_state.paso_actual < len(st.session_state.pasos_animacion):
                tipo, _ = st.session_state.pasos_animacion[st.session_state.paso_actual]
                
                estado_map = {
                    "nodo": "🌳 Dividiendo",
                    "merge": "🔄 Combinando",
                    "comparar": "⚖️ Comparando",
                    "resultado": "✅ Resultado"
                }
                
                st.write(f"**Estado:** {estado_map.get(tipo, 'Procesando')}")
            
            # Controles de pasos
            col1, col2 = st.columns(2)
            with col1:
                if st.button("⬅️ Anterior"):
                    if st.session_state.paso_actual > 0:
                        st.session_state.paso_actual -= 1
                        st.rerun()
            with col2:
                if st.button("Siguiente ➡️"):
                    if st.session_state.paso_actual < len(st.session_state.pasos_animacion) - 1:
                        st.session_state.paso_actual += 1
                        st.rerun()

# ─────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #8892b0; font-size: 0.85em;'>
    <p>AlgoSort - Visualizador Interactivo de Algoritmos de Ordenamiento</p>
    <p>Hecho con ❤️ para aprender algoritmos</p>
</div>
""", unsafe_allow_html=True)
