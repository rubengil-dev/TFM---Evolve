# TFM: calculadora web de edad biológica

Al empezar cada sesión, lee enteros `CONTEXTO.md` y `ESTADO.md`. Si ESTADO tiene una sección "PRÓXIMA SESIÓN", se empieza por ahí.

## Los archivos
- `CONTEXTO.md`: qué es el TFM, el producto, el enfoque del modelo y las decisiones ya tomadas (con su motivo). Es estable: no se toca salvo que yo lo pida.
- `ESTADO.md`: foto del punto actual, con lo hecho, lo que falla, lo que queda y las decisiones abiertas. No es un historial: si algo se prueba, falla y se arregla, solo queda el resultado final.
- `Docs/Entregas/`: entregas del máster, las escribo yo. No las edites salvo que te lo pida.
- Cuando una decisión abierta se cierre, se pasa de ESTADO a CONTEXTO (con su motivo), pidiéndome OK antes.

## Proyecto
- TFM del máster de Data Science e IA de EVOLVE. Se evalúa el producto completo: modelo + UX/front + despliegue con URL pública.
- Repo: https://github.com/rubengil-dev/TFM---Evolve (rama `main`).
- Stack sin decidir (ver ESTADO). Cuando se decida, se apunta aquí: versiones, cómo instalar el entorno y comandos para ejecutar, testear y desplegar.
- Idioma: hablamos en español. Código, variables y comentarios en inglés. Textos de la interfaz: por decidir.

## Perfil y cómo explicarme las cosas
- Soy bioquímico: la parte biomédica la domino, no hace falta explicármela. No tengo formación en ingeniería ni en front.
- Las decisiones técnicas (arquitectura, librerías, front, backend, hosting) me las explicas en lenguaje llano, con opciones y una recomendación. Si hace falta, primero me haces preguntas.
- Avísame cuando una decisión técnica perjudique la UX, el alcance del TFM o los límites de los planes gratuitos de hosting.
- Prioridad: MVP end-to-end funcional y desplegado antes de pulir cada pieza.

## Datos y privacidad
- Los datos de NHANES se descargan con script a `data/` (ignorada por `.gitignore`). Lo que sí se sube es el código que los descarga y procesa.
- Analíticas reales (mías o de otras personas) van solo a `private/` (ignorada): nunca se suben al repo ni se pegan en ESTADO/CONTEXTO. Para tests y ejemplos, usa analíticas sintéticas o anonimizadas.
- La app no guarda datos de usuarios: todo se procesa en memoria y se descarta.

## Forma de trabajo
- Primero hablamos el tema hasta estar de acuerdo. Después lo implementas entero del tirón y al final resumes en pocas líneas qué has hecho, como un dev junior a su jefe de proyecto.
- Análisis exploratorio y modelado: en notebooks, pero la lógica reutilizable (carga de datos, features, modelo, parser) va a módulos de código, no se queda solo en el notebook.
- Resultados del modelo (C-index, calibración, comparativas por subconjuntos de variables) siempre con la semilla y la partición indicadas, para que sean reproducibles en la memoria del TFM.
- Pruebas: las ejecutas tú (tests, scripts, servidor local + peticiones). Lo visual (pantallas, sensación de uso en móvil) no lo puedes juzgar bien: déjame en ESTADO una lista corta "Pendiente de probar yo" y lo pruebo.
- Cierre de sesión: cuando diga "cerramos", "actualiza", "hemos terminado por hoy" o algo similar:
  1. Haz un test rápido solo de lo nuevo, no de todo el proyecto, siguiendo el punto anterior.
  2. Actualiza `ESTADO.md` y dime resumidamente qué has cambiado en él para que dé el OK.
  3. Si todo lo anterior ha ido bien, propón el commit (y el merge, si hay rama) y espera mi OK.
  4. Si te doy el OK, haz el commit, (merge si aplica) y el push a GitHub.

## Git
- Cambios sencillos sin riesgo de romper nada: en la rama actual.
- Features nuevas, corrección de bugs o cualquier cosa con riesgo: en una rama nueva, que se fusiona a `main` al cerrar la sesión si todo va bien.
- Commits y merges solo con mi OK. Mensajes de commit breves.
