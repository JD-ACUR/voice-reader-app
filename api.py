import asyncio
import base64
import os
import sys
import tempfile
import webview
import edge_tts

# En Windows, cuando asyncio.run() se llama desde un hilo que no es el
# principal (como hace pywebview al ejecutar funciones de la API), la
# política de event loop por defecto (Proactor) puede fallar al resolver
# nombres de dominio (getaddrinfo failed). Forzamos la política Selector,
# que no tiene ese problema.
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


# Voces en inglés americano.
# "pitch" es opcional: sube el tono para simular una voz más juvenil
# cuando no existe una voz infantil real de ese género en edge-tts.
# Más voces disponibles en: https://github.com/rany2/edge-tts
VOCES_DISPONIBLES = {
    "Aria (Mujer adulta, EE.UU.)": {"voice": "en-US-AriaNeural", "pitch": "+0Hz"},
    "Guy (Hombre adulto, EE.UU.)": {"voice": "en-US-GuyNeural", "pitch": "+0Hz"},
    "Ana (Niña, EE.UU.)": {"voice": "en-US-AnaNeural", "pitch": "+0Hz"},
    "Niño (simulado, EE.UU.)": {"voice": "en-US-GuyNeural", "pitch": "+75Hz"},
#+75 sirve para que esa voz adquiero un tono parecido al de un infante
}


class Api:
    def __init__(self):
        self.window = None
        self._last_audio_path = None

    def set_window(self, window):
        self.window = window

    def obtener_voces(self):
        """Devuelve la lista de voces disponibles para llenar el <select> del HTML."""
        return list(VOCES_DISPONIBLES.keys())

    def generar_audio(self, texto, nombre_voz, velocidad):
        """
        Genera el audio a partir del texto.
        - texto: string a convertir
        - nombre_voz: una de las llaves de VOCES_DISPONIBLES
        - velocidad: string tipo "+0%", "+20%", "-15%" (formato que pide edge-tts)
        Devuelve un dict con éxito/error para que el JS reaccione.
        """
        texto = (texto or "").strip()
        if not texto:
            return {"ok": False, "error": "El texto está vacío."}

        voice_info = VOCES_DISPONIBLES.get(nombre_voz)
        if not voice_info:
            return {"ok": False, "error": "Voz no válida."}

        try:
            # Archivo temporal para poder reproducirlo antes de decidir si se guarda
            tmp_dir = tempfile.gettempdir()
            tmp_path = os.path.join(tmp_dir, "tts_mama_preview.mp3")

            asyncio.run(
                self._sintetizar(
                    texto, voice_info["voice"], velocidad, voice_info["pitch"], tmp_path
                )
            )

            self._last_audio_path = tmp_path

            with open(tmp_path, "rb") as f:
                audio_b64 = base64.b64encode(f.read()).decode("utf-8")

            return {"ok": True, "path": tmp_path, "audio_base64": audio_b64}

        except Exception as e:
            return {"ok": False, "error": str(e)}

    async def _sintetizar(self, texto, voice_id, velocidad, pitch, salida):
        communicate = edge_tts.Communicate(texto, voice_id, rate=velocidad, pitch=pitch)
        await communicate.save(salida)

    def guardar_como(self):
        """
        Abre un diálogo nativo para que el usuario elija dónde guardar
        el último audio generado.
        """
        if not self._last_audio_path or not os.path.exists(self._last_audio_path):
            return {"ok": False, "error": "Primero genera un audio."}

        result = self.window.create_file_dialog(
            webview.SAVE_DIALOG,
            save_filename="audio_clase.mp3",
            file_types=("Archivos de audio (*.mp3)",),
        )

        if not result:
            return {"ok": False, "error": "Guardado cancelado."}

        destino = result if isinstance(result, str) else result[0]

        with open(self._last_audio_path, "rb") as f_in:
            with open(destino, "wb") as f_out:
                f_out.write(f_in.read())

        return {"ok": True, "path": destino}
