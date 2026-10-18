# Contexto del TFM

## 1. Qué es
TFM del máster de Data Science e IA de EVOLVE. La idea elegida (de las 4 de la Entrega 01) es la **Idea 4: calculadora de edad biológica a partir de una analítica**. Sin recorte de alcance de momento.

Evaluación: no hay memoria escrita. Se evalúa el producto completo (modelo + UX/front + despliegue con URL pública), igual que un usuario evalúa una app: por su funcionalidad y su precisión.

Repo: https://github.com/rubengil-dev/TFM---Evolve.

## 2. El producto
Calculadora web gratuita, sin registro ni captura de email, que estima la edad biológica a partir de una analítica de sangre real.

Usuario objetivo: personas sin formación médica que la usan desde casa. Se accede con un enlace a una web pública, sin instalar nada. Interfaz en español.

Flujo: **subir PDF → revisar/corregir los datos extraídos → ver resultado**.

El resultado muestra:
- Edad biológica estimada ± X años, con X según la precisión de cada caso (menor si faltan datos), y la diferencia con la edad cronológica.
- Los mejores y los peores parámetros del usuario, en tablas y explicados en lenguaje llano.
- Si la edad biológica supera la cronológica por encima de un umbral: recomendación de revisar la analítica con su médico.
- Aviso asimétrico: salir por encima es señal para consultar, pero salir bien no significa estar sano.
- Aviso de que no es consejo médico ni diagnóstico. No se dan recomendaciones (suplementos, tratamientos…), solo observaciones de los datos.

Edad y sexo: se extraen del PDF si vienen; si no, se piden al usuario. Solo adultos, dentro del rango de edad de los datos de entrenamiento.

Dato opcional que el usuario puede añadir para afinar (nunca obligatorio): tensión arterial. La composición corporal (DXA) y la capacidad aeróbica (VO2 max) se descartan: el usuario no las conoce y en NHANES hay pocos ciclos y pocas defunciones con ellas.

Posible ampliación: hábitos de vida (tabaco, alcohol, actividad, sedentarismo, comida rápida, sueño) con preguntas de botones, sin escribir. Solo datos objetivos; nada de autovaloraciones ("¿cómo de sana es tu dieta?", "¿cómo es tu salud?").

Debe estar desplegada con URL pública para que el profesor la pruebe sin instalar nada, dentro de los límites de los planes gratuitos de hosting.

### Propuesta de valor (frente a lo que existe)
- Sin introducir datos a mano: se sube el PDF y la app lee los valores.
- Gratis de verdad: no es lead magnet ni parte de un funnel.
- Resultado comprensible: una edad y una explicación, no una tabla de valores.
- Mercado objetivo: españoles sin conocimientos médicos.

## 3. El modelo
- No existe una etiqueta de "edad biológica real", así que no se predice directamente. Se entrena un **modelo de supervivencia** que estima riesgo de mortalidad a partir de los biomarcadores, y ese riesgo se traduce a una **edad equivalente** (la edad a la que la población media tiene ese mismo riesgo), al estilo PhenoAge. El usuario solo ve su edad biológica.
- Datos: **NHANES con mortalidad enlazada** (Linked Mortality Files del NCHS). Se acepta la población de EE. UU. como referencia: lo que es saludable allí se asume saludable aquí. Se usa el **NHANES continuo 1999-2018** (mortalidad pública hasta 2019); NHANES III se descarta por métodos de laboratorio y formato distintos.
- Baseline publicado de referencia: **PhenoAge** (Levine et al., 2018).
- Población: adultos de 18 a 79 años (NHANES agrupa las edades superiores). Fuera las embarazadas (analítica alterada), las personas sin examen físico y las que no tienen ningún valor de laboratorio.
- Features: lo que trae una analítica de rutina española, lo que se pide a menudo (p. ej. vitamina D), lo que el usuario sabe sin pensar (edad, sexo, peso, talla) y un cuestionario de ~10 preguntas de botones. Siempre que exista en NHANES. Sin etnia ni datos socioeconómicos.
- De cada pareja de variables muy correlacionadas, solo una entra al modelo. La otra se conserva para que la app estime la que falta cuando el usuario solo trae la pareja.
- Rellenar huecos, recortar extremos, escalar y codificar forman parte del preprocesado del modelo y se ajustan solo con train, para no filtrar información del test. La tabla final del modelo solo lleva fórmulas fijas (features derivadas).
- **Requisito clave**: las analíticas no traen siempre los mismos parámetros. Si falta algún dato, se calcula igualmente con menos fiabilidad; si faltan demasiados, se avisa de que no se puede calcular. El umbral (mínimo viable de variables) se fija con los datos del modelo.
- **Baseline clásico primero**; deep learning solo si mejora de forma justificable.
- Evaluación con métricas de supervivencia (C-index, calibración) y también con distintos subconjuntos de variables, para saber cuánto se pierde según lo que falte.

## 4. Pipeline de la app
1. Extracción de texto del PDF digital. OCR y fotos quedan fuera del MVP.
2. Normalización de nombres de parámetros (glucosa / gluc / GLU…) y de unidades.
3. Pantalla de revisión donde el usuario corrige valores o los introduce a mano.
4. Modelo → riesgo de mortalidad → edad biológica.

Formato: PDF. Word solo si se comprueba que algún laboratorio entrega analíticas en Word.

## 5. Front y UX (parte evaluada)
- Prioridad de la UX sobre afinar el modelo: el modelo es fácil de iterar, una UX mal planteada obliga a rehacerla.
- Usable por cualquier persona: flujo corto, lenguaje claro sin jerga, responsive y pensado para móvil.
- Estados de carga y errores de parseo comprensibles y accionables (qué ha fallado y qué puede hacer el usuario).
- Resultado explicado de forma sencilla y honesta.

## 6. Privacidad
Son datos de salud (categoría especial en el RGPD):
- Minimizar el tratamiento y no almacenar nada: la app procesa todo en memoria y lo descarta.
- Informar al usuario de forma clara de qué se hace con sus datos.

## 7. Restricciones
- Hosting en planes gratuitos: condiciona el tamaño del modelo, el uso de OCR en servidor y los arranques en frío.

## 8. Entorno y datos
- Python 3.11 en un entorno virtual, con las dependencias congeladas en un archivo de requisitos. Motivo: es lo estándar, lo reproduce cualquiera (profesor incluido) y las plataformas de hosting lo leen directamente. La 3.11 tiene soporte hasta 2027 y todas las librerías la soportan; la 3.14 es demasiado nueva.
- Datos en capas: Bronze (tal como llega de la fuente, nunca se modifica), Silver (limpio, unido y armonizado) y Gold (tabla final que consume el modelo).

Todo lo de este archivo está decidido. Lo abierto está en el estado del proyecto.
