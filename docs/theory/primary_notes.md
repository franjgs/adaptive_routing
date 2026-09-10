# Primary technical notes

Cuaderno técnico de la línea **Adaptive Cost-Aware Routing with Learning Value** para derivaciones, intentos fallidos, hipótesis y resultados intermedios que todavía no deban incorporarse al paper.

El documento matemático principal es `paper/primary/sections/problem_formulation.tex`. Sólo las formulaciones y los resultados suficientemente estabilizados se trasladarán a `paper/primary/`. La novedad continúa pendiente de la revisión de falsación.

## Evidencia e interpretación

Los antecedentes comunicados de la segunda revisión y sus límites de verificación se registran en `docs/literature/primary_novelty_review.md`. Future value por sí solo no es nuevo. La interpretación actual concentra la investigación en la misma consulta costosa como acción de inferencia presente y fuente de adaptación del predictor barato. Esta interpretación no establece novedad ni resultados teóricos.

## Formulación candidata e hipótesis de trabajo

Sea $S_t=(\theta_t,\mathcal I_t)$ el estado del predictor barato y la información disponible, $x_t$ la observación actual y $Y_t$ el objetivo aleatorio. Los predictores son $M_F(x_t;\theta_t)$ y $M_D(x_t)$. Se mantienen el objetivo secuencial y los valores de acción generales del documento matemático principal.

$$
r_F(S_t,x_t)=\mathbb E[\ell(M_F(x_t;\theta_t),Y_t)\mid S_t,x_t],
\qquad
r_D(S_t,x_t)=\mathbb E[\ell(M_D(x_t),Y_t)\mid S_t,x_t].
$$

$$
\Delta_{\mathrm{pred}}(S_t,x_t)=r_F(S_t,x_t)-r_D(S_t,x_t).
$$

Al consultar al teacher, $Z_t=M_D(x_t)$ y $S_t^+=U(S_t,x_t,Z_t)$. El operador actualiza el estado completo y permite adaptar $\theta_t$; no presupone acceso al objetivo verdadero.

Sea $V_{\mathrm{future}}(S)$ el valor esperado de pérdida/coste acumulado futuro: menor valor es mejor. La definición conceptual central es

$$
\Delta_{\mathrm{learn}}(S_t,x_t)=V_{\mathrm{future}}(S_t)
-\mathbb E_{Z_t}[V_{\mathrm{future}}(U(S_t,x_t,Z_t))\mid S_t,x_t].
$$

Compara el estado de referencia sin actualización por el teacher con el estado actualizado, usando el mismo horizonte futuro, distribución futura y criterio de continuación. La dependencia contextual en el instante y la observación actuales queda implícita en $V_{\mathrm{future}}$; debe explicitarse al especializar el modelo. $S_t^+$ es un estado posterior a la consulta, no necesariamente todo el estado del siguiente instante. Si el teacher es determinista y conocido dado $(S_t,x_t)$, la esperanza sobre $Z_t$ es degenerada; no se postula aleatoriedad adicional.

El término valora la reducción esperada del coste/riesgo futuro atribuible a usar la respuesta del teacher para actualizar el predictor barato. No es una expresión cerrada computable ni se presupone que sea positivo. Al incluir costes futuros, no equivale necesariamente a reducción de pérdida predictiva exclusivamente.

La estructura candidata es

$$
\Delta_{\mathrm{pred}}(S_t,x_t)+\gamma\Delta_{\mathrm{learn}}(S_t,x_t)>C_D(S_t,x_t).
$$

$C_D$ es el coste incremental de consulta. Esta comparación emerge conceptualmente de $Q_D<Q_F$; no es un teorema. Para identificar la diferencia de continuación general con $\Delta_{\mathrm{learn}}$, hay que justificar que las dos continuaciones comparten dinámica, horizonte y criterio, y que su diferencia se representa mediante la actualización $U$. Otros efectos de la acción o actualizaciones bajo $F$ deben incluirse en el estado de referencia; de lo contrario, debe conservarse la comparación general de valores $Q$. La política de continuación y los supuestos de información suficiente siguen pendientes.

## No se presupone un umbral de confianza

Una política escalar $s(x_t)<\tau$ exige supuestos estructurales adicionales. No se adopta una corrección de umbral del tipo $\tau_{\mathrm{myopic}}-\Delta\tau_{\mathrm{distil}}$, ni se fija su signo o forma. No se supone incertidumbre Gaussiana ni que la incertidumbre epistémica sea suficiente.

Como posibilidades conceptuales, una muestra muy incierta puede tener poco valor futuro si su región apenas aparece después; otra moderadamente incierta puede tener mucho valor si representa una región de alta probabilidad futura. Por tanto, $\Delta_{\mathrm{learn}}$ puede depender de $x_t$, $S_t/\theta_t$, la distribución futura de entradas, el comportamiento y estructura de errores del teacher, $U$, el horizonte futuro efectivo y otras variables de estado. La existencia y la forma de un umbral son cuestiones teóricas abiertas.

## Programa teórico ordenado — resultados pendientes

1. **Derivación secuencial.** Derivar rigurosamente la formulación y establecer bajo qué supuestos la comparación de acciones se descompone en valor predictivo inmediato más valor futuro de aprendizaje menos coste de consulta.
2. **Familia mínima tratable.** Identificar una familia en la que $\Delta_{\mathrm{learn}}$ sea calculable exactamente o admita una aproximación analítica controlada. Posibilidades, sin seleccionar ninguna: clasificación/regresión lineal Bayesiana; regresión logística con actualización aproximada; otro aprendiz convexo con actualización analíticamente tratable. No se fija una distribución de incertidumbre.
3. **Interpretabilidad.** Determinar condiciones suficientes para reducir la regla general a una política de umbral interpretable, sin asumir previamente su existencia.
4. **Casos límite.** Formalizar las conexiones: con $\Delta_{\mathrm{learn}}=0$, la regla candidata debería reducirse a routing myopic sensible al coste; si se ignora el beneficio predictivo inmediato y sólo se valora el aprendizaje futuro, debería conectar conceptualmente con adquisición activa / active learning. Son relaciones pendientes de formalizar como resultados del modelo secuencial.
5. **Suboptimalidad myopic.** Investigar condiciones de suboptimalidad estricta. Una construcción potencialmente importante identificaría muestras con $\Delta_{\mathrm{pred}}<C_D$ pero $\Delta_{\mathrm{pred}}+\gamma\Delta_{\mathrm{learn}}>C_D$: el router myopic no consultaría y el sensible al aprendizaje sí. No se ha demostrado que exista esta región bajo un modelo concreto ni que la regla candidata sea óptima en él.
6. **Aproximación y garantías.** Si no es posible calcular exactamente $\Delta_{\mathrm{learn}}$, derivar una aproximación y cuantificar el error o la pérdida de rendimiento por sustituir el valor futuro exacto.

No hay todavía resultados demostrados ni una familia de modelos seleccionada. Las relaciones con VoI, dual control, active learning, knowledge distillation, learning to defer y contextual bandits siguen abiertas.
