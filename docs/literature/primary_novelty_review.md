# Primary novelty review

Documento de trabajo para falsar la novedad de **Adaptive Cost-Aware Routing with Learning Value**. La segunda revisión, deliberadamente orientada a falsar la hipótesis inicial, la ha refinado a una forma más estrecha. La línea permanece activa; su novedad no está establecida.

## Evidencia comunicada de la segunda revisión

Este apartado recoge los resultados de la segunda revisión aportados por el investigador, originalmente sin verificación independiente. La actualización asociada a Decision 004 incorpora abajo dos trabajos verificados y sus entradas en `references/bibliography.bib`; la trazabilidad de los demás antecedentes sigue pendiente. Se distinguen los antecedentes comunicados, la evidencia verificada, la interpretación y las hipótesis del proyecto.

- **Active Learning** no se limita a uncertainty sampling ni a incertidumbre epistémica. Expected Error Reduction y enfoques de Value of Information pueden evaluar explícitamente la reducción esperada del error predictivo futuro tras adquirir supervisión y actualizar el aprendiz. El principio «coste de consulta + reducción esperada del error futuro» ya existe y no es una afirmación de novedad.
- **Sequential Learning to Defer** puede considerar consecuencias a largo plazo de las decisiones actuales. No debe caracterizarse universalmente L2D como myopic.
- **Active Knowledge Distillation** incluye consultas al teacher sensibles al coste y mejora del student. No es necesariamente offline ni pool-based.
- **Value of Information y teoría secuencial de decisión** pueden ser suficientemente generales para representar el problema propuesto; no se afirma que sean incapaces de hacerlo.
- **Dual Control / POMDP** proporciona marcos generales de decisión secuencial. La dificultad computacional de sus soluciones genéricas no constituye evidencia de novedad.

## Evidencia verificada — actualización asociada a Decision 004

### Gao & Koller (2011)

**Active Classification based on Value of Classifier** (`gao2011active`). El artículo realiza selección específica por instancia, en tiempo de inferencia, entre clasificadores heterogéneos previamente entrenados. Evaluarlos tiene un coste computacional explícito. El criterio value-of-classifier contrapone el beneficio esperado para el estado de clasificación actual al coste de evaluación. Observar una respuesta modifica el posterior de la instancia actual; el procedimiento no actualiza los parámetros de un predictor barato para instancias futuras. Véanse las secciones 1 y 3 del [artículo](https://proceedings.neurips.cc/paper_files/paper/2011/file/303ed4c69846ab36c2904d3ba8573050-Paper.pdf).

**Interpretación conceptual:** `Delta_immediate - C`. Es una correspondencia con nuestra notación, no una reproducción literal: el artículo valora el estado posterior y pondera el coste; expresar mejora supone compararlo con el estado actual. La adquisición de clasificadores para la instancia actual sensible al coste no es novedosa.

### Roy & McCallum (2001)

**Toward Optimal Active Learning through Monte Carlo Estimation of Error Reduction** (`roy2001toward`). Selecciona consultas de etiquetado según el error futuro esperado tras incorporar la etiqueta y reentrenar/actualizar el aprendiz. La reducción explícita del error predictivo futuro causada por aprender es, por tanto, un antecedente establecido y no debe reivindicarse como novedosa. La consulta adquiere datos para aprender; no elige operativamente entre un predictor barato y otro costoso para resolver la instancia actual. Véanse las secciones 1 y 2 del [artículo](https://groups.csail.mit.edu/rrg/papers/icml01.pdf).

**Interpretación conceptual:** `Delta_learning - C_label`. El término de coste expresa aquí el recurso de etiquetado en nuestra comparación conceptual; no atribuye al artículo una ecuación literal de beneficio menos coste variable por consulta. Su criterio selecciona el menor error futuro esperado tras actualizar.

### Hipótesis de acoplamiento, todavía bajo falsación

La comparación candidata del proyecto es `Delta_immediate + gamma * Delta_learning - C_teacher`: la **misma consulta costosa** puede mejorar la predicción de la instancia operacional actual y aportar supervisión que actualiza el predictor barato, cambiando su rendimiento/coste futuro. Los nombres conceptuales `Delta_immediate` y `Delta_learning` corresponden a `Delta_pred` y `Delta_learn` en la formulación del proyecto; no se identifica el error predictivo de los antecedentes con todo nuestro coste futuro acumulado.

Ni el valor futuro del aprendizaje ni la adquisición de clasificadores para la instancia actual son novedosos por sí solos. Su acoplamiento descrito sigue siendo únicamente un posible vacío metodológico bajo falsación activa; estos dos trabajos no demuestran su novedad. Antes de continuar el desarrollo matemático debe fijarse el protocolo de observación y feedback indicado en Decision 004.

### Verificación bibliográfica

Los títulos y autores se comprobaron en los artículos. Año y publicación se corroboraron en los [proceedings de NIPS 2011](https://proceedings.neurips.cc/paper_files/paper/2011/hash/303ed4c69846ab36c2904d3ba8573050-Abstract.html) y en la [lista de publicaciones de McCallum](https://people.cs.umass.edu/~mccallum/publications-by-topic.html), que identifica ICML-2001. Esta última usa la variante de título «Sampling Estimation»; la entrada conserva «Monte Carlo Estimation», impreso en el PDF. Se omiten DOI, páginas, número de fascículo, editorial y editores al no haberse verificado en las fuentes consultadas. Las URLs incluidas son las de los artículos consultados.

## Interpretación actual y comparación conceptual

Future value, information gain y reducción esperada del riesgo futuro aparecen en distintas literaturas. El posible vacío no es el requisito 4 por sí solo: se investiga la combinación en la que la misma consulta costosa resuelve la inferencia actual y proporciona información para mejorar el predictor barato que resolverá observaciones futuras.

La tabla es una orientación conceptual provisional basada en los resultados comunicados, no una clasificación exhaustiva ni una prueba de ausencia de trabajos equivalentes. Cada caracterización queda pendiente de trazabilidad bibliográfica por trabajo.

| Familia | 1. Online operational routing between predictors | 2. Explicit consultation cost | 3. Consultation updates the cheap predictor | 4. Routing/query decision values the future effect of that update |
| --- | --- | --- | --- | --- |
| Learning to Defer / Model Routing | Typically, entre predicción autónoma y alternativa | Frecuente; depende de la formulación | No es un requisito general; depende del método | No es un requisito general; deben examinarse variantes |
| Sequential Learning to Defer | Sí, en formulaciones secuenciales; alcance variable | Depende del objetivo | No necesariamente; puede cambiar el entorno o la información | Puede valorar efectos futuros, pero no necesariamente la actualización del predictor barato |
| Active Learning / Selective Sampling | No en el mismo sentido operativo de elegir la respuesta actual entre predictores | Según la formulación, coste o presupuesto | Actualiza al aprendiz con supervisión; no necesariamente con otro predictor | Depende del criterio; no se limita a incertidumbre |
| Expected Error Reduction / Value of Information Active Learning | En general, adquisición de supervisión, no routing operativo en el mismo sentido | Puede incluirlo explícitamente | Sí, mediante la supervisión adquirida | Sí, puede valorar reducción esperada de error futuro |
| Active Knowledge Distillation | Consulta teacher/student; no necesariamente elección de la respuesta operativa actual | Explícito en variantes cost-aware | Sí, mejora del student con información del teacher | Puede valorar utilidad futura de aprendizaje; depende del método |
| Dual Control / POMDP | Representable en general; no especialización obligatoria a routing | Representable en el objetivo | Representable en la dinámica del estado | Representable en el valor de continuación |
| Proposed research direction | Requisito de la formulación candidata | Coste incremental explícito | La misma consulta permite actualizar el predictor barato | Valoración explícita candidata; cálculo y garantías pendientes |

En sequential L2D, el valor futuro puede surgir de cambios en estados del entorno, intervenciones o decisiones posteriores. Aquí interesa específicamente el valor de actualizar el predictor autónomo barato con la predicción diferida. Esta distinción más estrecha todavía debe verificarse frente a literatura adicional; no excluye que existan formulaciones L2D con ese mecanismo.

Las preguntas que guían la comparación son:

- Active Knowledge Distillation: «¿Consultar al teacher porque esta muestra es valiosa para mejorar al student?»
- Routing tradicional: «¿Consultar al predictor costoso porque ofrece una mejor respuesta ahora?»
- Dirección propuesta: «¿Consultar al teacher porque el beneficio predictivo inmediato y el beneficio futuro de aprendizaje combinados justifican su coste?»

Estas preguntas delimitan el análisis; no son definiciones exhaustivas de esas literaturas.

## Hipótesis de novedad de trabajo

> No direct equivalent has yet been identified that combines, within the same operational routing decision:
>
> 1. online routing between a cheap predictor and a costly predictor;
> 2. an explicit immediate cost of consulting the costly predictor;
> 3. an update of the cheap predictor using information returned by the costly predictor;
> 4. an explicit valuation of the expected reduction in future predictive risk caused by that update.
>
> This remains a working novelty hypothesis and is still subject to falsification.

Esta conclusión describe el alcance de la segunda revisión comunicada, no demuestra inexistencia de equivalentes. No se sostiene que el valor futuro de aprendizaje esté ausente de los métodos existentes.

## Resultados pendientes de demostrar

El objetivo de investigación es pasar de un principio general de decisión secuencial/VoI, mediante la estructura particular del routing predictivo adaptativo, a una regla computable e interpretable con garantías. Es un objetivo, no una contribución establecida. Debe determinarse si esa estructura permite una regla analítica o aproximadamente analítica más sencilla; ni la existencia de un umbral ni las garantías están demostradas.

Continúa pendiente contrastar los cuatro requisitos conjuntamente con trabajos verificados, incluidos contextual bandits y otras formulaciones relacionadas. Si no se identifica una diferencia metodológica defendible, se reconsiderará la formulación antes de implementar algoritmos o invertir esfuerzo experimental. La revisión narrativa del paper sólo se completará con referencias verificadas.
