# =================================================================
#               GEORAMÓN EXPLORER - APP.PY (PARTE 1)
# =================================================================

import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import geopandas as gpd
import os
import json
import webbrowser
from fastkml import kml
from shapely.geometry import mapping

# Configuración de la página en modo ancho completo
st.set_page_config(layout="wide", page_title="GeoRamón Explorer")

# --- ALMACENAMIENTO LOCAL (CSV) ---
ARCHIVO_DATOS = "puntos_prospeccion.csv"

def cargar_datos():
    if os.path.exists(ARCHIVO_DATOS):
        return pd.read_csv(ARCHIVO_DATOS)
    else:
        datos_iniciales = {
            "ID": ["P-001", "P-002", "P-003"],
            "Nombre": ["San Ramón Centro", "Río San Julián - Aluvión", "Cantera Zona Norte"],
            "Tipo": ["Terraza aluvial", "Paleocauce", "Veta"],
            "Potencial": ["Alto", "Medio", "Alto"],
            "Latitud": [-16.6167, -16.6350, -16.5980],
            "Longitud": [-62.4820, -62.4820, -62.5150],
            "Observaciones": [
                "Buen lugar. Acceso rápido desde el pueblo.",
                "Demasiada vegetación y vida salvaje. Requiere machete.",
                "Zona seca, propensa a incendios en agosto. Cuidado."
            ]
        }
        df = pd.DataFrame(datos_iniciales)
        df.to_csv(ARCHIVO_DATOS, index=False)
        return df

df_puntos = cargar_datos()

# --- INTERFAZ DE USUARIO ---
st.title("🗺️ GeoRamón Explorer - Prospección Aurífera")

# Estructura de 3 columnas principales (Panel Izquierdo | Mapa Central | Panel Derecho)
col_izquierda, col_mapa, col_derecha = st.columns([2.2, 4.3, 2.5])

# Panel Izquierdo: Capas, Filtros, Cargador Avanzado y Formulario
with col_izquierda:
    st.header("Capas")
    base_layer = st.radio("Base", ["OpenStreetMap", "Satélite (ESRI)", "Topográfico", "Relieve"])
    
    st.subheader("📁 Capas Geológicas / Concesiones")
    archivo_capa = st.file_uploader("Subir KML o GeoJSON", type=["kml", "geojson"])
    
    st.subheader("Análisis")
    filtro_potencial = st.selectbox("Filtrar por Potencial", ["Todos", "Alto", "Medio", "Bajo"])
    
    st.markdown("---")
    
    st.header("➕ Registrar Punto")
    with st.form("formulario_punto", clear_on_submit=True):
        nuevo_nombre = st.text_input("Nombre de la zona", placeholder="Ej. Quebrada Amarilla")
        nuevo_tipo = st.selectbox("Tipo de depósito", ["Terraza aluvial", "Paleocauce", "Veta", "Diseminado"])
        nuevo_potencial = st.selectbox("Potencial estimado", ["Alto", "Medio", "Bajo"])
        
        nueva_lat = st.number_input("Latitud (Y)", min_value=-22.0, max_value=-9.0, value=-16.6167, format="%.4f")
        nueva_lon = st.number_input("Longitud (X)", min_value=-70.0, max_value=-57.0, value=-62.5000, format="%.4f")
        
        nuevas_obs = st.text_area("Observaciones de campo")
        
        boton_guardar = st.form_submit_button("Guardar Punto de Interés")
        
        if boton_guardar:
            if nuevo_nombre.strip() == "":
                st.error("El nombre de la zona es obligatorio.")
            else:
                if not df_puntos.empty:
                    valores_id = df_puntos["ID"].str.replace("P-", "").astype(int)
                    proximo_numero = valores_id.max() + 1
                else:
                    proximo_numero = 1
                proximo_id = f"P-{proximo_numero:03d}"
                
                nueva_fila = {
                    "ID": proximo_id, "Nombre": nuevo_nombre, "Tipo": nuevo_tipo,
                    "Potencial": nuevo_potencial, "Latitud": nueva_lat, "Longitud": nueva_lon, "Observaciones": nuevas_obs
                }
                
                df_actualizado = pd.concat([df_puntos, pd.DataFrame([nueva_fila])], ignore_index=True)
                df_actualizado.to_csv(ARCHIVO_DATOS, index=False)
                st.success(f"Punto {proximo_id} guardado.")
                st.rerun()

# Aplicar el filtro de potencial en memoria para el despliegue posterior
df_filtrado = df_puntos if filtro_potencial == "Todos" else df_puntos[df_puntos["Potencial"] == filtro_potencial]

# =================================================================
#               GEORAMÓN EXPLORER - APP.PY (PARTE 2)
# =================================================================

# Panel Central: Mapa Georreferenciado
with col_mapa:
    coordenadas_centro = [-16.6167, -62.5000]
    
    if base_layer == "Satélite (ESRI)":
        m = folium.Map(location=coordenadas_centro, zoom_start=11, tiles="https://arcgisonline.com{z}/{y}/{x}", attr="Esri")
    elif base_layer == "Topográfico":
        m = folium.Map(location=coordenadas_centro, zoom_start=11, tiles="https://{s}.tile.opentopomap.org/{z}/{y}/{x}.png", attr="OpenTopoMap")
    elif base_layer == "Relieve":
        m = folium.Map(location=coordenadas_centro, zoom_start=11, tiles="https://arcgisonline.com{z}/{y}/{x}", attr="EsriRelief")
    else:
        m = folium.Map(location=coordenadas_centro, zoom_start=11, tiles="openstreetmap")
        
    folium.LayerControl().add_to(m)

    # BLOQUE CORREGIDO: Carga de KML/GeoJSON
    if archivo_capa is not None:
        try:
            nombre_archivo = archivo_capa.name.lower()
            if nombre_archivo.endswith(".geojson"):
                datos_geo = json.load(archivo_capa)
                folium.GeoJson(datos_geo, name="Capa Geológica", style_function=lambda x: {'fillColor': '#ffcc00', 'color': '#ff9900', 'weight': 2, 'fillOpacity': 0.4}).add_to(m)
            
            elif nombre_archivo.endswith(".kml"):
                contenido_kml = archivo_capa.read().decode("utf-8")
                kml_obj = kml.KML()
                kml_obj.from_string(contenido_kml)
                
                features = []
                for document in kml_obj.features():
                    for folder in document.features():
                        for feature in folder.features():
                            if hasattr(feature, 'geometry') and feature.geometry is not None:
                                try:
                                    geom_dict = mapping(feature.geometry)
                                    features.append({
                                        "type": "Feature",
                                        "geometry": geom_dict,
                                        "properties": {"name": feature.name if hasattr(feature, 'name') else "Sin nombre"}
                                    })
                                except Exception as geom_err:
                                    st.warning(f"No se pudo procesar geometría: {geom_err}")
                
                if features:
                    geojson_convertido = {"type": "FeatureCollection", "features": features}
                    folium.GeoJson(geojson_convertido, name="Capa KML", style_function=lambda x: {'fillColor': '#00ccff', 'color': '#0066ff', 'weight': 2, 'fillOpacity': 0.4}).add_to(m)
                else:
                    st.warning("El archivo KML no contiene geometrías válidas.")
        
        except Exception as e:
            st.error(f"Error al procesar el archivo espacial: {e}")
    
    for _, fila in df_filtrado.iterrows():
        color_pino = "red" if fila["Potencial"] == "Alto" else "orange" if fila["Potencial"] == "Medio" else "green"
        folium.Marker(
            location=[fila["Latitud"], fila["Longitud"]],
            popup=f"<b>{fila['Nombre']}</b>",
            tooltip=fila["ID"],
            icon=folium.Icon(color=color_pino, icon="info-sign")
        ).add_to(m)
    
    datos_mapa = st_folium(m, width="100%", height=600, key="mapa_principal")

# BLOQUE CORREGIDO: Captura de clic estable con session_state
if "id_clicado_actual" not in st.session_state:
    st.session_state.id_clicado_actual = None

# Detectar clic nuevo
if datos_mapa and isinstance(datos_mapa, dict) and "last_object_clicked_tooltip" in datos_mapa:
    tooltip_capturado = datos_mapa["last_object_clicked_tooltip"]
    if tooltip_capturado is not None and tooltip_capturado != st.session_state.id_clicado_actual:
        st.session_state.id_clicado_actual = tooltip_capturado

id_clicado = st.session_state.id_clicado_actual

# Panel Derecho: Visualizador, Edición, Eliminación y Enlace IA
with col_derecha:
    st.header("Punto Seleccionado")
    
    if id_clicado and not df_puntos.empty and id_clicado in df_puntos["ID"].values:
        filas_coincidentes = df_puntos[df_puntos["ID"] == id_clicado].to_dict(orient="records")
        fila_punto = filas_coincidentes[0]
        st.success(f"Modo Edición activo: {id_clicado}")
        
        with st.form("formulario_edicion"):
            edit_nombre = st.text_input("Nombre de la Zona", value=fila_punto["Nombre"])
            edit_tipo = st.selectbox("Tipo de Terreno", ["Terraza aluvial", "Paleocauce", "Veta", "Diseminado"], index=["Terraza aluvial", "Paleocauce", "Veta", "Diseminado"].index(fila_punto["Tipo"]))
            edit_potencial = st.selectbox("Nivel de Potencial", ["Alto", "Medio", "Bajo"], index=["Alto", "Medio", "Bajo"].index(fila_punto["Potencial"]))
            edit_lat = st.number_input("Latitud Exacta", value=float(fila_punto["Latitud"]), format="%.4f")
            edit_lon = st.number_input("Longitud Exacta", value=float(fila_punto["Longitud"]), format="%.4f")
            edit_obs = st.text_area("Alertas / Observaciones de Terreno", value=str(fila_punto["Observaciones"]) if pd.notna(fila_punto["Observaciones"]) else "")
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1: btn_actualizar = st.form_submit_button("Actualizar Punto")
            with col_btn2: btn_eliminar = st.form_submit_button("Eliminar Punto")
            
            if btn_actualizar:
                df_puntos.loc[df_puntos["ID"] == id_clicado, ["Nombre", "Tipo", "Potencial", "Latitud", "Longitud", "Observaciones"]] = [edit_nombre, edit_tipo, edit_potencial, edit_lat, edit_lon, edit_obs]
                df_puntos.to_csv(ARCHIVO_DATOS, index=False)
                st.success("Registro actualizado.")
                st.rerun()
                
            if btn_eliminar:
                df_puntos = df_puntos[df_puntos["ID"] != id_clicado]
                df_puntos.to_csv(ARCHIVO_DATOS, index=False)
                st.warning("Registro eliminado.")
                st.rerun()
                
        st.markdown("---")
        st.subheader("🧠 Análisis Geológico Personalizado")
        
        # Generar prompt maestro pre-rellenado
        prompt_maestro = f"""Actúa como un Geólogo Consultor e Ingeniero de Minas experto en la región aurífera de San Ramón (Santa Cruz, Bolivia). Analiza minuciosamente la captura de pantalla adjunta de mi aplicación GeoRamón Explorer considerando de forma estricta que la ubicación se encuentra dentro de la faja del Escudo Precámbrico Boliviano (Cratón de Guaporé).

Para romper cualquier modelo de respuesta estándar, toma en cuenta las siguientes variables reales de mi campaña:
• Nombre de la Zona: {fila_punto["Nombre"]}
• Tipo de Depósito / Formación: {fila_punto["Tipo"]}
• Observaciones de Terreno: {fila_punto["Observaciones"]}
• Coordenadas: {fila_punto["Latitud"]:.4f}, {fila_punto["Longitud"]:.4f}

Proporcióname un diagnóstico técnico personalizado estructurado estrictamente en los siguientes tres puntos:

1. TIPO DE YACIMIENTO PROBABLE: Determina si bajo estas condiciones el objetivo primario en esa coordenada exacta es de tipo estructural/orogénico (veta) o aluvial/placer (secundario), detallando la roca caja esperable (ej. esquistos verdes del Supergrupo San Ignacio).
2. DIAGNÓSTICO OPERATIVO (¿DETECTOR O PALA Y PICOTA?): Justifica técnicamente si la morfología, la vegetación y la profundidad estimada del 'bedrock' (roca madre basamento) permiten una prospección rápida con detector de metales en superficie (VLF/PI), o si el terreno exige obligatoriamente excavación física profunda con picota, pala y batea.
3. GUÍA VISUAL PARA EL CATEADOR AL LLEGAR AL SITIO: Detalla exactamente qué indicadores físicos (como cuarzo con limonitas/goethita, fuchsita, micas o concentrados de arenas negras de fierro/magnetita) debe buscar el personal de apoyo al limpiar el terreno.

Evita respuestas genéricas o ambiguas; habla con base en la metalogenia real de San Ramón."""

        st.info("📋 **Prompt pre-rellenado para IA** — Copia el texto, pega en tu IA + adjunta captura")
        
        # Mostrar prompt en textarea para copiar fácilmente
        st.text_area("Copia este prompt y pégalo en ChatGPT/Gemini/Claude:", 
                     value=prompt_maestro, 
                     height=250,
                     disabled=True,
                     label_visibility="collapsed")
        
        col_abrir1, col_abrir2, col_abrir3 = st.columns(3)
        
        with col_abrir1:
            if st.button("💬 ChatGPT", use_container_width=True):
                webbrowser.open_new_tab("https://chatgpt.com")
                st.success("✓ ChatGPT abierto — pega el prompt de arriba")
        
        with col_abrir2:
            if st.button("✨ Google Gemini", use_container_width=True):
                webbrowser.open_new_tab("https://gemini.google.com")
                st.success("✓ Google Gemini abierto — pega el prompt de arriba")
        
        with col_abrir3:
            if st.button("🤖 Claude", use_container_width=True):
                webbrowser.open_new_tab("https://claude.ai")
                st.success("✓ Claude abierto — pega el prompt de arriba")
            
    else:
        st.info("Haz clic en un marcador del mapa para habilitar su edición o análisis.")
        st.text_input("Nombre de la Zona", "Seleccione un punto...", disabled=True)
        st.text_input("Tipo de Terreno", "", disabled=True)
        st.text_input("Coordenadas Exactas", "", disabled=True)
        st.text_input("Nivel de Potencial", "", disabled=True)
        st.text_area("Alertas / Observaciones de Terreno", "", disabled=True, height=120)
    
    st.markdown("---")
    if st.button("🔄 Limpiar Selección", use_container_width=True):
        st.session_state.id_clicado_actual = None
        st.rerun()

# Panel Inferior: Tabla General
st.markdown("---")
col_tabla, col_exportar = st.columns(2)

with col_tabla:
    st.subheader("📋 Registro Local de Puntos de Interés")

with col_exportar:
    st.subheader("📥 Exportar Datos")
    tab_csv, tab_geojson = st.tabs(["CSV", "GeoJSON"])
    
    with tab_csv:
        col_sel, col_todo = st.columns(2)
        
        with col_sel:
            csv_filtrado = df_filtrado.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📋 Filtrado",
                data=csv_filtrado,
                file_name="reporte_georamon_filtrado.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col_todo:
            csv_todos = df_puntos.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📊 Todos los Puntos",
                data=csv_todos,
                file_name="reporte_georamon_completo.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    with tab_geojson:
        # Crear GeoJSON desde df_puntos
        features = []
        for _, fila in df_puntos.iterrows():
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [float(fila["Longitud"]), float(fila["Latitud"])]
                },
                "properties": {
                    "ID": fila["ID"],
                    "Nombre": fila["Nombre"],
                    "Tipo": fila["Tipo"],
                    "Potencial": fila["Potencial"],
                    "Observaciones": fila["Observaciones"]
                }
            }
            features.append(feature)
        
        geojson_data = {
            "type": "FeatureCollection",
            "features": features
        }
        geojson_str = json.dumps(geojson_data, ensure_ascii=False, indent=2).encode('utf-8')
        
        st.download_button(
            label="🗺️ GeoJSON (Todos los Puntos)",
            data=geojson_str,
            file_name="puntos_prospeccion_georamon.geojson",
            mime="application/json",
            use_container_width=True
        )

st.dataframe(df_filtrado, use_container_width=True, hide_index=True)
