# Primary novelty review

Documento de trabajo para falsar la novedad de **Adaptive Cost-Aware Routing with Learning Value**. Estado vigente: consolidation checkpoint de Decision 005 (2026-09-11), antes de la siguiente fase de búsqueda de novedad. La hipótesis amplia original ya no es defendible. La línea permanece activa; su novedad no está establecida.

## Evidencia comunicada de la segunda revisión

Este apartado conserva los resultados de la segunda revisión aportados por el investigador, originalmente sin verificación independiente. Decision 005 añade las conclusiones de consolidación comunicadas y la identificación de los PDFs locales; no supone una nueva verificación externa. La actualización asociada a Decision 004 incorpora abajo dos trabajos verificados y sus entradas en `references/bibliography.bib`; la trazabilidad de los demás antecedentes sigue pendiente. Se distinguen los antecedentes comunicados, la evidencia verificada, la interpretación y las hipótesis del proyecto.

- **Active Learning** no se limita a uncertainty sampling ni a incertidumbre epistémica. Expected Error Reduction y enfoques de Value of Information pueden evaluar explícitamente la reducción esperada del error predictivo futuro tras adquirir supervisión y actualizar el aprendiz. El principio «coste de consulta + reducción esperada del error futuro» ya existe y no es una afirmación de novedad.
- **Sequential Learning to Defer** puede considerar consecuencias a largo plazo de las decisiones actuales. No debe caracterizarse universalmente L2D como myopic.
- **Active Knowledge Distillation** incluye consultas al teacher sensibles al coste y mejora del student. No es necesariamente offline ni pool-based.
- **Value of Information y teoría secuencial de decisión** pueden ser suficientemente generales para representar el problema propuesto; no se afirma que sean incapaces de hacerlo.
- **Dual Control / POMDP** proporciona marcos generales de decisión secuencial. La dificultad computacional de sus soluciones genéricas no constituye evidencia de novedad.

## Evidencia por trabajo — Decision 004 y consolidación de Decision 005

### Gao & Koller (2011)

**Active Classification based on Value of Classifier** (`gao2011active`). El artículo realiza selección específica por instancia, en tiempo de inferencia, entre clasificadores heterogéneos previamente entrenados. Evaluarlos tiene un coste computacional explícito. El criterio value-of-classifier contrapone el beneficio esperado para el estado de clasificación actual al coste de evaluación. Observar una respuesta modifica el posterior de la instancia actual; el procedimiento no actualiza los parámetros de un predictor barato para instancias futuras. Véanse las secciones 1 y 3 del [artículo](https://proceedings.neurips.cc/paper_files/paper/2011/file/303ed4c69846ab36c2904d3ba8573050-Paper.pdf).

**Interpretación conceptual:** `Delta_immediate - C`. Es una correspondencia con nuestra notación, no una reproducción literal: el artículo valora el estado posterior y pondera el coste; expresar mejora supone compararlo con el estado actual. La adquisición de clasificadores para la instancia actual sensible al coste no es novedosa.

### Roy & McCallum (2001)

**Toward Optimal Active Learning through Monte Carlo Estimation of Error Reduction** (`roy2001toward`). Selecciona consultas de etiquetado según el error futuro esperado tras incorporar la etiqueta y reentrenar/actualizar el aprendiz. La reducción explícita del error predictivo futuro causada por aprender es, por tanto, un antecedente establecido y no debe reivindicarse como novedosa. La consulta adquiere datos para aprender; no elige operativamente entre un predictor barato y otro costoso para resolver la instancia actual. Véanse las secciones 1 y 2 del [artículo](https://groups.csail.mit.edu/rrg/papers/icml01.pdf).

**Interpretación conceptual:** `Delta_learning - C_label`. El término de coste expresa aquí el recurso de etiquetado en nuestra comparación conceptual; no atribuye al artículo una ecuación literal de beneficio menos coste variable por consulta. Su criterio selecciona el menor error futuro esperado tras actualizar.

### Kapoor, Horvitz & Basu (2007)

Según la conclusión comunicada por el investigador, su formulación de supervisión selectiva decision-theoretic incluye coste explícito de etiquetado y coste esperado de clasificación errónea durante el uso del clasificador. Valora consecuencias futuras de aprender, pero formula adquisición de supervisión/active learning, no routing operacional entre modelos. El título exacto y el venue no están establecidos en la documentación local consultada; no se crea una entrada BibTeX. El PDF local *Active Learning with Gaussian Processes for Object Categorization*, de Kapoor, Grauman, Urtasun y Darrell, es otro trabajo y no verifica este antecedente.

### ThriftyDAgger — Hoque et al. (CoRL 2021)

**ThriftyDAgger: Budget-Aware Novelty and Risk Gating for Interactive Imitation Learning**. PDF local: `ThriftyDAgger_hoque22a.pdf`; la primera página identifica CoRL 2021, aunque el nombre del archivo contiene `22a`. La intervención solicitada por el robot controla el sistema actual y genera demostraciones usadas para actualizar la política del robot. Es, por tanto, un antecedente de una intervención que sirve a la tarea presente y al entrenamiento posterior.

El gating se basa en novedad/riesgo y un presupuesto de intervenciones. Según la conclusión consolidada, no valora explícitamente el beneficio esperado de aprendizaje futuro de la intervención particular al decidir solicitarla. **Queda invalidada cualquier afirmación amplia de novedad basada en que una intervención experta sirve al control actual y al entrenamiento posterior de la política autónoma.** Esa doble función no equivale a valorar explícitamente su efecto de actualización en la decisión.

### TRACER — Rida (preprint 2026)

**TRACER: Trace-Based Adaptive Cost-Efficient Routing for LLM Classification**. PDF local: `Trace-Based Adaptive Cost-Efficient Routing for LLM Classification.pdf`, identificado como preprint/work in progress, arXiv:2604.14531v1, 16 April 2026. Es un antecedente arquitectónico extremadamente próximo: un surrogate barato atiende entradas aceptadas y un LLM teacher atiende las diferidas. Cada consulta al teacher produce una traza reutilizada para reentrenar el surrogate, creando un ciclo de aprendizaje continuo.

**TRACER invalida cualquier reivindicación amplia de novedad de reutilizar consultas diferidas al teacher para entrenar y mejorar continuamente el modelo barato.** El routing usa acuerdo predicho con el teacher/confianza y una restricción de paridad. Según la conclusión consolidada, la decisión no incorpora explícitamente cuánto se espera que la consulta actual mejore el rendimiento futuro del surrogate. Considerar el aprendizaje futuro en el diseño del sistema no equivale a valorar el efecto esperado de cada actualización al decidir consultar.

### Pregunta PRIMARY y estructura candidata

Dado un predictor barato adaptable $F$ y un teacher costoso $D$, ¿cómo decidir si consultar a $D$ para la muestra actual cuando esa misma consulta puede mejorar la predicción operacional actual y devolver supervisión que actualiza $F$, cambiando el coste predictivo/de routing futuro?

```text
query D iff
Delta_now(S_t,x_t) + gamma Delta_adapt(S_t,x_t) > C_D
```

`Delta_now` y `Delta_adapt` corresponden a `Delta_pred` y `Delta_learn` en las notas y el manuscrito. `Delta_adapt` es una diferencia de valor de continuación causada por actualizar el predictor barato; puede incluir pérdida predictiva y costes futuros de routing. Se conserva la dependencia contextual del coste de consulta de la formulación existente. Esta descomposición es un **resultado estructural candidato, NO un teorema**; su identificación con la comparación general de valores de acción requiere las justificaciones pendientes ya descritas en el documento matemático.

La hipótesis restante exige que la decisión de routing **valore explícitamente ambos efectos de la misma consulta**. No basta con que el sistema use esa consulta para predecir y aprender: ThriftyDAgger y TRACER ya impiden atribuir novedad a esa arquitectura general.

### Verificación bibliográfica

Los títulos y autores se comprobaron en los artículos. Año y publicación se corroboraron en los [proceedings de NIPS 2011](https://proceedings.neurips.cc/paper_files/paper/2011/hash/303ed4c69846ab36c2904d3ba8573050-Abstract.html) y en la [lista de publicaciones de McCallum](https://people.cs.umass.edu/~mccallum/publications-by-topic.html), que identifica ICML-2001. Esta última usa la variante de título «Sampling Estimation»; la entrada conserva «Monte Carlo Estimation», impreso en el PDF. Se omiten DOI, páginas, número de fascículo, editorial y editores al no haberse verificado en las fuentes consultadas. Las URLs incluidas son las de los artículos consultados.

## Interpretación actual y comparación conceptual

La hipótesis amplia original —routing adaptativo barato/costoso, competencia local, coste de consulta, routing online/no estacionario, exploración y valor futuro de información— ya no es defendible. Future value en sí no es novedoso: expected-error-reduction active learning, decision-theoretic active learning, sequential learning-to-defer, information-directed routing y marcos genéricos de decisión secuencial ya consideran efectos futuros. No se atribuyen propiedades universales a familias enteras a partir de un ejemplo.

Se distinguen cuatro aspectos: beneficio operacional de consultar ahora; valor de información para efectos futuros; actualización efectiva del aprendiz con lo consultado; y valoración explícita de esa actualización en la decisión de routing. La tabla usa las conclusiones consolidadas y los documentos locales; no demuestra ausencia de equivalentes. «Futuro considerado» no implica un término de valor esperado de actualización en el gating.

| Trabajo / familia | Operational routing? | Consultation/query cost? | Current-query benefit? | Learner updated from query? | Future effect considered? | Future learner-update value explicitly enters routing decision? |
| --- | --- | --- | --- | --- | --- | --- |
| Gao & Koller (2011) | Sí, adquisición de clasificadores en inferencia | Coste computacional explícito | Información para clasificar la instancia actual | No; clasificadores fijos | Información adicional dentro de la instancia; no adaptación entre muestras | No |
| Roy & McCallum (2001) | No; adquisición de supervisión | Recurso de etiquetado; no se atribuye coste variable por consulta | No como elección operacional barato/costoso | Sí | Error futuro tras reentrenar | Sí en selección de supervisión; no routing operacional |
| Kapoor, Horvitz & Basu (2007), resultado comunicado | No; supervisión selectiva | Coste explícito de etiquetado | No como routing operacional | Sí, en la formulación de supervisión | Coste esperado de errores durante el uso del clasificador | En la decisión de supervisión; no routing operacional |
| ThriftyDAgger (2021) | Sí, robot/humano para control | Presupuesto y carga de intervención | Control de la tarea actual | Sí, demostraciones actualizan la política | Aprendizaje posterior considerado en el sistema | No explícitamente para la intervención particular; gating por novedad/riesgo |
| TRACER (2026) | Sí, surrogate/teacher | Coste de llamadas al LLM | Teacher resuelve la entrada diferida | Sí, trazas para reentrenamiento | Ciclo de mejora continua | No explícitamente para la consulta particular; acuerdo/confianza y paridad |
| Sequential L2D / information-directed routing | Depende del trabajo | Depende del objetivo | Depende del trabajo | Pendiente por trabajo | Sí, efectos futuros según formulación | No inferir de «future value»; pendiente por trabajo |
| Active knowledge distillation | Consulta teacher/student; alcance operacional variable | En variantes cost-aware | Pendiente por trabajo | Sí | Puede considerar utilidad de aprendizaje | Pendiente por trabajo |
| Dual control / POMDP / decisión secuencial | Representable | Representable | Representable | Representable en el estado | Sí, valor de continuación | Representable; generalidad no prueba novedad |
| Online active learning / selective sampling / abstention | Posible equivalencia; auditoría prioritaria | Consulta o abstención según formulación | Puede evitar/reducir pérdida actual | Puede aprender de la etiqueta consultada | Objetivos secuenciales; precisar por trabajo | Principal cuestión pendiente; no se presupone ausencia |
| Dirección PRIMARY candidata | Sí | Coste incremental explícito | Puede mejorar la predicción actual | La misma consulta permite actualizar F | Cambio de coste predictivo/de routing futuro | Requisito explícito candidato; cálculo y garantías pendientes |

## Hipótesis de novedad de trabajo

> No direct equivalent has yet been identified that combines, within the same operational routing decision:
>
> 1. online routing between a cheap predictor and a costly predictor;
> 2. an explicit immediate cost of consulting the costly predictor;
> 3. an update of the cheap predictor using information returned by the costly predictor;
> 4. an explicit valuation, in the routing decision, of the continuation-value difference in future predictive/routing cost caused by that update.
>
> This remains a working novelty hypothesis and is still subject to falsification.

Esta conclusión describe sólo la revisión documentada hasta Decision 005; no demuestra inexistencia de equivalentes. No se reivindica novedad para teacher/student routing, costly deferral, entrenar con respuestas diferidas, mejora continua mediante trazas del teacher, ni intervención que controla y genera demostraciones. La cuestión pendiente es la internalización explícita del valor futuro de la actualización en la DECISIÓN.

## Amenaza prioritaria y decisiones abiertas

**Online active learning / selective sampling / abstention es la amenaza de novedad no resuelta de máxima prioridad.** Puede contener el problema matemáticamente equivalente: observar $x_t$; predecir autónomamente o consultar un oráculo con coste; consultar evita/reduce pérdida actual y proporciona una etiqueta que actualiza al aprendiz; optimizar pérdida predictiva acumulada más coste de consulta. Debe auditarse antes de reivindicar novedad.

El PDF local **Online Selective Classification with Limited Feedback**, de Gangrade, Kag, Cutkosky y Saligrama (2021, arXiv:2110.14243v1), documenta abstención online con feedback sólo al abstenerse y una comparación en términos de errores y abstenciones. Es un punto de partida concreto para la auditoría; esa descripción no establece equivalencia con nuestro objetivo ni valoración explícita del efecto de actualización. La auditoría debe distinguir esos aspectos y el protocolo de feedback.

El feedback de $Y_t$ sigue abierto: nunca observado, retrasado/ocasional o siempre observado. Es científicamente decisivo y no se fija aquí. El teacher es falible y actualizar con su respuesta puede perjudicar al student: `Delta_adapt` no se supone no negativo. Antes de avanzar matemáticamente debe fijarse el protocolo, sin anticiparlo en esta consolidación.

## Otros documentos locales

*Active Learning with Gaussian Processes for Object Categorization* (Kapoor, Grauman, Urtasun y Darrell, 2007) es un antecedente adyacente de adquisición activa de etiquetas con un aprendiz GP; no debe confundirse con Kapoor, Horvitz & Basu. *Active Learning Literature Survey* (Anita Krishnakumar, 2007) es material de contexto sobre active learning. No se establece una comparación detallada de estos documentos con la decisión PRIMARY. El inventario y el estado de PDFs/BibTeX se encuentran en [consolidation_inventory.md](consolidation_inventory.md).

## Resultados pendientes de demostrar

El objetivo de investigación es pasar de un principio general de decisión secuencial/VoI, mediante la estructura particular del routing predictivo adaptativo, a una regla computable e interpretable con garantías. Es un objetivo, no una contribución establecida. Debe determinarse si esa estructura permite una regla analítica o aproximadamente analítica más sencilla; ni la existencia de un umbral ni las garantías están demostradas.

Continúa pendiente contrastar los cuatro requisitos conjuntamente con trabajos verificados, incluidos contextual bandits y otras formulaciones relacionadas. Si no se identifica una diferencia metodológica defendible, se reconsiderará la formulación antes de implementar algoritmos o invertir esfuerzo experimental. La revisión narrativa del paper sólo se completará con referencias verificadas.
