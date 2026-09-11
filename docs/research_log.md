# Research log

Las decisiones anteriores conservan su contexto histórico. Decision 005 establece el estado científico vigente y sustituye las formulaciones de novedad más amplias de Decisions 003–004.

## Decision 001 — Elección de las líneas de investigación

Fecha: 2026-09-10.

La línea primaria es **Adaptive Cost-Aware Routing with Learning Value**. Se consideran dos modelos predictivos heterogéneos: uno barato y adaptable y otro más competente pero costoso. Consultar al segundo puede mejorar la predicción actual y aportar información para adaptar el primero. La decisión debe considerar el valor predictivo inmediato y el valor de aprendizaje futuro frente al coste de consulta; la acción presente puede modificar la competencia futura del modelo barato.

La línea secundaria es **Bayesian Cost-Aware Routing under Changing Operating Conditions**. Con modelos inicialmente fijos, separa la estimación de la competencia predictiva relativa de la toma de decisiones Bayesiana. Estudia cuándo los cambios de costes computacionales, de latencia o de error, priors de clase, composición poblacional o restricciones operativas permiten transformar analíticamente la regla óptima sin reentrenar el router.

Antes de implementar algoritmos debe realizarse una revisión bibliográfica rigurosa destinada a intentar falsar la novedad de la línea primaria. Si no puede identificarse con claridad una diferencia metodológica defendible respecto a learning-to-defer, model routing, contextual bandits, active learning, knowledge distillation y trabajos relacionados, la formulación primaria deberá reconsiderarse antes de invertir esfuerzo experimental. No se debe asumir novedad hasta completar esa revisión.

Label Switching no forma parte del método ni es un eje de investigación. Su relevancia se limita al antecedente metodológico de analizar cómo cambios en poblaciones, priors o probabilidades a posteriori transforman la regla Bayesiana y permiten derivar umbrales óptimos.

La primera etapa excluye LLM routing como problema principal, concept drift, imbalanced learning, aplicaciones SOC/NOC, múltiples expertos, grandes arquitecturas neuronales y código experimental. Las posibles extensiones no son componentes necesarios del primer trabajo. La prioridad es determinar la novedad y formular el problema científico.

## Decision 002 — Documentación científica en Markdown y LaTeX

Fecha: 2026-09-10.

La investigación se documentará simultáneamente mediante Markdown y LaTeX. Markdown se utilizará como cuaderno científico y registro de decisiones; `paper/primary/` contendrá únicamente formulaciones y resultados suficientemente estabilizados, manteniendo explícitas las cuestiones abiertas.

Desde este momento, `paper/primary/sections/problem_formulation.tex` será el documento matemático principal de la línea primaria. El working paper mantendrá una formulación matemática acumulativa y verificable que pueda evolucionar hacia el artículo; no constituye todavía un manuscrito completo.

`docs/literature/primary_novelty_review.md` será el documento de trabajo para falsar la novedad y `docs/theory/primary_notes.md` recogerá derivaciones, intentos fallidos, hipótesis y resultados intermedios todavía no incorporables al paper. La base bibliográfica común será `references/bibliography.bib`.

Ninguna afirmación de novedad se incorporará al paper mientras no sobreviva a la revisión bibliográfica de falsación. Esta decisión no modifica las líneas científicas ni la prioridad de la revisión previa a la implementación.

## Decision 003 — Refinamiento tras la segunda revisión de falsación

Fecha: 2026-09-10.

La hipótesis inicial ha sobrevivido a la segunda revisión de falsación únicamente en una forma más estrecha, según los resultados comunicados por el investigador. La trazabilidad mediante referencias verificadas sigue pendiente en `docs/literature/primary_novelty_review.md`; la bibliografía del repositorio permanece vacía.

Future value por sí solo no es nuevo. La reducción de error futuro sensible al coste ya existe en Active Learning / Value of Information. Sequential L2D puede considerar efectos a largo plazo y no debe describirse universalmente L2D como myopic. Active Knowledge Distillation ya combina coste de consulta al teacher y mejora del student.

La hipótesis candidata restante es la decisión operativa unificada en la que la misma consulta costosa tiene valor de inferencia inmediata y valor futuro de aprendizaje mediante la adaptación del predictor barato. No se ha identificado todavía un equivalente directo en la revisión comunicada; esto no demuestra su ausencia. La línea primaria permanece activa y no se ha establecido su novedad.

El objeto central de estudio teórico es ahora $\Delta_{\mathrm{learn}}(S_t,x_t)$. Se define conceptualmente mediante una diferencia de valor futuro con y sin actualización, con valores menores correspondientes a menor pérdida/coste futuro. Esta convención incluye costes futuros cuando forman parte del objetivo; no debe confundirse con una reducción exclusiva de riesgo predictivo.

El proyecto no afirmará un umbral Bayesiano en forma cerrada salvo que esa estructura se derive realmente. La siguiente tarea teórica es determinar si $\Delta_{\mathrm{learn}}$ puede calcularse o aproximarse para un modelo mínimo tratable y si ello permite una regla de routing interpretable. La descomposición candidata, su equivalencia con la comparación secuencial general, la suboptimalidad myopic y las garantías de aproximación son objetivos pendientes, no contribuciones demostradas.

## Decision 004 — Antecedentes verificados y protocolo de feedback pendiente

Fecha: 2026-09-10.

La actualización de `docs/literature/primary_novelty_review.md` y las entradas `roy2001toward` y `gao2011active` de `references/bibliography.bib` documentan que el valor futuro del aprendizaje no es novedoso por sí mismo, ni tampoco lo es la adquisición de clasificadores sensible al coste para la instancia actual.

La contribución candidata restante es su acoplamiento en una única acción operacional de routing: la información devuelta por la misma consulta al teacher puede mejorar la inferencia actual y actualizar el predictor barato para modificar rendimiento/coste futuro. Sigue siendo una hipótesis bajo falsación activa, no una contribución establecida.

Antes de continuar el desarrollo matemático debe fijarse el protocolo de observación y feedback. Sigue sin decidirse si el verdadero $Y_t$ se observa después de cada predicción, se observa con retraso u ocasionalmente, o no está disponible operacionalmente. La salida del teacher puede ser una etiqueta dura, un vector de probabilidades/logits u otra señal de supervisión; no se selecciona todavía una opción.

Las salidas del teacher pueden ser imperfectas, de modo que no debe suponerse que $\Delta_{\mathrm{learn}}$ sea no negativo. La formulación en `paper/primary/sections/problem_formulation.tex` permanece sin cambios hasta decidir el protocolo. Esta prioridad precede a la siguiente tarea teórica registrada en Decision 003; no establece un nuevo modelo ni un resultado.

## Decision 005 — Consolidation checkpoint antes de la siguiente fase de búsqueda de novedad

Fecha: 2026-09-11.

Este checkpoint consolida las decisiones comunicadas por el investigador y la documentación existente; no introduce referencias externas, supuestos matemáticos ni resultados nuevos. La hipótesis amplia original ya no es defendible: routing adaptativo entre predictores baratos y costosos, competencia local, coste de consulta, routing online/no estacionario, exploración e incluso valor futuro de información cuentan con antecedentes sustanciales.

La pregunta PRIMARY vigente es: dado un predictor barato adaptable $F$ y un teacher costoso $D$, ¿cómo decidir si consultar a $D$ para la muestra actual cuando esa misma consulta (a) puede mejorar la predicción operacional actual y (b) devuelve información que puede actualizar $F$ y, por tanto, cambiar el coste predictivo/de routing futuro?

La descomposición candidata permanece:

```text
query D iff
Delta_now(S_t,x_t) + gamma Delta_adapt(S_t,x_t) > C_D
```

$\Delta_{\mathrm{adapt}}$ es una diferencia de valor de continuación causada por actualizar el predictor barato. `Delta_now` y `Delta_adapt` corresponden a `Delta_pred` y `Delta_learn` en la formulación existente; se conserva allí la dependencia contextual de $C_D$. Es un resultado estructural candidato, NO un teorema ni una equivalencia ya demostrada bajo un modelo especificado. Se mantienen las cautelas de la formulación sobre otras diferencias entre continuaciones.

El valor futuro en sí NO es novedoso: expected-error-reduction active learning, decision-theoretic active learning, sequential learning-to-defer, information-directed routing y marcos generales de decisión secuencial ya valoran efectos futuros. La hipótesis restante es más estrecha: la MISMA consulta costosa es una acción de inferencia operacional actual y proporciona supervisión que cambia la competencia futura de $F$, mientras la decisión de routing valora explícitamente ambos efectos.

Resultados recientes de falsación:

- **Gao & Koller (2011):** adquisición secuencial costosa de clasificadores fijos en inferencia; valor de información adicional para la instancia actual frente al coste computacional; no actualiza un predictor barato para muestras futuras.
- **Roy & McCallum (2001):** expected-error-reduction active learning; valora explícitamente cómo adquirir una etiqueta y reentrenar cambia el error futuro; la consulta adquiere información de entrenamiento, no selecciona operativamente entre predictores barato/costoso.
- **Kapoor, Horvitz & Basu (2007):** supervisión selectiva decision-theoretic; coste explícito de etiquetado y coste esperado de clasificación errónea durante el uso del clasificador; sigue siendo una formulación de active learning/supervisión, no routing operacional de modelos. Conclusión comunicada por el investigador; falta el PDF correspondiente y su identificación bibliográfica completa.
- **ThriftyDAgger (Hoque et al., CoRL 2021):** intervención solicitada por el robot; la intervención humana controla el sistema actual y genera demostraciones para actualizar la política. El gating usa novedad/riesgo y presupuesto de intervención, sin valorar explícitamente el beneficio esperado de aprendizaje futuro de esa intervención particular.
- **TRACER (Rida, preprint 2026):** antecedente arquitectónico extremadamente próximo; el surrogate barato resuelve entradas aceptadas y el LLM teacher las diferidas; cada consulta también genera una traza para reentrenar el surrogate en un ciclo de aprendizaje continuo. «Teacher routing + teacher traces train the cheap model» NO es novedoso. El routing usa acuerdo predicho con el teacher/confianza y una restricción de paridad, sin valorar explícitamente cuánto se espera que esa consulta mejore el rendimiento futuro del surrogate.

No se reivindicará novedad para teacher/student routing, costly deferral, entrenar al student con respuestas diferidas del teacher, mejorar continuamente el modelo barato con trazas del teacher, ni intervenciones que controlan el sistema actual y generan demostraciones de entrenamiento. La pregunta sin resolver es si la DECISIÓN de routing internaliza explícitamente el valor futuro causado por esa actualización. No direct equivalent has yet been identified within the review documented here; esto no demuestra que no exista.

La principal amenaza pendiente de falsación es **online active learning / selective sampling / abstention**: observar $x_t$; predecir autónomamente o consultar a un oráculo con coste; la consulta evita/reduce pérdida actual y proporciona una etiqueta que actualiza al aprendiz; optimizar pérdida predictiva acumulada más coste de consulta. Puede contener un problema matemáticamente equivalente y debe auditarse antes de afirmar novedad. El PDF local de *Online Selective Classification with Limited Feedback* es un punto de partida pendiente de auditoría, no una equivalencia establecida.

El modelo de feedback sigue sin decidirse: $Y_t$ nunca observado, observado con retraso/ocasionalmente o siempre observado. Esta elección es científicamente decisiva y no se fija en este checkpoint. El teacher puede equivocarse; su actualización puede perjudicar al student y $\Delta_{\mathrm{adapt}}$ NO se supone no negativo. No se modifican los supuestos ni las ecuaciones del manuscrito. La siguiente fase prioriza la falsación bibliográfica; el protocolo deberá fijarse antes de continuar el desarrollo matemático.
