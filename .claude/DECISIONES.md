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
- **Decisión:** las del laboratorio español: urea (BUN × 2,14), PCR en mg/L (los dos ensayos en una columna), cociente albúmina/creatinina en orina en mg/g y vitamina D en ng/mL (nmol/L ÷ 2,5).
- **Por qué:** el usuario trae una analítica española, y así no hay que convertir al recibirla.

### ¿Qué se hace con los valores imposibles?
- **Decisión:** en Silver clean se vacían los valores fuera de un rango posible por variable. El criterio es el de un adulto que va por su pie a una analítica programada: fuera del rango queda lo que solo se ve en una emergencia vital o es un artefacto (p. ej. glucosa > 600, sodio < 100, potasio > 6,5 por muestra hemolizada, diastólica < 30). Los extremos de una enfermedad conocida se quedan (glucosa de 300 en un diabético, creatinina de 15 en diálisis, hierro muy bajo en una ferropenia). La tabla guarda también el rango normal y el porqué de cada límite.
- **Por qué:** son errores o casos que no representan al usuario de la app, no outliers. Se vacían antes de Gold para que no entren en las features derivadas, y no es leakage porque es una regla fija. Los outliers reales se tratan en el preprocesado.

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

### ¿Cómo se valida Gold?
- **Decisión:** antes de guardar, en un módulo aparte que llama el paso de Gold. Bloquean (Gold no se guarda): columnas y tipos, tamaño mínimo (personas en total y por ciclo, y defunciones), cobertura mínima (más baja para las variables medidas solo en parte de la muestra), obligatorias sin huecos y sin personas repetidas, desenlace, población, respuestas permitidas y rangos posibles. Solo avisan: las coherencias entre variables (HDL < colesterol total, albúmina < proteínas, diastólica < sistólica, IMC con peso y talla).
- **Por qué:** una Gold rota o incompleta no avisa por sí sola y falsearía el modelo. Los mínimos de tamaño cuentan las defunciones porque el modelo de supervivencia aprende de ellas, no de las filas.

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

### ¿Qué tipo de problema es?
- **Decisión:** supervivencia (tiempo hasta la muerte). El modelo estima el riesgo de morir y ese riesgo se traduce a edad biológica, que es lo que recibe el front.
- **Por qué:** no existe una etiqueta de edad biológica real; la mortalidad sí se observa.

### ¿A qué horizonte?
- **Decisión:** 10 años. Fija a qué plazo se traduce el riesgo a edad y a qué plazo se evalúan el C-index y la calibración. Se entrena con todo el seguimiento, censurados incluidos.
- **Por qué:** es el horizonte de PhenoAge, y así la comparación es directa. A 5 años hay pocas muertes y en jóvenes el riesgo es casi cero; a 15, solo 3 de los 10 ciclos tienen seguimiento completo.

### ¿Cómo se separan los datos?
- **Decisión:** 80/20 aleatorio, estratificado por ciclo y muerte. El test se mira una sola vez, al final; la comparación de modelos y el preprocesado se hacen con validación cruzada de 5 bloques dentro de train.
- **Por qué:** la estratificación reparte por igual los huecos por ciclo y las muertes. Separar por ciclos dejaría un test con muy pocas muertes (los ciclos recientes tienen poco seguimiento).

### ¿Qué columnas no pueden ser predictores?
- **Decisión:** las de contexto y el desenlace: `seqn`, `cycle`, `weight_exam`, `follow_up_months` y `death`.
- **Por qué:** no existen para el usuario de la app. `cycle` además filtraría: los ciclos recientes tienen menos muertes por su seguimiento más corto, no por estar más sanos.

### ¿Cuál es el baseline?
- **Decisión:** un Cox solo con edad y sexo, que equivale a decir que la edad biológica es la cronológica. Lo tiene que superar el Cox con biomarcadores; PhenoAge es la referencia externa.
- **Por qué:** es el baseline sencillo, interpretable y realista: si la analítica no mejora la predicción de la mortalidad frente a la edad, la edad biológica no aporta nada.

### ¿Modelo clásico o deep learning?
- **Decisión:** primero un modelo clásico como baseline; deep learning solo si mejora de forma justificable.
- **Por qué:** un modelo clásico es más fácil de explicar y de desplegar en un plan gratuito; la complejidad extra solo compensa si mejora claramente.

### ¿Cómo se evalúa?
- **Decisión:** a 10 años, fuera de entrenamiento y con un resumen por nivel: C-index de Uno global y dentro del mismo grupo de edad, C-index por sexo, calibración por deciles de riesgo con su peor infraestimación, C-index en entrenamiento y tiempo. Un nivel mejora de verdad si el intervalo de confianza por bootstrap de la diferencia de C-index no incluye el 0. PhenoAge se mide una vez, al final, contra el mejor modelo de cada nivel y con las personas que tienen todas sus variables, porque usa variables de Extras.
- **Por qué:** son las métricas estándar de supervivencia. La edad sola ya ordena muy bien, así que el C-index dentro del mismo grupo de edad es el que dice si la analítica aporta algo. La infraestimación es el error peor. El C-index en entrenamiento delata el sobreajuste.

### ¿Cuántos modelos y cómo se comparan?
- **Decisión:** una escalera de niveles. Nivel 0: el baseline (Cox con edad y sexo). Nivel 1: Base (edad, sexo y el bloque principal). Nivel 2: Base + Extras. Nivel 3: Base + Cuestionario. Nivel 4, si es pertinente: los dos juntos. Cada nivel se compara con el ganador de Base, y cada salto se explica por lo que aporta.
- **Por qué:** cada comparación responde a una pregunta del producto: cuánto aporta la analítica frente a la edad, cuánto la analítica ampliada y cuánto los hábitos.

### ¿Qué algoritmos compiten?
- **Decisión:** en los niveles 1 a 3, los mismos cuatro y en igualdad: Cox, Cox elastic net, random survival forest y gradient boosting (XGBoost o similar). Gana el mejor de cada nivel. El nivel 4 usa directamente Cox simple, sin competición.
- **Por qué:** el elastic net selecciona variables por sí solo; los árboles captan relaciones no lineales. Con los mismos contendientes en cada nivel, los saltos entre niveles son comparables. El nivel 4 solo junta bloques ya probados, y Cox ganó en los tres niveles con XGBoost optimizado lejos del listón: repetirlo costaría casi toda la ejecución para confirmar lo sabido.

### ¿Con qué librerías?
- **Decisión:** scikit-survival para Cox, elastic net y random survival forest; XGBoost para gradient boosting, adaptado al formato de los demás.
- **Por qué:** scikit-survival encaja en el `Pipeline`, pero su gradient boosting tardaba unos 46 minutos por entrenamiento, y XGBoost, unos segundos con los mismos ajustes.

### ¿Cómo se ajustan los modelos?
- **Decisión:** primero, con valores fijos razonables, para tener una estimación. Después se optimiza solo el ganador, con Optuna; si dos quedan cerca, ambos. Los modelos optimizados se comparan con otros bloques. En los niveles 1, 2 y 3 se queda Cox simple.
- **Por qué:** optimizar los cuatro en cada nivel costaría horas sin saber aún cuál importa. No compensa perder la explicabilidad por clasificar mejor 1 de cada 100. Comparar con otros bloques evita que la optimización infle el resultado.

### ¿Se usan los pesos muestrales de NHANES?
- **Decisión:** no, ni al entrenar ni al traducir el riesgo a edad ni al evaluar. Se declara como limitación.
- **Por qué:** el usuario es español, así que representar exactamente a la población de EE. UU. no es el objetivo.

### ¿Cómo se eligen las variables de cada nivel?
- **Decisión:** se anidan. Cada nivel parte de las variables que sobrevivieron en el anterior y solo añade su bloque. Si en un nivel no sobrevive casi nada de lo añadido, ese modelo se descarta.
- **Por qué:** así cada salto mide solo lo que aporta el bloque nuevo, y se evita volver a probar lo ya descartado.

### ¿Qué variables forman cada bloque?
- **Decisión:** las listas viven en `src/config/model_sets.py`. Base: lo que trae una analítica básica española (hemograma con fórmula e índices, glucosa, función renal, colesterol total y HDL, transaminasas, ácido úrico, sodio, potasio y calcio), más edad, sexo e IMC. Extras: lo que se pide a menudo o es opcional, incluidos triglicéridos, GGT, albúmina, PCR, vitamina D, tensión y el cociente albúmina/creatinina en orina. Cuestionario: las siete variables de hábitos. Las variables de Gold que no se usan quedan en una lista de descartadas con su motivo.
- **Por qué:** cada bloque responde a qué trae el usuario, no a cuánto predice cada variable: si una aporta o no, lo dice el modelo en la escalera de niveles. Triglicéridos va a Extras porque solo está medido en el subgrupo en ayunas. Cintura y CPK se descartan porque el usuario no conoce la primera y la segunda solo existe en 4 ciclos.

### ¿Qué queda de Base tras el nivel 1?
- **Decisión:** Cox simple con 18 variables. Salen plaquetas, VPM, eosinófilos, basófilos, colesterol total y calcio, y después el RDW (ver su salto). La serie roja se mantiene con hemoglobina, hematíes y CHCM.
- **Por qué:** las seis no tienen un efecto claro y quitarlas no baja el C-index misma edad. Dejar solo la hemoglobina corregiría su signo, pero baja 0,008 ese C-index y no arregla otros signos; las variables ligadas se agruparán al explicar el resultado.

### ¿Qué queda de Extras tras el nivel 2?
- **Decisión:** Cox simple con las de Base y 10 de Extras: cociente albúmina/creatinina en orina, albúmina, GGT, vitamina D, LDH, cloro, fósforo, fosfatasa alcalina, sistólica y diastólica. Salen triglicéridos, PCR, bilirrubina, hierro, proteínas totales y HbA1c. Las de Base se quedan aunque pierdan fuerza.
- **Por qué:** los seis no tienen efecto claro y quitarlos no baja el C-index misma edad; dejar los de poca cobertura (triglicéridos y PCR) tampoco suma. XGBoost optimizado no llega al listón fijado de antemano (+0,02 en misma edad) y se queda menos corto en el grupo de mayor riesgo, pero ese desajuste de calibración se puede corregir al traducir el riesgo a edad, y con Cox los dos niveles se explican igual. Base tiene que funcionar sola.

### ¿Qué queda del Cuestionario tras el nivel 3?
- **Decisión:** Cox simple con las de Base y 4 hábitos: tabaco, actividad física, horas sentado y horas de sueño. Sale el alcohol, con sus dos preguntas, y la comida rápida. Un hábito con efecto claro contrario al conocido no entra aunque suba el C-index, y las preguntas de un mismo hábito se juzgan juntas.
- **Por qué:** beber sale protector frente a no beber nunca, por la causalidad inversa de quienes lo dejaron por enfermedad; al quitar solo la frecuencia, las bebidas pasaban a salir protectoras. Quitar el alcohol cuesta 0,004 de C-index misma edad, el precio de no decir al usuario que beber le quita años. La comida rápida no tiene efecto claro y quitarla no baja ese C-index. XGBoost optimizado no llega al listón (+0,02 en misma edad), como en los niveles 1 y 2. Juzgar el alcohol entero se fijó tras la primera ejecución, al ver el cambio de signo.

### ¿Hay modelo del nivel 4?
- **Decisión:** sí, Cox simple con las 32 variables de Base, Extras y Cuestionario, sin quitar ninguna. La app lo usa cuando el usuario trae Extras y responde el cuestionario.
- **Por qué:** supera al nivel 2 con bootstrap (+0,013 de C-index misma edad, intervalo de 0,009 a 0,017) y ningún hábito cambia de signo al juntar los bloques. Lo que solo pierda fuerza se habría quedado igualmente: cada bloque tiene que funcionar con el otro o sin él. Las mejoras no se suman (+0,013 frente a +0,021 de los hábitos sobre Base), porque los Extras recogen parte de lo mismo. Las cifras son con RDW; sin él, el nivel 4 sigue por delante del 2 (0,739 frente a 0,720 misma edad), sin repetir el bootstrap.

### ¿Qué entra de cada pareja y combinación lineal?
- **Decisión:** por defecto, las variables que vienen escritas en el PDF. Serie roja: hemoglobina, hematíes y CHCM. Serie blanca: los cinco tipos, sin leucocitos. Colesterol total + HDL, proteínas totales + albúmina y sistólica + diastólica. El IMC sustituye a peso y talla, que el usuario sigue dando. Fuera insulina, HOMA-IR y los cocientes derivados.
- **Por qué:** en una combinación lineal, el juego no cambia lo que sabe un Cox, y así la app no tiene que calcular nada. Hemoglobina, hematíes y CHCM son tres datos independientes de los que salen hematocrito, VCM y HCM. Leucocitos es la suma de los cinco tipos. Un Cox no puede construir por sí solo un cociente como el IMC. Insulina y HOMA-IR cubren menos de la mitad, con un salto sin explicar y rara vez pedidas. Si el modelo se queda corto, en futuras iteraciones se pueden reintroducir los descartados.

### ¿Qué se hace con el salto del RDW?
- **Decisión:** se quita del modelo en todos los niveles. Se midió cuántos años cambia la edad biológica si el RDW de todos sube lo que subió con el cambio de analizador (1 punto), con un límite de 1 año de mediana fijado antes: lo supera en todos los niveles (de 1,8 a 2,8 años).
- **Por qué:** en la app sería un sesgo de todo un laboratorio que el usuario no puede ver ni corregir. La CDC no da corrección oficial, y un ajuste propio no resolvería la escala de los analizadores españoles, que es desconocida. Quitarlo cuesta de 0,006 (nivel 4) a 0,018 (nivel 1) de C-index misma edad, y ninguna variable del nivel 1 cambia entre efecto claro y no claro.

### ¿Cómo se traduce el riesgo a edad?
- **Decisión:** la edad biológica es la edad a la que la persona típica del mismo sexo tiene el mismo riesgo a 10 años según el modelo del nivel. La persona típica es la mediana del riesgo que ese modelo, ya entrenado, da a la gente de train de cada edad y sexo, en la escala log(−log(1 − riesgo)), con una curva de segundo grado por sexo. Fuera de 18-79 la curva sigue en línea recta.
- **Por qué:** con una referencia común (el baseline, como PhenoAge) la persona típica salía hasta 5 años más joven, y peor cuanto más completo el modelo: al separar más a la gente, la media en escala logarítmica cae. Con la media de cada nivel, la persona típica seguía 1-2 años por debajo por la cola de personas muy enfermas; con la mediana y la curva, la mediana de cada grupo de edad y sexo queda dentro de ±1 año y la media algo por encima, el lado prudente. Por sexo, porque a igual edad un hombre tiene el riesgo de una mujer 5 años mayor.

### ¿Cómo se tratan las analíticas incompletas?
- **Decisión:** con los cuatro modelos más imputación. En la app, la variable que falte de una pareja correlacionada se estima desde su pareja; en NHANES no hace falta, porque las parejas faltan juntas. El resto de huecos se imputan con un imputador ajustado solo con train. No se usan los nulos como información.
- **Por qué:** en NHANES un hueco suele significar "ciclo sin esa prueba", y los ciclos antiguos tienen más muertes por su seguimiento largo: un modelo que aprenda de los nulos aprendería el ciclo. En la app, un hueco significa "no me lo han pedido".

### ¿Cómo se preprocesa?
- **Decisión:** un `Pipeline` de scikit-learn, ajustado solo con train (el de cada ronda, en validación cruzada), que se guarda entero con el modelo. En este orden: recorte a los percentiles 0,1 y 99,9; huecos con la mediana, o la respuesta más frecuente, de su sexo y grupo de edad; logaritmo en las variables con asimetría mayor de 2; escalado; una columna 0/1 por categoría; y término al cuadrado en IMC y horas de sueño. Quien nunca bebe queda con 0 bebidas.
- **Por qué:** con la mediana general, una persona mayor con un hueco parecería más joven, que es el error peor. El recorte y el logaritmo evitan que un valor extremo domine un modelo lineal; el cuadrado le deja ver las U conocidas, y se elige por conocimiento previo. Todos los modelos reciben los mismos datos, para que la comparación sea justa. El `Pipeline` reaprende cada ronda por sí solo, lo que evita fugas por descuido, y la app aplica exactamente el mismo objeto; a cambio, necesita las mismas versiones de scikit-learn. Imputar con otras variables o usar curvas flexibles queda para futuras iteraciones si el modelo se queda corto.

### ¿Qué modelo usa la app?
- **Decisión:** el más completo que permitan los datos del usuario, pero solo si ese nivel ha superado de verdad al anterior; si no, el anterior. No se promedian modelos.
- **Por qué:** promediar con un modelo peor empeora el resultado, y un modelo que no mejora solo añade preguntas y datos que pueden faltar.

### ¿Con qué datos se entrena el modelo final y dónde se guarda?
- **Decisión:** el pipeline entrena con todos los datos (train y test), y ese es el único modelo que se guarda: un archivo por nivel (1 a 4) en una carpeta del repo, versionada en git, que es lo que usa la app. La evaluación final no lo carga: entrena sus propios modelos con train, con la misma función del pipeline, y también el baseline.
- **Por qué:** todas las decisiones se tomaron con validación cruzada dentro de train, así que solo el test da una cifra sin sesgo; reentrenar con todo después solo añade gente y la cifra del test sigue valiendo. Si la evaluación cargara los modelos guardados, al volver a ejecutarla evaluaría con gente ya vista y daría cifras infladas sin avisar; así no puede pasar. Al reentrenar, ningún coeficiente cambia de signo y la edad de cada persona se mueve menos de ±0,85 años en el 90 % de los casos. Los modelos van en git porque el servidor de la app no puede regenerarlos sin descargar NHANES, y pesan poco.

### ¿Cómo se organiza el código del modelo?
- **Decisión:** un archivo por paso, no por modelo, en `src/models/` con prefijo `s1_`…`s5_` (split, preprocesado, algoritmos, edad biológica, evaluación). Las variables de cada bloque y el algoritmo ganador de cada modelo, en `src/config/model_sets.py`. El entrenamiento se lanza desde `src/pipeline/s5_build_model.py`, el quinto paso del pipeline, que llama a esos archivos. Un notebook de trabajo por nivel, con todos sus modelos para poder compararlos, que importa de `src/`.
- **Por qué:** los cuatro modelos son el mismo proceso con otra lista de variables; por modelo serían cuatro copias. Split se separa del preprocesado porque la app usa el preprocesado y nunca el split. La edad biológica va aparte porque es igual para todos los algoritmos. Python no importa módulos que empiezan por número; de ahí la `s`.

### ¿Cómo se mide la infraestimación?
- **Decisión:** en años. En cada decil de riesgo, cuántos años habría que sumar a la edad biológica de ese decil para que su riesgo predicho cuadre con el observado. Por encima de 0, la edad se queda corta. Las colas se miden con el porcentaje de personas a más de 10 años de su edad, por arriba y por abajo.
- **Por qué:** es la unidad que ve el usuario, y el signo separa el error peor (infraestimar) del otro.

### ¿Qué se mide en la evaluación final y qué cuenta como aprobado?
- **Decisión:** en test, una sola vez, a 10 años, con los modelos guardados, el baseline y PhenoAge. Se fijaron antes de abrir el test: cada salto (1 vs 0, 2 vs 1, 3 vs 1 y 4 vs 2) es real si el intervalo del bootstrap de la diferencia de C-index misma edad queda entero por encima de 0; el C-index misma edad cae como mucho 0,02 frente a la validación cruzada; ningún decil infraestima más de 2 años; la mediana de cada grupo de edad y sexo queda dentro de ±1,5 años; el nivel 2 no queda por debajo de PhenoAge; y sin las muertes de los 2 primeros años el C-index misma edad cae como mucho 0,02. Si se suspende un criterio, no se vuelve a ajustar el modelo: va a limitaciones, salvo si el nivel 1 no supera al baseline.
- **Resultado:** se cumple todo menos la infraestimación, que en los deciles de riesgo bajo llega a entre 3,7 y 9,6 años (el baseline, que es la edad misma, también falla con 5,2), y desde el decil 6 no pasa de 1,4. Los cuatro saltos son reales (el 4 vs 2, +0,018 sin RDW), así que la app usa los cuatro niveles.
- **Por qué:** fijar los listones después de mirar el test los ajustaría a lo que saliera. La infraestimación en riesgo bajo es sobre todo ruido (unas 970 personas por decil con pocas muertes, y a esas edades poco riesgo equivale a muchos años), pero se mantiene como limitación: en jóvenes de riesgo bajo, el margen ± X años tiene que ser más ancho.

### ¿Se quitan las muertes de los 2 primeros años (causalidad inversa)?
- **Decisión:** no, se quedan dentro, como en PhenoAge.
- **Por qué:** en test, quitarlas baja el C-index misma edad entre 0,007 y 0,012, dentro del listón de 0,02 fijado antes. El modelo no se apoya sobre todo en enfermedad ya avanzada.

### ¿Qué error es peor?
- **Decisión:** infraestimar la edad biológica (falso negativo) es peor que sobreestimarla. Con métricas parecidas, se prefiere el modelo con menos errores grandes aunque su media sea algo peor.
- **Por qué:** infraestimar da una falsa tranquilidad; sobreestimar solo manda al médico. Y un error grande en una persona concreta resta más confianza en el producto que una media algo peor.

## App

### ¿Qué pasa si la analítica trae un valor fuera del rango posible?
- **Decisión:** primero, en la pantalla de revisión, se pide al usuario que compruebe el valor (puede ser una mala lectura del PDF). Si lo confirma, la app no calcula la edad biológica y muestra un aviso para ir al médico cuanto antes. Usa la misma tabla de rangos que Silver clean.
- **Por qué:** son valores de emergencia o de una muestra defectuosa. Dar una edad biológica ahí sería engañoso, y el modelo no ha visto esos valores.

### ¿Qué hacer si el usuario trae la pareja de una variable del modelo pero no la variable?
- **Decisión:** estimarla con una ecuación ajustada sobre Gold (p. ej. hemoglobina a partir del hematocrito), solo para parejas con correlación alta.
- **Por qué:** así se pierden menos variables sin pedir nada más al usuario.

### ¿Se usa el filtrado glomerular que traen las analíticas?
- **Decisión:** no como variable del modelo, pero el parser puede usarlo para recuperar la creatinina si falta.
- **Por qué:** es redundante con creatinina, edad y sexo.

### ¿Se pregunta el alcohol?
- **Decisión:** no, porque el modelo no lo usa. La app explica por qué falta en el cuestionario.
- **Por qué:** en NHANES beber sale protector por causalidad inversa (ver el nivel 3), y el usuario espera que el alcohol esté en un cuestionario de hábitos.