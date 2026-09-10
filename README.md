# Adaptive model routing

Proyecto de investigación sobre decisiones adaptativas y coste-sensibles entre modelos predictivos heterogéneos. El cuello de botella actual es determinar la novedad y formular correctamente el problema científico, antes de implementar algoritmos.

## Línea primaria: Adaptive Cost-Aware Routing with Learning Value

Se consideran inicialmente dos modelos predictivos heterogéneos: uno barato y adaptable y otro más competente pero costoso. Consultar al modelo costoso puede aportar dos beneficios:

1. **Immediate predictive value**: mejorar la decisión correspondiente a la observación actual.
2. **Learning value**: proporcionar información para adaptar el modelo barato y mejorar su competencia futura.

La acción presente puede, por tanto, modificar la competencia futura del sistema barato. Conceptualmente, la decisión debe considerar:

```text
immediate predictive value + future learning value
versus
cost of using the expensive model
```

Se ha completado una segunda revisión de falsación de la línea primaria, registrada en Decision 003 de `docs/research_log.md`. La hipótesis inicial de novedad se ha estrechado: future value por sí solo no constituye novedad; cost-aware future error reduction aparece ya en Active Learning / Value of Information; Sequential Learning to Defer puede considerar consecuencias futuras; y Active Knowledge Distillation puede combinar coste de consulta al teacher con mejora del student. La trazabilidad mediante referencias verificadas sigue pendiente en `docs/literature/primary_novelty_review.md`.

La hipótesis que permanece bajo investigación es la combinación, dentro de una misma decisión operacional, de:

1. Routing online entre un predictor barato y un predictor costoso.
2. Coste explícito de consultar al predictor costoso.
3. Utilización de esa misma consulta para actualizar el predictor barato.
4. Valoración explícita del beneficio futuro producido por dicha actualización.

Esta hipótesis todavía no está establecida como novedosa y continúa sujeta a falsación. Si no se identifica una diferencia metodológica clara y defendible respecto a learning-to-defer, model routing, contextual bandits, active learning, knowledge distillation y trabajos relacionados, se reconsiderará esta línea antes de implementar algoritmos o invertir esfuerzo experimental.

El principal objeto teórico de estudio es actualmente $\Delta_{\mathrm{learn}}(S_t,x_t)$, entendido de forma general como la reducción esperada del coste futuro acumulado inducida por la actualización del predictor barato. Este valor puede incluir pérdida predictiva y costes futuros de consulta; no representa exclusivamente una reducción del riesgo predictivo. Determinar cómo calcularlo o aproximarlo y si la política óptima puede reducirse a una regla interpretable de umbral son objetivos teóricos pendientes. No se ha establecido una regla de umbral cerrada.

### Current research overview

The following diagram summarizes the current interpretation of the problem,
the neighboring research areas, and the candidate methodological gap.
It is a working research overview and does not imply that novelty has been
established.

![Primary research overview](docs/graphics/primary_research_overview.png)

## Línea secundaria: Bayesian Cost-Aware Routing under Changing Operating Conditions

Esta línea estudia modelos inicialmente fijos y separa explícitamente:

1. La estimación de la competencia predictiva relativa entre modelos.
2. La toma de decisiones Bayesiana.

Se estimará la ganancia predictiva relativa y se estudiará cómo debe transformarse la regla óptima de routing ante cambios en el coste computacional, el coste de latencia, el coste del error, los priors de clase, la composición de la población o las restricciones operativas. La cuestión central es determinar cuándo puede modificarse analíticamente la regla de decisión sin reentrenar el router.

Label Switching no forma parte del método propuesto ni constituye un eje de investigación. La experiencia previa sólo aporta un antecedente metodológico: estudiar cómo modificaciones de poblaciones, priors o probabilidades a posteriori transforman la regla Bayesiana de decisión y permiten derivar umbrales óptimos.

## Alcance de la primera etapa

La primera etapa se centra en la revisión bibliográfica y la formulación científica. No incluye LLM routing como problema principal, concept drift, imbalanced learning, aplicaciones SOC/NOC, múltiples expertos, grandes arquitecturas neuronales ni código experimental. LLMs, concept drift, imbalance, SOC/NOC y múltiples niveles de procesamiento quedan como posibles extensiones o aplicaciones futuras.

## Organización

- `docs/literature/`: documentación de la revisión bibliográfica.
- `docs/theory/`: documentación de la formulación teórica.
- `docs/research_log.md`: registro de decisiones científicas.
- `references/bibliography.bib`: bibliografía, inicialmente vacía.
- `references/papers/`: PDFs locales, excluidos del control de versiones.
- `code/`: directorio vacío; no se añaden algoritmos ni dependencias Python.
