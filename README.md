# Adaptive model routing

Proyecto de investigación sobre decisiones adaptativas y coste-sensibles entre modelos predictivos heterogéneos. El cuello de botella actual es determinar la novedad y formular correctamente el problema científico, antes de implementar algoritmos.

## Línea primaria: Adaptive Cost-Aware Routing with Learning Value

Se consideran inicialmente dos modelos predictivos heterogéneos: uno barato y adaptable y un teacher costoso y potencialmente falible. Consultar al modelo costoso puede aportar dos beneficios:

1. **Immediate predictive value**: mejorar la decisión correspondiente a la observación actual.
2. **Learning value**: proporcionar información para adaptar el modelo barato y mejorar su competencia futura.

La acción presente puede, por tanto, modificar la competencia futura del sistema barato. Conceptualmente, la decisión debe considerar:

```text
immediate predictive value + future learning value
versus
cost of using the expensive model
```

Decision 006 de `docs/research_log.md` cierra la auditoría dirigida de Sogawa (2013), Sekhari et al. (2023), Hanneke & Yang (2021) y Dekel et al. (2012), junto con los antecedentes ya revisados Gangrade (2021), TRACER y ThriftyDAgger. Valor futuro de aprendizaje, supervisión falible, consultas selectivas, compromiso errores/consultas, actualización online, expertos locales múltiples, coste de consulta y perjuicio empírico por información adicional ya tienen antecedentes. Selective sampling no debe describirse globalmente como myopic: puede buscar información deliberadamente para mejorar decisiones futuras.

La hipótesis candidata es la conjunción de:

1. Decisión de routing antes de la respuesta operacional final.
2. El predictor costoso D reemplaza la respuesta de F para la muestra actual.
3. Esa misma respuesta de D actualiza F.
4. La política valora la consecuencia predictiva inmediata.
5. La política valora explícitamente el cambio de valor de continuación causado por esa actualización particular.
6. D puede ser falible y el valor de adaptación puede ser negativo.

**No direct equivalent has yet been identified after targeted audit** satisfying all six properties jointly. Se trata de una región candidata, no de una novedad establecida. La búsqueda bibliográfica amplia queda pausada: el siguiente paso es definir el protocolo operacional/de feedback exacto antes de desarrollar un modelo matemático. El checkpoint completo y la matriz comparativa están en `docs/literature/primary_novelty_review.md`.

Esta hipótesis todavía no está establecida como novedosa y continúa sujeta a falsación. Si no se identifica una diferencia metodológica clara y defendible respecto a learning-to-defer, model routing, contextual bandits, active learning, knowledge distillation y trabajos relacionados, se reconsiderará esta línea antes de implementar algoritmos o invertir esfuerzo experimental.

El principal objeto teórico de estudio es actualmente $\Delta_{\mathrm{learn}}(S_t,x_t)$, entendido de forma general como la reducción esperada del coste futuro acumulado inducida por la actualización del predictor barato. Este valor puede incluir pérdida predictiva y costes futuros de consulta; no representa exclusivamente una reducción del riesgo predictivo. Determinar cómo calcularlo o aproximarlo y si la política óptima puede reducirse a una regla interpretable de umbral son objetivos teóricos pendientes. No se ha establecido una regla de umbral cerrada.

Antes de continuar el desarrollo matemático debe fijarse el protocolo de observación y feedback (prioridad reafirmada en Decision 006): si el verdadero $Y_t$ se observa tras cada predicción, con retraso u ocasionalmente, o no está disponible operacionalmente. También queda abierta la forma de supervisión del teacher. Sus salidas pueden ser imperfectas y no se presupone que $\Delta_{\mathrm{learn}}$ sea no negativo. La hipótesis de valorar explícitamente ambos efectos en la decisión de consulta continúa bajo falsación activa; la doble función de predecir y entrenar ya tiene antecedentes.

### Current research overview

The following diagram records the interpretation after Decision 003 and predates
the consolidations in Decisions 005–006. It requires scientific review against
the targeted audit, ThriftyDAgger, and TRACER; use the current novelty review for the working hypothesis.

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
- `references/bibliography.bib`: bibliografía común con diez entradas verificadas; el inventario distingue evidencia local y metadatos verificados aportados por el investigador.
- `references/papers/`: directorio previsto para PDFs locales, actualmente vacío; los trece PDFs presentes están en `docs/literature/`. Véase `docs/literature/consolidation_inventory.md`.
- `code/`: directorio vacío; no se añaden algoritmos ni dependencias Python.
