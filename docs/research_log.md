# Research log

## Decision 001 — Elección de las líneas de investigación

Fecha: 2026-09-10.

La línea primaria es **Adaptive Cost-Aware Routing with Learning Value**. Se consideran dos modelos predictivos heterogéneos: uno barato y adaptable y otro más competente pero costoso. Consultar al segundo puede mejorar la predicción actual y aportar información para adaptar el primero. La decisión debe considerar el valor predictivo inmediato y el valor de aprendizaje futuro frente al coste de consulta; la acción presente puede modificar la competencia futura del modelo barato.

La línea secundaria es **Bayesian Cost-Aware Routing under Changing Operating Conditions**. Con modelos inicialmente fijos, separa la estimación de la competencia predictiva relativa de la toma de decisiones Bayesiana. Estudia cuándo los cambios de costes computacionales, de latencia o de error, priors de clase, composición poblacional o restricciones operativas permiten transformar analíticamente la regla óptima sin reentrenar el router.

Antes de implementar algoritmos debe realizarse una revisión bibliográfica rigurosa destinada a intentar falsar la novedad de la línea primaria. Si no puede identificarse con claridad una diferencia metodológica defendible respecto a learning-to-defer, model routing, contextual bandits, active learning, knowledge distillation y trabajos relacionados, la formulación primaria deberá reconsiderarse antes de invertir esfuerzo experimental. No se debe asumir novedad hasta completar esa revisión.

Label Switching no forma parte del método ni es un eje de investigación. Su relevancia se limita al antecedente metodológico de analizar cómo cambios en poblaciones, priors o probabilidades a posteriori transforman la regla Bayesiana y permiten derivar umbrales óptimos.

La primera etapa excluye LLM routing como problema principal, concept drift, imbalanced learning, aplicaciones SOC/NOC, múltiples expertos, grandes arquitecturas neuronales y código experimental. Las posibles extensiones no son componentes necesarios del primer trabajo. La prioridad es determinar la novedad y formular el problema científico.
