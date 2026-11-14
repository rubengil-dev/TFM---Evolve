# Metadatos

## Qué contiene
Cómo se ejecuta cada procedimiento que repetimos: pruebas, edición de archivos de `.claude/`, anotación de decisiones, cierre de implementación, cierre de sesión y revisión integral. Es igual en todos los proyectos.

Lo que no encaje en esta descripción no va aquí.

## Actualización
Cuando cambio un procedimiento o añado uno nuevo. Si añado o quito un protocolo, actualiza también la fila de `PROTOCOLOS.md` en `CLAUDE.md`. Si cambio algo, recuérdame actualizarlo también en la skill `/nuevo-proyecto` (`fijos/PROTOCOLOS.md`).


# Contenido

## Pruebas
- Las ejecutas tú, en mi máquina y en el entorno del proyecto: tests, scripts, servidor local y peticiones.
- Dime qué comandos has ejecutado y qué ha salido, de forma breve.
- Lo visual no lo puedes juzgar bien: pídeme que lo pruebe en ese momento. Solo si te digo que ahora no, lo apuntas en `ESTADO.md` como algo que me toca a mí.

## Edición de archivos de `.claude/`
1. Antes de editar un archivo, léelo y sigue su apartado "Actualización".
2. Dime qué archivos has tocado.

## Cómo anotar decisiones relevantes
Solo es una decisión lo no obvio: una elección real entre alternativas, con coste de cambiarla. Lo trivial no se registra, y lo que simplemente quiero que haga el proyecto no es una decisión ni lleva etiqueta.

Cada decisión de `REQUISITOS.md` o `TECNICO.md` ocupa una línea: qué, el porqué en una frase y, entre paréntesis, cómo se decidió:

- **(Rubén, de acuerdo):** decidí yo y estabas de acuerdo.
- **(Rubén, en desacuerdo):** decidí yo contra tu consejo. No se vuelve a plantear salvo que yo lo pida.
- **(Claude, a petición):** decidiste tú porque te lo pedí.
- **(Claude, autónomo):** decidiste tú sin preguntarme.

Si hubo alternativas descartadas, se añade en la misma línea: `Descartado: X, motivo corto.` Solo cuando aporta: si decidí contra tu consejo, o si la alternativa es tentadora y alguien la volvería a proponer.

## Cierre de implementación
Cuando terminemos una implementación, por ejemplo un punto del checklist:
1. Haz un test rápido solo de lo nuevo (ver "Pruebas").
2. Actualiza los archivos de `.claude/` que toquen, como mínimo las casillas del `PLAN.md` y `ESTRUCTURA.md` (ver "Edición de archivos de `.claude/`").
3. Con mi OK, haz commit (ver `ESTILO.md`).

## Cierre de sesión
Cuando diga "cerrar", "cerramos", "hemos terminado por hoy" o similar:
1. Haz push.
2. Suma una sesión al contador de revisiones de `ESTADO.md`.
3. Si la rama de feature está acabada y todo funciona perfectamente: merge a la rama de su fase (o a `main`), según `ESTILO.md`, y push.
4. Si además la fase está terminada y todo funciona perfectamente: merge de la rama de la fase a `main` y push.

## Revisión integral
Cada 2 o 3 sesiones, según cuánto código hayamos avanzado. Lo nuevo puede funcionar y haberse cargado algo que no hemos mirado, así que la revisión mira todo el proyecto, no solo lo último.
1. Ejecuta todos los tests y prueba de punta a punta lo que se pueda.
2. Compara el código con los archivos de `.claude/` y dime cada discrepancia.
3. Ordena `NOTAS.md`: cada nota va a `PLAN.md`, `REQUISITOS.md`, `TECNICO.md` o `FUTURO.md`, o se descarta.
4. Propón las mejoras que salgan como casillas del `PLAN.md`.
5. Pon a cero el contador de revisiones de `ESTADO.md`.
6. Recuérdame hacer la copia a la NAS.
