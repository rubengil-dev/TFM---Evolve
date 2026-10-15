# Contexto del TFM

## 1. Qué es
TFM del máster de Data Science e IA de EVOLVE. La idea elegida (de las 4 de `Docs/Entregas/01_ideas_producto.md`) es la **Idea 4: calculadora de edad biológica a partir de una analítica**.

Se evalúa el producto completo, no solo el modelo: tiene que demostrar que ML/DL permite crear un producto usable por usuarios finales no técnicos.
Nota = modelo sólido + UX/front cuidado + producto desplegado.

## 2. El producto
Calculadora web gratuita, sin registro ni captura de email, que estima la edad biológica a partir de una analítica de sangre real.

Flujo: **subir PDF → revisar/corregir los datos extraídos → ver resultado**.

El resultado muestra:
- Edad biológica estimada y diferencia con la edad cronológica.
- Los marcadores que más influyen en el resultado, explicados en lenguaje llano.
- Nivel de fiabilidad según los datos aportados.
- Aviso de que no es consejo médico ni diagnóstico.

Datos opcionales que el usuario puede añadir para afinar (nunca obligatorios): tensión arterial, composición corporal, capacidad aeróbica (VO2 max o su mejor aproximación).

Debe estar desplegada con URL pública para que el profesor la pruebe sin instalar nada, dentro de los límites de los planes gratuitos de hosting.

### Propuesta de valor (frente a lo que existe)
- Sin introducir datos a mano: se sube el PDF y la app lee los valores.
- Gratis de verdad: no es lead magnet ni parte de un funnel (la única calculadora revisada que aceptaba analíticas mandaba el resultado por email como puerta a un producto de pago).
- Resultado comprensible: una edad y una explicación, no una tabla de valores.
- Mercado objetivo: analíticas de laboratorios españoles.

## 3. El modelo
- No existe una etiqueta de "edad biológica real", así que no se predice directamente. Se entrena un **modelo de supervivencia** que estima riesgo de mortalidad a partir de los biomarcadores, y ese riesgo se traduce a una **edad equivalente** (la edad a la que la población media tiene ese mismo riesgo), al estilo PhenoAge. El usuario solo ve su edad biológica.
- Datos: **NHANES con mortalidad enlazada** (Linked Mortality Files del NCHS).
- Baseline publicado de referencia: **PhenoAge** (Levine et al., 2018).
- Features: intersección entre lo que hay en NHANES y lo que aparece en analíticas habituales españolas, más datos fáciles de aportar (edad, sexo, peso, altura).
- **Requisito clave**: las analíticas no traen siempre los mismos parámetros. El modelo debe funcionar con conjuntos variables de datos, con un **mínimo viable de variables** definido, y debe mostrar al usuario cuánta fiabilidad tiene su resultado según lo que ha aportado.
- **Baseline clásico primero**; deep learning solo si mejora de forma justificable.
- Evaluación con métricas de supervivencia (C-index, calibración) y también con distintos subconjuntos de variables, para saber cuánto se pierde según lo que falte.

## 4. Pipeline de la app
1. Extracción de texto del PDF (valorar OCR para PDFs escaneados).
2. Normalización de nombres de parámetros (glucosa / gluc / GLU…) y de unidades.
3. Pantalla de revisión donde el usuario corrige valores o los introduce a mano.
4. Modelo → riesgo de mortalidad → edad biológica.

Formato: solo PDF por ahora; Word se valorará si resulta común.

## 5. Front y UX (parte evaluada)
- Usable por cualquier persona: flujo corto, lenguaje claro sin jerga, responsive y pensado para móvil.
- Estados de carga y errores de parseo comprensibles y accionables (qué ha fallado y qué puede hacer el usuario).
- Resultado explicado de forma sencilla y honesta.

## 6. Privacidad
Son datos de salud (categoría especial en el RGPD):
- Minimizar el tratamiento y no almacenar nada.
- Informar al usuario de forma clara de qué se hace con sus datos.

## 7. Restricciones
- Hosting en planes gratuitos: condiciona el tamaño del modelo, el uso de OCR en servidor y los arranques en frío.
- Perfil del autor: bioquímico sin formación en ingeniería; el código, la arquitectura, el front y el despliegue necesitan apoyo y explicaciones en lenguaje llano.

## 8. Decisiones tomadas
- Idea 4 elegida como TFM.
- Enfoque: supervivencia → edad equivalente, no regresión directa de edad.
- Datos de entrenamiento: NHANES con mortalidad enlazada; baseline PhenoAge.
- Producto gratuito, sin registro, sin almacenar datos.
- Entrada: PDF de analítica, con pantalla de revisión obligatoria antes del cálculo.
- Clásico antes que deep learning.

Las decisiones aún abiertas están en `ESTADO.md`.
