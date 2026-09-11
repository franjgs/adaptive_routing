# Primary technical notes

Cuaderno de razonamiento y derivaciones de **Adaptive Cost-Aware Routing with Learning Value**. Decision 007 fija el protocolo base y el modelo lineal mínimo. El protocolo estabilizado se documenta en `paper/primary/sections/problem_formulation.tex`; los resultados algebraicos, con pruebas y carácter preliminar para revisión científica, en `theoretical_analysis.tex`. Una identidad algebraica demostrada bajo condiciones explícitas no establece novedad ni optimalidad de una política secuencial.

## Estado científico y relación con Decision 006

La auditoría dirigida de Decision 006 y sus límites siguen vigentes. Valor futuro de aprendizaje, ruido, consulta selectiva, actualización online, expertos locales y perjuicio por supervisión adicional tienen antecedentes. Selective sampling puede ser exploratorio y no-myopic; no se caracteriza globalmente como miope. La búsqueda amplia permanece pausada. Decision 007 satisface la prioridad protocolaria de Decision 006 y adopta una especialización lineal; no reinterpreta la auditoría como prueba de novedad.

La región candidata conserva los seis componentes: routing antes de la respuesta final; D sustituye a F; la misma respuesta actualiza F; valoración inmediata; valoración del efecto futuro de esa actualización particular; y D falible con valor de adaptación potencialmente negativo. La geometría de gradientes no se reivindica como novedosa. Véase la cautela bibliográfica en la revisión de novedad.

## Protocolo: supervisión anticipada, no compra de ground truth

En la ronda t se observa x_t y se elige A_t en {F,D} antes de responder. Si se elige D, su salida Z_t=D(x_t) es la respuesta operacional y se reutiliza inmediatamente para pseudoactualizar F_theta. Si se elige F, no se genera esa pseudoactualización. El target fiable Y_t llega tras un retardo fijo tau, exógeno e independiente de A_t, y puede usarse después para corregir/actualizar F. No se presupone que esa corrección deshaga exactamente el update ni que haga coincidir ambas historias.

Para contar el horizonte, Y_t queda disponible después de la respuesta de t+tau, antes de que pueda usarse en respuestas posteriores. Así las respuestas t+1,...,t+tau no usan todavía Y_t. Durante ese intervalo pueden llegar labels de muestras anteriores. El estado conserva parámetros, información disponible, tiempos y feedback pendiente; no se afirma suficiencia de un estado finito.

El protocolo base comienza con hard labels en clasificación. En la especialización de regresión lineal, la supervisión es una respuesta escalar puntual, no una etiqueta binaria ni logits. Logits, confianza y ground truth ocasional son extensiones. «Fiable» significa que se observa el target real, no que el proceso generador carezca de ruido intrínseco.

Sin Y observado, el rendimiento frente a Y no es identificable en general sólo a partir de D sin supuestos fuertes sobre D: distintas relaciones con Y pueden ser compatibles con los mismos outputs del teacher. El feedback retrasado permite evaluar y corregir respecto a la tarea, sin convertir la consulta a D en adquisición activa de Y. Se distinguen:

- **Imitation of D:** acuerdo con el teacher.
- **Task performance wrt Y:** pérdida respecto al target fiable.
- **Total system objective:** pérdida operacional más coste de routing.

La consulta compra una posible mejora de inferencia actual y supervisión anticipada imperfecta; no compra Y ni garantiza mejora.

## Notación y condiciones de validez

Se usa una única notación vigente: F_theta y D para los predictores; A_t para routing; e=theta-w*; M=E[XX^T]; alpha=x^T e; beta=x^T b; sigma_D^2 para la varianza del ruido del teacher; Delta_now para ganancia inmediata; Delta_R para el cambio de riesgo poblacional de UNA pseudoactualización; Delta_adapt para el valor ACUMULADO, indicando horizonte y origen de descuento. Los antiguos Delta_pred y Delta_learn son denominaciones históricas de ganancia inmediata y continuación, respectivamente; Delta_R no sustituye al segundo como si fueran iguales. Se reserva a=eta||x||^2 para el tamaño local del paso y tau exclusivamente para el retardo.

Modelo mínimo bajo pérdida cuadrática:

$$
Y=(w^*)^T X+\epsilon,\qquad F_\theta(x)=\theta^T x,
\qquad D(x)=(w^*+b)^T x+\nu,
$$

$$
e=\theta-w^*,\quad M=\mathbb E[XX^T]\succ0,\quad
\alpha=x^T e,\quad\beta=x^T b,\quad
\mathbb E[\nu]=0,\quad\operatorname{Var}(\nu)=\sigma_D^2.
$$

M es el segundo momento, no necesariamente la covarianza centrada. Se mantienen fijos el estado previo, e y b al comparar acciones. Las identidades condicionadas en x requieren **E[nu|x]=0 y E[nu^2|x]=sigma_D^2**; no se deducen sólo de los momentos marginales anteriores. La interpretación de Delta_now como diferencia de pérdidas frente a Y requiere además **E[epsilon|x]=0, E[epsilon nu|x]=0**, con segundos momentos finitos. Son condiciones explícitas de validez de esta especialización, no una hipótesis de gaussianidad o independencia completa. Si esos momentos condicionales no se sostienen, deben conservarse los términos adicionales; no debe usarse silenciosamente la fórmula simplificada.

En efecto, antes de imponerlos,

$$
\mathbb E[(F_\theta(x)-Y)^2-(D(x)-Y)^2\mid x]
=\alpha^2-\beta^2-\mathbb E[\nu^2\mid x]
-2(\alpha-\beta)\mathbb E[\epsilon\mid x]
-2\beta\mathbb E[\nu\mid x]+2\mathbb E[\epsilon\nu\mid x].
$$

Bajo las condiciones declaradas, el ruido intrínseco común de la tarea se cancela y

$$
\boxed{\Delta_{\mathrm{now}}=\alpha^2-\beta^2-\sigma_D^2.}
$$

El riesgo poblacional excedente del predictor barato es

$$
R(e)=\mathbb E[(X^T e)^2]=e^T M e.
$$

El riesgo frente a Y añade el ruido irreducible común; R no incluye costes de consulta y no es el objetivo total del sistema. Las cantidades w*, b y M no se suponen conocidas por un router implementable: por ahora son objetos del análisis idealizado, no estimadores operacionales ya construidos.

## Antecedente escalar

En una dimensión, M=c=E[X^2]>0, e=theta-w*, alpha=xe, beta=xb. Para una entrada fija x distinta de cero y a=eta x^2,

$$
\theta^+=\theta+\eta x(D(x)-\theta x),\qquad
e^+=(1-a)e+ab+\eta x\nu.
$$

Por tanto,

$$
\mathbb E[(e^+)^2\mid x]=[(1-a)e+ab]^2+\eta^2x^2\sigma_D^2,
$$

$$
\Delta_R=c\{2a e(e-b)-a^2(e-b)^2-\eta^2x^2\sigma_D^2\}
=\frac{c}{x^2}\{2a\alpha(\alpha-\beta)-a^2[(\alpha-\beta)^2+\sigma_D^2]\}.
$$

Si Delta_now>0, entonces sigma_D^2<alpha^2-beta^2 y |alpha|>|beta|, de donde alpha(alpha-beta)>0. Además,

$$
(\alpha-\beta)^2+\sigma_D^2
<(\alpha-\beta)^2+\alpha^2-\beta^2
=2\alpha(\alpha-\beta).
$$

Para 0<a<1,

$$
\Delta_R>\frac{2ca}{x^2}\alpha(\alpha-\beta)(1-a)>0.
$$

Así es imposible el patrón **(Delta_now>0, Delta_R<0)** en 1D en ese régimen. El resultado se extiende a a=1: la cota final vale cero, pero la primera desigualdad continúa siendo estricta. Para x=0, no hay pseudoactualización y Delta_now=-sigma_D^2<=0, por lo que la hipótesis de superioridad estricta no se cumple.

Esta compatibilidad no dice que el router miope sea óptimo: compara signos, no beneficio total frente a un coste. Tampoco permite extender el resultado a cualquier paso localmente estable.

## Extensión vectorial: resultado algebraico central

La misma salida realizada del teacher se usa para responder y para actualizar:

$$
\theta^+=\theta+\eta x(D(x)-\theta^T x),\qquad
e^+=e-\eta x(\alpha-\beta)+\eta x\nu.
$$

Escribiendo d=alpha-beta y h=eta x(nu-d),

$$
R(e+h)=R(e)+2h^TMe+h^TMh.
$$

Los momentos condicionales dan E[h|x]=-eta xd y
E[h^TMh|x]=eta^2(d^2+sigma_D^2)x^TMx. Por tanto,

$$
\boxed{
\Delta_R(x)=R(e)-\mathbb E[R(e^+)\mid x]
=2\eta(\alpha-\beta)x^TMe
-\eta^2[(\alpha-\beta)^2+\sigma_D^2]x^TMx.
}
$$

Esta identidad exacta es el resultado algebraico central del modelo mínimo. No es una fórmula del valor secuencial total. La parte cuadrática no es positiva, y es estrictamente negativa cuando x no es cero y (alpha-beta)^2+sigma_D^2>0. Sin momentos condicionales centrados, los términos serían 2eta(d-E[nu|x])x^TMe y -eta^2 E[(nu-d)^2|x]x^TMx.

## Geometría: calidad de respuesta y valor de entrenamiento

Delta_now sólo compara los errores locales alpha y beta y el ruido del teacher. Delta_R evalúa cómo una actualización dirigida por esa muestra modifica el riesgo sobre la población futura ponderada por M. En particular,

$$
\nabla R(e)=2Me,\qquad x^TMe=\tfrac12x^T\nabla R(e).
$$

El término de primer orden para eta pequeño es **(alpha-beta)x^TMe**. Una respuesta localmente superior no garantiza que su dirección de entrenamiento reduzca el riesgo poblacional. Teacher reliability / immediate superiority no equivale a training value. Si ese producto es positivo, el término lineal domina para pasos suficientemente pequeños; si es negativo, ambos términos son negativos para cualquier eta>0. Si es cero, el término cuadrático determina el signo salvo degeneración.

La posibilidad general de desalineamiento entre el gradiente de una muestra y el gradiente poblacional ya pertenece a gradient alignment, influence functions y data valuation. No se reivindica como novedad ni tampoco el perjuicio de una actualización. TODO bibliográfico: identificar referencias específicas verificadas si se desea citar estas familias; no se añade BibTeX sin metadata verificada.

## Prueba de compatibilidad isotrópica

Si M=cI, c>0, entonces x^TMe=c alpha y x^TMx=c||x||^2. Con a=eta||x||^2,

$$
\Delta_R=c\eta\{2\alpha(\alpha-\beta)-a[(\alpha-\beta)^2+\sigma_D^2]\}.
$$

Bajo Delta_now>0, la misma desigualdad estricta del caso escalar implica

$$
\Delta_R>2c\eta\alpha(\alpha-\beta)[1-\eta\|x\|^2]\geq0
\quad\text{si }0<\eta\|x\|^2\leq1.
$$

La positividad es estricta también en a=1. Es compatibilidad universal entre superioridad inmediata y adaptación positiva **dentro del régimen conservador**, no una afirmación de optimalidad de routing ni de ausencia de fallos fuera del régimen.

## Estabilidad y overshoot

Para una entrada fija, el componente residual noiseless en la dirección de x tiene multiplicador 1-a. Deben distinguirse:

- **Conservative regime:** 0<a<=1, sin cambio de signo de ese multiplicador.
- **Locally stable / possible overshoot:** 1<a<2, multiplicador negativo de módulo menor que uno.

«Localmente estable» en ese sentido no garantiza descenso del riesgo poblacional con ruido, anisotropía o secuencias de entradas. No se debe etiquetar simplemente como «stable» todo 0<a<2 y usarlo como premisa de compatibilidad.

Como comprobación algebraica escalar, x=1, M=1, e=1, b=-0.9, sigma_D^2=0 y eta=1.5 dan Delta_now=0.19>0 pero e^+=-1.85 y Delta_R=1-1.85^2<0. Es overshoot fuera del régimen conservador, no el conflicto anisotrópico para pasos arbitrariamente pequeños. No es un experimento ni un resultado general adicional.

## Construcción anisotrópica por Cauchy–Schwarz estricta

Si M es definida positiva y no es cI, existe un x no nulo que no es autovector. Entonces Mx no es colineal con x y

$$
(x^TMx)^2<\|x\|^2\|Mx\|^2.
$$

Como x^TMx>0, esta desigualdad equivale a que el intervalo siguiente no sea vacío:

$$
\frac{x^TMx}{\|Mx\|^2}<k<\frac{\|x\|^2}{x^TMx}.
$$

Elegir cualquier k interior y e=x-kMx da

$$
x^Te=\|x\|^2-kx^TMx>0,\qquad
x^TMe=x^TMx-k\|Mx\|^2<0.
$$

Tomando b=0 y 0<sigma_D^2<alpha^2 se obtiene Delta_now>0, pero

$$
\Delta_R=2\eta\alpha x^TMe-\eta^2(\alpha^2+\sigma_D^2)x^TMx<0
\qquad\text{para todo }\eta>0.
$$

La construcción elige una configuración de theta mediante e; no afirma que cualquier estado del aprendiz presente ese conflicto. Tampoco garantiza que un x de conflicto tenga probabilidad positiva bajo toda distribución con segundo momento M: la existencia algebraica no es un teorema de frecuencia de consultas conflictivas.

La conclusión correcta es: M=cI da compatibilidad universal bajo updates conservadores; M distinto de cI permite **existencia** de configuraciones con conflicto incluso para updates arbitrariamente pequeños. No se afirma que la anisotropía haga perjudicial toda consulta, ni que ruido o sesgo sean necesarios para generar el desalineamiento geométrico.

## Fallos del comparador miope y horizonte aislado H

El comparador miope consulta D iff Delta_now>C_D. «Miope» describe este comparador que omite valor de adaptación, no selective sampling en general.

En una simplificación de aislamiento, ambas ramas difieren sólo en esa pseudoactualización; el riesgo se mantiene sin nuevos updates durante H respuestas futuras anteriores al uso de Y_t. Se omiten diferencias de routing/coste posteriores y efectos después del horizonte. Esta truncación no se deduce del mero retardo ni de la existencia de una corrección fiable.

Para el objetivo descontado desde la ronda actual,

$$
B_H=\sum_{k=1}^{H}\gamma^k,\qquad
\Delta_{\mathrm{adapt}}^{(H)}=B_H\Delta_R,
$$

$$
\text{consult D iff}\quad\Delta_{\mathrm{now}}+B_H\Delta_R>C_D.
$$

Es un criterio future-aware idealizado, no la solución del objetivo completo. Se contemplan separadamente:

1. **Under-querying:** Delta_now<C_D pero Delta_now+B_H Delta_R>C_D.
2. **Over-querying:** Delta_now>C_D pero Delta_now+B_H Delta_R<C_D.

Under-querying ya es posible en 1D. Por ejemplo algebraico, x=1, M=1, e=1, b=0, sigma_D^2=1/4 y eta=1/2 dan Delta_now=3/4 y Delta_R=11/16. Para H=1, gamma=1 y C_D=1, el comparador miope no consulta pero 3/4+11/16=23/16>1. El signo positivo de ambos valores no evita la diferencia de decisión frente al coste.

Para over-querying, una configuración de conflicto anisotrópico da Delta_now>0 y Delta_R<0. Si B_H>0, el intervalo

$$
\max\{0,\Delta_{\mathrm{now}}+B_H\Delta_R\}<C_D<\Delta_{\mathrm{now}}
$$

no es vacío y produce la decisión opuesta entre comparadores. Es un corolario de existencia bajo aislamiento y elección del coste en ese intervalo; no demuestra over-querying para todos los costes ni una política secuencial óptima. Ambos mecanismos no se presentan como un único teorema general. Si gamma=0, B_H=0 y estos fallos por valor futuro no aparecen en el objetivo actual.

## Próximo problema: eliminar el aislamiento durante tau pasos

Partiendo del mismo estado previo, comparar las ramas contrafactuales iniciadas por F y D, incluyendo updates intermedios y feedback retrasado de muestras anteriores. Definir e_{t+k}^F y e_{t+k}^D como los errores del predictor barato antes de cada respuesta futura en esas ramas. El siguiente objeto a calcular es

$$
\Delta_{\mathrm{adapt}}^{(\tau)}=
\sum_{k=1}^{\tau}\gamma^{k-1}\mathbb E\left[
(e_{t+k}^F)^T M e_{t+k}^F-(e_{t+k}^D)^T M e_{t+k}^D
\right].
$$

La esperanza se refiere al estado inicial común y a las evoluciones contrafactuales bajo políticas de continuación y reglas de actualización que deberán especificarse. Este problema **no está resuelto**: hay que calcular la evolución, no sustituirla por un gap congelado.

**Convención de descuento:** esta última expresión toma la primera respuesta futura como origen. El B_H anterior descuenta desde la ronda actual; por eso, bajo aislamiento con H=tau,

$$
\gamma\Delta_{\mathrm{adapt}}^{(\tau)}=B_H\Delta_R.
$$

Si se usa en su lugar un peso con origen futuro, sum_{k=1}^H gamma^{k-1}, hay que multiplicarlo por gamma al compararlo con la pérdida inmediata del objetivo J. No se omite ni se duplica ese factor. Con gamma=1 ambas convenciones coinciden.

La suma propuesta mide riesgo poblacional del predictor barato. Identificarla con el valor de continuación total requiere además contabilizar la elección de respuestas operacionales futuras y sus costes. La llegada exógena de Y_t no implica que las ramas se igualen ni que el efecto causal termine allí. Quedan abiertos la regla de corrección fiable, las políticas de continuación, los efectos después de tau y la computabilidad de estos valores. No se afirman regret bounds ni tasas asintóticas de regret.

## Revisión independiente posterior a Decision 007

Esta sección registra la red-team review de Decision 008. Separa los resultados confirmados de la crítica externa, la respuesta y los problemas abiertos; no modifica las derivaciones anteriores ni las ecuaciones del paper.

### Resultado probado y confirmado

La revisión recalculó de forma independiente y confirmó:

- $\Delta_{\mathrm{now}}=\alpha^2-\beta^2-\sigma_D^2$ bajo las condiciones ya declaradas;
- la expresión exacta de $\Delta_R$ para una pseudoactualización;
- la compatibilidad isotrópica si $0<\eta\|x\|^2\leq1$;
- la construcción anisotrópica basada en Cauchy--Schwarz estricta;
- la lógica algebraica de under-querying y over-querying bajo el horizonte aislado.

El teorema anisotrópico se mantiene. Es una afirmación geométrica de existencia sobre configuraciones $(x,e)$: no establece probabilidad positiva bajo una distribución concreta ni frecuencia bajo trayectorias naturales de SGD. La construcción tampoco describe por sí sola cómo el aprendizaje lleva a esas configuraciones.

### Crítica externa

La revisión planteó que la dinámica de SGD podría alinear $e_t$ con direcciones de mayor autovalor de $M$ y reducir así la relevancia del conflicto anisotrópico. También señaló la necesidad de concretar la corrección con ground truth y de no interpretar el horizonte aislado como dinámica real.

### Respuesta a la crítica

La afirmación general sobre alineamiento no se acepta tal como fue formulada. En gradient descent lineal, las componentes asociadas a mayor curvatura se contraen más rápidamente; de ello no se sigue un alineamiento general de $e_t$ con los mayores autovalores. A la vez, que $e$ sea autovector de $M$ sólo fija la relación de signo del término de primer orden: no garantiza $\Delta_R>0$ para cualquier $\eta$, porque permanece el término cuadrático negativo.

Esta respuesta preserva el resultado de existencia, pero no demuestra que el conflicto sea dinámicamente relevante. No se introducen para sostenerla supuestos gaussianos, covarianza estacionaria de SGD ni distribution shift.

### Feedback fiable retrasado: decisión metodológica abierta

Antes de resolver las trayectorias contrafactuales debe especificarse $U_Y$. El uso posterior de $(x_t,Y_t)$ no es matemáticamente inválido por sí mismo y no exige necesariamente deshacer la pseudoactualización. Las posibles reglas de corrección requieren definición y análisis; Decision 008 no selecciona ninguna.

### Horizonte aislado y dinámica real

$B_H\Delta_R$ sigue siendo un dispositivo ilustrativo que congela el gap de una pseudoactualización. No representa la dinámica real. Tampoco debe sustituirse automáticamente por una evolución determinista $(I-\eta M)^\tau$. Con SGD por muestras, la evolución puede contener productos aleatorios

$$
\prod_j (I-\eta X_jX_j^T),
$$

además de términos debidos a pseudo-supervisión, feedback fiable retrasado y reglas de actualización intermedias. Una dinámica cerrada requiere hipótesis adicionales; no se adoptan aquí.

### Framing de novedad conservado

La auditoría independiente no identificó un fallo fatal de novedad, pero esto no constituye prueba de novedad. Se conserva literalmente:

> No direct antecedent was identified in the targeted review that jointly models the immediate operational value of routing to an expensive predictor and the future population-risk effect of updating the cheap predictor with that same routed output.

### Problemas abiertos prioritarios

La prioridad es pasar de una teoría de una pseudoactualización a una teoría del valor de la decisión durante el periodo de anticipación $\tau$:

1. especificar $U_Y$;
2. derivar la evolución contrafactual durante $\tau$ con updates intermedios;
3. determinar bajo qué condiciones el conflicto geométrico tiene relevancia probabilística o dinámica.

El tercer punto no es todavía un teorema candidato. Debe relacionar $(X_t,e_t)$ con la dinámica inducida por el aprendizaje sin inferir frecuencia a partir de la construcción geométrica de existencia.
