# Qué hay en este archivo y cómo usarlo
- **Contiene:** qué es el proyecto, por qué y para qué: la idea, el usuario, cómo debe ser la experiencia, cómo se va a construir a grandes rasgos y las restricciones.
- **No contiene:** nombres de carpetas, archivos ni variables, detalles técnicos, decisiones técnicas o metodológicas ni lo pendiente.
- **Se actualiza:** solo si yo lo pido, porque cambie la idea o el diseño del producto.

## Qué es
TFM del máster de Data Science e IA de EVOLVE: la **Idea 4 de la Entrega 01, calculadora de edad biológica a partir de una analítica**.

No hay memoria escrita. Se evalúa el producto completo (modelo + UX/front + despliegue), igual que un usuario evalúa una app: por su funcionalidad y su precisión.

## El producto
Calculadora web gratuita, sin registro ni captura de email, que estima la edad biológica a partir de una analítica de sangre real. Se accede con un enlace a una web pública, sin instalar nada. Interfaz en español.

Usuario objetivo: españoles sin formación médica que la usan desde casa.

Flujo: **subir PDF → revisar/corregir los datos extraídos (y responder el cuestionario, si se elige ese modo) → ver resultado**.

El resultado muestra:
- Edad biológica estimada ± X años, con X según la precisión de cada caso (menor si faltan datos), y la diferencia con la edad cronológica.
- Los mejores y los peores parámetros del usuario, en tablas y explicados en lenguaje llano.
- Si la edad biológica supera la cronológica por encima de un umbral: recomendación de revisar la analítica con su médico.
- Aviso asimétrico: salir por encima es señal para consultar, pero salir bien no significa estar sano.
- Aviso de que no es consejo médico ni diagnóstico. No se dan recomendaciones (suplementos, tratamientos…), solo observaciones de los datos.

Qué datos usa: lo que trae una analítica de rutina española, lo que se pide a menudo (p. ej. vitamina D) y lo que el usuario sabe sin pensar (edad, sexo, peso, talla), siempre que exista en NHANES. Edad y sexo se extraen del PDF si vienen; si no, se piden. Dato opcional para afinar, nunca obligatorio: tensión arterial. Solo adultos, dentro del rango de edad de los datos de entrenamiento.

Las analíticas no traen siempre los mismos parámetros: si falta algún dato, se calcula igualmente con menos fiabilidad; si faltan demasiados, se avisa de que no se puede calcular.

Dos modos, a elección del usuario: solo con la analítica, o con la analítica más un cuestionario de hábitos de vida (tabaco, alcohol, actividad, sedentarismo, comida rápida, sueño) de ~10 preguntas de botones, sin escribir. Solo datos objetivos; nada de autovaloraciones ("¿cómo de sana es tu dieta?", "¿cómo es tu salud?").

### Propuesta de valor (frente a lo que existe)
- Sin introducir datos a mano: la app lee los valores del PDF.
- Gratis de verdad: no es lead magnet ni parte de un funnel.
- Resultado comprensible: una edad y una explicación, no una tabla de valores.

## Cómo se construye
1. **Datos:** NHANES con mortalidad enlazada. Se toma la población de EE. UU. como referencia: se asume equivalencia entre EE. UU. y España.
2. **Preparación:** descargar → unir y limpiar → tabla final para el modelo.
3. **Modelo:** no existe una etiqueta de "edad biológica real", así que no se predice directamente. Un **modelo de supervivencia** estima el riesgo de mortalidad a partir de los biomarcadores, y ese riesgo se traduce a una **edad equivalente** (la edad a la que la población media tiene ese mismo riesgo), al estilo de **PhenoAge** (Levine et al., 2018), que es también la referencia con la que compararse.
4. **App:** lee el PDF y normaliza nombres de parámetros (glucosa / gluc / GLU…) y unidades antes de la pantalla de revisión.
5. **Despliegue:** web pública.

## Experiencia de usuario (parte evaluada)
- Prioridad de la UX sobre afinar el modelo: el modelo es fácil de iterar, una UX mal planteada obliga a rehacerla.
- Usable por cualquier persona: flujo corto, lenguaje claro sin jerga, responsive y pensado para móvil.
- Estados de carga y errores de parseo comprensibles y accionables (qué ha fallado y qué puede hacer el usuario).

### Diseño visual
Por definir.

## Privacidad
Son datos de salud (categoría especial en el RGPD):
- Minimizar el tratamiento y no almacenar nada: la app procesa todo en memoria y lo descarta.
- No se usan etnia ni datos socioeconómicos.
- Informar al usuario de forma clara de qué se hace con sus datos.

## Restricciones
- Hosting en planes gratuitos.
- Formato de entrada: PDF digital.
