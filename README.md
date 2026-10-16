# 🗺️ GeoRamón Explorer

**Aplicación de prospección aurífera para la región de San Ramón, Bolivia**

Una herramienta geoespacial para registrar, editar y analizar puntos de interés minero con asistencia de IA especializada en geología de yacimientos auríferos.

---

## 🎯 Características

✅ **Mapa interactivo** con múltiples capas base (OpenStreetMap, Satélite ESRI, Topográfico)
✅ **Registro de puntos** con nombre, tipo de depósito, potencial y observaciones
✅ **Edición y eliminación** de puntos desde el mapa
✅ **Filtrado por potencial** (Alto, Medio, Bajo)
✅ **Carga de capas geológicas** (KML, GeoJSON)
✅ **Exportación de datos** en CSV y GeoJSON
✅ **Análisis geológico automatizado** con prompt pre-rellenado para IA especializada
✅ **Persistencia local** en navegador (sin dependencias de servidor)

---

## 📋 Requisitos

- Python 3.8+
- pip (gestor de paquetes)

## 🚀 Instalación Rápida

### 1. Clonar o descargar el repositorio

```bash
git clone https://github.com/armandocoroneo/georamon-explorer.git
cd georamon-explorer
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar la aplicación

```bash
streamlit run app.py
```

La app se abrirá en `http://localhost:8501`

---

## 💾 Cómo Usar

### Registrar un Punto

1. Completa el formulario en el panel izquierdo:
   - **Nombre de la zona** (obligatorio)
   - **Tipo de depósito** (Terraza aluvial, Paleocauce, Veta, Diseminado)
   - **Potencial estimado** (Alto, Medio, Bajo)
   - **Coordenadas** (Latitud, Longitud)
   - **Observaciones de campo**

2. Presiona **"Guardar Punto de Interés"**
3. El punto aparecerá en el mapa

### Editar o Eliminar un Punto

1. Haz clic en un marcador del mapa
2. El panel derecho mostrará los datos del punto
3. Edita los campos que necesites
4. Presiona **"Actualizar Punto"** o **"Eliminar Punto"**

### Cargar Capas Geológicas

1. En el panel izquierdo, sección "📁 Capas Geológicas / Concesiones"
2. Sube un archivo KML o GeoJSON
3. Se renderizará sobre el mapa

### Análisis Geológico con IA

1. Haz clic en un punto del mapa
2. En el panel derecho, verás un **textarea con prompt pre-rellenado**
3. El prompt contiene:
   - Nombre de la Zona
   - Tipo de Depósito
   - Observaciones de Terreno
   - Coordenadas

4. Copia el prompt (Ctrl+A → Ctrl+C)
5. Presiona uno de los botones para abrir tu IA favorita:
   - **💬 ChatGPT**
   - **✨ Google Gemini**
   - **🤖 Claude**

6. En la IA, pega el prompt (Ctrl+V) y adjunta una captura de pantalla de GeoRamón Explorer
7. Recibirás un análisis técnico estructurado en 3 puntos:
   - **TIPO DE YACIMIENTO PROBABLE**
   - **DIAGNÓSTICO OPERATIVO** (¿detector o excavación?)
   - **GUÍA VISUAL PARA EL CATEADOR**

### Exportar Datos

1. En la tabla inferior, haz clic en la pestaña **"📥 Exportar Datos"**
2. Elige formato:
   - **CSV Filtrado**: solo puntos visibles según filtro actual
   - **CSV Todos**: todos los puntos registrados
   - **GeoJSON**: compatible con QGIS, ArcGIS, Google Earth

---

## 📊 Estructura de Datos

Cada punto registra:

```
ID          → Identificador único (P-001, P-002, etc.)
Nombre      → Nombre de la zona
Tipo        → Terraza aluvial | Paleocauce | Veta | Diseminado
Potencial   → Alto | Medio | Bajo
Latitud     → Coordenada Y
Longitud    → Coordenada X
Observaciones → Notas de terreno
```

---

## 🗺️ Capas de Mapa Disponibles

| Capa | Descripción |
|------|-------------|
| OpenStreetMap | Mapa base gratuito |
| Satélite (ESRI) | Imágenes satelitales de alta resolución |
| Topográfico | Mapa con contornos de elevación |
| Relieve | Mapa con sombreado de relieve |

---

## 🤖 Prompt Maestro para IA

El prompt pre-rellenado automáticamente instruye a la IA para actuar como:

> **Geólogo Consultor e Ingeniero de Minas experto en la región aurífera de San Ramón (Santa Cruz, Bolivia)**

Con contexto del **Escudo Precámbrico Boliviano (Cratón de Guaporé)** y análisis específico de:
- Tipo de yacimiento (estructural vs. aluvial)
- Método operativo (detector vs. excavación)
- Indicadores visuales para cateadores en terreno

---

## 📁 Archivos del Proyecto

```
georamon-explorer/
├── app.py                    # Aplicación principal
├── requirements.txt          # Dependencias Python
├── README.md                 # Este archivo
└── CAMBIOS_REALIZADOS.md    # Historial técnico de cambios
```

---

## 🔧 Dependencias

```
streamlit              # Framework web
folium                 # Mapas interactivos
streamlit-folium       # Integración Folium + Streamlit
pandas                 # Manipulación de datos
geopandas              # Datos geoespaciales
fastkml                # Parsing de archivos KML
```

---

## 🌐 Desplegar en Streamlit Cloud (Gratis)

1. Sube este repositorio a tu GitHub (ya está hecho)
2. Ve a [streamlit.io/cloud](https://streamlit.io/cloud)
3. Clic en "New app"
4. Conecta tu repo GitHub
5. Selecciona `main` branch, archivo `app.py`
6. Presiona "Deploy"

**Acceso público:** Tu app tendrá un link público que otros pueden visitar sin instalar nada

---

## 💡 Casos de Uso

- **Prospección aurífera** en San Ramón, Bolivia
- **Mapeo de depósitos** (primarios y secundarios)
- **Análisis geológico personalizado** con contexto local
- **Documentación de campaña** exportable a CSV/GeoJSON
- **Validación operativa** antes de excavación

---

## ⚠️ Notas Importantes

- **Datos locales**: Los puntos se guardan en el navegador del usuario (localStorage), no en servidor
- **Sin sincronización**: Cada usuario/dispositivo tiene su propio dataset
- **Para compartir datos**: Exporta a CSV/GeoJSON y comparte con el equipo
- **Offline**: La app funciona sin conexión a internet (excepto para mapas base)

---

## 🐛 Reportar Problemas

Si encuentras bugs o tienes sugerencias, abre un issue en GitHub:
[armandocoroneo/georamon-explorer/issues](https://github.com/armandocoroneo/georamon-explorer/issues)

---

## 📄 Licencia

Código abierto. Úsalo libremente.

---

## 👤 Autor

Desarrollado para prospección aurífera en San Ramón, Bolivia.

**Última actualización:** Octubre 2026
