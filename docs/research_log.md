# Research log

Decision 009 establece el estado científico vigente y extiende temporalmente la teoría de una pseudoactualización. Las decisiones anteriores conservan su contexto histórico: siguen vigentes la auditoría y las cautelas de Decision 006, el protocolo y los resultados algebraicos de Decision 007 y la revisión independiente y limitaciones de Decision 008. Los objetivos que entonces estaban abiertos se actualizan en Decision 009.

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
