# Qué hay en este archivo y cómo usarlo
- **Contiene:** las decisiones técnicas y metodológicas ya tomadas, agrupadas por fase. Cada una es una pregunta con la decisión y su porqué.
- **No contiene:** decisiones abiertas ni decisiones de producto.
- **Se actualiza:** cuando se cierra una decisión abierta o se cambia una ya tomada. Para cambiar una, antes hay que hablarlo.

## Entorno

### ¿Qué versión de Python y qué gestión de dependencias?
- **Decisión:** Python 3.11 en un entorno virtual, con las dependencias congeladas con `pip freeze`.
- **Por qué:** es lo estándar, lo reproduce cualquiera y las plataformas de hosting leen el archivo de requisitos directamente. La 3.11 tiene soporte hasta 2027 y todas las librerías la soportan; la 3.14 es demasiado nueva.

### ¿Cómo se organizan los datos?
- **Decisión:** en capas: Bronze (tal como llega de la fuente, nunca se modifica), Silver (unido, limpio y armonizado) y Gold (tabla final que consume el modelo).
- **Por qué:** cada paso se puede rehacer sin volver a descargar, y siempre se puede volver al dato original.

### ¿De qué capa leen el modelo y la app?
- **Decisión:** solo de Gold. Toda variable que necesiten el modelo o la app (también las parejas para el relleno) tiene que estar en Gold.
- **Por qué:** Silver es una capa intermedia del pipeline. Con un único punto de lectura se sabe exactamente qué datos usan, y Silver se puede cambiar sin romperlos. Lo pide el profesor.

## Datos

### ¿Qué NHANES?
- **Decisión:** NHANES continuo 1999-2018. NHANES III se descarta.
- **Por qué:** NHANES III tiene métodos de laboratorio y formato distintos, y 20 años de seguimiento bastan.

### ¿Qué mortalidad?
- **Decisión:** la pública, con seguimiento hasta 2019. El seguimiento corto de los últimos ciclos se trata como censura.
- **Por qué:** la versión hasta 2022 es de acceso restringido.

### ¿Descargar todo NHANES o una lista cerrada?
- **Decisión:** una lista cerrada de ficheros, verificada contra el catálogo oficial de la CDC.
- **Por qué:** el producto solo usa la analítica y pocos datos más; descargar todo era lento e innecesario.

### ¿Qué ficheros se descartan?
- **Decisión:** ferritina, PSA, TSH, B12/folato/homocisteína/ApoB, fuerza de prensión, bioimpedancia, acelerómetro y salud general autovalorada.
- **Por qué:** ferritina solo en mujeres de 12-49 años y niños; PSA solo en varones ≥ 40 y en pocos ciclos; TSH en pocos ciclos; B12 y similares con cobertura irregular; prensión, bioimpedancia y acelerómetro en pocos ciclos o no medibles en casa; la salud autovalorada es subjetiva.

## Preparación

### ¿Qué población entra?
- **Decisión:** adultos de 18 a 79 años elegibles para mortalidad. Fuera las personas sin examen físico, las embarazadas y las que no tienen ningún valor de laboratorio.
- **Por qué:** NHANES agrupa las edades superiores a 80; el embarazo altera la analítica; sin laboratorio la persona no se parece a ningún usuario de la app.

### ¿Cuándo se renombran las columnas entre ciclos?
- **Decisión:** los alias de laboratorio se renombran antes de apilar los ciclos. Los cuestionarios no se renombran a ciegas.
- **Por qué:** apilar sin renombrar crea columnas medio vacías; en los cuestionarios, el mismo nombre puede ser una pregunta distinta según el ciclo.

### ¿Se corrigen los cambios de método de laboratorio?
- **Decisión:** sí, con las ecuaciones oficiales de la CDC: creatinina sérica en 1999-2000 y 2005-2006; 13 analitos de la bioquímica y la PCR ultrasensible en 2017-2018, llevados a la escala anterior; insulina, con cinco métodos encadenados; y creatinina en orina antes de 2007, llevada a la escala de 2007 en adelante.
- **Por qué:** sin corregir, el modelo confundiría el cambio de analizador con un cambio real de la población.

### ¿A qué escala se lleva la insulina?
- **Decisión:** a la de 2013-2018 (Tosoh), encadenando las ecuaciones de cada cambio de método: Pharmacia → Tosoh → Mercodia → Roche → Tosoh.
- **Por qué:** es el método más reciente y cubre tres ciclos.

### ¿Qué pasa con los valores que la corrección deja por debajo del límite de detección?
- **Decisión:** en la PCR ultrasensible de 2017-2018 no bajan de 0,08 mg/L, el valor que la escala de destino (2015-2016) pone por debajo de su límite de detección.
- **Por qué:** la ecuación de la CDC da valores negativos por debajo de unos 0,3 mg/L.

### ¿Cómo se tratan los códigos "no sabe / no contesta"?
- **Decisión:** con una lista de códigos por variable.
- **Por qué:** una lista global (7, 9…) borraría respuestas numéricas reales.

### ¿Qué se hace con las preguntas que el cuestionario se salta?
- **Decisión:** se rellenan con la respuesta implícita: quien nunca ha fumado o nunca ha bebido no ve las preguntas siguientes y queda como "never" (y 0 bebidas por día).
- **Por qué:** el hueco no es un dato que falta, es una respuesta que ya se conoce; dejarlo vacío haría perder a todos los no fumadores y no bebedores.

### ¿Cómo se completa el tabaco de los de 18-19 años hasta 2012?
- **Decisión:** con las preguntas juveniles de NHANES. En 2011-2012, con los cigarrillos fumados en la vida (100 o más: fumador actual si fumó en el último mes; si no, exfumador). Hasta 2010, que no tiene esa pregunta: nunca lo probó o nunca fumó un cigarrillo entero → nunca; fumó 10 días o más del último mes → fumador actual; menos → nunca.
- **Por qué:** el cuestionario de adultos solo se pasó a mayores de 20. En 2011-2012, que tiene las dos preguntas, la regla de los 10 días coincide en el 97% con la definición de adultos (100 cigarrillos). No detecta exfumadores, que a esa edad son muy pocos.

### ¿Se completa el alcohol de los de 18-19 años?
- **Decisión:** no. Queda sin dato en 1999-2010.
- **Por qué:** solo hay cuestionario juvenil en 2009-2010 (278 personas, 2 defunciones), así que 1999-2008 seguiría vacío; y no encaja con el de adultos: pregunta por los últimos 30 días en vez del último año y no recoge bebidas por día.

### ¿En qué unidades?
- **Decisión:** las del laboratorio español: urea (BUN × 2,14), PCR en mg/L (los dos ensayos en una columna) y cociente albúmina/creatinina en orina en mg/g.
- **Por qué:** el usuario trae una analítica española, y así no hay que convertir al recibirla.

### ¿Glucosa, triglicéridos y LDL con o sin ayuno?
- **Decisión:** glucosa en suero en todas las personas; triglicéridos solo con ayuno ≥ 8 h; LDL fuera.
- **Por qué:** el ayuno apenas cambia la mediana de la glucosa, pero sí los triglicéridos (y la analítica española es en ayunas). El LDL de NHANES es calculado (Friedewald), solo en ayunas, y sale protector por causalidad inversa.

### ¿Hemograma en porcentajes o en recuentos?
- **Decisión:** recuentos absolutos.
- **Por qué:** los porcentajes dependen unos de otros.

### ¿Qué se hace con las variables muy correlacionadas y las combinaciones lineales?
- **Decisión:** se guardan todas en Gold, y en la fase de modelo se elige cuál entra de cada pareja (p. ej. hemoglobina/hematocrito, HOMA-IR/insulina) y qué juego de cada combinación lineal (colesterol total/HDL/no-HDL, proteínas/albúmina/globulinas, sistólica/diastólica/presión de pulso).
- **Por qué:** en el modelo serían redundantes (en Cox, las tres de una combinación lineal no pueden entrar a la vez), y cuál conviene depende del modelo. Las que no entren siguen sirviendo a la app para estimar la que falte cuando el usuario solo trae su pareja.

### ¿Qué se hace en Gold y qué en el preprocesado del modelo?
- **Decisión:** en Gold solo fórmulas fijas (features derivadas). Rellenar huecos, recortar extremos, escalar y codificar van al preprocesado, ajustado solo con train.
- **Por qué:** hacerlo con todo el dataset filtraría información del test.

### ¿Dónde viven las fórmulas de las features derivadas?
- **Decisión:** en un único módulo compartido entre el pipeline y la futura app.
- **Por qué:** el modelo y la app tienen que calcularlas exactamente igual.

### ¿Seguimiento de 0 meses?
- **Decisión:** se pasa a 0,1 meses.
- **Por qué:** algunos modelos de supervivencia (los paramétricos) no aceptan tiempos de 0.

### ¿Por qué se descartan DXA y VO2 max?
- **Decisión:** no pasan a Silver clean, así que quedan fuera del modelo y de la app. Se siguen descargando y llegan a Silver raw.
- **Por qué:** el usuario no los conoce.

## Modelo

### ¿Modelo clásico o deep learning?
- **Decisión:** primero un modelo clásico como baseline; deep learning solo si mejora de forma justificable.
- **Por qué:** un modelo clásico es más fácil de explicar y de desplegar en un plan gratuito; la complejidad extra solo compensa si mejora claramente.

### ¿Cómo se evalúa?
- **Decisión:** con métricas de supervivencia (C-index y calibración) y con distintos subconjuntos de variables.
- **Por qué:** son las métricas estándar de supervivencia, y los subconjuntos dicen cuánto se pierde según lo que falte en la analítica.

## App

### ¿Qué hacer si el usuario trae la pareja de una variable del modelo pero no la variable?
- **Decisión:** estimarla con una ecuación ajustada sobre Gold (p. ej. hemoglobina a partir del hematocrito), solo para parejas con correlación alta.
- **Por qué:** así se pierden menos variables sin pedir nada más al usuario.

### ¿Se usa el filtrado glomerular que traen las analíticas?
- **Decisión:** no como variable del modelo, pero el parser puede usarlo para recuperar la creatinina si falta.
- **Por qué:** es redundante con creatinina, edad y sexo.

### ¿Cómo se pregunta el alcohol?
- **Decisión:** frecuencia y, solo si no marca "nunca", bebidas por día.
- **Por qué:** es como lo pregunta NHANES, y la segunda pregunta no tiene sentido si nunca bebe.
