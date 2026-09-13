# Research log

Decision 010 establece el estado científico vigente: cierra la cuestión estructural de persistencia/inversión bajo isotropía de segundo orden y congela la teoría principal para el primer ciclo experimental. Las decisiones anteriores conservan su contexto histórico: siguen vigentes la auditoría y las cautelas de Decision 006, el protocolo y resultados de Decision 007, la revisión y limitaciones de Decision 008 y el transporte común de Decision 009. Los problemas abiertos de esos checkpoints se actualizan en Decision 010.

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

## Decision 006 — Targeted selective-sampling audit completed

Fecha: 2026-09-11.

La auditoría dirigida cubrió Sogawa et al. (2013), Sekhari et al. (2023), Hanneke & Yang (2021) y Dekel et al. (2012), además de Gangrade (2021), TRACER y ThriftyDAgger previamente revisados. Los cuatro nuevos PDFs están presentes e identificados en el inventario. Sekhari et al. se registra como NeurIPS 2023, volumen 36, Main Conference Track, según los metadatos verificados aportados por el investigador; su copia local es la versión arXiv de julio de 2023. No se presenta esa copia como PDF oficial de proceedings.

Los siguientes componentes ya están ocupados y no pueden reivindicarse como novedosos individualmente: valor esperado del aprendizaje futuro; supervisión ruidosa/falible; consulta selectiva; compromiso errores/consultas; actualización online del aprendiz con feedback consultado; múltiples expertos con experiencia local; coste de consulta; e información adicional de teachers empíricamente perjudicial.

Sogawa establece valor de aprendizaje bajo oráculo ruidoso mediante expected-error-reduction pool-based y un criterio asintótico de error esperado de estimación, sin sustitución operacional actual. Sekhari combina feedback experto ruidoso, actualización online y garantías de regret/consultas, pero SAGE predice antes de consultar y RAVIOLI ejecuta la acción y transiciona antes del feedback. Hanneke & Yang estudian el compromiso acumulado errores/consultas con búsqueda de información no trivial, bajo un protocolo predict-first y etiquetas perfectas en la formulación realizable principal. Dekel estudia teachers estocásticos y múltiples expertos locales, coste de consulta y actualización online, e informa perjuicio por más etiquetas en sus experimentos; también predice antes de consultar y usa incertidumbre/estabilidad, no una diferencia explícita de continuación por actualización. El perjuicio observado no equivale a un valor negativo de adaptación explícitamente modelado en la consulta.

Selective sampling no debe describirse globalmente como myopic. Varios métodos consultan deliberadamente para obtener información que mejora decisiones futuras. Se separan (A) el aprendizaje futuro como consecuencia buscada, (B) la exploración o carácter globalmente no myopic de la política y (C) la valoración explícita en la decisión operacional actual de la consecuencia futura esperada de la actualización específica inducida por esa consulta.

La hipótesis candidata vigente es la conjunción de:

1. Decisión de routing antes de la respuesta operacional final.
2. El predictor costoso D reemplaza operacionalmente a F en la muestra actual.
3. La misma respuesta de D actualiza F.
4. La política valora la consecuencia predictiva inmediata.
5. La política valora explícitamente el cambio de valor de continuación futuro causado por esa actualización particular.
6. D puede ser falible; por tanto, el valor de adaptación puede ser negativo.

**No direct equivalent has yet been identified after targeted audit** satisfying all six properties jointly. Esto NO prueba novedad ni autoriza afirmar «No prior method exists». Tampoco convierte la descomposición candidata en un teorema.

La búsqueda bibliográfica amplia queda **pausada**. El siguiente paso es definir el protocolo operacional/de feedback exacto antes de desarrollar un modelo matemático. No se decide todavía cómo se observa ground truth, la definición exacta de Delta_adapt, la regla U ni un modelo específico como RLS o regresión logística Bayesiana. Las ecuaciones conceptuales existentes se conservan, sin nuevos supuestos ni resultados.

## Decision 007 — Delayed reliable feedback and geometric adaptation value

Fecha: 2026-09-11.

### A. Protocolo operacional base

Se adopta F_theta barato y adaptativo, D caro y falible, y routing antes de emitir la respuesta final. Si se elige D, sustituye operacionalmente a F; la misma salida realizada Z_t=D(x_t) se usa como pseudo-supervisión inmediata de F. Y_t llega tras un retardo fijo tau de forma exógena e independiente de la acción de routing y puede usarse después para corregir/actualizar F. La convención de rondas sitúa su disponibilidad después de la respuesta t+tau, permitiendo contar las tau respuestas futuras anteriores a su uso; durante ese intervalo puede llegar feedback de muestras previas. No se supone que corregir deshaga exactamente el pseudo-update.

Se comienza con hard labels en clasificación; logits, confianza y feedback ocasional quedan como extensiones. La especialización lineal de regresión emplea respuestas escalares puntuales, no labels binarios. La consulta compra simultáneamente una posible mejora de inferencia presente y supervisión anticipada imperfecta; **no compra ground truth**, ni garantiza una mejora.

### B. Razón para adoptar feedback fiable retrasado

Si Y nunca se observa, el rendimiento respecto a Y no es identificable en general a partir de D salvo supuestos fuertes sobre D. El feedback fiable retrasado permite evaluar/corregir respecto a Y sin convertir la consulta a D en adquisición activa de Y. Se distinguen imitation of D, task performance wrt Y y total system objective: pérdida operacional más coste de routing. Fiabilidad de Y significa observación del target real, no ausencia de ruido intrínseco de la tarea.

### C. Modelo lineal vectorial mínimo y resultado central

Bajo pérdida cuadrática:

$$
Y=(w^*)^T X+\epsilon,\qquad F_\theta(x)=\theta^T x,\qquad
D(x)=(w^*+b)^T x+\nu,
$$

$$
\mathbb E[\nu]=0,\quad\operatorname{Var}(\nu)=\sigma_D^2,\quad
e=\theta-w^*,\quad M=\mathbb E[XX^T]\succ0,\quad
\alpha=x^T e,\quad\beta=x^T b.
$$

Para las identidades condicionadas en x se explicitan las condiciones E[nu|x]=0 y E[nu^2|x]=sigma_D^2; los momentos marginales solos no bastan. Para interpretar la diferencia de pérdidas respecto a Y se requieren también E[epsilon|x]=0 y E[epsilon nu|x]=0, con segundos momentos finitos. No se exige gaussianidad ni independencia completa. Las notas conservan la expresión con términos adicionales si no se cumplen estas condiciones.

$$
\Delta_{\mathrm{now}}=\alpha^2-\beta^2-\sigma_D^2,
$$

$$
\theta^+=\theta+\eta x(D(x)-\theta^T x),\qquad
e^+=e-\eta x(\alpha-\beta)+\eta x\nu,\qquad R(e)=e^TMe.
$$

El **resultado algebraico central exacto del modelo mínimo** es

$$
\Delta_R(x)=R(e)-\mathbb E[R(e^+)\mid x]
=2\eta(\alpha-\beta)x^TMe
-\eta^2[(\alpha-\beta)^2+\sigma_D^2]x^TMx.
$$

R es riesgo poblacional excedente del predictor barato, no el objetivo total. Delta_R mide una pseudoactualización; Delta_adapt se reserva para valor acumulado/secuencial. Se reemplaza en la formulación vigente la antigua notación Delta_pred/Delta_learn sin alterar su registro histórico.

### D. Interpretación geométrica

Delta_now mide calidad local de la respuesta; Delta_R mide el efecto de entrenar con esa misma salida sobre el riesgo poblacional futuro. No son equivalentes. El factor de primer orden para eta pequeño es (alpha-beta)x^TMe, donde x^TMe=(1/2)x^T grad R(e). Teacher reliability / immediate superiority no equivale a training value.

### E. Compatibilidad isotrópica y régimen del paso

Si M=cI, c>0, y 0<a=eta||x||^2<=1, entonces Delta_now>0 implica Delta_R>0. La prueba usa sigma_D^2<alpha^2-beta^2 y alpha(alpha-beta)>0, obteniendo

$$
\Delta_R>2c\eta\alpha(\alpha-\beta)[1-\eta\|x\|^2]\geq0.
$$

La primera desigualdad es estricta incluso en a=1. En 1D excluye el patrón (+,-) en el régimen conservador, en particular 0<a<1. Se distingue **conservative regime: 0<a<=1** de **locally stable / possible overshoot: 1<a<2**. La contracción local del residual para entrada fija no garantiza mejora poblacional bajo ruido o geometría anisotrópica; no se denomina simplemente «stable» a todo 0<a<2 para extender indebidamente la proposición.

### F. Existencia de conflicto anisotrópico

Si M es definida positiva y no es cI, elegir x no autovector y e=x-kMx con

$$
\frac{x^TMx}{\|Mx\|^2}<k<\frac{\|x\|^2}{x^TMx}.
$$

Cauchy–Schwarz estricta garantiza el intervalo: (x^TMx)^2<||x||^2||Mx||^2. Así x^Te>0 y x^TMe<0. Tomando b=0 y 0<sigma_D^2<alpha^2, Delta_now>0 pero Delta_R<0 para todo eta>0.

La conclusión es de **existencia**: isotropía da compatibilidad universal bajo updates conservadores; anisotropía permite configuraciones con conflicto para pasos arbitrariamente pequeños. No toda consulta anisotrópica tiene conflicto, ni se demuestra frecuencia positiva de esas configuraciones bajo cualquier distribución con momento M.

### G. Comparador miope y simplificación de horizonte aislado

Myopic: consultar iff Delta_now>C_D. Bajo aislamiento de H respuestas anteriores al uso de ground truth, sin evolución intermedia ni diferencias de routing futuro, el criterio idealizado es consultar iff Delta_now+B_H Delta_R>C_D, con B_H=sum_{k=1}^H gamma^k cuando se descuenta desde la ronda actual. Se escribe Delta_adapt^(H)=B_H Delta_R sólo bajo esa simplificación.

Posibles fallos, sin agruparlos en un teorema general:

1. Under-querying: Delta_now<C_D pero Delta_now+B_H Delta_R>C_D; la región ya existe en 1D (ejemplo derivado en las notas).
2. Over-querying: Delta_now>C_D pero Delta_now+B_H Delta_R<C_D; el conflicto anisotrópico permite un intervalo no vacío de costes cuando B_H>0.

Se trata de comparaciones idealizadas, no de optimalidad secuencial ni resultados para todos los costes. No se afirma que la llegada de Y_t elimine cualquier efecto posterior.

### H. Cautela bibliográfica y novedad

Gradient alignment, influence functions y data valuation ya contienen el hecho general de que el gradiente de una muestra puede desalinearse con el poblacional; esto no es nuestra novedad. Tampoco lo es una actualización perjudicial. No se añaden referencias no verificadas; queda TODO bibliográfico en Markdown para citas específicas de esas familias.

La región candidata mantiene la conjunción de Decision 006: (1) routing antes de la respuesta final; (2) D sustituye operacionalmente a F; (3) la misma salida de D actualiza F; (4) valoración explícita del beneficio inmediato; (5) valoración explícita del impacto futuro de esa actualización; (6) D falible con valor futuro potencialmente negativo.

“No direct antecedent was identified in the targeted review that jointly models the immediate operational value of routing to an expensive predictor and the future population-risk effect of updating the cheap predictor with that same routed output.” Es una conclusión limitada a la revisión dirigida, no una prueba de novedad. Selective sampling / active learning pueden ser no-myopic y exploratorios; la diferencia candidata no es negar esos efectos.

### I. Problema abierto prioritario

Eliminar el aislamiento y calcular explícitamente la evolución contrafactual durante tau pasos, permitiendo updates intermedios:

$$
\Delta_{\mathrm{adapt}}^{(\tau)}=
\sum_{k=1}^{\tau}\gamma^{k-1}\mathbb E\left[
(e_{t+k}^F)^TM e_{t+k}^F-(e_{t+k}^D)^TM e_{t+k}^D\right].
$$

Esta suma descuenta desde la primera respuesta futura; su peso desde la ronda actual es gamma Delta_adapt^(tau). Bajo aislamiento con H=tau, gamma Delta_adapt^(tau)=B_H Delta_R. Se explicita el origen temporal para no perder ni duplicar gamma. La suma de riesgo barato tampoco equivale por sí sola al coste operacional futuro total: deben modelarse respuestas y consultas posteriores.

Este es el próximo problema matemático, **no resuelto**. Quedan pendientes la corrección fiable concreta, la evolución intermedia, las políticas de continuación y los efectos posteriores al horizonte. Las pruebas de una pseudoactualización se incorporan al manuscrito con carácter preliminar/candidato para revisión científica; no se afirman regret bounds ni tasas comparativas de regret.

## Decision 008 — Independent red-team review of the single-update theory

Fecha: 2026-09-11.

### Resultado confirmado

Una revisión independiente recalculó y confirmó $\Delta_{\mathrm{now}}$, la expresión exacta de $\Delta_R$, la proposición de compatibilidad isotrópica para $0<\eta\|x\|^2\leq1$, la construcción anisotrópica mediante Cauchy--Schwarz y la lógica algebraica de under-querying/over-querying en el horizonte aislado. Se mantiene el teorema anisotrópico como resultado geométrico de existencia.

Su alcance queda delimitado: no demuestra que el conflicto tenga probabilidad positiva bajo una distribución dada ni que sea frecuente en trayectorias naturales de SGD. El siguiente nivel de teoría debe conectar el estado aleatorio $(X_t,e_t)$ con la dinámica inducida por el aprendizaje.

### Crítica externa y respuesta

No se acepta tal como fue formulada la crítica de que SGD hace que $e_t$ se alinee en general con las direcciones de mayor autovalor de $M$. En gradient descent lineal, las componentes de mayor curvatura se contraen más rápidamente. Además, si $e$ es autovector de $M$, la coincidencia de signo del término de primer orden no basta para garantizar $\Delta_R>0$ para cualquier $\eta$, debido al término cuadrático negativo. Esta respuesta no añade un teorema sobre la distribución o la dinámica de $(X_t,e_t)$.

### Feedback retrasado y horizonte aislado

$U_Y$ debe especificarse antes de resolver las trayectorias contrafactuales. No se presupone que usar posteriormente $(x_t,Y_t)$ sea matemáticamente inválido ni que deba deshacerse necesariamente la pseudoactualización. Las posibles reglas de corrección siguen siendo una decisión metodológica abierta; no se elige todavía ninguna.

$B_H\Delta_R$ se conserva sólo como dispositivo ilustrativo y no representa la dinámica real. No se presupone automáticamente una evolución $(I-\eta M)^\tau$: con SGD por muestras pueden aparecer productos aleatorios de operadores $(I-\eta X_jX_j^T)$. Obtener una dinámica cerrada exige hipótesis adicionales, que no se introducen en este checkpoint.

### Novedad y prioridad abierta

La auditoría independiente no encontró un fallo fatal de novedad, pero esto no prueba novedad. Se mantiene exactamente el framing prudente:

> No direct antecedent was identified in the targeted review that jointly models the immediate operational value of routing to an expensive predictor and the future population-risk effect of updating the cheap predictor with that same routed output.

La prioridad es pasar de una teoría de **una** pseudoactualización a una teoría del valor de la decisión durante el periodo de anticipación $\tau$. Los problemas pendientes son: (a) especificar $U_Y$; (b) derivar la evolución contrafactual durante $\tau$ con updates intermedios; y (c) determinar bajo qué condiciones el conflicto geométrico tiene relevancia probabilística o dinámica. El punto (c) permanece como problema abierto, no como nuevo teorema. No se introducen supuestos gaussianos, covarianza estacionaria de SGD ni distribution shift para responder a la crítica.

## Decision 009 — Transported adaptation value under subsequent learning

Fecha: 2026-09-12.

### A. Motivo y alcance de la extensión

Se pasa del efecto de una pseudoactualización a estudiar cómo ese mismo efecto se transporta a través del aprendizaje posterior del cheap predictor. La pregunta es: **How does the future learning dynamics transform the benefit or harm caused by querying an expensive predictor now?** La secuencia conceptual es current operational value + transported adaptation value − query cost. El modelo lineal-cuadrático permite estudiar exactamente este componente, sin presentar el desarrollo como «new SGD theory» ni como contribución novedosa definitiva del paper.

Decision 008 dejó abiertas la evolución intermedia, la regla de feedback fiable y la relevancia probabilística de la construcción geométrica. Esta decisión resuelve una especialización con aprendizaje posterior común, elige SGD ordinario como regla fiable mínima admisible y demuestra probabilidad positiva sobre inputs en un ejemplo a estado fijo. No resuelve la dinámica completa de routing ni la distribución de estados inducidos por aprendizaje. El teorema anisotrópico anterior, la compatibilidad isotrópica single-update y sus pruebas se conservan.

### B. Contrafactuales comunes e hipótesis explícitas

Condicionados en la información actual, e_t=e y x_t=x, se definen e_t^F=e y e_t^D=e+h_0, con

$$
h_0=-\eta_Dxd+\eta_Dx\nu_t,\qquad
d=\alpha-\beta,\quad\alpha=x^Te,\quad\beta=x^Tb.
$$

h_0 es la perturbación paramétrica causal producida por consultar D y usar **la misma salida** como pseudo-supervisión. Sus momentos son E[h_0|e,x]=−eta_D d x y E[h_0h_0^T|e,x]=eta_D²(d²+sigma_D²)xx^T. eta_D es el eta de la teoría single-update anterior; se distingue del paso eta de SGD posterior y de eta_Y para el target fiable.

Para aislar adaptación se imponen después los mismos inputs, targets y reglas en ambas ramas. El reloj de updates se reinicia con e_0^F=e y e_0^D=e+h_0; para j>=1,

$$
e_j^u=A_je_{j-1}^u+\xi_j,\quad
A_j=I-\eta X_jX_j^T,\quad\xi_j=\eta X_j\epsilon_j,
\quad u\in\{F,D\}.
$$

Para la esperanza cerrada se explicita que los **pares** (X_j,epsilon_j) son i.i.d. condicionalmente en la información actual, con ley de inputs P_X, E[epsilon_j|X_j]=0 e independencia respecto de nu_t. Se requieren los momentos condicionales iniciales del teacher, E||X||⁴ finito y E[||X||² epsilon²] finito, suficientes para riesgos finitos a horizonte finito. No se presupone estabilidad de largo plazo ni gaussianidad general.

La precisión «pares i.i.d.» evita una laguna: inputs i.i.d. y centrado sólo respecto de X_j no bastarían si epsilon_j dependiera de otros inputs futuros. Lo necesario en la prueba es centrar cada epsilon_j dado todo X_1,...,X_k. Esta condición se prueba a partir de los pares i.i.d., no se presupone independencia entre el producto de matrices y el ruido acumulado.

### C. Resultados exactos por realización y operador probado

Restando las ramas, h_j=A_jh_{j-1}, por lo que

$$
h_k=P_kh_0,\qquad P_k=A_k\cdots A_1,\quad P_0=I.
$$

Los targets comunes desaparecen de la diferencia de parámetros, pero siguen afectando cada trayectoria. Con R(e)=e^TMe,

$$
R(e_k^F)-R(e_k^D)
=-2h_k^TMe_k^F-h_k^TMh_k
=-2h_0^TP_k^TMe_k^F-h_0^TP_k^TMP_kh_0.
$$

Esta igualdad es por realización, antes de cerrar esperanzas. Se define K_k=E[P_k^TMP_k], K_0=M y

$$
\mathcal T(Q)=\mathbb E[(I-\eta XX^T)^TQ(I-\eta XX^T)]
=Q-\eta(MQ+QM)+\eta^2\mathbb E[XX^TQXX^T].
$$

La independencia y la ley común de los factores dan K_{k+1}=T(K_k), K_k=T^k(M); la prueba condiciona en A_1 y no conmuta matrices. T es un operador sobre matrices de riesgo que preserva semidefinitud positiva. El transporte depende en general de cuartos momentos, no sólo de M=E[XX^T]. No se reivindica novedad de este hecho en teoría de SGD.

### D. Teorema probado de valor transportado y consecuencias

Desarrollar e_k^F=P_ke+q_k, con q_k=sum_{i=1}^k A_k...A_{i+1} xi_i. Los pares i.i.d. centrados implican E[q_k|X_1,...,X_k]=0 y por tanto E[P_k^T M q_k]=0. La independencia de h_0 respecto del futuro permite factorizar sus momentos. El cálculo de traza del término cuadrático y esta anulación del término cruzado prueban

$$
\Delta_k:=\mathbb E[R(e_k^F)-R(e_k^D)\mid e_t=e,x_t=x]
=2\eta_Dd x^TK_ke
-\eta_D^2(d^2+\sigma_D^2)x^TK_kx.
$$

Para k=0 se recupera exactamente Delta_0=Delta_R con paso eta_D. El paper incluye la prueba y el cuaderno desarrolla también el término que habría que retener si fallara el centrado. No se presenta la fórmula como válida para cualquier secuencia de targets, feedback pendiente o decisiones adaptativas.

Si x^T K_k x>0, s_k=d x^T K_k e/(x^T K_k x) satisface Delta_k>0 iff s_k>(eta_D/2)(d²+sigma_D²). Es un criterio de signo, sin interpretación adicional de s_k: el umbral depende de tamaño/ruido de la pseudoactualización y K_k fija la geometría efectiva. Si x^T K_k x=0, semidefinitud implica K_k x=0 y Delta_k=0.

Se prueba por sustitución la proposición: K_k=c_k M con c_k>0 implica Delta_k=c_k Delta_0 y preservación del signo. Sólo reescalar positivamente puede cambiar magnitud pero no signo. No se afirma el recíproco ni se incluye c_k=0 en una garantía de preservación de signos no nulos.

### E. Valor acumulado y corrección de la convención de descuento

Para H etapas con origen de descuento en la primera etapa futura,

$$
\overline K_H=\sum_{k=0}^{H-1}\gamma^kK_k,\qquad
\Delta_{\mathrm{adapt}}^{(H)}=\sum_{k=0}^{H-1}\gamma^k\Delta_k
=2\eta_Dd x^T\overline K_He
-\eta_D^2(d^2+\sigma_D^2)x^T\overline K_Hx.
$$

k=0 evalúa los parámetros post-query antes de updates posteriores. Para identificar k=r−1 con la respuesta t+r se requiere que no haya update común antes de t+1 y que haya uno entre respuestas sucesivas. Sólo bajo ese calendario H=tau termina con K_{tau−1} en la respuesta t+tau. Si hay updates pendientes antes de t+1 o múltiples updates entre respuestas, deben usarse los productos correspondientes al calendario real; un calendario seleccionado por datos requiere además revisar las esperanzas. El protocolo de retardo por sí solo no garantiza la especialización i.i.d.

La contribución desde la ronda actual lleva gamma. Si K_k=M en todas las etapas, Kbar_H=(sum_{k=0}^{H−1} gamma^k)M y gamma Delta_adapt^(H)=B_H Delta_R, con B_H=sum_{r=1}^H gamma^r. Así se conserva el comparador anterior. B_H Delta_R era un analytical device sin transporte/deformación efectiva, no una descripción general de SGD. Gamma=0 da peso futuro cero en el objetivo actual.

**Inconsistencia notacional detectada y corregida:** en las secciones de horizonte aislado del paper y del cuaderno, Delta_adapt^(H) se había escrito con origen actual, mientras que la suma contrafactual con tau tenía origen en la primera respuesta futura. Se unifica la notación vigente al origen futuro y se añade gamma al miembro izquierdo de la identidad aislada. No se modifica ningún riesgo, signo ni comparador; el registro histórico de Decision 007 se conserva y esta entrada documenta la corrección.

### F. Contraejemplo recalculado: inversión dinámica bajo M=I

Se toma X=(G,R)^T, G normal estándar y R Rademacher ±1 equiprobable e independiente. Es una ley concreta para el ejemplo, **no rotacionalmente invariante**; no impone gaussianidad de los estados ni de la teoría base. M=I y

$$
\mathbb E[\|X\|^2XX^T]=\operatorname{diag}(3+1,1+1)=\operatorname{diag}(4,2).
$$

Los elementos cruzados se anulan por simetría e independencia. Con eta=0.4, K_1=diag(0.84,0.52). Para x=(1,1)^T, e=(−0.2012,0.2564)^T, b=0, sigma_D²=0.001, eta_D=0.2, aritmética racional exacta confirma:

- alpha=d=0.0552, alpha²=0.00304704;
- Delta_now=0.00204704>0;
- Delta_0=0.0008950528>0;
- x^T K_1 e=−0.03568 y x^T K_1 x=1.36;
- Delta_1=−0.0007878144−0.000220158976=−0.001007973376<0;
- eta_D‖x‖²=0.4<1.

El cuaderno conserva los cálculos y un fragmento reproducible de Python estándar con fracciones y aserciones; no se añaden simulaciones ni experimentos. Una elección completa admisible es ruido inicial independiente simétrico ±sqrt(0.001) y ruido de tarea/futuro cero.

**Interpretación:** D mejora la expected current task loss antes del coste de consulta; la pseudoactualización reduce inicialmente population risk; después de una actualización posterior común, el efecto transportado de esa misma pseudoactualización sobre population risk es negativo. La actualización inicial no cambia retrospectivamente: cambia el signo de su efecto contrafactual tras el aprendizaje posterior. No se deduce una decisión óptima de routing ni el signo de cualquier horizonte acumulado.

Aunque M=I, K_1 no es cI porque el cuarto momento relevante es anisotrópico. Isotropía a segundo orden no garantiza preservación temporal de la isotropía. No contradice la proposición previa, que se refiere sólo a una pseudoactualización y que aquí da correctamente Delta_0>0.

### G. Probabilidad positiva: respuesta parcial a Decision 008

Para el e fijo del ejemplo, las tres ganancias son continuas en x y estrictas en (1,1). Existe un entorno abierto donde persiste el patrón (y el paso inicial conservador). En la rama R=+1, ese entorno contiene un intervalo de G alrededor de 1, de densidad positiva; su probabilidad es al menos (1/2)P(|G−1|<delta)>0 para algún delta>0. No se atribuye masa al punto exacto ni se supone densidad bidimensional de X.

Esto demuestra probabilidad positiva **sobre inputs condicionada en ese estado e**. No demuestra que dicho estado aparezca con probabilidad positiva bajo una trayectoria natural de SGD, que el fenómeno sea frecuente o estacionario, que ocurra para todo e ni para toda distribución con M=I. La respuesta a la limitación de Decision 008 es parcial; la relevancia bajo estados inducidos por aprendizaje sigue abierta.

### H. Regla fiable mínima y alcance del common coupling

Se permite usar SGD ordinario al recibir Y_t:

$$
\theta^+=\theta+\eta_Yx_t(Y_t-\theta^Tx_t),\qquad
h^+=(I-\eta_Yx_tx_t^T)h.
$$

La segunda identidad se prueba por resta de los updates con el mismo target. No se obliga a deshacer la pseudoactualización. La diferencia histórica se transforma: la componente paralela a x_t se multiplica por 1−eta_Y‖x_t‖² y las ortogonales se conservan. La contracción paralela necesita 0<eta_Y‖x_t‖²<2; no se afirma contracción universal ni borrado automático. Otras U_Y siguen siendo posibles, sin ser necesarias para el modelo mínimo.

Se mantiene que Y_t llega después de la respuesta en t+tau y puede afectar por primera vez a t+tau+1. La identidad por realización no exige que esa reutilización de x_t cumpla los supuestos de muestras futuras i.i.d.; la fórmula cerrada de K_k y Delta_k sí debe justificarse de nuevo si se aplica a feedback condicionado/pendiente. No se oculta ese límite del teorema base.

El common coupling aísla el efecto adaptativo manteniendo común la evolución posterior. Si el cambio de parámetros altera decisiones futuras de routing, se necesita la diferencia completa de continuation/Q values, incluyendo respuestas y costes posteriores. Ninguna de las fórmulas de riesgo barato prueba optimalidad secuencial.

### I. Próximo objetivo abierto y cambios documentales

Analizar condiciones estructurales de persistencia/inversión. En particular, comprobar formalmente si una distribución rotacionalmente invariante con M=cI implica T(c'I)=c''I y, por inducción, K_k=c_kI. **No se resuelve aquí ni se afirma como resultado.** Si se confirma, estudiar la positividad de los factores necesaria para una condición limpia de persistencia del signo. Después, y sólo si es necesario, conectar con estados e_t inducidos por trayectorias naturales. No se introduce steady-state covariance de SGD, Gaussian e_t, distribution shift ni experimentos.

La extensión se integra tras la teoría single-update en `theoretical_analysis.tex`; `primary_notes.md` conserva las derivaciones completas, hipótesis, cálculo reproducible y caveats. `problem_formulation.tex` delimita el common coupling y la regla fiable mínima. Se corrigen brevemente las frases de Introduction que aún dejaban toda evolución contrafactual y U_Y sin especificar. README sólo cambia la frase que situaba como siguiente paso un desarrollo que ahora está parcialmente calculado. Related Work no requiere cambios ni expansión; no se añaden referencias ni se hace búsqueda bibliográfica. No se alteran los resultados matemáticos anteriores salvo la unificación explícita del origen de descuento.

### J. Validación documental

El recálculo racional confirma todas las cifras y signos del contraejemplo. `git diff --check` no detecta errores de whitespace. El paper compila con las herramientas disponibles de TeX Live 2026, sin instalar dependencias: pdfLaTeX, BibTeX y dos pasadas posteriores de pdfLaTeX. Los auxiliares y el PDF se generan fuera del repositorio, en un directorio temporal que conserva la relación `paper/primary`–`references` para resolver la bibliografía existente.

La compilación final produce 20 páginas, sin errores ni citas/referencias sin resolver. Quedan ocho avisos `Overfull \\hbox` en texto previo de Introduction, Related Work y los apartados anteriores de teoría/horizonte aislado; el mayor es 39.52344 pt en Related Work. Las ecuaciones nuevas no dejan avisos de desbordamiento. Se muestran `git status --short` y `git diff --stat` al cerrar la revisión. No se hace commit ni push.

## Decision 010 — Fourth-order geometry determines temporal sign persistence under second-order isotropy

Fecha: 2026-09-12.

### A. Decisión y alcance

Se cierra la pregunta estructural planteada en Decision 009: cuándo el aprendizaje posterior preserva el signo del valor de adaptación y cuándo puede deformarlo hasta invertirlo. El alcance es el modelo lineal-cuadrático, con M=E[XX^T]=cI, c>0, p>=2 y las hipótesis de common coupling, pares posteriores i.i.d., ruido condicionalmente centrado e independiente de la perturbación teacher inicial, y momentos finitos de Decision 009. No se generaliza al full continuation/Q value.

La finalidad sigue siendo **operational routing with learning value**: valorar una consulta atendiendo a su respuesta actual y al efecto de entrenar con ella después del aprendizaje posterior. No se presenta como nueva teoría de SGD, como contribución novedosa ni como un trabajo sobre estadísticas de cuarto orden. No se busca bibliografía ni se añaden referencias.

### B. Resultados probados: transporte escalar y persistencia

Definir H=E[||X||²XX^T], escrita mathsf H para distinguirla del horizonte escalar H de Decision 009. El cuarto momento finito hace finitas sus entradas. Para Q=qI, XX^T Q XX^T=q||X||²XX^T, por lo que

$$
\mathcal T(qI)=q[(1-2\eta c)I+\eta^2\mathsf H],\qquad
K_1=c[(1-2\eta c)I+\eta^2\mathsf H].
$$

Se verifican los factores c: el exterior corresponde al riesgo inicial K_0=cI y el interior al segundo momento de los inputs posteriores. No se introduce un factor c adicional dentro de mathsf H. Si mathsf H=rho I, lambda=1−2eta c+eta²rho satisface T(qI)=q lambda I. Por inducción K_k=c lambda^k I y, por el teorema de transporte, Delta_k=lambda^k Delta_0.

La positividad no se supone: T(I)=E[A²]=lambda I es PSD, y para cada X

$$
\operatorname{tr}(A^2)=p-1+(1-\eta\|X\|^2)^2\geq p-1.
$$

Para X no nulo, A es la identidad en las p−1 direcciones ortogonales. Para X=0, A=I y la igualdad da exactamente p. Es válida para cualquier eta real. Tomando esperanza, lambda>=(p−1)/p>0 si p>=2. La proposición de persistencia concluye sign(Delta_k)=sign(Delta_0) para todo k finito, incluyendo el signo cero. No se deduce contracción ni se toma un límite temporal infinito.

### C. Corolarios probados

**Compatibilidad temporal:** Delta_now>0 y 0<eta_D||x||²<=1 implican Delta_0>0 por la compatibilidad isotrópica previa; la proposición implica Delta_k>0 para todo k finito. Esto se refiere al componente de adaptación bajo continuación común, no al beneficio total neto de consulta ni a optimalidad.

**Invariancia rotacional:** si OX tiene la misma ley que X para toda matriz ortogonal O, M y mathsf H son invariantes bajo conjugación por O. Cambios de signo de coordenadas anulan términos fuera de la diagonal y permutaciones igualan las diagonales. Las trazas dan

$$
M=\frac{\mathbb E\|X\|^2}{p}I,\qquad
\mathsf H=\frac{\mathbb E\|X\|^4}{p}I.
$$

Con cuarto momento finito y E||X||²>0 aplica la proposición bajo las restantes hipótesis de transporte. Se excluye la ley degenerada X=0 casi seguramente porque no cumple c>0. Rotational invariance es suficiente, no necesaria; se presenta como corolario.

### D. Brazo anisótropo y auditoría singular

Si mathsf H no es escalar y eta>0, K_1 no es escalar, ya que c eta²>0. Su definición E[A^T M A] garantiza simetría y semidefinitud positiva. La construcción geométrica sólo necesita PSD: elegir autovectores ortonormales u,v con autovalores 0<=r<s y x=u+v da x^T K_1 x=r+s>0, ||K_1x||²=r²+s²>0 y x no autovector. La diferencia de Cauchy–Schwarz es (s−r)²>0. Todo sigue siendo válido con r=0<s.

Los denominadores son positivos y el intervalo

$$
\frac{x^TK_1x}{\|K_1x\|^2}<\kappa<\frac{\|x\|^2}{x^TK_1x}
$$

es no vacío. Con e=x−kappa K_1x se obtiene alpha=x^T e>0 y x^T K_1e<0. No se invierte K_1 ni aparece una excepción por singularidad.

**Precisión detectada en la auditoría solicitada:** el K_1 realizable bajo M=cI, c>0 y p>=2 no puede ser singular. Si z no nulo anulara z^T K_1z=c E||Az||², tendríamos Az=0 casi seguramente, es decir z=eta X(X^Tz), y X estaría casi seguramente en la recta de z. Esto contradice M=cI de rango p>=2. Se documentan tanto esta exclusión específica del modelo como la validez de la construcción PSD incluso para una matriz singular abstracta. No se añade una hipótesis de invertibilidad.

### E. Teorema probado de posibilidad de inversión

Para el x,e construidos, elegir b=0, 0<sigma_D²<alpha² y 0<eta_D||x||²<=1. Un teacher de ruido simétrico independiente ±sqrt(sigma_D²) satisface los momentos requeridos y la ortogonalidad con el ruido de tarea. Entonces Delta_now=alpha²−sigma_D²>0 y la compatibilidad isotrópica da Delta_0>0. Pero

$$
\Delta_1=2\eta_D\alpha x^TK_1e
-\eta_D^2(\alpha^2+\sigma_D^2)x^TK_1x<0.
$$

El término lineal y el término cuadrático con su signo negativo son estrictamente negativos. Se demuestra existencia algebraica de input, estado, teacher unbiased/falible y pseudo-step conservador con Delta_now>0, Delta_0>0 y Delta_1<0. No se afirma inversión universal, frecuencia ni tipicidad de estados de SGD.

### F. Dos implicaciones y cuantificadores del iff

Se mantienen dos implicaciones: mathsf H isotrópica implica preservación temporal universal del componente transportado; mathsf H anisótropa hace posible una inversión en una configuración algebraica inicialmente beneficiosa. El teorema permite elegir x en R^p y no garantiza que ese vector esté en el soporte de P_X.

Un iff sería defendible si «universal» cuantificara expresamente sobre todos los x del espacio ambiente, estados, teachers y pseudo-steps compatibles, con una ley futura y eta>0 fijos: la construcción negaría esa propiedad en el brazo anisótropo. Pero no justifica un iff sobre inputs del soporte o configuraciones realmente encontradas, ni para cualquier teacher/paso previamente fijados. Por esa sutileza operacional, no se escribe un bicondicional formal en el paper. Las conclusiones no se traducen en frecuencia o tipicidad bajo aprendizaje.

### G. Ejemplo preservado e interpretación científica

Se conserva y recalcula el contraejemplo de Decision 009: M=I, mathsf H=diag(4,2), eta=0.4 y K_1=diag(0.84,0.52). Los valores exactos permanecen alpha=0.0552, Delta_now=0.00204704, Delta_0=0.0008950528, x^T K_1e=−0.03568, Delta_1=−0.001007973376 y eta_D||x||²=0.4. Es una instancia concreta del teorema; su argumento específico de probabilidad positiva sobre inputs a estado fijo sigue siendo válido y no se generaliza al teorema de existencia.

Decision 010 generaliza la explicación estructural: con mathsf H isotrópica el efecto sólo se reescala positivamente; con mathsf H anisótropa la geometría puede deformarse lo suficiente para invertir el signo transportado. La pseudoactualización inicial no cambia retrospectivamente. Para routing, valorar sólo Delta_R puede valorar mal una consulta cuyo efecto debe transportarse a través del aprendizaje posterior.

### H. Bridge al diseño experimental

El paper tenía el comparador aislado y Delta_adapt acumulado, pero faltaba una expresión compacta que los conectara para transporte general. Se añade una única formulación bajo continuación fija/común de H etapas:

$$
\Delta_{\mathrm{now}}(S_t,x_t)-C_D(S_t,x_t)
+\gamma\Delta_{\mathrm{adapt}}^{(H)}.
$$

C_D es el coste incremental ya definido en Problem Formulation; no hay un C_F adicional que restar. Se conserva el origen futuro de Delta_adapt y su gamma exterior. Las etapas deben corresponder al calendario documentado: Y_t llega después de responder en t+tau y puede afectar por primera vez a t+tau+1. Es un surrogate gain para evaluación, no una regla práctica ni un teorema de optimalidad. El riesgo barato no equivale automáticamente a toda la continuación operacional cuando cambia el routing futuro.

### I. Auditoría final de suficiencia

The core theoretical chain is now:

1. (a) current operational gain Delta_now;
2. (b) exact single-update population-risk gain Delta_R;
3. (c) compatibility/conflict geometry;
4. (d) delayed reliable feedback protocol;
5. (e) common-coupled transport h_k=P_k h_0;
6. (f) exact transported adaptation value Delta_k;
7. (g) accumulated value through Kbar_H;
8. (h) dynamic sign reversal;
9. (i) structural characterization of sign preservation/reversal under M=cI, con el alcance geométrico y los límites de soporte declarados.

**Valoración de suficiencia:** esta cadena queda suficientemente cerrada para comenzar el diseño del primer ciclo experimental. El paper mantiene pruebas y limitaciones y el cuaderno conserva derivaciones completas y comprobaciones reproducibles. No hace falta demostrar frecuencia de los estados construidos para que el mecanismo sea una pregunta experimental bien definida. No se afirma que ya haya validación empírica ni un algoritmo implementado.

No se consideran prerrequisitos del primer paper resolver full adaptive Q values, regret bounds, stationary SGD distributions, la distribución de e_t, teoría general de learners no lineales, feedback pendiente arbitrario no i.i.d. ni una forma cerrada general de T^k fuera del caso estructural. Son posibles extensiones y se enumeran sin desarrollarlas. Las cuestiones experimentales son si valorar el transporte mejora la valoración de consultas frente al valor de una sola actualización y cómo se refleja en pérdida operacional más costes; no se anticipan las respuestas.

### J. Congelación de la teoría principal

**Core theory frozen for first experimental cycle.** Se pueden corregir errores matemáticos y añadir aclaraciones necesarias. Las extensiones teóricas nuevas quedan congeladas hasta que los experimentos indiquen una necesidad concreta. Tras integrar esta decisión no se resuelven nuevos problemas matemáticos ni se diseñan o ejecutan experimentos en este cambio.

Se actualizan el cuaderno, la teoría del paper, el framing breve de Introduction y el alcance de Problem Formulation. README actualiza el estado para dar paso al diseño experimental y conserva las cautelas sobre novedad. Related Work no presenta contradicción y no se modifica. Los resultados previos se conservan; las precisiones matemáticas nuevas son la cota estricta de lambda, la exclusión de singularidad de K_1 bajo las hipótesis actuales, el caso degenerado del corolario rotacional y los cuantificadores de la construcción.

### K. Validación final

Se ejecutan los fragmentos reproducibles del cuaderno con Python estándar y aritmética racional: pasan el contraejemplo de Decision 009, los factores de transporte con c=2 y las construcciones PSD con autovalores distintos, incluido uno cero en una matriz abstracta. Las pruebas generales se verifican algebraicamente; estas comprobaciones no las sustituyen. Una comparación textual con el estado inicial confirma que las secciones anteriores de compatibilidad, conflicto y transporte se conservan.

`git diff --check` termina sin errores. Se compila el estado inicial para comparar avisos y, después del cambio, se ejecutan pdfLaTeX, BibTeX y dos pasadas adicionales de pdfLaTeX, sin instalar dependencias ni escribir auxiliares en el repositorio. El PDF final tiene 24 páginas, sin errores ni citas/referencias sin resolver. Persisten exactamente los ocho avisos `Overfull hbox` de la compilación inicial, con las mismas anchuras; el mayor es 39.52344 pt en Related Work. No aparecen warnings nuevos. Se muestran `git status --short` y `git diff --stat`; no se hace commit ni push.

## EP001-B2 — Preregistration frozen before execution

Se congela [EP001-B2 — Scalar reducibility of transported adaptation value](experiments/ep001b2_scalar_reducibility.md) mediante este registro y el commit que incorpora ambos documentos. El texto del protocolo conserva su encabezado de preparación; este registro establece su congelación antes de implementación o ejecución. La amenaza de reducibilidad escalar observada después de EP001-B motiva una prueba adversarial de compresibilidad, no una validación externa del funcional de transporte. EP001-A sigue cerrado con el veredicto `FAILS TO SUPPORT THE PHENOMENON IN THE TESTED REGIME`.

- La población primaria son todos los casos congelados de EP001-A con `Delta_now` y `Delta_0,...,Delta_9` finitos; el antiguo filtro `eligible` es secundario exclusivamente. Se conservan H=10 y gamma en {0.5, 0.9, 1.0} con el gamma exterior de la convención teórica.
- La rejilla primaria fija comprende configs 0–75, en 19 grupos de trayectorias base. Se excluyen configs 76–79: config79 generó la hipótesis y todo el cuarteto comparte trayectorias y queries. No se considera la rejilla una muestra aleatoria de entornos.
- Q1 evalúa reducibilidad escalar funcional y Q2 reducibilidad operacional sobre costes factibles `C_D >= 0`. La jerarquía es M0 estático, M1 escalar global y M2 escalar por configuración. M2 es deliberadamente un adversario fuerte de compresibilidad, calibrado con información oracle; no se presupone que sea desplegable.
- Las calibraciones funcional LAD y operacional son separadas, con escalares primarios no restringidos. La minimización operacional es global por regiones lineales, con desempate determinista que favorece el escalar funcional congelado.
- El endpoint operacional primario sigue siendo el ancho factible de desacuerdo sobre todos los casos, `L_A+`. Las pérdidas absolutas y sus intervalos son obligatorias antes de interpretar reducciones relativas. Los diagnósticos de región activa fija y regiones positivas inducidas por el escalar son secundarios; no sustituyen el endpoint global.
- Los escalares se aprenden sólo con discovery (seeds 0–19) y se congelan antes de inspeccionar confirmation (20–49). La ponderación es configuración, trayectoria y caso, con igual peso en cada nivel. El bootstrap confirmatorio de 10.000 réplicas preserva las trayectorias completas y el emparejamiento dentro de cada cuarteto, remuestrea independientemente los 19 grupos y no reajusta coeficientes.
- No se establece un margen arbitrario de equivalencia ni de pass/fail. Las conclusiones quedan condicionadas a la rejilla sintética y al surrogate; no prueban superioridad operacional ni autorizan avanzar automáticamente a EP001-C.

La comprobación final documental confirma compatibilidad con el horizonte, descuento, dominio de costes y claves RNG existentes; no identifica una contradicción que impida implementar el protocolo. Las discrepancias históricas de redacción sobre independencia y la columna `median_delta_c` de EP001-B ya están delimitadas en el protocolo y no se heredan como definiciones de B2. Antes de esta congelación no se ha ajustado ningún escalar B2, ejecutado ningún análisis B2 ni inspeccionado resultados de reducibilidad confirmatoria para configs 0–75. No se autorizan nuevas simulaciones para B2; cualquier ejecución posterior requiere autorización separada y utiliza exclusivamente los datos preservados. Teoría, paper y resultados EP001-A/B permanecen intactos.

## Applied novelty gate after EP001-B2 — 2026-09-13

EP001-B2 demotes exact state-dependent transport $K_k$ as the empirical centerpiece. Before any EP001-C, the project therefore moves to an applied novelty gate. Cloud-edge forecasting is currently the strongest candidate application because delayed reliable ground truth arrives naturally and independently of routing. CE-CoLSM (ICC 2026) is the current anchor prior-art and novelty threat.

The surviving candidate gap is not cloud-edge collaboration or distillation itself. It is whether the query decision should explicitly value the future learning consequence of the queried supervision. No claim of practical scalar “persistence” is made: B2 supports only configuration-specific scalar compressibility in the frozen synthetic grid. Closed-loop evaluation will be required before making operational claims. The applied audit is preserved in `docs/literature/applied_novelty_audit.md`.

## Standing research direction: complementary timescales under concept drift — 2026-09-13

The broader project must not collapse into a narrow cloud-edge routing problem.

**Established core.** The established problem structure comprises a cheap/adaptive predictor F and an expensive/more capable predictor D; selective routing with query cost; the possibility that D supplies the current operational response and its output supervises F; reliable Y arriving later independently of routing; and the decomposition into immediate value plus future learning value. The transported-effect theory and the EP001-A/B/B2 findings remain part of this established project record, with their documented scopes and limitations.

**Dynamic condition to be covered.** The environment or regime may change over time. Consequently, relative model performance, query value and learning value may also change. This condition motivates the broader direction but is not yet a new formal model or experimental result.

**Open working hypotheses, not an established architecture.** Future work may study adaptation under concept drift through models with complementary timescales and capabilities:

- fast, shallow, rapidly adaptable models;
- slow, deep, more capable models;
- dynamic redistribution of their roles according to individual and collective performance;
- under sufficiently strong regime change, replacement or regeneration of one or more models may be preferable to transferring knowledge from obsolete models.

Two candidate adaptation scales organize these open hypotheses:

1. **Intra-regime:** routing/querying and adaptation of existing models.
2. **Inter-regime:** drift detection, role redistribution, retraining, replacement, or creation of new models.

CE-CoLSM and traffic forecasting are currently a candidate testbed for the applied gate, not the definition of the research problem.

## EP001-C — Closed-loop routing closure, confirmation_001 — 2026-09-13

**Protocol and implementation.** EP001-C was preregistered in commit
`157765a`, then transparently amended before any implementation or EP001-C
result to fix the previously omitted trajectory length at (T=2000) rounds
(`5050470`). The amended preregistration SHA-256 is
`9d5af0f7652bd36e3c05c96a247a3e989df32fa1fb9534ca1900f91c3e1c1d1b`.
It compares P0 immediate routing, P1 static future value, P2 frozen
configuration-specific scalar compression, and P3 the exact
reference-coupled local transported-value surrogate. P3 is not a
policy-dependent continuation-value oracle. P2 coefficients are frozen from
EP001-B2 and never refit. Two pre-artifact performance corrections (operator
stack caching and seed vectorization) were tested and committed before the
completed discovery output; no parameter or endpoint changed.

**Empirical result.** Discovery seeds 0--19 fixed the cost grid and were
frozen before confirmation. Confirmation uses configs 0--75 and seeds 20--49,
with paired policy streams and 10,000 trajectory-level bootstrap replicates
preserving shared quartet dependence. The full artifact record and all
gamma/cost/configuration outcomes are in
`docs/experiments/ep001c_results_001.md` and the versioned results hierarchy.

**Interpretation.** The confirmation verdict is **AMBIGUOUS**. At gamma 1.0,
P3 improves P0 across low/intermediate costs and P2 almost exactly reproduces
that improvement (C1-type behavior). At gamma 0.9, P3 is systematically worse
than P0 at several low/intermediate costs even though it is generally slightly
better than P1 there (C5-type behavior). Gamma 0.5 is mainly null/mixed. Thus the exact
reference-coupled transported quantity is not a robustly beneficial
closed-loop routing rule across the frozen grid. It can help or harm depending
on discount/cost regime. P1 is not uniformly sufficient, but neither P2 nor
P3 supplies a stable universal improvement.

**Scope and retained record.** Routing and policy differences are concentrated
in the initial stationary learning transient; later thirds are largely
inactive. EP001-C therefore speaks only to transient adaptive routing in this
stationary synthetic environment. The mathematical (K_k) derivation remains
valid for its common-update reference counterfactual; it is demoted as an
empirical centerpiece and should not be advanced as a universal practical
mechanism. The immediate/static baselines, the reference-coupled diagnostic,
and B2's within-configuration scalar-compressibility observation are retained
with their stated limitations. No conclusion is drawn about general
future-aware routing, real deployments, concept drift, or applications.
