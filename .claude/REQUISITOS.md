# Metadatos

## Qué contiene
Qué debe hacer el proyecto en el MVP, desde mi punto de vista y sin entrar en cómo se construye: funciones, reglas, experiencia de uso y restricciones que no son técnicas. Las decisiones de producto llevan cómo se decidieron.

Lo que no encaje en esta descripción no va aquí. Lo que queda fuera del MVP va a `FUTURO.md`.

## Actualización
Casi inmutable: se escribe en la entrevista inicial y solo cambia si yo lo pido porque añada o cambie algo de lo que debe hacer.

Lo que quiero que haga el proyecto se escribe tal cual: un requisito por línea, sin justificarlo. Solo las decisiones indican entre paréntesis cómo se decidieron, con `Descartado` en la misma línea solo si aporta (ver `PROTOCOLOS.md`). Lo que se afina más adelante no se desarrolla: se deja como "se afina en la fase X".

Se carga siempre, así que si crece demasiado (unas 300 líneas), avísame para dividirlo.


# Contenido

## Qué debe hacer

### Acceso
- Web pública y gratuita: se entra con un enlace, sin instalar nada.
- Interfaz en español.

### Flujo
- Subir PDF → peso y talla (y edad y sexo si el PDF no los trae), en los dos modos → (hábitos, si se elige ese modo) → ver resultado.
- La pantalla de revisión se construye solo si las pruebas del parser muestran que hace falta. Si se construye, solo aparece si el parser marca algún valor como dudoso (sin reconocer, sin unidad, fuera del rango posible o edad y sexo ausentes), y solo con esos valores: revisarlo todo mete la fricción que la app quiere quitar. Se valida con los PDFs reales de Rubén; si fallan, se replantea. (Rubén, de acuerdo) Descartado: revisión siempre.
- La app lee los valores del PDF y normaliza los nombres de los parámetros (glucosa / gluc / GLU…) y las unidades antes de la pantalla de revisión.

### Modos
- Dos modos, a elección del usuario: solo con la analítica, o con la analítica más un cuestionario de hábitos de vida.
- El modo se elige con dos botones en la portada, y el de analítica + cuestionario es el destacado porque da la mejor respuesta. Al pulsar cualquiera se abre el selector de archivos. (Rubén, de acuerdo) Descartado: dos pestañas.
- El cuestionario va una pregunta por pantalla, al estilo Typeform: las opciones en tarjetas con icono y aclaración, que pasan solas a la siguiente pregunta; los números en una barra deslizable para el valor grueso con − y + en los extremos para el ajuste fino, y una barra de progreso fina arriba. Peso y talla siguen el mismo estilo. Los rangos de las barras son los rangos posibles del modelo. (Rubén, de acuerdo) Descartado: hélice como barra de progreso; fichas que se deslizan, demasiados toques para peso y talla.
- El cuestionario pregunta por tabaco, actividad física, horas sentado y horas de sueño.
- Preguntas sin inputs escritos y solo de datos objetivos: nada de autovaloraciones ("¿cómo de sana es tu dieta?", "¿cómo es tu salud?").
- **El alcohol no se pregunta, y la app explica por qué falta, en la pregunta del tabaco:** el modelo no lo usa (en los datos, beber sale protector por causalidad inversa) y el usuario espera verlo en un cuestionario de hábitos.

### Datos de entrada
- Usa lo que trae una analítica de rutina española, lo que se pide a menudo (p. ej. vitamina D) y lo que el usuario sabe sin pensar (edad, sexo, peso, talla), siempre que exista en NHANES.
- Edad y sexo se extraen del PDF si vienen (la edad, de la fecha de nacimiento si no viene directa); si no, se piden como primeras preguntas del cuestionario, solo las que falten. El sexo falta a menudo; la edad, casi nunca.
- Tensión arterial: dato opcional para afinar, nunca obligatorio.
- Solo adultos, dentro del rango de edad de los datos de entrenamiento (18 a 79 años). La portada lo dice en una línea. (Rubén, de acuerdo) Descartado: pop-up al entrar, añade un clic.
- Edad real fuera de 18-79: se calcula igualmente, con un aviso rojo debajo de la frase de la diferencia que diga que está fuera del rango de los datos. Por debajo de 16 años no se calcula: los valores normales de una analítica son otros y extrapolar ya no tiene sentido. (Rubén, de acuerdo) Descartado: bloquear a los menores de 18, a los 16-17 la extrapolación es corta.
- Solo se admiten PDFs: cualquier otro archivo da el error de "no podemos leer este PDF".
- Errores (PDF ilegible o que no es una analítica, faltan demasiados datos, valor imposible confirmado, menor de 16): pantalla propia al estilo de la portada, con el título grande ("No podemos / calcular tu edad"), el icono en un círculo debajo, la explicación y qué puede hacer el usuario en texto gris, sin viñetas ni recuadro, "Subir otro PDF" y "Volver al inicio". (Rubén, de acuerdo) Descartado: aviso en la portada, en móvil se pasa por alto; tarjeta con borde rosa; viñetas en recuadros.
- Valor imposible: el resultado se ve difuminado detrás de una ventana que muestra el valor y deja corregirlo en la misma casilla, con el botón o tocándola, con los mismos decimales con que lo da el laboratorio, o confirmarlo. Si se confirma, no se calcula: pantalla de error con "Si el valor es real, acude a un médico con urgencia" en una franja amarilla como la del aviso, con texto negro y un triángulo de alerta. (Rubén, de acuerdo)
- Las analíticas no traen siempre los mismos parámetros: si falta algún dato, se calcula igualmente con menos fiabilidad; si faltan demasiados, se avisa de que no se puede calcular.
- **Valor fuera del rango posible:** se pide al usuario que lo compruebe (puede ser una mala lectura del PDF); si lo confirma, la app no calcula la edad biológica y avisa de ir al médico cuanto antes. Son valores de emergencia o de una muestra defectuosa: dar una edad ahí sería engañoso.

### Resultado
Siempre:
- Edad biológica estimada ± X años y la diferencia con la edad cronológica. X depende de la precisión de cada caso: más ancho si faltan datos o en jóvenes de riesgo bajo.
- [pendiente: cómo se calcula el ±. Descartado: bootstrap del modelo con relleno de huecos, a Rubén no le convence; si no hay un método claro, se quita.]
- Edades fuera de 18-79: por debajo de 18, "menos de 18"; de 79 a 90, el número con la nota "orientativo"; por encima de 90, "más de 90". (Rubén, de acuerdo)
- Una tabla fija, igual para todos, con los grupos que la gente entiende: vitaminas y minerales, azúcar, corazón (HDL y tensión), glóbulos rojos, defensas (con un escudo), hígado, riñón y peso (IMC). Cada fila dice cuántos años suma o resta frente a una persona típica de su edad y sexo, sin ±. Se parte en dos columnas, "te quitan años" y "te suman años", cada una ordenada por valor absoluto de mayor a menor; los grupos sin datos van en una línea aparte. (Rubén, de acuerdo) Descartado: los mejores y peores parámetros de cada persona, la tabla cambiaría de un usuario a otro; porcentajes por órgano, escala inventada
- Aviso de que no es consejo médico ni diagnóstico. No se dan recomendaciones (suplementos, tratamientos…), solo observaciones de los datos.
- Aviso asimétrico: salir por encima es señal para consultar, pero salir bien no significa estar sano. De momento no se muestra: la franja amarilla ya avisa y Rubén no quiere más mensajes. (Rubén, en desacuerdo)

Cuando se hace el cuestionario:
- Una segunda tabla igual con sus hábitos: tabaco, ejercicio, horas sentado y horas de sueño.

Diseño del resultado:
- La pestaña del navegador se llama "BioAge".
- El resultado va dentro de un recuadro de bordes redondeados. La edad biológica en grande, sin título encima, con el ± en pequeño a su lado (no debajo), y debajo la frase "X años menos/más que tu edad real (Y)". (Rubén, de acuerdo) Descartado: medidor en arco, no aporta; tarjetas y pastillas.
- Al final, compartir (en el móvil) y descargar el resultado como imagen; la imagen se crea en el navegador, sin subir nada. (Rubén, de acuerdo) Descartado: "calcular otra vez"; texto pequeño de aviso bajo las tablas, ya lo hace la franja amarilla.
- Iconos anatómicos de Healthicons para corazón, hígado y riñón; gota para glóbulos rojos, escudo para defensas, diamante para vitaminas y minerales, un montoncito de azúcar y "kg" para el peso.

Cuando la edad biológica está 10 o más años por encima de la real (haya o no cuestionario):
- [pendiente: si se recomienda comentarla con el médico y con qué frase; Rubén lo consulta con el profesor. De momento, sin mensaje.]

## Experiencia de uso
- La UX tiene prioridad sobre afinar el modelo: el modelo es fácil de iterar, y una UX mal planteada obliga a rehacerla.
- Usable por cualquier persona: flujo corto, lenguaje claro sin jerga, responsive y pensado para móvil.
- Estados de carga y errores de parseo comprensibles y accionables: qué ha fallado y qué puede hacer el usuario.
- Portada: título, "Para adultos de 18 a 79 años" como subtítulo, los dos botones, la línea "No guardamos nada: tu analítica se procesa y se descarta" con una llamada ¹ y, en una franja inferior muy visible, el aviso de que no es consejo médico. La llamada baja a la letra pequeña, debajo de la franja, como en las webs de bancos: qué se hace con los datos (consentimiento al subir el PDF, sin conservación), responsable, cómo se calcula y qué no es. (Rubén, de acuerdo) Descartado: solo la frase "no guardamos nada", el RGPD pide más; pop-up.
- La app abre siempre arriba, en la portada, aunque se recargue.
- La franja está en la portada y en el resultado, no en el cuestionario ni en la carga: si está siempre, pasa a ser parte del fondo y deja de leerse. (Rubén, de acuerdo)
- Estética "microscopio": oscuro, verde profundo con acentos esmeralda, titulares en Fraunces y el aviso en amarillo de peligro con el símbolo de riesgo biológico. (Rubén, de acuerdo) Descartado: neón con red de partículas, no evoca biología; mezclar la hélice de ADN con las células en el fondo, recargado.
- Fondo animado en todas las pantallas: células flotando como bajo la lente. Manda la fluidez sobre la estética: si no va fluido, imagen fija.
- Al tocar el fondo salen destellos y nacen o explotan células; al pulsar botones, no.
- Pantalla de carga cosmética antes del resultado, de 1,5 a 2 segundos: una hélice de ADN verde que se construye de arriba abajo, "Calculando tu edad" y un porcentaje que sube rápido de 0 a 100. (Rubén, de acuerdo) Descartado: frases que cambian y lista de pasos; hélice bicolor, cansa la vista.
- En la portada, "solo analítica" va a la izquierda y "analítica + hábitos", destacado, a la derecha.

## Restricciones
- **Privacidad:** son datos de salud (categoría especial en el RGPD).
  - Minimizar el tratamiento y no almacenar nada: la app procesa todo en memoria y lo descarta.
  - No se usan etnia ni datos socioeconómicos.
  - Informar al usuario de forma clara de qué se hace con sus datos.
- **Formato de entrada:** PDF digital.
- **Plazos:** Entrega 04 (solución UX), el 29 de noviembre de 2026. Entrega final, el 9 de diciembre de 2026 (fecha del enunciado de la Entrega 04; ante la duda, la más corta).
