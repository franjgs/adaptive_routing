# Applied audit after EP001-B2: cloud–edge forecasting as candidate domain

**Date:** 2026-09-13
**Status:** working research note

## Core conclusion

Cloud–edge traffic forecasting is currently the strongest application candidate because delayed reliable ground truth arrives naturally and independently of the query decision. CE-CoLSM (ICC 2026) is the anchor prior art and a serious novelty threat: it already combines selective cloud inference with later distillation of the edge model. Therefore novelty cannot be claimed for cloud querying, hard-sample routing, or cloud-to-edge retraining itself.

The candidate gap that remains is narrower: whether the query decision should explicitly price the future learning consequence of the queried supervision, rather than rely only on current confidence/difficulty.

## Anchor prior art: CE-CoLSM (ICC 2026)

H. Zhou, X. Li, J. Li, Y. Xiao, Y. Li, “CE-CoLSM: Cloud-Edge Large and Small Models Collaborative Framework for Traffic Prediction,” IEEE ICC 2026. DOI: 10.1109/ICC59461.2026.11587333.

Verified:
- network traffic prediction;
- lightweight model at the edge;
- cloud large model queried on demand;
- query triggered by a real-time confidence score for abnormal samples;
- cloud model provides immediate prediction assistance;
- accumulated abnormal samples trigger cross-architecture knowledge distillation to adapt the edge model;
- authors report 41.09% fewer cloud large-model requests.

Not yet established from the public material inspected:
- whether the query score explicitly values future edge-model improvement caused by the query;
- whether every queried output is exactly the supervision later used for distillation;
- full details of the confidence score, models, datasets, code availability and distillation cadence.

## Earlier close prior art: SCECS 2025

X. Jin et al., “Efficient and Accurate Inference in Edge-Cloud Framework via Large and Small Model Collaboration,” SCECS 2025. DOI: 10.1109/SCECS65243.2025.11065186.

Verified:
- local lightweight model detects hard samples;
- hard samples are uploaded to the cloud;
- local model is subsequently retrained;
- experiments use roughly 10% hard examples.

This means the pattern hard sample → cloud processing → local retraining is already prior art.

## Video comparator: Shoggoth (DAC 2023)

L. Wang et al., “Shoggoth: Towards Efficient Edge-Cloud Collaborative Real-Time Video Inference via Adaptive Online Learning,” DAC 2023 / arXiv:2306.15333.

Verified:
- real-time inference runs at the edge;
- selected frames are sent to a cloud teacher for online labeling;
- returned pseudo-labels train the edge student;
- adaptive sampling controls bandwidth and adaptation frequency.

Important distinction:
the cloud teacher is used for labeling/adaptation; the paper states that real-time inference runs at the edge. Thus it does not clearly implement the exact mechanism “same cloud answer replaces the current operational output and also trains F.”

## L2D-SLDS comparator (2026)

Y. Montreuil et al., “Learning to Defer in Non-Stationary Time Series via Switching State-Space Models,” arXiv:2601.22538.

Verified:
- routing among experts under non-stationarity;
- partial feedback;
- switching state-space model of expert residuals;
- IDS-inspired trade-off between predicted cost and information gain about latent regime/shared factor.

Not supported by the inspected source:
the claim that the queried expert output updates a cheap internal predictor F and that the router explicitly values the resulting future improvement of that predictor.

## Why forecasting currently wins

Forecasting naturally provides delayed independent ground truth. A prediction for Y_(t+h) can be made by F or D now; the true Y_(t+h) later occurs and is observed whether or not D was queried.

Consequences:
- delayed Y is not artificially engineered;
- D can be imperfect;
- later Y can evaluate/correct both F and D;
- routing cannot censor ground-truth arrival;
- the problem remains sequential, so present learning can affect future cloud demand.

## Claims that are no longer available

Do not claim novelty for:
- cloud–edge large/small model prediction;
- querying the cloud for difficult samples;
- using cloud outputs for edge retraining/distillation;
- reducing cloud calls through adaptation;
- combining immediate cloud assistance with edge adaptation.

## Candidate gap that survives

Provisional formulation:

“When a cloud query can both improve the current forecast and provide supervision that changes the future edge predictor, existing confidence/hard-sample routing rules do not appear to explicitly price the future learning consequence of the query itself.”

The contribution would therefore have to be the query valuation rule, not the architecture.

## Consequence for theory

Do not force “one query = one immediate SGD update.” A natural forecasting system may accumulate queried samples and adapt F in micro-batches. The application should decide how much of the existing theory survives.

EP001-B2 currently supports only configuration-specific scalar compressibility in the synthetic model. It does not yet establish persistence, macroscopic predictability, or deployable online estimation.

Use a neutral name for c:
- regime-dependent transport factor;
- transport compression factor.

## Required next experiment

Build a closed-loop forecasting experiment where routing decisions determine which D outputs are observed and therefore how F evolves.

Minimum baselines:
- edge-only;
- cloud-only;
- random/periodic queries;
- confidence/hard-sample myopic routing;
- CE-CoLSM-like confidence + distillation;
- oracle future-value policy as upper bound;
- proposed cheap future-learning-value approximation.

Primary evaluation:
accuracy–cloud-cost Pareto frontier under closed-loop trajectories.

Falsification:
if explicit future-learning valuation cannot improve this Pareto frontier over a strong confidence+distillation baseline, the applied contribution should be abandoned or substantially reframed.

## Current verdict

GO, but only through an applied novelty gate.

The surviving question is:

“Should the cloud-query decision explicitly value how the queried supervision changes future edge autonomy, and can that value be approximated cheaply enough to improve the closed-loop accuracy–cost trade-off?”

No current evidence justifies EP001-C centered on exact state-dependent K_k.
