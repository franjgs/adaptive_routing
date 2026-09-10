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

Antes de implementar algoritmos se realizará una revisión bibliográfica rigurosa orientada específicamente a intentar falsar la novedad de esta formulación. No se asume novedad. Si no se identifica una diferencia metodológica clara y defendible respecto a learning-to-defer, model routing, contextual bandits, active learning, knowledge distillation y trabajos relacionados, se reconsiderará esta línea antes de invertir esfuerzo experimental.

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
