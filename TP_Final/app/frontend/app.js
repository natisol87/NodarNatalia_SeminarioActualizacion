// La página y la API están en el mismo dominio, por eso alcanza con la ruta relativa.
// (Si algún día el backend queda en otro dominio, acá va la URL completa y hay que habilitar CORS.)
const URL_API = "/predecir";

const formulario = document.getElementById("formulario");
const boton = document.getElementById("boton");
const resultado = document.getElementById("resultado");

const EJEMPLOS = {
  bajo:   { horas_uso_diario: 3,   horas_sueno: 8,   horas_redes: 1,   horas_juegos: 0.5, chequeos_por_dia: 50,  apps_por_dia: 8 },
  limite: { horas_uso_diario: 5,   horas_sueno: 6.5, horas_redes: 2,   horas_juegos: 1.5, chequeos_por_dia: 80,  apps_por_dia: 12 },
  alto:   { horas_uso_diario: 6.5, horas_sueno: 5.5, horas_redes: 3,   horas_juegos: 2,   chequeos_por_dia: 120, apps_por_dia: 15 },
};

const NOMBRES = {
  horas_uso_diario: "Horas de uso por día",
  horas_sueno: "Horas de sueño",
  horas_redes: "Horas en redes sociales",
  horas_juegos: "Horas en juegos",
  chequeos_por_dia: "Veces que mira el celular",
  apps_por_dia: "Apps usadas por día",
};

// Botones de ejemplo: completan el formulario
document.querySelectorAll("[data-ejemplo]").forEach((b) => {
  b.addEventListener("click", () => {
    const datos = EJEMPLOS[b.dataset.ejemplo];
    for (const [campo, valor] of Object.entries(datos)) {
      formulario.elements[campo].value = valor;
    }
  });
});

formulario.addEventListener("submit", async (evento) => {
  evento.preventDefault();

  // Armamos el JSON. Los campos vacíos se mandan como null para que la API responda 422.
  const datos = {};
  for (const campo of Object.keys(NOMBRES)) {
    const texto = formulario.elements[campo].value.trim();
    datos[campo] = texto === "" ? null : Number(texto);
  }

  boton.disabled = true;
  boton.textContent = "Consultando…";

  try {
    const respuesta = await fetch(URL_API, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(datos),
    });

    const cuerpo = await respuesta.json().catch(() => null);

    if (respuesta.ok) {
      mostrarPrediccion(cuerpo);
    } else if (respuesta.status === 422) {
      mostrarError("Revisá los datos ingresados", explicarErrores422(cuerpo));
    } else {
      mostrarError(`La API respondió con un error (${respuesta.status})`,
                   [cuerpo?.detail ?? "Probá de nuevo en unos segundos."]);
    }
  } catch (error) {
    // fetch falla sin respuesta: servidor caído, sin conexión, etc.
    mostrarError("No se pudo conectar con la API",
                 ["El servidor puede estar caído o sin conexión. Probá de nuevo en unos segundos."]);
  } finally {
    boton.disabled = false;
    boton.textContent = "Predecir";
  }
});

function mostrarPrediccion({ adiccion_alta, probabilidad }) {
  const porcentaje = Math.round(probabilidad * 100);
  const color = adiccion_alta ? "var(--alto)" : "var(--bajo)";
  resultado.className = "";
  resultado.innerHTML = `
    <p class="titulo-resultado ${adiccion_alta ? "alto" : "bajo"}">
      ${adiccion_alta ? "Adicción alta" : "Adicción no alta"}
    </p>
    <p>Probabilidad de adicción alta: <strong>${porcentaje}%</strong></p>
    <div class="barra"><div style="width:${porcentaje}%; background:${color}"></div></div>
  `;
}

function mostrarError(titulo, detalles) {
  resultado.className = "error";
  resultado.innerHTML = `
    <p class="titulo-resultado">${titulo}</p>
    <ul>${detalles.map((d) => `<li>${d}</li>`).join("")}</ul>
  `;
}

// Traduce los errores de validación de Pydantic a mensajes legibles
function explicarErrores422(cuerpo) {
  if (!cuerpo?.detail || !Array.isArray(cuerpo.detail)) return ["Datos inválidos."];
  return cuerpo.detail.map((e) => {
    const campo = e.loc?.[e.loc.length - 1];
    const nombre = NOMBRES[campo];
    if (!nombre) return e.msg.replace("Value error, ", "");
    if (e.type === "missing" || e.input === null) return `${nombre}: falta completar.`;
    if (e.type === "greater_than_equal") return `${nombre}: tiene que ser ${e.ctx.ge} o más.`;
    if (e.type === "less_than_equal") return `${nombre}: tiene que ser ${e.ctx.le} o menos.`;
    if (e.type.startsWith("int")) return `${nombre}: tiene que ser un número entero.`;
    return `${nombre}: ${e.msg}`;
  });
}
