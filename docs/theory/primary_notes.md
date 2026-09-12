# Primary technical notes

Cuaderno de razonamiento y derivaciones de **Adaptive Cost-Aware Routing with Learning Value**. Decision 007 fija el protocolo base y el modelo lineal mínimo. El protocolo estabilizado se documenta en `paper/primary/sections/problem_formulation.tex`; los resultados algebraicos, con pruebas y carácter preliminar para revisión científica, en `theoretical_analysis.tex`. Una identidad algebraica demostrada bajo condiciones explícitas no establece novedad ni optimalidad de una política secuencial.

Decision 009 extiende temporalmente la teoría de una pseudoactualización mediante transporte bajo aprendizaje posterior común. Las secciones de Decisions 007–008 conservan sus pruebas y contexto; los problemas entonces abiertos se actualizan al final de este cuaderno. En particular, se adopta SGD ordinario como regla fiable mínima admisible y se resuelve un componente de adaptación bajo hipótesis explícitas, no la continuación secuencial completa.

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
\gamma\Delta_{\mathrm{adapt}}^{(H)}=B_H\Delta_R,
$$

$$
\text{consult D iff}\quad\Delta_{\mathrm{now}}+B_H\Delta_R>C_D.
$$

Se unifica aquí la notación con Decision 009: Delta_adapt descuenta desde la primera respuesta futura; su contribución desde la ronda actual lleva gamma. La versión anterior de este párrafo llamaba Delta_adapt al valor ya descontado desde la ronda actual, mientras que la sección siguiente usaba el origen futuro. Se corrige esa colisión notacional sin modificar B_H ni el comparador aislado.

Es un criterio future-aware idealizado, no la solución del objetivo completo. Se contemplan separadamente:

1. **Under-querying:** Delta_now<C_D pero Delta_now+B_H Delta_R>C_D.
2. **Over-querying:** Delta_now>C_D pero Delta_now+B_H Delta_R<C_D.

Under-querying ya es posible en 1D. Por ejemplo algebraico, x=1, M=1, e=1, b=0, sigma_D^2=1/4 y eta=1/2 dan Delta_now=3/4 y Delta_R=11/16. Para H=1, gamma=1 y C_D=1, el comparador miope no consulta pero 3/4+11/16=23/16>1. El signo positivo de ambos valores no evita la diferencia de decisión frente al coste.

Para over-querying, una configuración de conflicto anisotrópico da Delta_now>0 y Delta_R<0. Si B_H>0, el intervalo

$$
\max\{0,\Delta_{\mathrm{now}}+B_H\Delta_R\}<C_D<\Delta_{\mathrm{now}}
$$

no es vacío y produce la decisión opuesta entre comparadores. Es un corolario de existencia bajo aislamiento y elección del coste en ese intervalo; no demuestra over-querying para todos los costes ni una política secuencial óptima. Ambos mecanismos no se presentan como un único teorema general. Si gamma=0, B_H=0 y estos fallos por valor futuro no aparecen en el objetivo actual.

## Problema planteado en Decision 007: eliminar el aislamiento durante tau pasos

Partiendo del mismo estado previo, comparar las ramas contrafactuales iniciadas por F y D, incluyendo updates intermedios y feedback retrasado de muestras anteriores. Definir e_{t+k}^F y e_{t+k}^D como los errores del predictor barato antes de cada respuesta futura en esas ramas. El siguiente objeto a calcular es

$$
\Delta_{\mathrm{adapt}}^{(\tau)}=
\sum_{k=1}^{\tau}\gamma^{k-1}\mathbb E\left[
(e_{t+k}^F)^T M e_{t+k}^F-(e_{t+k}^D)^T M e_{t+k}^D
\right].
$$

La esperanza se refiere al estado inicial común y a las evoluciones contrafactuales bajo políticas de continuación y reglas de actualización que deberán especificarse. En Decision 007 este problema no estaba resuelto. Decision 009 calcula más abajo la especialización con aprendizaje posterior común e i.i.d.; el problema completo sigue abierto.

**Convención de descuento:** esta última expresión toma la primera respuesta futura como origen. El B_H anterior descuenta desde la ronda actual; por eso, bajo aislamiento con H=tau,

$$
\gamma\Delta_{\mathrm{adapt}}^{(\tau)}=B_H\Delta_R.
$$

Si se usa en su lugar un peso con origen futuro, sum_{k=1}^H gamma^{k-1}, hay que multiplicarlo por gamma al compararlo con la pérdida inmediata del objetivo J. No se omite ni se duplica ese factor. Con gamma=1 ambas convenciones coinciden.

La suma propuesta mide riesgo poblacional del predictor barato. Identificarla con el valor de continuación total requiere además contabilizar la elección de respuestas operacionales futuras y sus costes. La llegada exógena de Y_t no implica que las ramas se igualen ni que el efecto causal termine allí. En ese checkpoint quedaban abiertos la regla de corrección fiable, las políticas de continuación, los efectos después de tau y la computabilidad de estos valores. Decision 009 concreta una regla fiable mínima sin resolver la política completa. No se afirman regret bounds ni tasas asintóticas de regret.

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

## Decision 009 — Transported adaptation value under subsequent learning

### Pregunta, alcance y notación

**Interpretación científica.** How does the future learning dynamics transform the benefit or harm caused by querying an expensive predictor now? El esquema conceptual es valor operacional actual + valor de adaptación transportado − coste de consulta. La especialización lineal-cuadrática hace analizable exactamente una parte de esta pregunta. No se presenta como nueva teoría de SGD ni como contribución novedosa definitiva del paper.

Se conserva íntegro el teorema anisotrópico anterior. El desarrollo siguiente extiende temporalmente Delta_R: no sustituye su prueba ni modifica las condiciones de compatibilidad isotrópica de una pseudoactualización. Ahora eta_D>0 designa el paso de esa pseudoactualización (el eta de las secciones anteriores); eta designa el paso constante del SGD posterior y eta_Y el de la actualización fiable específica. Se reserva k para el número de updates posteriores; no es automáticamente un número de rondas ni el retardo tau.

### Hipótesis suficientes para la esperanza cerrada

Se fija toda la información actual, en particular e_t=e, x_t=x y b. En lo que sigue E[·|e,x] abrevia ese condicionamiento completo; E[·|x] en los momentos iniciales mantiene también e y el estado fijos.

1. El ruido de la consulta actual satisface E[nu_t|e,x]=0 y E[nu_t²|e,x]=sigma_D², entendidos bajo la información actual. Para Delta_now se conservan las condiciones sobre epsilon_t de la teoría previa.
2. Tras la decisión inicial, ambas ramas reciben exactamente los mismos inputs, targets y reglas de actualización. Son targets comunes dados por (w*)^T X_j+epsilon_j, sin dependencia de la rama.
3. Condicionalmente en la información actual, los **pares** (X_j,epsilon_j), j>=1, son i.i.d., con X_j de ley P_X y E[epsilon_j|X_j]=0, e independientes del ruido inicial nu_t. No se exige independencia de epsilon_j respecto de su propio X_j.
4. Se supone E||X||⁴<infinito y E[||X||² epsilon²]<infinito, además de los momentos del teacher y los segundos momentos de la comparación de pérdidas. Son condiciones suficientes para riesgos y esperanzas finitos a todo horizonte finito. No se afirma estabilidad ni se toma límite de horizonte infinito.

**Precisión necesaria:** si «muestras futuras i.i.d.» sólo significara que los X_j son i.i.d., E[epsilon_j|X_j]=0 no excluiría dependencia de epsilon_j con otros X_i. Para anular el término cruzado necesitamos E[epsilon_j|X_1,...,X_k]=0 para cada j<=k; los pares i.i.d. son una condición suficiente transparente. No se añade gaussianidad. La independencia del ruido inicial se exige condicionada en la información actual, no se infiere de momentos marginales.

### Resultado exacto por realización: perturbación y dos trayectorias

Inmediatamente después de la decisión inicial, escribir e_t^F=e y e_t^D=e+h_0, con

$$
d=\alpha-\beta,\qquad h_0=-\eta_D d x+\eta_D x\nu_t.
$$

La misma nu_t aparece en la respuesta operacional de D y en su pseudo-supervisión. h_0 es la perturbación paramétrica causal de esa consulta. Sus momentos son

$$
\mathbb E[h_0\mid e,x]=-\eta_D d x,\qquad
\mathbb E[h_0h_0^T\mid e,x]=\eta_D^2(d^2+\sigma_D^2)xx^T.
$$

Para no mezclar índices, reiniciar el reloj de updates con e_0^F=e, e_0^D=e+h_0. Para una rama u en {F,D},

$$
e_j^u=A_j e_{j-1}^u+\xi_j,\qquad
A_j=I-\eta X_jX_j^T,\qquad \xi_j=\eta X_j\epsilon_j,
\quad j\geq1.
$$

Es la recurrencia e_{j+1}=A_j e_j+xi_j tras un mero cambio de índice, escogido para que P_k=A_k...A_1 contenga exactamente k updates. Al restar,

$$
h_j=e_j^D-e_j^F=A_jh_{j-1},\qquad
h_k=P_kh_0,\qquad P_k=A_k\cdots A_1,\quad P_0=I.
$$

La cancelación del target común es exacta por realización. No afirma que el target sea irrelevante para cada trayectoria: xi_j entra en ambas y modifica sus riesgos. Tampoco basta aplicar «la misma política» de routing para obtener este acoplamiento, pues una política dependiente de parámetros puede elegir acciones distintas en cada rama. Si eso ocurre, hace falta la diferencia completa de continuation/Q values.

Por e_k^D=e_k^F+h_k y la simetría de M,

$$
R(e_k^F)-R(e_k^D)
=-2h_k^TMe_k^F-h_k^TMh_k
=-2h_0^TP_k^TMe_k^F-h_0^TP_k^TMP_kh_0.
$$

Esta identidad no necesita centrar los targets. Cerrar su esperanza sí requiere controlar el término con e_k^F; la cancelación en la diferencia de parámetros no elimina automáticamente ese término cruzado de riesgo.

### Resultado probado: operador de transporte de matrices de riesgo

Definir

$$
K_k=\mathbb E[P_k^TMP_k],\quad K_0=M,\qquad
\mathcal T(Q)=\mathbb E[(I-\eta XX^T)^TQ(I-\eta XX^T)].
$$

La esperanza usa la secuencia futura bajo el estado condicionado. Es importante mantener el orden de productos: las matrices A_j no tienen por qué conmutar. Para P_{k+1}=(A_{k+1}...A_2)A_1, el bloque A_{k+1}...A_2 es independiente de A_1 y tiene la misma ley que P_k. Por tanto,

$$
K_{k+1}
=\mathbb E\!\left[A_1^T\,
\mathbb E[(A_{k+1}\cdots A_2)^TM(A_{k+1}\cdots A_2)\mid A_1]
\,A_1\right]
=\mathbb E[A_1^TK_kA_1]
=\mathcal T(K_k).
$$

Así K_k=T^k(M), por inducción desde K_0=M. La expansión da

$$
\mathcal T(Q)
=Q-\eta(MQ+QM)+\eta^2\mathbb E[XX^TQXX^T].
$$

T actúa sobre matrices de riesgo, es lineal y preserva semidefinitud positiva: v^T T(Q)v=E[(Av)^TQ(Av)]>=0 si Q es semidefinida positiva. En particular K_k es semidefinida positiva, aunque M sea definida positiva no debemos presuponer que todos los K_k sean definidos positivos. Aparecen cuartos momentos; M por sí solo no determina el transporte. No se sustituye el producto aleatorio por (I−eta M)^k ni K_k por su análogo determinista. No se reivindica novedad de este operador dentro de SGD.

### Teorema probado: valor de adaptación transportado

Para todo k finito, bajo las hipótesis suficientes anteriores,

$$
\boxed{
\Delta_k:=\mathbb E[R(e_k^F)-R(e_k^D)\mid e_t=e,x_t=x]
=2\eta_D d x^TK_ke
-\eta_D^2(d^2+\sigma_D^2)x^TK_kx.
}
$$

**Derivación del término cruzado.** Desarrollar la rama sin consulta inicial:

$$
e_k^F=P_ke+q_k,\qquad
q_k=\sum_{i=1}^k A_k\cdots A_{i+1}\xi_i
=\eta\sum_{i=1}^k A_k\cdots A_{i+1}X_i\epsilon_i.
$$

Los productos vacíos valen I y q_0=0. Sea la sigma-álgebra de inputs futuros F_k^X=sigma(X_1,...,X_k). Cada matriz que multiplica epsilon_i es medible respecto de ella. Por independencia de los pares y centrado,

$$
\mathbb E[\epsilon_i\mid\mathcal F_k^X]=0,
\qquad \mathbb E[q_k\mid\mathcal F_k^X]=0,
\qquad \mathbb E[P_k^TMq_k]=0.
$$

No hemos supuesto independencia entre P_k y q_k, que comparten inputs. La independencia de h_0 respecto de todos los pares futuros permite escribir

$$
\begin{aligned}
\mathbb E[h_0^TP_k^TMe_k^F]
&=\mathbb E[h_0]^T\mathbb E[P_k^TMP_k]e
  +\mathbb E[h_0]^T\mathbb E[P_k^TMq_k]\\
&=-\eta_D d x^TK_ke.
\end{aligned}
$$

Para el término cuadrático, usar independencia y la identidad de traza:

$$
\mathbb E[h_0^TP_k^TMP_kh_0]
=\operatorname{tr}(K_k\mathbb E[h_0h_0^T])
=\eta_D^2(d^2+\sigma_D^2)x^TK_kx.
$$

Sustituir ambos términos en la identidad por realización prueba el teorema. Para k=0 se obtiene exactamente Delta_0=Delta_R con paso eta_D.

**Límite de la simplificación.** Si h_0 sigue siendo independiente del futuro pero el centrado condicional falla, debe retenerse −2 E[h_0]^T E[P_k^T M q_k], que con los momentos iniciales vale +2 eta_D d x^T E[P_k^T M q_k]. Si también falla esa independencia, ni siquiera esas factorizaciones están justificadas. La identidad por realización sigue siendo el punto de partida. Targets posteriores sesgados, selección adaptativa de updates o feedback pendiente no satisfacen automáticamente las hipótesis base.

### Resultados probados: signo y persistencia bajo reescalado

Si x^T K_k x>0, definir únicamente para el criterio de signo

$$
s_k(x,e)=\frac{d x^TK_ke}{x^TK_kx}.
$$

Factorizando el teorema,

$$
\Delta_k=\eta_D(x^TK_kx)
\left[2s_k(x,e)-\eta_D(d^2+\sigma_D^2)\right].
$$

Como eta_D>0,

$$
\Delta_k>0\quad\Longleftrightarrow\quad
s_k(x,e)>\frac{\eta_D}{2}(d^2+\sigma_D^2).
$$

El lado derecho refleja tamaño y ruido de la pseudoactualización; K_k fija la geometría efectiva tras k updates posteriores. No se interpreta s_k como política, probabilidad ni valor de continuación. Si x^T K_k x=0, semidefinitud implica K_k x=0 y Delta_k=0; no se divide por cero.

**Proposición de persistencia.** Si para un k dado K_k=c_k M con c_k>0, entonces Delta_k=c_k Delta_0 y sign(Delta_k)=sign(Delta_0). Prueba: sustituir en los dos términos del teorema y factorizar c_k. Si el transporte sólo reescala positivamente la geometría, cambia la magnitud pero no el signo. No se afirma el recíproco. c_k=0 daría Delta_k=0, por lo que la positividad estricta es necesaria para esta conclusión de igualdad de signos en general.

### Valor acumulado probado y convención temporal

Para H>=1 etapas de evaluación, con 0<=gamma<=1 y origen de descuento en la primera etapa,

$$
\overline K_H=\sum_{k=0}^{H-1}\gamma^kK_k,\qquad
\Delta_{\mathrm{adapt}}^{(H)}=\sum_{k=0}^{H-1}\gamma^k\Delta_k
=2\eta_D d x^T\overline K_He
-\eta_D^2(d^2+\sigma_D^2)x^T\overline K_Hx.
$$

La prueba es sumar el teorema, sin intercambios con límites infinitos. Se toma el peso de k=0 igual a 1, también cuando gamma=0. k=0 evalúa las ramas inmediatamente después de la pseudoactualización, antes de nuevos updates: mide riesgo poblacional de los parámetros destinados al futuro, no la respuesta operacional ya emitida en t. Por eso no duplica Delta_now.

Hay dos relojes que deben mantenerse separados:

- En el reloj de updates, e_k^u corresponde a k actualizaciones posteriores.
- En el reloj operacional, e_{t+r}^u es el estado antes de responder en t+r. Sólo si no hay actualización común antes de t+1 y hay exactamente una entre cada par de respuestas siguientes se cumple e_{t+r}^u=e_{r-1}^u. En esa especialización H=tau cuenta t+1,...,t+tau y el último K es K_{tau-1}, no K_tau.

Ese calendario es una especialización, no una consecuencia del protocolo: feedback de muestras anteriores puede llegar incluso después de la respuesta en t y antes de t+1. Si n_r es un número determinista de updates antes de la respuesta t+r, con la misma secuencia que satisface el teorema, la suma correspondiente usa sum_{r=1}^tau gamma^{r-1} K_{n_r}. Si n_r depende de los datos/decisiones, no se inserta automáticamente un índice aleatorio en la fórmula incondicional; hay que evaluar las esperanzas con ese calendario y selección. La identidad de productos por realización sigue siendo válida bajo targets y reglas comunes.

Para etapas que coinciden con respuestas futuras bajo el calendario indicado, el peso desde t es gamma Delta_adapt^(H). Si K_k=M en todas las etapas,

$$
\overline K_H=\left(\sum_{k=0}^{H-1}\gamma^k\right)M,\qquad
\gamma\Delta_{\mathrm{adapt}}^{(H)}
=\left(\sum_{r=1}^H\gamma^r\right)\Delta_R=B_H\Delta_R.
$$

Se recupera el antiguo comparador sin cambiarlo. B_H Delta_R era un analytical device sin transporte/deformación efectiva, no la dinámica general. La ausencia de updates es una condición suficiente para ese caso. Gamma=0 anula la contribución futura al objetivo actual aunque Delta_adapt, con origen futuro, conserve su primera etapa.

### Contraejemplo recalculado: inversión dinámica con segundo momento isotrópico

**Ejemplo, no teorema general.** En R² sea X=(G,R)^T, con G normal estándar y R Rademacher simétrico, independientes. La normalidad se usa exclusivamente para esta construcción concreta. No es una distribución rotacionalmente invariante. E[G]=E[R]=0, E[G²]=E[R²]=1, por lo que M=I. Los momentos E[G⁴]=3, R⁴=1 y E[G²R²]=1 dan

$$
\mathbb E[\|X\|^2XX^T]
=\begin{pmatrix}
\mathbb E[G^4+G^2R^2]&\mathbb E[G^3R+GR^3]\\
\mathbb E[G^3R+GR^3]&\mathbb E[G^2R^2+R^4]
\end{pmatrix}
=\operatorname{diag}(4,2).
$$

Los términos cruzados son cero por independencia y simetría. Con eta=0.4,

$$
K_1=I-2(0.4)I+(0.4)^2\operatorname{diag}(4,2)
=\operatorname{diag}(0.84,0.52).
$$

Fijar x=(1,1)^T, e=(-0.2012,0.2564)^T, b=0, sigma_D²=0.001 y eta_D=0.2. Para completar una ley admisible, puede elegirse nu_t simétrico ±sqrt(0.001), independiente de inputs futuros, y epsilon_t=epsilon_j=0. Esto cumple las hipótesis sin requerir ruido general gaussiano. El teorema permite otros ruidos futuros centrados que cumplan sus condiciones.

Los valores siguientes se recalcularon con aritmética racional exacta a partir de los decimales suministrados; sus expansiones decimales mostradas son exactas:

| Cantidad | Cálculo / valor |
| --- | --- |
| alpha=d | −0.2012+0.2564 = 0.0552 |
| alpha² | 0.00304704 |
| Delta_now | 0.00304704−0.001 = 0.00204704 |
| x^T M x | 2 |
| eta_D ‖x‖² | 0.4 < 1 |
| Delta_0 | 2(0.2)(0.0552)²−(0.2)²(0.00304704+0.001)2 = 0.0008950528 |
| x^T K_1 e | 0.84(−0.2012)+0.52(0.2564) = −0.03568 |
| x^T K_1 x | 0.84+0.52 = 1.36 |
| Término lineal de Delta_1 | 2(0.2)(0.0552)(−0.03568) = −0.0007878144 |
| Penalización cuadrática de Delta_1 | (0.2)²(0.00304704+0.001)(1.36) = 0.000220158976 |
| Delta_1 | −0.0007878144−0.000220158976 = −0.001007973376 |

Comprobación reproducible sin dependencias externas (Python estándar; cálculo algebraico, no simulación ni experimento):

```python
from fractions import Fraction as F

eta, eta_D, variance = F('0.4'), F('0.2'), F('0.001')
e = [F('-0.2012'), F('0.2564')]
K1 = [1 - 2*eta + 4*eta**2, 1 - 2*eta + 2*eta**2]
alpha = sum(e)
xK1e = sum(q*v for q, v in zip(K1, e))
now = alpha**2 - variance
delta0 = 2*eta_D*alpha**2 - eta_D**2*(alpha**2 + variance)*2
delta1 = 2*eta_D*alpha*xK1e - eta_D**2*(alpha**2 + variance)*sum(K1)
assert K1 == [F('0.84'), F('0.52')]
assert now == F('0.00204704')
assert delta0 == F('0.0008950528')
assert xK1e == F('-0.03568')
assert delta1 == F('-0.001007973376')
assert now > 0 and delta0 > 0 and delta1 < 0 and eta_D*2 < 1
```

**Interpretación acotada.** D mejora la expected current task loss antes del consultation cost. La pseudoactualización reduce inicialmente el population risk. Después de una actualización posterior común, el efecto transportado de aquella misma pseudoactualización sobre el population risk tiene signo negativo. No cambia retrospectivamente la actualización inicial; cambia el signo de su efecto contrafactual después del aprendizaje posterior. Tampoco se deduce de Delta_1<0 un signo para toda suma acumulada ni una decisión óptima de routing.

M=I garantiza la compatibilidad single-update ya demostrada, que efectivamente se observa aquí. No garantiza K_1=cI: el cuarto momento relevante es anisotrópico. La isotropía poblacional a segundo orden no basta para preservar la geometría durante el aprendizaje posterior. No se generaliza esta construcción a toda distribución con M=I.

### Resultado del ejemplo: probabilidad positiva sobre inputs condicionada en e

Con este e fijo, b, pasos y varianza fijos, Delta_now(x), Delta_0(x) y Delta_1(x) son funciones continuas (polinomios) de x. K_1 es fijo porque el futuro i.i.d. mantiene la misma ley al condicionar en x. Las tres desigualdades son estrictas en (1,1), así que hay un entorno abierto U de (1,1) en el que conservan sus signos. También se mantiene eta_D||x||²<1 reduciendo U si hace falta.

Existe delta>0 tal que {(g,1): |g−1|<delta} está contenido en U. Por independencia y densidad normal positiva,

$$
P_X(U)\geq\tfrac12\,P(|G-1|<\delta)
=\tfrac12\int_{1-\delta}^{1+\delta}
\frac{1}{\sqrt{2\pi}}e^{-g^2/2}\,dg>0.
$$

No se atribuye masa al punto x=(1,1), que tiene probabilidad cero, ni se supone una densidad bidimensional de X: la masa positiva procede del intervalo en la rama R=+1. Es probabilidad positiva **sobre inputs, condicionada en el estado fijo e elegido** (en el modelo con entrada actual de ley P_X). No demuestra que ese estado aparezca con probabilidad positiva bajo una trayectoria natural de SGD, que el fenómeno sea frecuente, que ocurra en estado estacionario, que tenga probabilidad positiva para todo e, ni que ocurra para toda distribución con M=I. Responde parcialmente a la limitación de Decision 008, sin resolver la distribución conjunta de estados e inputs inducida por aprendizaje.

### U_Y mínimo y feedback retrasado: identidad exacta y límites

Se adopta como opción base admisible SGD ordinario al llegar Y_t:

$$
\theta^+=\theta+\eta_Yx_t(Y_t-\theta^Tx_t).
$$

Sean theta^D y theta^F los parámetros justo antes de esa actualización común, con h=theta^D−theta^F que ya incluye el transporte histórico. Restando,

$$
h^+=h+\eta_Yx_t[(Y_t-(\theta^D)^Tx_t)-(Y_t-(\theta^F)^Tx_t)]
=(I-\eta_Yx_tx_t^T)h.
$$

No se introduce una regla que deba deshacer la pseudoactualización. Para x_t no nulo, escribir h=h_parallel+h_perp con componentes paralela y ortogonal a x_t da h^+=(1−eta_Y||x_t||²)h_parallel+h_perp. Por tanto recibir Y_t no borra necesariamente la diferencia: la transforma. Contrae la componente paralela si 0<eta_Y||x_t||²<2; anula esa componente si eta_Y||x_t||²=1, pero conserva la ortogonal. Sin restricciones de paso no debe afirmarse contracción universal. Para x_t=0 no hay cambio. Otras reglas U_Y son posibles, pero no necesarias para este modelo mínimo.

Y_t se revela después de emitir la respuesta operacional en t+tau. Su uso puede modificar por primera vez la respuesta de t+tau+1. No se inserta esa actualización antes de la última de las tau respuestas anticipadas. La identidad anterior es por realización y no exige la independencia de nu_t respecto de epsilon_t. El teorema i.i.d. de transporte no cubre automáticamente esa reutilización de x_t ni los datos ya pendientes al condicionar en el estado actual; deben revisarse sus hipótesis antes de cerrar esperanzas. Esto no invalida SGD ordinario con feedback retrasado, sólo delimita el resultado cerrado base.

### Siguiente problema abierto, sin resolver

Analizar condiciones estructurales de persistencia e inversión. La siguiente comprobación formal es si una ley rotacionalmente invariante con M=cI implica T(c'I)=c''I y, por inducción, K_k=c_k I, bajo los momentos necesarios. Aquí no se demuestra ni se afirma esa implicación como resultado. Si se confirma, habrá que estudiar las condiciones de positividad de los factores que permitan aplicar la proposición de persistencia; factor cero no preserva un signo no nulo.

Después, y sólo si resulta necesario, conectar la relevancia del conflicto con los estados e_t inducidos por trayectorias naturales. No se introduce covarianza estacionaria de SGD, gaussianidad de e_t, distribution shift ni experimentos. El full continuation/Q value y la optimalidad secuencial siguen abiertos, incluso cuando un componente de adaptación bajo common coupling sea exactamente calculable.
