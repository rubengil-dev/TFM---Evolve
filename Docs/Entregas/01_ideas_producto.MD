# 4 Ideas para mi TFM

## Idea 1 - Sistema de Recomendación Cruzada basada en Perfil de Personalidad

Algoritmo de recomendación centrado inicialmente en películas, libros y música que cruza los perfiles de consumo del usuario para predecir sus gustos más allá de una única plataforma cerrada. De cara a un futuro, se contempla la integración de videojuegos, ropa, actividades y un test de personalidad avanzado para mejorar aún más las predicciones y el valor para el usuario.

### ¿Qué problema que resuelve?

Actualmente, los sistemas de recomendación operan en silos estancos: cada plataforma (Netflix, Spotify, etc.) analiza únicamente el consumo dentro de su propio ecosistema, ignorando que los gustos humanos son transversales e interconectados. Usando un cliché como ejemplo, quizá alguien que disfrute de música clásica también encuentre interesantes libros de literatura clásica.

Esta fragmentación genera un problema evidente en las fases de arranque en frío, donde las plataformas fallan al intentar sugerir contenido a un usuario nuevo. El uso de datos cruzados y perfiles de personalidad optimiza la toma de decisiones algorítmica, permitiendo predecir preferencias con alta precisión desde el primer momento y ofreciendo una experiencia de usuario radicalmente superior a los algoritmos unidimensionales actuales.

### Motivación para desarrollar el proyecto

Por un lado, me fascinaría explicar matemáticamente cómo los patrones de consumo de un área cultural impactan y explican los de otra completamente distinta.

Por otro lado, resuelve la necesidad real que existe a la hora de dar las primeras recomendaciones a un usuario, que yo mismo sufro. Al no usar demasiado ninguna plataforma, las recomendaciones no llegan a ser precisas. Pero estoy seguro de que combinando todas ellas sí lo serían.

Por último, me parece un producto viable de manera independiente que se podría llegar a monetizar e iniciar como un emprendimiento.

### ¿Qué problema que resuelve?

El valor del producto se puede explicar mediante 2 vías:

- B2B / Alianzas estratégicas: Funciona como un motor de recomendación externo que puede integrarse en plataformas digitales para mitigar el problema del arranque en frío o servir como puente de colaboración cruzada entre distintas industrias de entretenimiento.

- Producto independiente (B2C): Funciona de manera autónoma como una plataforma web unificada donde el usuario podría sincronizar sus cuentas (perfiles de música, cine, lectura), centralizando su ocio en una plataforma para descubrir nuevos libros, películas, canciones... La hipótesis es: "Si los test de personalidad presentan una altísima demanda en internet, esto sería una evolución de los mismos. Por tanto, tendría igual o más demanda, haciendo el producto monetizable (display ads o patrocinios) en caso de no cerrar acuerdos corporativos directos."

## Idea 2 - Identificación de Estructuras Químicas a partir de Espectros de Masas en Tándem (MS/MS)

Modelo de Machine Learning / Deep Learning que, a partir de los espectros de masas en tándem (LC-MS/MS) de una molécula pequeña presente en un extracto biológico complejo, predice su estructura química 2D y devuelve un ranking con las 25 estructuras candidatas más probables. El modelo se entrena y se evalúa con los datos de la competición de [Kaggle "Enveda CASMI 2026 - Molecule ID From Mass Spectra"](https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra), utilizando su métrica oficial, el MRR@25. Se complementa con una interfaz web donde el usuario sube un espectro, consulta el ranking de candidatas y visualiza cada estructura en 3D, en lugar de recibir simplemente un archivo plano con la descripción de las moléculas. De cara a un futuro, se contempla ampliar la interfaz a otros instrumentos y formatos de espectro.

### ¿Qué problema que resuelve?

La espectrometría de masas en tándem es una de las técnicas principales para detectar moléculas en muestras biológicas complejas (extractos de plantas, microorganismos, fluidos...). Cada molécula genera un patrón de fragmentación característico, pero traducir ese patrón a una estructura química es el cuello de botella: las librerías de espectros de referencia cubren solo una pequeña parte de la química posible, por lo que una parte muy importante de las señales detectadas queda sin identificar, y hacerlo a mano exige mucho tiempo de personal experto.

Esto ralentiza el descubrimiento de nuevos compuestos bioactivos y el análisis de muestras. Un modelo capaz de generalizar más allá de las librerías, prediciendo la estructura de moléculas que nunca ha visto, reduce el problema de millones de estructuras posibles a una lista corta de 25 candidatas que un experto puede revisar y validar.

### Motivación para desarrollar el proyecto

Por un lado, mi formación es en bioquímica, por lo que entiendo tanto los datos como la utilidad del problema, y me permite retomar un área más cercana a mi background.

Por otro lado, la utilidad del problema está validada externamente: una empresa del sector (Enveda) lo ha convertido en una competición con 50.000 $ en premios, lo que indica que hay organizaciones dispuestas a pagar por resolverlo. 

### ¿Qué problema que resuelve?

El valor del producto se puede explicar mediante 2 vías:

- B2B / Industria y laboratorios: Funciona como herramienta de apoyo para empresas de descubrimiento de fármacos a partir de productos naturales y para laboratorios de metabolómica, toxicología, alimentación o medio ambiente, acelerando la identificación de moléculas desconocidas y reduciendo el tiempo de análisis experto por muestra.

- Herramienta abierta para investigación (B2C / académico): Funciona como aplicación web donde un grupo de investigación sube sus espectros y obtiene el ranking de candidatas con su visualización 3D, sin necesidad de programar.

## Idea 3 - Radar de Catalizadores: Predicción de la Probabilidad de Éxito de Ensayos Clínicos para Inversores en Biotecnología

Modelo de Machine Learning entrenado con el histórico público de ensayos clínicos de ClinicalTrials.gov (a través de AACT, su versión en base de datos PostgreSQL) que, a partir de las características de diseño de un ensayo, estima la probabilidad de que tenga éxito, por ejemplo, de que avance a la siguiente fase. En la interfaz, el usuario elige una empresa biotecnológica cotizada y consulta las fichas de los ensayos activos de su pipeline, cada una con su probabilidad, los factores que la explican y ensayos históricos comparables.

### ¿Qué problema que resuelve?

En la biotecnología de pequeña capitalización, el valor de una empresa depende de unos pocos eventos binarios: los resultados de sus ensayos clínicos. El inversor minorista no dispone de herramientas para estimar la probabilidad de cada uno y suele decidir con titulares, foros o intuición, mientras que las plataformas profesionales suelen ser de pago y estar pensadas para grandes fondos y farmacéuticas. El resultado es una asimetría de información muy grande a la hora de tomar decisiones.

El producto ofrece una estimación objetiva, calibrada y explicable de la probabilidad de éxito de cada ensayo, y la presenta organizada por empresa, que es como piensa el inversor, y no por registro de ensayo.

### Motivación para desarrollar el proyecto

Por un lado, mi formación en bioquímica me permite entender el diseño de un ensayo: qué mide, en qué fase está y qué mecanismo hay detrás, algo que a un perfil puramente financiero o puramente de datos le costaría más.

Por otro lado, los mercados y la inversión son un tema que me interesa mucho, y este proyecto une ambos mundos en un producto con un usuario muy claro.

Por último, los datos son públicos, relacionales y se actualizan a diario, lo que permite construir un producto "vivo" sobre una base de datos real y no sobre un CSV estático. Además, existen etiquetas públicas y reproducibles de resultados de ensayos con las que entrenar y validar el modelo.

### ¿Qué problema que resuelve?

El producto es altamente monetizable dado que se asocia a la inversión. Es decir, donde el dinero ya se está moviendo significa que hay demanda, por lo que el producto se podría monetizar de múltiples formas: asesoramiento a fondos, minoristas...

## Idea 4 - Calculadora de Edad Biológica a partir de Analítica

Aplicación que estima la edad biológica de una persona a partir de su analítica de sangre rutinaria. El usuario sube el PDF de su analítica y la aplicación extrae los valores automáticamente, le pide que los confirme y devuelve una edad biológica estimada, la diferencia con su edad cronológica y los marcadores que más influyen en el resultado, explicados en lenguaje llano. De forma opcional, el usuario puede añadir datos que normalmente no aparecen en una analítica (tensión arterial, composición corporal, capacidad aeróbica o su mejor aproximación), que el modelo utiliza para afinar la estimación.

Cómo se calcula. No existe un conjunto de datos con la "edad biológica real" como etiqueta, por lo que no se puede predecir directamente. El enfoque habitual en la literatura es entrenar un modelo de supervivencia que estima el riesgo de mortalidad a partir de los biomarcadores y traducir ese riesgo a una "edad equivalente": la edad a la que la población media tiene ese mismo riesgo. El modelo se entrena con datos públicos de NHANES (analíticas con mortalidad enlazada) y se compara con un baseline publicado (PhenoAge, Levine et al., 2018).

### ¿Qué problema que resuelve?

Mucha gente se hace analíticas con regularidad, pero un "todo dentro de rango" no dice nada sobre cómo de rápido está envejeciendo su organismo, e interpretar una docena de valores sueltos exige conocimientos que la mayoría no tiene.

En una revisión informal de calculadoras de edad biológica, la mayoría exige introducir los valores a mano uno a uno, y muchas ni siquiera parten de una analítica. La única que permitía subir una analítica entregaba el resultado por correo, como puerta de entrada a un producto de pago. Esta fricción impide que la herramienta llegue a quien más la necesita: una persona sin formación sanitaria que solo quiere saber qué significa su analítica.

### Motivación para desarrollar el proyecto

- Formación: mi formación en bioquímica me permite interpretar los biomarcadores, comprobar que el modelo tiene sentido biológico y no tratarlo como una caja negra.

- Interés personal: soy muy frikie del deporte, la salud y el biohacking, y yo mismo usaría esta herramienta.

- Extra: a la gente le gusta jugar con estas cosas y compararse, lo que hace el producto atractivo y fácil de entender para un usuario sin conocimientos "bio".

### ¿Qué problema que resuelve?

La propuesta de valor diferencial reside en:

- Sin introducir datos a mano: se sube el PDF y la aplicación lee los valores. 

- Gratuitidad: Sin necesidad de usarlo como lead magnet o parte de un funnel.

- Datos que no están en la analítica: el usuario puede completar su perfil con parámetros funcionales o de estilo de vida (sólo si es posible y da tiempo).

- Resultado comprensible: una edad y una explicación en lenguaje llano en lugar de una tabla de valores.