# Primary novelty review

Documento de trabajo para falsar la novedad de **Adaptive Cost-Aware Routing with Learning Value**. Estado vigente: Decision 006 (2026-09-11), targeted selective-sampling audit completed. La búsqueda bibliográfica amplia queda pausada; el siguiente paso es definir el protocolo operacional/de feedback antes de desarrollar un modelo matemático. La hipótesis amplia original ya no es defendible. La línea permanece activa; su novedad no está establecida.

## Evidencia comunicada de la segunda revisión

Este apartado conserva los resultados de la segunda revisión aportados por el investigador, originalmente sin verificación independiente. Decision 005 añade las conclusiones de consolidación comunicadas y la identificación de los PDFs locales; no supone una nueva verificación externa. La actualización asociada a Decision 004 incorpora abajo dos trabajos verificados y sus entradas en `references/bibliography.bib`; el inventario registra las verificaciones bibliográficas posteriores, incluidas las de Decision 006. Se distinguen los antecedentes comunicados, la evidencia verificada, la interpretación y las hipótesis del proyecto.

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

Según la conclusión comunicada por el investigador, su formulación de supervisión selectiva decision-theoretic incluye coste explícito de etiquetado y coste esperado de clasificación errónea durante el uso del clasificador. Valora consecuencias futuras de aprender, pero formula adquisición de supervisión/active learning, no routing operacional entre modelos. **Selective Supervision: Guiding Supervised Learning with Decision-Theoretic Active Learning** (`kapoor2007selective`), IJCAI-07, pp. 877–882, ya está verificado en el PDF local `Guiding Supervised Learning with Decision-Theoretic Active Learning.pdf` y registrado en BibTeX. El PDF local *Active Learning with Gaussian Processes for Object Categorization*, de Kapoor, Grauman, Urtasun y Darrell, es otro trabajo y no verifica este antecedente.

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

## Targeted audit: selective sampling and noisy experts

Auditoría dirigida cerrada en Decision 006. Las conclusiones siguientes consolidan los cuatro trabajos verificados indicados por el investigador y su evidencia local, junto con Gangrade (2021), TRACER y ThriftyDAgger ya revisados. No constituyen una revisión exhaustiva de toda la literatura. Los nombres exactos de PDF y la procedencia de los metadatos se registran en el inventario.

### Sogawa et al. (2013)

**Active learning for noisy oracle via density power divergence** (`sogawa2013active`), *Neural Networks* 46, 133–143, DOI 10.1016/j.neunet.2013.05.007. Es active learning pool-based con oráculo explícitamente ruidoso. La selección de consultas pertenece a la familia expected-error-reduction y deriva un criterio asintótico de error esperado de estimación (introducción y análisis asintótico de la sección 3).

Por tanto, **valor futuro del aprendizaje con supervisión ruidosa no es novedoso**. La consulta adquiere supervisión para el modelo, no reemplaza una predicción operacional para la muestra actual. No resuelve el problema combinado de routing para inferencia actual y adaptación futura. Su criterio de error esperado no se identifica con nuestra diferencia de valor de continuación ni establece que modele explícitamente un valor de adaptación negativo por consulta.

### Sekhari et al. (2023)

**Selective Sampling and Imitation Learning via Online Regression** (`sekhari2023selective`), *Advances in Neural Information Processing Systems* 36, NeurIPS 2023 Main Conference Track. Se registra como publicación NeurIPS 2023, no meramente como preprint. La copia local es arXiv:2307.04998v1; la publicación y el volumen corresponden a los metadatos verificados aportados por el investigador.

Estudia selective sampling online e imitation learning interactivo con feedback experto ruidoso, un oráculo de regresión online que se actualiza sólo en muestras consultadas, y garantías fuertes de regret y complejidad de consultas. En **SAGE**, el aprendiz primero ejecuta/predice y después decide si consultar (Algorithm 1, líneas 4 y 6–9 de la copia local). En **RAVIOLI**, se ejecuta la acción del aprendiz y el entorno transiciona antes de consultar feedback experto (Algorithm 3). El feedback experto no reemplaza operacionalmente la acción actual del aprendiz.

La regla de consulta usa margen/incertidumbre, no una estimación explícita de la diferencia de continuación inducida por la actualización particular que se está considerando. Esto no significa que el método ignore el aprendizaje futuro: sus consultas y garantías secuenciales lo tienen como propósito. La sección 5 también contempla múltiples expertos; no debe reducirse el antecedente a un único experto.

### Hanneke & Yang (2021)

**Toward a General Theory of Online Selective Sampling: Trading Off Mistakes and Queries** (`hanneke2021toward`), AISTATS 2021, PMLR 130, 3997–4005. Ofrece una teoría general del compromiso óptimo entre errores acumulados y consultas. Incluye estrategias no triviales de búsqueda de información como **PickyActive** y **PickySplitting**; no es correcto describir globalmente selective sampling como myopic ni como ajeno al aprendizaje futuro.

El protocolo predice primero y opcionalmente consulta después la etiqueta verdadera (abstract e introducción). La consulta no sustituye la predicción actual. La formulación principal es realizable, con etiquetas verdaderas perfectas. Esta propiedad es de este trabajo, no de toda la familia. El objetivo global errores/consultas y la búsqueda de información no se identifican automáticamente con un término explícito de valor de continuación de una actualización particular en una decisión operacional anterior a la respuesta.

### Dekel, Gentile & Sridharan (2012)

**Selective Sampling and Active Learning from Single and Multiple Teachers** (`dekel2012selective`), *Journal of Machine Learning Research* 13, 2655–2697. Estudia selective sampling online con instancias adaptativas/adversariales, un aprendiz tipo ridge regression, un teacher estocástico y múltiples teachers con competencia local/regiones de experiencia desconocidas. El coste de consulta es explícito; las etiquetas consultadas actualizan al aprendiz para rondas futuras. Los teachers pueden ser poco fiables, particularmente fuera de su experiencia (secciones 1–3).

Los experimentos informan que más etiquetas de teachers pueden ser perjudiciales; la significación estadística de esa observación se limita allí a los escenarios de pocos teachers (p. 2681). **Supervisión falible, competencia local, consulta selectiva a teachers y perjuicio empírico por supervisión adicional no son individualmente novedosos.** Observar ese perjuicio no equivale a modelar explícitamente una diferencia negativa de valor de continuación en la regla de consulta.

El aprendiz predice antes de decidir si consultar, tanto en la formulación inicial como en la de múltiples teachers (pp. 2655 y 2669–2670). La consulta no reemplaza la predicción ya emitida. La regla se basa en incertidumbre/estabilidad, no en un valor de continuación explícito causado por la futura actualización particular.

### Corrección terminológica

Se distinguen tres afirmaciones:

- **A.** El aprendizaje futuro es una consecuencia buscada de consultar.
- **B.** La política de consulta puede explorar o ser globalmente no myopic.
- **C.** La consecuencia futura esperada de la actualización específica inducida por la consulta actual entra explícitamente en la decisión de routing operacional actual.

A y B ya tienen antecedentes; no prueban ni excluyen C. No se afirmará que selective sampling sea globalmente myopic, ignore consecuencias futuras, presuponga siempre teachers perfectos, ni que ningún trabajo previo considere información experta perjudicial. La cuestión candidata es C junto con sustitución operacional antes de la respuesta final, no el aprendizaje futuro por sí solo.

## Interpretación actual y comparación conceptual

La hipótesis amplia original —routing adaptativo barato/costoso, competencia local, coste de consulta, routing online/no estacionario, exploración y valor futuro de información— ya no es defendible. Future value en sí no es novedoso: expected-error-reduction active learning, decision-theoretic active learning, sequential learning-to-defer, information-directed routing y marcos genéricos de decisión secuencial ya consideran efectos futuros. No se atribuyen propiedades universales a familias enteras a partir de un ejemplo.

La matriz separa temporalidad, sustitución operacional, aprendizaje y valoración explícita de una actualización. **ND** significa que la propiedad específica no queda establecida en la evidencia auditada, no que se haya probado su ausencia. **N/A** indica adquisición de entrenamiento sin respuesta operacional actual. «Actualiza» en una fila de selective sampling se refiere al feedback consultado; no implica que ese feedback sirviera como respuesta operacional. El valor futuro genérico no sustituye la columna 5. La columna 7 exige modelado explícito del valor de adaptación negativo, no sólo ruido o perjuicio observado.

| Trabajo | 1. Decision before final operational response? | 2. Expensive expert replaces cheap response now? | 3. Same queried response updates learner? | 4. Immediate current-query benefit explicitly valued? | 5. Future update-induced value explicitly enters query/routing rule? | 6. Noisy/fallible teacher? | 7. Negative future adaptation value explicitly modeled? | 8. Cumulative query cost / regret objective? | 9. Multiple/local experts supported? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Gao & Koller 2011 | Sí | Información adicional; no sustitución F/D estricta | No, clasificadores fijos | Sí, value-of-classifier | No, no actualización entre muestras | ND | No, no actualización | Coste de inferencia por instancia | Múltiples clasificadores heterogéneos |
| Roy & McCallum 2001 | N/A, pool/entrenamiento | No | Sí, supervisión | No operacional | Sí, error futuro esperado; no continuación de routing | ND | ND | Recurso de etiquetas; no atribuir suma pérdida+coste variable | ND |
| Kapoor et al. 2007 | N/A, supervisión | No | Sí, supervisión | No operacional | Sí, valor de supervisión/error de uso; no continuación de routing | ND | ND | Coste de etiquetado y uso del clasificador | ND |
| Sogawa et al. 2013 | N/A, pool | No | Sí, supervisión | No operacional | Error esperado de estimación asintótico; no continuación de routing | Sí | ND; robustez no equivale a valor negativo explícito | Error de estimación/adquisición; no objetivo operacional conjunto | ND |
| Sekhari et al. 2023 | No; acción antes de consulta | No | Sí, feedback consultado | No como sustitución actual | No término explícito; margen/incertidumbre | Sí | ND | Regret y complejidad de consultas | Sí, extensión sección 5 |
| Hanneke & Yang 2021 | No; predicción antes de consulta | No | Sí, información para aprendizaje futuro | No como sustitución actual | Búsqueda de información global; no término C establecido | No en formulación principal realizable | No establecido | Compromiso acumulado errores/consultas | No en formulación principal |
| Dekel et al. 2012 | No; predicción antes de consulta | No | Sí, feedback consultado | No como sustitución actual | No término explícito; incertidumbre/estabilidad | Sí | Perjuicio observado, no término de continuación explícito | Coste unitario por consulta; regret y número de consultas | Sí, competencia local desconocida |
| Gangrade et al. 2021 | Abstención antes del feedback | Abstención sin error; no especifica respuesta de D | Sí, feedback al abstenerse | Errores/abstenciones; no diferencia de riesgo F/D explícita establecida | No término C establecido en revisión documentada | Etiqueta verdadera al abstenerse | ND | Errores y exceso de abstenciones | ND |
| ThriftyDAgger 2021 | Sí, gating antes del control | Sí, intervención humana | Sí, demostraciones | Riesgo/novedad; no comparación explícita de riesgo F/D establecida | No explícito para la intervención particular | ND | ND | Presupuesto/carga de intervención | ND |
| TRACER 2026 | Sí | Sí | Sí, trazas | Acuerdo/confianza y paridad; no diferencia de riesgo F/D explícita | No explícito para la consulta particular | Sí, ruido de etiquetas del teacher documentado | ND | Coste de llamadas y paridad; no equiparar a regret acumulado | ND |
| PRIMARY candidata | Sí, requisito | Sí, requisito | Sí, requisito | Sí, consecuencia inmediata | Sí, diferencia de continuación de esa actualización | Sí | Signo no restringido; modelo exacto pendiente | Coste predictivo/de consulta secuencial candidato | Dos predictores; múltiples experts no fijados |

Las familias generales (sequential L2D, information-directed routing, active knowledge distillation y dual control/POMDP) conservan las cautelas descritas arriba: no se les asigna un «no» universal por falta de una comparación individual en esta tabla. La representabilidad en un marco secuencial general no demuestra novedad.

## Hipótesis de novedad de trabajo

> No direct equivalent has yet been identified after targeted audit that jointly satisfies all six properties:
>
> 1. the routing decision is made before the final operational response;
> 2. the costly predictor D operationally replaces F on the current sample;
> 3. the same D response updates F;
> 4. the policy values the immediate predictive consequence;
> 5. the policy explicitly values the future continuation-value change caused by that specific update;
> 6. D may be fallible, so the adaptation value may be negative.
>
> This remains a candidate novelty region, not an established novelty claim or proof that no prior method exists.

Esta conclusión describe el alcance de Decision 006. Ninguno de los componentes —valor esperado de aprendizaje futuro, supervisión falible, consultas selectivas, compromiso errores/consultas, actualización online, múltiples expertos locales, coste de consulta o perjuicio empírico por información adicional— es individualmente novedoso. TRACER y ThriftyDAgger siguen descartando la novedad de la doble función operacional/de aprendizaje por sí sola.

## Scientific checkpoint

The novelty hypothesis has been further narrowed after a targeted audit of online selective sampling, noisy-oracle active learning, and interactive imitation learning. Expected future model improvement under noisy supervision, cumulative mistake-query trade-offs, selective querying with noisy expert feedback, online learner updates, and multiple locally competent teachers are all established independently in prior work. The remaining candidate problem is more specific: a routing decision made before the final operational response, where choosing a costly predictor both replaces the cheap prediction on the current sample and produces supervision that changes the cheap predictor, while the policy explicitly values both the immediate inference consequence and the continuation-value change caused by that update. The expensive predictor may be fallible, so the adaptation value is not assumed nonnegative. No direct equivalent satisfying all of these properties jointly has yet been identified after targeted audit; this remains a candidate novelty region rather than an established novelty claim.

## Protocolo pendiente y pausa de búsqueda amplia

La auditoría dirigida queda cerrada; la búsqueda bibliográfica amplia se pausa. El siguiente paso es definir el protocolo operacional/de feedback exacto antes de desarrollar un modelo matemático. Esto no certifica exhaustividad bibliográfica ni resuelve toda posible equivalencia con abstención. Gangrade (2021) permanece en la comparación como antecedente de abstención con feedback limitado, sin atribuirle una respuesta operacional de teacher ni una valoración específica de actualización no establecidas en la revisión.

El feedback de $Y_t$ sigue abierto: nunca observado, retrasado/ocasional o siempre observado. No se fijan aún la definición exacta de `Delta_adapt`, el operador `U` ni una familia como RLS o regresión logística Bayesiana. El teacher es falible y actualizar con su respuesta puede perjudicar al student. Las ecuaciones existentes son conceptuales y la descomposición candidata no es un teorema.

## Otros documentos locales

*Active Learning with Gaussian Processes for Object Categorization* (Kapoor, Grauman, Urtasun y Darrell, 2007) es un antecedente adyacente de adquisición activa de etiquetas con un aprendiz GP; no debe confundirse con Kapoor, Horvitz & Basu. *Active Learning Literature Survey* (Anita Krishnakumar, 2007) es material de contexto sobre active learning. No se establece una comparación detallada de estos documentos con la decisión PRIMARY. El inventario y el estado de PDFs/BibTeX se encuentran en [consolidation_inventory.md](consolidation_inventory.md).

## Resultados pendientes de demostrar

El objetivo de investigación es pasar de un principio general de decisión secuencial/VoI, mediante la estructura particular del routing predictivo adaptativo, a una regla computable e interpretable con garantías. Es un objetivo, no una contribución establecida. Debe determinarse si esa estructura permite una regla analítica o aproximadamente analítica más sencilla; ni la existencia de un umbral ni las garantías están demostradas.

El contraste dirigido de los seis requisitos queda documentado arriba, sin establecer novedad. La búsqueda amplia queda pausada y la prioridad inmediata es precisar el protocolo; el programa teórico sólo podrá retomarse después. Si no se identifica una diferencia metodológica defendible, se reconsiderará la formulación antes de implementar algoritmos o invertir esfuerzo experimental. La revisión narrativa del paper sólo se completará con referencias verificadas.
