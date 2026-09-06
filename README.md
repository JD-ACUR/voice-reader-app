# 🎙️ Conversor de Texto a Audio

Aplicación de escritorio que convierte texto en inglés a audio, pensada originalmente para ayudar a una profesora de inglés a generar material de clase sin depender de conversores en línea de pago o con anuncios.

## Problema que resuelve

Existen muchos conversores de texto a audio en internet, pero casi todos:
- Requieren pago o suscripción para uso frecuente
- Muestran anuncios molestos
- Tienen límites de caracteres muy cortos en su versión gratuita

Este proyecto ofrece una alternativa **gratuita, sin anuncios y sin límites**, corriendo como una app de escritorio nativa (Windows), sin necesidad de conexión a un servidor propio ni de pagar ninguna API.

## Funcionalidades

- Conversión de texto a audio en inglés americano
- 4 voces disponibles:
  - Mujer adulta (Aria)
  - Hombre adulto (Guy)
  - Niña (Ana — voz infantil real)
  - Niño (voz simulada mediante ajuste de tono)
- Control de velocidad de habla
- Control de tono (pitch) para ajustar cómo suena cada voz
- Reproducción del audio directamente en la app
- Guardado del audio como archivo `.mp3` en la ubicación que elija el usuario
- Corre como aplicación de escritorio (`.exe`), sin necesidad de navegador ni terminal

## Stack técnico

- **[edge-tts](https://github.com/rany2/edge-tts)** — generación de voz neuronal (usa el motor de Microsoft Edge sin necesidad de licencia ni API key)
- **[pywebview](https://pywebview.flowrl.com/)** — muestra la interfaz (HTML/CSS/JS) dentro de una ventana nativa de escritorio
- **HTML / CSS / JavaScript** — interfaz de usuario
- **PyInstaller** — empaquetado de la app en un `.exe` ejecutable

> ⚠️ **Nota:** aunque la app corre como programa de escritorio, `edge-tts` necesita conexión a internet para generar el audio (se comunica con los servidores de voz de Microsoft). No funciona en modo completamente offline.

## Estructura del proyecto

```
proyecto/
├── main.py              # Punto de entrada: crea la ventana de la app
├── api.py                # Lógica de generación de audio (edge-tts)
├── requirements.txt
└── frontend/
    ├── index.html        # Interfaz
    ├── style.css
    └── script.js         # Comunicación con la API de Python
```

## Cómo correrlo en desarrollo

1. Clona el repositorio y entra a la carpeta del proyecto.
2. Crea y activa un entorno virtual:
   ```
   python -m venv venv
   venv\Scripts\activate   # Windows
   ```
3. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```
4. Corre la app:
   ```
   python main.py
   ```

## Cómo generar el ejecutable (.exe)

Con el entorno virtual activado, desde la raíz del proyecto:

```
pyinstaller --onefile --windowed --name "ConversorDeAudio" --add-data "frontend;frontend" main.py
```

El ejecutable final queda en `dist\ConversorDeAudio.exe`. Ese es el único archivo que se necesita compartir para que alguien más use la app (no requiere Python, VS Code ni ninguna instalación adicional — solo conexión a internet).

> La primera vez que se ejecuta, Windows Defender SmartScreen puede mostrar una advertencia por tratarse de un `.exe` sin firma digital. Esto es normal en proyectos personales; basta con hacer clic en "Más información" → "Ejecutar de todas formas".

## Motivación del proyecto

Proyecto desarrollado como práctica de portafolio, combinando backend en Python, integración con un servicio de síntesis de voz, 
empaquetado de aplicaciones de escritorio, y una interfaz simple e intuitiva pensada para una usuaria no técnica.

primer proyecto