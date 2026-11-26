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
- El PDF se lee antes de las preguntas, con su pantalla de carga: si no se puede calcular, se avisa ahí y no después de contestar. (Rubén, de acuerdo) Descartado: cortar a mitad del cuestionario, el PDF ya dice si hay que preguntar el sexo.
- La pantalla de revisión se construye solo si las pruebas del parser muestran que hace falta. Si se construye, solo aparece si el parser marca algún valor como dudoso (sin reconocer, sin unidad, fuera del rango posible o edad y sexo ausentes), y solo con esos valores: revisarlo todo mete la fricción que la app quiere quitar. Se valida con los PDFs reales de Rubén; si fallan, se replantea. (Rubén, de acuerdo) Descartado: revisión siempre.
- La app lee los valores del PDF y normaliza los nombres de los parámetros (glucosa / gluc / GLU…) y las unidades antes de la pantalla de revisión.

### Modos
- Dos modos, a elección del usuario: solo con la analítica, o con la analítica más un cuestionario de hábitos de vida.
- El modo se elige con dos botones en la portada, y el de analítica + cuestionario es el destacado porque da la mejor respuesta. Al pulsar cualquiera se abre el selector de archivos. (Rubén, de acuerdo) Descartado: dos pestañas.
- El cuestionario va una pregunta por pantalla, al estilo Typeform: las opciones en tarjetas con icono y aclaración, que pasan solas a la siguiente pregunta; los números en una barra deslizable para el valor grueso con − y + en los extremos para el ajuste fino, y una barra de progreso fina arriba. Peso y talla siguen el mismo estilo. Los rangos de las barras son los rangos posibles del modelo. (Rubén, de acuerdo) Descartado: hélice como barra de progreso; fichas que se deslizan, demasiados toques para peso y talla.
- El cuestionario pregunta por tabaco, actividad física, horas sentado y horas de sueño.
- El tabaco incluye el vapeo. (Rubén, en desacuerdo) Descartado: solo tabaco, el modelo aprendió con fumadores de cigarrillos y no hay datos de mortalidad del vapeo.
- El ejercicio se pregunta como "al menos una vez por semana", intenso o suave, que es la definición de NHANES.
- Las horas de sueño se piden en promedio semanal. (Rubén, en desacuerdo) Descartado: entre semana, que es lo que preguntaba NHANES; la diferencia es pequeña y la media es como la gente piensa su sueño.
- Preguntas sin inputs escritos y solo de datos objetivos: nada de autovaloraciones ("¿cómo de sana es tu dieta?", "¿cómo es tu salud?").
- **El alcohol no se pregunta, y la app no explica por qué:** al usuario le importa su edad, no los límites del modelo. (Rubén, de acuerdo) Descartado: explicarlo en la pregunta del tabaco.

### Datos de entrada
- Usa lo que trae una analítica de rutina española, lo que se pide a menudo (p. ej. vitamina D) y lo que el usuario sabe sin pensar (edad, sexo, peso, talla), siempre que exista en NHANES.
- Edad y sexo se extraen del PDF si vienen (la edad, de la fecha de nacimiento si no viene directa); si no, se piden como primeras preguntas del cuestionario, solo las que falten. El sexo falta a menudo; la edad, casi nunca.
- La tensión arterial no se usa ni se pregunta: casi nadie la sabe de memoria. (Rubén, de acuerdo)
- Solo adultos, dentro del rango de edad de los datos de entrenamiento (18 a 79 años). La portada dice "De 16 a 90 años". (Rubén, de acuerdo) Descartado: pop-up al entrar, añade un clic; "para adultos", suena raro y no es verdad.
- Edad real fuera de 18-79: se calcula igualmente, con un aviso rojo debajo de la frase de la diferencia que diga que está fuera del rango de los datos. Por debajo de 16 años no se calcula: los valores normales de una analítica son otros y extrapolar ya no tiene sentido. Por encima de 90 tampoco: los datos llegan a 79. (Rubén, de acuerdo) Descartado: bloquear a los menores de 18, a los 16-17 la extrapolación es corta.
- Solo se admiten PDFs: cualquier otro archivo da el error de "No puedo leer este PDF".
- Errores (PDF ilegible o que no es una analítica, faltan demasiados datos, valor imposible confirmado, menor de 16, mayor de 90, sin conexión con el servidor): pantalla propia al estilo de la portada, con el título grande ("No puedo / calcular tu edad"), el icono en un círculo debajo, la explicación y qué puede hacer el usuario en texto gris, sin viñetas ni recuadro, "Subir otro PDF" (o "Reintentar" si el servidor no responde, sin perder las respuestas) y "Volver al inicio". (Rubén, de acuerdo) Descartado: aviso en la portada, en móvil se pasa por alto; tarjeta con borde rosa; viñetas en recuadros.
- Si el servidor responde con un error que no sabe explicar, la pantalla ofrece "Subir otro PDF" y no "Reintentar", que volvería a fallar; "Reintentar" queda para cuando no responde (sin conexión o el hosting despertando). (Claude, autónomo)
- Valor imposible: justo después de leer el PDF sale una ventana que muestra el valor y deja corregirlo en la misma casilla, con el botón o tocándola, con los mismos decimales con que lo da el laboratorio, o confirmarlo. Si lo corregido sigue siendo imposible, se vuelve a preguntar en la misma ventana. Si se confirma, no se calcula: pantalla de error con "Si el valor es real, acude a un médico con urgencia" en una franja amarilla como la del aviso, con texto negro y un triángulo de alerta. Si hay varios, salen todos en la misma ventana, uno debajo de otro. (Rubén, de acuerdo) Descartado: uno detrás de otro; al final, sobre el resultado difuminado, haría contestar las preguntas para nada.
- Las analíticas no traen siempre los mismos parámetros: si falta algún dato, se calcula igualmente con menos fiabilidad; si faltan demasiados, se avisa de que no se puede calcular. Criterio laxo, para que casi cualquier analítica sirva: se acepta que la edad se mueva hasta 7 años (en 9 de cada 10 personas) por lo que falta, y hoy eso son hasta 5 valores de Routine sin cuestionario y hasta 8 con él (se vuelve a medir en cada reentreno). (Rubén, de acuerdo) Descartado: 3 años, casi nadie tendría resultado.
- Los Extras se usan (modelo de nivel 2, o 4 con cuestionario) si el PDF trae al menos 3 de los 8, o 4 con cuestionario (se vuelve a medir en cada reentreno): desde ahí su modelo ordena mejor y se acerca más a la edad con todos, con el criterio fijado antes de ver los datos. (Rubén, de acuerdo) Descartado: 7 u 8, la idea inicial de Rubén, los datos dicen otra cosa.
- **IMC imposible:** se avisa al contestar el segundo de los dos datos, peso o talla, con una pantalla de humor y un ogro que deja corregirlos sin perder el resto de respuestas. No se calcula si se confirma. (Rubén, de acuerdo)
- **Valor fuera del rango posible:** se pide al usuario que lo compruebe (puede ser una mala lectura del PDF); si lo confirma, la app no calcula la edad biológica y avisa de ir al médico cuanto antes. Son valores de emergencia o de una muestra defectuosa: dar una edad ahí sería engañoso.

### Resultado
Siempre:
- Edad biológica estimada ± X años y la diferencia con la edad cronológica. X depende de la precisión de cada caso: más ancho si faltan datos o en jóvenes de riesgo bajo.
- El ± junta dos errores, sumados en cuadrado (`√(base² + lo que falta²)`), porque dos errores independientes no suelen ir a la vez en la misma dirección. **Error base:** la calibración en años (cuánto se aleja la edad de las muertes reales), con los 5 bloques de train juntos, en dos tramos de riesgo: bajo (décimos 1 a 5, sobre todo jóvenes) y el resto. **Lo que falta:** la mediana de cuánto se mueve la edad según cuántos valores de Routine y de Extras no trae el PDF, medida en el modelo de cada nivel. (Rubén, de acuerdo) Descartado: calibrar cada bloque por separado, con tan pocas muertes en riesgo bajo era sobre todo ruido (unos 5 años en vez de 3 a 4); solo lo que falta, con el PDF completo parecería perfecto, aunque Rubén lo reconsideró al ver aquel ruido; variación de un día a otro, exige buscar una tabla publicada por analito; bootstrap del modelo, mide poco (lo seguro que está de sus pesos) y cuesta horas de entrenamiento.
- Si el ± llega a 5 años, debajo de la frase de la diferencia sale un aviso en gris, como el rojo de la edad pero más suave, que pide tomarlo con más precaución de lo normal. El texto no culpa solo a los datos que faltan, porque en jóvenes de riesgo bajo el ± ya es ancho con la analítica completa. (Rubén, de acuerdo; el texto exacto, con la revisión final de textos)
- El ± se muestra en años enteros, con el ,5 hacia arriba, y no se muestra si redondea a 0. (Rubén, de acuerdo) Tampoco junto a "menos de 18" o "más de 90": no hay número al que sumárselo. (Claude, autónomo)
- Edad real fuera de 18-79: la diferencia se calcula como si tuviera 18 o 79 y se suma a la edad real.
- Edad biológica fuera de 18-79: por debajo de 18, "menos de 18"; de 79 a 90, el número con la nota "orientativo"; por encima de 90, "más de 90". (Rubén, de acuerdo)
- Una tabla fija, igual para todos, con los grupos que la gente entiende: vitaminas y minerales, azúcar, glóbulos rojos, defensas (con un escudo), hígado, riñón, peso (IMC) y otros (HDL, LDH y lo que no explica ningún grupo). Cada fila dice cuántos años suma o resta frente a una persona típica de su edad y sexo, sin ± ni signo: la columna y el color ya lo dicen. Se parte en dos columnas, "te quitan años" y "te suman años", cada una ordenada por valor absoluto de mayor a menor; los grupos sin datos van en una línea aparte. (Rubén, de acuerdo) Descartado: los mejores y peores parámetros de cada persona, la tabla cambiaría de un usuario a otro; porcentajes por órgano, escala inventada
- Aviso de que no es consejo médico ni diagnóstico. No se dan recomendaciones (suplementos, tratamientos…), solo observaciones de los datos.
- Aviso asimétrico: salir por encima es señal para consultar, pero salir bien no significa estar sano. De momento no se muestra: la franja amarilla ya avisa y Rubén no quiere más mensajes. (Rubén, en desacuerdo)

Cuando se hace el cuestionario:
- Una segunda tabla igual con sus hábitos: tabaco, ejercicio, horas sentado y horas de sueño.

Diseño del resultado:
- La pestaña del navegador se llama "BioAge".
- Logo: una hoja en trazo esmeralda dentro de un círculo verde apagado, con una red de IA en lugar de nervios. Va en la marca de agua de la imagen y, simplificado para que se lea a 16 px, en el icono de la pestaña. (Rubén, de acuerdo) Descartado: ADN como red neuronal, célula reloj, anillos, reloj de arena.
- El resultado va dentro de un recuadro de bordes redondeados. La edad biológica en grande, sin título encima, con el ± en pequeño a su lado (no debajo), y debajo la frase "X años menos/más que tu edad real", sin repetir la edad. (Rubén, de acuerdo) Descartado: medidor en arco, no aporta; tarjetas y pastillas.
- Al final, compartir (en el móvil) y descargar el resultado como imagen, sin texto adjunto. La imagen enseña el recuadro entero con margen alrededor y las células por detrás y por los lados, y el logo con "BioAge" abajo a la derecha, fuera del recuadro, como marca de agua; se crea en el navegador, sin subir nada. (Rubén, de acuerdo) Descartado: "calcular otra vez"; texto pequeño de aviso bajo las tablas, ya lo hace la franja amarilla.
- Iconos anatómicos de Healthicons para hígado y riñón; gota para glóbulos rojos, escudo para defensas, diamante para vitaminas y minerales, un montoncito de azúcar, "kg" para el peso y tres puntos para otros.

Cuando la edad biológica está 10 o más años por encima de la real (haya o no cuestionario):
- [pendiente: si se recomienda comentarla con el médico y con qué frase; Rubén lo consulta con el profesor. De momento, sin mensaje.]

## Experiencia de uso
- La UX tiene prioridad sobre afinar el modelo: el modelo es fácil de iterar, y una UX mal planteada obliga a rehacerla.
- Usable por cualquier persona: flujo corto, lenguaje claro sin jerga, responsive y pensado para móvil.
- Estados de carga y errores de parseo comprensibles y accionables: qué ha fallado y qué puede hacer el usuario.
- Portada: título, "De 16 a 90 años" como subtítulo, los dos botones, la línea "Sube un PDF con tu analítica y calcula tu edad" con una llamada ¹ (dice qué hacer antes de que se abra el selector de archivos) y, en una franja inferior muy visible, el aviso de que no es consejo médico. La llamada baja a la letra pequeña, debajo de la franja, como en las webs de bancos, en tres preguntas que cualquiera entienda: qué hago con tus datos (no se guardan ni se envían, enlace al repositorio y "IMPORTANTE: al subir el PDF con tu analítica aceptas que lo use para esto"), cómo calculo la edad biológica y por qué no es un diagnóstico. (Rubén, de acuerdo) Descartado: solo la frase "no guardamos nada", el RGPD pide más; pop-up.
- La app habla en primera persona del singular, como el autor ("No puedo leer este PDF"). (Rubén, de acuerdo)
- La app abre siempre arriba, en la portada, aunque se recargue.
- La franja está en la portada y en el resultado, no en el cuestionario ni en la carga: si está siempre, pasa a ser parte del fondo y deja de leerse. (Rubén, de acuerdo)
- Estética "microscopio": oscuro, verde profundo con acentos esmeralda, titulares en Fraunces y el aviso en amarillo de peligro con el símbolo de riesgo biológico. (Rubén, de acuerdo) Descartado: neón con red de partículas, no evoca biología; mezclar la hélice de ADN con las células en el fondo, recargado.
- Fondo animado en todas las pantallas: células flotando como bajo la lente. Manda la fluidez sobre la estética: si no va fluido, imagen fija.
- Al tocar el fondo salen destellos y nacen o explotan células; al pulsar botones, no.
- Pantalla de carga al leer el PDF ("Leyendo tu analítica"), que dura lo que tarde la lectura y va sin porcentaje, y antes del resultado ("Calculando tu edad"), de 1 segundo: una hélice de ADN verde que se construye de arriba abajo y un porcentaje que sube rápido de 0 a 100. (Rubén, de acuerdo) Descartado: frases que cambian y lista de pasos; hélice bicolor, cansa la vista.
- En cualquier pareja de botones, el destacado va a la derecha, más cerca del pulgar: en la portada, "solo analítica" a la izquierda y "analítica y hábitos" a la derecha; en el resultado, "descargar" y "compartir"; en el valor imposible, "es correcto" y "corregirlo". (Rubén, de acuerdo)

## Restricciones
- **Privacidad:** son datos de salud (categoría especial en el RGPD).
  - Minimizar el tratamiento y no almacenar nada: la app procesa todo en memoria y lo descarta.
  - No se usan etnia ni datos socioeconómicos.
  - Informar al usuario de forma clara de qué se hace con sus datos.
- **Formato de entrada:** PDF digital.
- **Plazos:** Entrega 04 (solución UX), el 29 de noviembre de 2026. Entrega final, el 9 de diciembre de 2026 (fecha del enunciado de la Entrega 04; ante la duda, la más corta).
