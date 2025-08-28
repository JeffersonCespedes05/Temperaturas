# app.py
import streamlit as st
import sys
import os
import traceback
import logging

st.set_page_config(page_title="Conversor °C ↔ °F (diagnóstico)", page_icon="🌡️", layout="centered")

# Logger -> envia a stdout (Streamlit Cloud lo captura en logs)
logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    fmt = "%(asctime)s - %(levelname)s - %(message)s"
    handler.setFormatter(logging.Formatter(fmt))
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

def c_to_f(c): return c * 9.0 / 5.0 + 32.0
def f_to_c(f): return (f - 32.0) * 5.0 / 9.0

try:
    st.title("Conversor: °C ↔ °F 🌡️")
    st.write("Prueba de carga y conversión — si algo falla verás el traceback abajo.")

    # --- Health check rápido ---
    with st.expander("Comprobación del entorno (útil para depurar)"):
        st.write("Python:", sys.version.splitlines()[0])
        import importlib
        streamlit_version = importlib.import_module("streamlit").__version__
        st.write("Streamlit:", streamlit_version)
        # muestra variables de entorno relevantes si existen
        env_keys = ["PORT", "STREAMLIT_SERVER_PORT", "GITHUB_ACTIONS", "STREAMLIT_RUN_FROM_CLOUD"]
        st.write({k: os.environ.get(k) for k in env_keys if os.environ.get(k) is not None})

    st.markdown("---")
    modo = st.radio("Selecciona la conversión:", ("Celsius → Fahrenheit", "Fahrenheit → Celsius"))

    if modo == "Celsius → Fahrenheit":
        c = st.number_input("Grados Celsius (°C):", value=25.0, step=0.1, format="%.2f")
        if st.button("Convertir → °F"):
            f = c_to_f(c)
            st.success(f"{c:.2f} °C = {f:.2f} °F")
    else:
        f = st.number_input("Grados Fahrenheit (°F):", value=77.0, step=0.1, format="%.2f")
        if st.button("Convertir → °C"):
            c = f_to_c(f)
            st.success(f"{f:.2f} °F = {c:.2f} °C")

except Exception:
    # log y muestra el traceback en la UI (ayuda muchísimo para depurar en Cloud)
    logger.exception("Excepción al ejecutar la app")
    st.error("La app encontró un error al arrancar — despliega el traceback para ver detalles.")
    with st.expander("Traceback completo"):
        st.text(traceback.format_exc())
