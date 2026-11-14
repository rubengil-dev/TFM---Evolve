# Metadatos

## Qué contiene
El índice de los archivos de `.claude/`, cuáles se cargan siempre y las reglas generales para trabajar con ellos.

Lo que no encaje en esta descripción no va aquí.

## Actualización
Cuando se añade, se quita o se redefine un archivo de `.claude/`: se actualiza su fila de la tabla y, si cambia qué se carga siempre, la lista de archivos que se cargan solos.


# Contenido

## Al abrir un chat
Los archivos marcados "Siempre" en la tabla se cargan solos (están importados al final de este archivo).
1. Si el primer mensaje no pide nada concreto, empieza por la fase marcada como activa (`[*]`) en `PLAN.md`.
2. Si pide otra cosa, recuérdame en una línea qué tocaba según `PLAN.md` y `ESTADO.md` y sigue con mi petición. Pregunta antes de seguir solo si choca con algo: depende de un bloqueo, contradice una decisión de `REQUISITOS.md` o `TECNICO.md`, o cambia el orden del `PLAN.md`.
3. Si el contador de revisiones de `ESTADO.md` indica que toca una revisión integral, propónmela (ver `PROTOCOLOS.md`).

## El equipo
Cada archivo tiene una sola tarea. Pregúntale a cada uno lo que le toca.

| Archivo | Para qué | Cuándo leerlo |
|---|---|---|
| `CLAUDE.md` | Presenta al equipo y fija las reglas generales | Siempre (se carga solo) |
| `ABOUTME.md` | Quién soy, qué sé y cómo se trabaja conmigo | Siempre (se importa) |
| `CONTEXTO.md` | Por qué existe el proyecto | Siempre (se importa) |
| `REQUISITOS.md` | Qué debe hacer el proyecto, con las decisiones de producto tomadas | Siempre (se importa) |
| `PLAN.md` | Qué hay que construir, en qué orden y en qué fase estamos | Siempre (se importa) |
| `ESTADO.md` | Qué bloquea (incluidas las decisiones pendientes que bloquean), qué me toca a mí y cuándo toca revisión integral | Siempre (se importa) |
| `ESTRUCTURA.md` | Qué hay en cada carpeta y archivo | Siempre (se importa) |
| `PROTOCOLOS.md` | Cómo se ejecuta cada procedimiento: cierre de sesión, pruebas, revisión integral… | Siempre (se importa) y, además, justo antes de ejecutar uno |
| `TECNICO.md` | Con qué y dónde está construido, con las decisiones técnicas tomadas | Antes de tocar código, configuración o estructura |
| `ESTILO.md` | Cómo se escribe, se organiza y se versiona: convenciones y mis gustos | Antes de tocar código, configuración o estructura |
| `FUTURO.md` | Ideas buenas que quedan fuera del MVP | Al planificar una nueva versión o al ordenar `NOTAS.md` |
| `NOTAS.md` | Bandeja de ideas sin clasificar y de decisiones pendientes que no bloquean | Al empezar una fase y en la revisión integral |

## Reglas para trabajar con los archivos
- Cada dato vive en un solo archivo. Si encaja en dos, va al más específico y el otro no lo repite.
- Cada archivo empieza con sus Metadatos. Lo que no encaja en su "Qué contiene" no va en ese archivo; si no encaja en ninguno, propón crear uno nuevo y, si lo apruebo, añádelo a la tabla.
- Antes de editar un archivo, léelo y sigue su apartado "Actualización", aunque ya lo hayas leído antes en la sesión. Lo mismo con un protocolo justo antes de ejecutarlo.
- No se guarda lo que se saca rápido del código, de la configuración o de git.
- Si un archivo y el código discrepan, dime cuál es la discrepancia: yo decido cuál manda.
- Lo que falte al redactar un archivo se marca `[pendiente: qué falta]`. Si lo que vamos a hacer depende de un pendiente, pregúntamelo antes de seguir.

## Archivos que se cargan solos
@ABOUTME.md
@CONTEXTO.md
@REQUISITOS.md
@PLAN.md
@ESTADO.md
@ESTRUCTURA.md
@PROTOCOLOS.md
