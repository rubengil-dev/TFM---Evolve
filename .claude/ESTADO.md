# Estado

## PRÓXIMA SESIÓN
Empezar la fase de modelo, en este orden:
1. Estrategia para analíticas incompletas.
2. Arquitectura: Cox primero como baseline.
3. Elegir el juego de variables entre las correlacionadas y las combinaciones lineales.

## CONSTRUIDO
- Entrega 01 (ideas de producto) y Entrega 02 (datos y preparación): entregadas.
- Pipeline de datos completo y reproducible con un único comando, de la descarga a Gold: Bronze → Silver raw → Silver clean → Gold.
- Notebook de exploración de Silver raw y notebook de la muestra de Gold para la Entrega 02.
- Gold contiene todas las candidatas, sin rellenar, recortar, escalar ni codificar (eso es el preprocesado del modelo). Incluye a propósito las combinaciones lineales (colesterol total/HDL/no-HDL; proteínas/albúmina/globulinas; sistólica/diastólica/presión de pulso) para elegir el juego en la fase de modelo. Silver clean conserva las parejas que no entran a Gold, para las ecuaciones de relleno de la app.

## PENDIENTE

### Plazos
- Entrega final: diciembre de 2026, día por confirmar.

### Tareas
- Conseguir analíticas de ejemplo de distintos laboratorios españoles para probar el parser (tengo PDFs propios para la carpeta privada).

### Decisiones abiertas
Modelo:
- Estrategia para analíticas incompletas: imputación, un modelo por subconjunto de variables o modelos que toleren valores ausentes. Ojo: en NHANES los huecos van por ciclo (PCR, sueño, dieta), pero en la app dependen de cada usuario. Un modelo que aprenda de los nulos podría confundir "falta el dato" con "es de tal época".
- Arquitectura: Cox, modelos de árboles para supervivencia, DL…
- Variables concretas: qué variable entra de cada pareja muy correlacionada y qué juego de cada combinación lineal (en Cox no pueden entrar las tres).
- Mínimo viable de variables: con qué datos faltantes se deja de calcular.
- Hábitos: uno o dos modelos (solo analítica / analítica + hábitos) o uno que tolere nulos, según el C-index. En la app, idea no cerrada: dos pestañas, "simple" por defecto (solo analítica) y "avanzada" (cuestionario de botones + analítica). Descartado "primero simple y luego afinar": son dos procesos.

Resultado:
- Cómo calcular y mostrar el margen ± X años.
- Definición de "mejor/peor parámetro". Propuesta para el MVP: cuánto empuja cada parámetro la edad hacia arriba o hacia abajo frente a una persona media de la misma edad y sexo. La versión "distancia al óptimo" requiere un modelo no lineal.
- Cuántos parámetros mejores/peores se muestran (3, 5, configurable…).
- Umbral de años por encima para remitir al médico, según el error del modelo y la literatura.

App:
- Diseño del parser de PDF y de la normalización de nombres y unidades.
- Stack de front y backend, y estructura de la app.
- Hosting.
- Separar las dependencias de la app y las del análisis en el despliegue (ahora incluyen Jupyter).

Preguntas al profesor:
- ¿Los notebooks deben quedarse en el repo final?
- ¿Hace falta una analítica de ejemplo (sintética) para probar la app sin PDF propio?

### Notas para la app
- Relleno desde la pareja: si el usuario trae la variable "pareja" y no la que usa el modelo (p. ej. hematocrito sin hemoglobina), estimarla con una ecuación sacada de NHANES. Solo para parejas con correlación alta.
- El filtrado glomerular (CKD-EPI) suele venir en las analíticas españolas. No es variable del modelo (es redundante con creatinina, edad y sexo), pero el parser puede usarlo para recuperar la creatinina si falta.
- Triglicéridos: el modelo se entrena con valores en ayunas, igual que la analítica española. Mejora futura: usar también los valores sin ayuno corrigiéndolos.

### Problemas conocidos
Limitaciones de los datos a tener en cuenta en el modelo:
- Fosfatasa alcalina y LDH más altas en 1999-2000, sin ecuación oficial de corrección. Urea algo más alta en 2017-2018 incluso corregida.
- Actividad física con salto en 2007 por el cambio de cuestionario.
- Alcohol sin dato para 18-19 años en 1999-2006 (cuestionario solo para mayores de 20).
- Variables solo en parte de la muestra: subgrupo en ayunas (triglicéridos, insulina), CPK solo en 2011-2018 y PCR sin 2011-2014.
- Últimos ciclos con pocas defunciones por su seguimiento corto.
