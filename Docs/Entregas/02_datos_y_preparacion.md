# Entrega 02: Datos y preparación

> **BORRADOR.** Notas por apartado para redactar en la próxima sesión. Falta Gold, la muestra y las cifras finales.

## 1. Qué datos necesita el producto

- **Observación:** un adulto de 18 a 79 años de NHANES, con examen físico y seguimiento de mortalidad. Una fila = una persona (cada ciclo es una muestra independiente; nadie se repite).
- **Imprescindibles:**
  - Edad y sexo.
  - Analítica de rutina española: hemograma, glucosa, urea, creatinina, ácido úrico, colesterol total, HDL, triglicéridos (en ayunas), AST, ALT, GGT, fosfatasa alcalina, bilirrubina, sodio, potasio.
  - Resultado: fallecido sí/no y meses de seguimiento desde el examen (hasta 31/12/2019).
- **Deseables:**
  - Analítica frecuente pero no de rutina: HbA1c, calcio, fósforo, proteínas, albúmina, hierro, LDH, CPK, cloro, PCR, vitamina D, insulina, cociente albúmina/creatinina en orina.
  - Medidas que el usuario sabe: peso, talla (→ IMC), tensión, cintura.
  - Hábitos (modo avanzado, ~10 preguntas de botones): tabaco, alcohol (frecuencia y cantidad), actividad física, horas sentado, comida rápida, sueño.
- **Descartado (y por qué):** VO2 max y DXA (el usuario no los sabe, pocas defunciones); ferritina (solo mujeres 12-49 años); PSA y TSH (pocos ciclos); etnia (no se pide al usuario); autovaloraciones de dieta y salud (subjetivas).
- **Granularidad e histórico:** una medición por persona (transversal) + seguimiento de mortalidad. 10 ciclos bienales, 1999-2018. Seguimiento mediano 9,6 años.

## 2. Fuentes reales y viabilidad

- **NHANES continuo 1999-2018** (CDC): open data, ficheros `.xpt` por módulo y ciclo, descarga directa por URL. Población no institucionalizada de EE. UU.
- **Linked Mortality Files** (NCHS), versión pública: un `.dat` de ancho fijo por ciclo, seguimiento hasta 2019.
- **Acceso:** script de descarga (`src/pipeline/download_bronze.py`, lanzado desde `src.main`), reanudable, con manifiesto (URL, tamaño, fecha).
- **Cobertura:** 54.809 adultos de 18-79 años elegibles para mortalidad → 50.969 en el estudio, con 5.808 defunciones.
- **Actualización:** NHANES sigue publicando ciclos, pero 2017-2020 no tiene mortalidad pública. La mortalidad hasta 2022 existe, pero es de acceso restringido.
- **Estabilidad:** URLs de la CDC estables. Hubo una caída puntual del servidor de mortalidad, resuelta con reintentos.
- **Alternativa si NHANES no estuviera disponible:** UK Biobank (requiere solicitud y es de pago). NHANES III queda descartado por métodos de laboratorio distintos.

## 3. Uso, privacidad y datos personales

- NHANES es de dominio público y viene desidentificado; la mortalidad pública está perturbada por el NCHS para evitar reidentificación. No hay que anonimizar.
- **Minimización:** de ~1.000 variables descargadas solo se usan ~70; edad limitada a 18-79 (por encima, NHANES agrupa la edad).
- **En la app** (datos de salud, categoría especial RGPD): se procesa todo en memoria y no se almacena nada; se informa al usuario.

## 4. Del dato bruto al dato utilizable

| Capa | Qué es | Cifras |
|---|---|---|
| Bronze | Ficheros tal como los publica la CDC, una carpeta por ciclo | 400 ficheros, ~419 MB |
| Silver raw | Todos los ficheros unidos por persona (SEQN), alias renombrados, 10 ciclos apilados | 54.809 personas, 993 columnas |
| Silver clean | Población de estudio y variables candidatas limpias | 50.969 personas, 72 columnas |
| Gold | *Pendiente* | |

Transformaciones principales hasta Silver clean:
- Unión de ~25 ficheros por ciclo + mortalidad; DXA con imputación múltiple promediada.
- Alias entre ciclos (p. ej. HDL con 3 nombres) unificados antes de apilar.
- Exclusiones: sin examen físico (sin analítica), embarazadas.
- Correcciones oficiales de la CDC: creatinina 1999-2000 y 2005-2006; 13 analitos de 2017-2018 por cambio de analizador.
- Unidades de laboratorio español (urea, PCR en mg/L, cociente albúmina/creatinina).
- Triglicéridos solo con ayuno ≥ 8 h.
- Cuestionarios convertidos a respuestas de botón (preguntas saltadas = "nunca").
- Pesos muestrales combinados para los 10 ciclos.

**Gold (pendiente de definir):** qué significa cada fila, columnas principales y para qué se usan.

## 5. Riesgos y limitaciones (3-5 líneas)

Ideas a condensar:
- Población de referencia de EE. UU., no española.
- Cambios de método entre ciclos sin corrección oficial (fosfatasa alcalina y LDH en 1999-2000) y cambio de cuestionario de actividad en 2007.
- Seguimiento corto en los últimos ciclos (pocas defunciones en 2015-2018).
- Variables solo en parte de la muestra (subgrupo en ayunas, CPK, PCR sin 2011-2014).
- Si NHANES dejara de estar disponible: los datos ya descargados siguen siendo válidos; alternativa UK Biobank.

## Muestra de datos

*Pendiente:* ~100 filas del Gold en CSV (NHANES es de dominio público).

## Código

`.venv/Scripts/python -m src.main` reproduce todo: Bronze → Silver raw → Silver clean (→ Gold).
