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

Por un lado, mi formación es en bioquímica, por lo que entiendo tanto los datos como la utilidad del problema, y me permite retomar un área más cercana a mi background que siempre he tenido algo olvidada.

Por otro lado, la utilidad del problema está validada externamente: una empresa del sector (Enveda) lo ha convertido en una competición con 50.000 $ en premios, lo que indica que hay organizaciones dispuestas a pagar por resolverlo. No es una necesidad inventada para justificar un proyecto.

Por último, la competición ofrece una forma objetiva de evaluar el trabajo: una métrica definida y un ranking público con cientos de equipos con el que contrastar los resultados, algo que normalmente falta en un TFM.

### ¿Qué problema que resuelve?

El valor del producto se puede explicar mediante 2 vías:

- B2B / Industria y laboratorios: Funciona como herramienta de apoyo para empresas de descubrimiento de fármacos a partir de productos naturales y para laboratorios de metabolómica, toxicología, alimentación o medio ambiente, acelerando la identificación de moléculas desconocidas y reduciendo el tiempo de análisis experto por muestra.

- Herramienta abierta para investigación (B2C / académico): Funciona como aplicación web donde un grupo de investigación sube sus espectros y obtiene el ranking de candidatas con su visualización 3D, sin necesidad de programar. Podría monetizarse con un modelo freemium o con una API para uso intensivo. La hipótesis es: "Si el cuello de botella es la identificación manual, una herramienta que reduzca miles de candidatas a 25 ahorra horas de trabajo experto por molécula, lo que justifica su uso y su pago." Existen herramientas previas (como SIRIUS); el objetivo no es sustituirlas, sino ofrecer una alternativa abierta basada en Deep Learning con una interfaz visual pensada para usuarios que no son programadores.

## Idea 3 - Radar de Catalizadores: Predicción de la Probabilidad de Éxito de Ensayos Clínicos para Inversores en Biotecnología

Modelo de Machine Learning entrenado con el histórico público de ensayos clínicos de ClinicalTrials.gov (a través de AACT, su versión en base de datos PostgreSQL) que, a partir de las características de diseño de un ensayo (fase, enfermedad, tipo de intervención, tamaño muestral, aleatorización y enmascaramiento, patrocinador, criterios de inclusión...), estima la probabilidad de que tenga éxito, por ejemplo, de que avance a la siguiente fase. En la interfaz, el usuario elige una empresa biotecnológica cotizada y consulta las fichas de los ensayos activos de su pipeline, cada una con su probabilidad, los factores que la explican y ensayos históricos comparables. De cara a un futuro, se contempla ampliar el número de empresas y añadir alertas ante hitos próximos. La herramienta es informativa y no constituye asesoramiento financiero.

### ¿Qué problema que resuelve?

En la biotecnología de pequeña capitalización, el valor de una empresa depende de unos pocos eventos binarios: los resultados de sus ensayos clínicos. El inversor minorista no dispone de herramientas para estimar la probabilidad de cada uno y suele decidir con titulares, foros o intuición, mientras que las plataformas profesionales suelen ser de pago y estar pensadas para grandes fondos y farmacéuticas. El resultado es una asimetría de información muy grande a la hora de tomar decisiones.

El producto ofrece una estimación objetiva, calibrada y explicable de la probabilidad de éxito de cada ensayo, y la presenta organizada por empresa, que es como piensa el inversor, y no por registro de ensayo.

### Motivación para desarrollar el proyecto

Por un lado, mi formación en bioquímica me permite entender el diseño de un ensayo: qué mide, en qué fase está y qué mecanismo hay detrás, algo que a un perfil puramente financiero o puramente de datos le costaría más.

Por otro lado, los mercados y la inversión son un tema que me interesa mucho, y este proyecto une ambos mundos en un producto con un usuario muy claro.

Por último, los datos son públicos, relacionales y se actualizan a diario, lo que permite construir un producto "vivo" sobre una base de datos real y no sobre un CSV estático. Además, existen etiquetas públicas y reproducibles de resultados de ensayos con las que entrenar y validar el modelo.

### ¿Qué problema que resuelve?

El valor del producto se puede explicar mediante 2 vías:

- B2B / Fondos y equipos de desarrollo de negocio: Pequeños fondos, comunidades y newsletters de inversión en biotecnología, y equipos de desarrollo de negocio de farmacéuticas pueden usarlo para cribar rápidamente programas competidores o candidatos de licencia antes de dedicarles análisis experto.

- Producto independiente (B2C): Plataforma web para inversores minoristas con un modelo freemium: consulta básica gratuita y suscripción para alertas, listas de seguimiento y comparables. La hipótesis es: "Aunque la precisión absoluta sea limitada, sobre todo en fases tempranas, una probabilidad calibrada y explicable ya aporta valor como herramienta de triaje frente a decidir sin ningún dato."

## Idea 4 - Estimación de la Edad Biológica a partir de Analítica y Parámetros Funcionales, con Simulador Interactivo

Modelo de Machine Learning que estima la edad biológica de una persona a partir de los biomarcadores de una analítica de sangre rutinaria (glucosa, HbA1c, creatinina, albúmina, PCR, hemograma...) y de parámetros funcionales y de estilo de vida adicionales, como la capacidad aeróbica (VO2 máx, o su mejor aproximación disponible en los datos de entrenamiento), la presión arterial o la composición corporal. En la interfaz, el usuario introduce sus valores y obtiene su edad biológica estimada y la contribución de cada parámetro, y dispone de un simulador visual con controles deslizantes para modificar cualquier valor y ver en tiempo real cómo cambia la edad predicha. El modelo se entrena con datos públicos de NHANES (analíticas con mortalidad enlazada) almacenados en una base de datos PostgreSQL. De cara a un futuro, se contempla el seguimiento de la evolución a lo largo de varias analíticas. La herramienta es informativa y de bienestar, no diagnóstica ni sustituye el consejo médico.

### ¿Qué problema que resuelve?

La edad cronológica no refleja el estado fisiológico real de una persona. Mucha gente se hace analíticas con regularidad, pero un "todo dentro de rango" no dice nada sobre cómo de rápido está envejeciendo su organismo. Las calculadoras existentes suelen dar un único número a partir de parámetros sanguíneos, sin permitir entender qué lo impulsa ni explorar cómo cambiaría.

Este producto incorpora parámetros funcionales como la capacidad aeróbica, uno de los indicadores más ligados a la salud a largo plazo, y hace el modelo explorable: el usuario ve qué parámetros pesan más en su resultado y cómo se movería la edad estimada si cambiaran. El simulador muestra cómo responde el modelo, no un plan de tratamiento.

### Motivación para desarrollar el proyecto

Por un lado, mi formación en bioquímica me permite interpretar con criterio los biomarcadores, validar que el modelo tiene sentido biológico y no tratarlo como una caja negra.

Por otro lado, a la gente le gusta jugar con estas cosas y compararse, lo que hace el producto atractivo y fácil de entender para un usuario sin conocimientos técnicos. Además, la parte de interpretabilidad y de simulación visual es lo que más me motiva desde el punto de vista del diseño del producto.

Por último, los datos son públicos, abundantes y están bien documentados, lo que permite centrar el esfuerzo en un modelo sólido y en una experiencia de usuario cuidada, y no en conseguir datos.

### ¿Qué problema que resuelve?

El valor del producto se puede explicar mediante 2 vías:

- B2B / Salud y bienestar: Gimnasios y centros de entrenamiento, nutricionistas, clínicas de longevidad, programas de bienestar corporativo y laboratorios de análisis clínicos pueden integrarlo como un valor añadido al informe que ya entregan a sus clientes, o como herramienta de seguimiento.

- Producto independiente (B2C): Aplicación web para personas interesadas en su salud, el deporte o la longevidad, con un modelo freemium: cálculo y simulador básicos gratuitos y plan de pago con histórico de analíticas y comparación entre fechas. La hipótesis es: "Si la gente ya se hace analíticas y le interesa conocer su edad biológica, una herramienta que además le deje explorar qué la mueve tendrá más uso y más retención que una calculadora de un solo resultado."
