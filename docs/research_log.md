# Research log

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
