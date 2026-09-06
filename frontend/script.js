const selectVoz = document.getElementById("voz");
const inputVelocidad = document.getElementById("velocidad");
const velocidadValor = document.getElementById("velocidad-valor");
const textarea = document.getElementById("texto");
const btnGenerar = document.getElementById("btn-generar");
const btnGuardar = document.getElementById("btn-guardar");
const mensaje = document.getElementById("mensaje");
const reproductor = document.getElementById("reproductor");

function mostrarMensaje(texto, esError = false) {
  mensaje.textContent = texto;
  mensaje.style.color = esError ? "#dc2626" : "#16a34a";
}

function formatoVelocidad(valor) {
  const n = Number(valor);
  if (n === 0) return "+0%";
  return n > 0 ? `+${n}%` : `${n}%`;
}

function etiquetaVelocidad(valor) {
  const n = Number(valor);
  if (n === 0) return "Normal";
  return n > 0 ? `${n}% más rápido` : `${Math.abs(n)}% más lento`;
}

inputVelocidad.addEventListener("input", () => {
  velocidadValor.textContent = etiquetaVelocidad(inputVelocidad.value);
});

// pywebview dispara este evento cuando window.pywebview.api ya está listo
window.addEventListener("pywebviewready", async () => {
  try {
    const voces = await window.pywebview.api.obtener_voces();
    selectVoz.innerHTML = "";
    voces.forEach((v) => {
      const opt = document.createElement("option");
      opt.value = v;
      opt.textContent = v;
      selectVoz.appendChild(opt);
    });
  } catch (e) {
    mostrarMensaje("No se pudieron cargar las voces.", true);
  }
});

btnGenerar.addEventListener("click", async () => {
  const texto = textarea.value.trim();

  if (!texto) {
    mostrarMensaje("Escribe algo de texto primero.", true);
    return;
  }

  btnGenerar.disabled = true;
  btnGenerar.textContent = "Generando...";
  mostrarMensaje("");

  try {
    const resultado = await window.pywebview.api.generar_audio(
      texto,
      selectVoz.value,
      formatoVelocidad(inputVelocidad.value)
    );

    if (resultado.ok) {
      // Usamos data URL (base64) en vez de file:// porque el navegador
      // interno de pywebview bloquea la reproducción de rutas locales.
      reproductor.src = `data:audio/mpeg;base64,${resultado.audio_base64}`;
      reproductor.style.display = "block";
      reproductor.play();
      btnGuardar.disabled = false;
      mostrarMensaje("Audio generado. Puedes escucharlo o guardarlo.");
    } else {
      mostrarMensaje(resultado.error || "Ocurrió un error.", true);
    }
  } catch (e) {
    mostrarMensaje("Error al generar el audio: " + e, true);
  } finally {
    btnGenerar.disabled = false;
    btnGenerar.textContent = "Generar audio";
  }
});

btnGuardar.addEventListener("click", async () => {
  try {
    const resultado = await window.pywebview.api.guardar_como();
    if (resultado.ok) {
      mostrarMensaje(`Guardado en: ${resultado.path}`);
    } else {
      mostrarMensaje(resultado.error || "No se pudo guardar.", true);
    }
  } catch (e) {
    mostrarMensaje("Error al guardar: " + e, true);
  }
});