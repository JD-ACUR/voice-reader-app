import os
import sys
import webview

from api import Api


def get_frontend_path():
    """
    Devuelve la ruta correcta al index.html, ya sea corriendo
    normal con Python o ya empaquetado con PyInstaller (.exe).
    """
    if getattr(sys, "frozen", False):
        # Corriendo como .exe (PyInstaller)
        base_path = sys._MEIPASS
    else:
        # Corriendo normal con python main.py
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, "frontend", "index.html")


def main():
    api = Api()

    window = webview.create_window(
        "Conversor de Texto a Audio",
        get_frontend_path(),
        js_api=api,
        width=800,
        height=650,
        resizable=True,
        min_size=(600, 500),
    )

    api.set_window(window)

    webview.start(debug=False)


if __name__ == "__main__":
    main()