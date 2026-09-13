# EP001-B2 locked confirmation report

This report evaluates frozen discovery coefficients on confirmation seeds 20--49. Absolute losses precede relative reductions. No coefficient was refitted.

Primary cases: 729600 finite of 729600 candidates; 0 excluded.

## Primary grid results

### gamma = 0.5

Functional absolute LAD losses:

| model | loss | 95% bootstrap interval |
|---|---:|---:|
| M0 | 0.00177065406 | [0.001728192429573256, 0.0018144662347343308] |
| M1F | 0.000529803489 | [0.0005077411551264176, 0.0005517781495093433] |
| M2F | 8.35442552e-06 | [7.83111431217416e-06, 8.900041451663155e-06] |

Functional reductions: `{'R1': 0.7007865615530668, 'R2': 0.9952817290962006, 'G_2_1': 0.9842310862497035, 'difference_1_0': -0.0012408505682829085, 'difference_2_0': -0.0017622996314507623, 'difference_2_1': -0.0005214490631678537}`

Feasible-cost absolute disagreement losses:

| model | loss | 95% bootstrap interval | active loss | active mass | induced loss | induced-positive |
|---|---:|---:|---:|---:|---:|---:|
| M0 | 0.000878088541 | [0.0008567757163744665, 0.0009000292583289467] | 0.00245106091 | 0.358248355 | 0 | 0 |
| M1O | 0.000262376207 | [0.0002513265134986701, 0.0002734049024916547] | 0.000732386356 | 0.358248355 | 0 | 0 |
| M2O | 4.06732013e-06 | [3.8042857226546834e-06, 4.340111263221913e-06] | 1.13533532e-05 | 0.358248355 | 0 | 0 |

Operational reductions: `{'R1': 0.7011961835843197, 'R2': 0.9953679840542257, 'G_2_1': 0.9844981365989968, 'difference_1_0': -0.0006157123340956364, 'difference_2_0': -0.0008740212212983306, 'difference_2_1': -0.00025830888720269413}`

Active-region W+ quantiles (P50/P90/P99):

- M0: [0.0009250865380451279, 0.006413314225319766, 0.020850487513373928]
- M1O: [1.2925152237261428e-05, 0.0020100453345430758, 0.01069648110482646]
- M2O: [0.0, 1.9082975646123046e-05, 0.00019622920227835294]

### gamma = 0.9

Functional absolute LAD losses:

| model | loss | 95% bootstrap interval |
|---|---:|---:|
| M0 | 0.0194068512 | [0.018949751534051075, 0.019879894225744085] |
| M1F | 0.00529539133 | [0.005074898041632414, 0.005514965786388138] |
| M2F | 8.02974739e-05 | [7.538823226558643e-05, 8.537358446097121e-05] |

Functional reductions: `{'R1': 0.7271380461146714, 'R2': 0.9958624161561103, 'G_2_1': 0.9848363475194178, 'difference_1_0': -0.014111459839411712, 'difference_2_0': -0.019326553693973895, 'difference_2_1': -0.005215093854562184}`

Feasible-cost absolute disagreement losses:

| model | loss | 95% bootstrap interval | active loss | active mass | induced loss | induced-positive |
|---|---:|---:|---:|---:|---:|---:|
| M0 | 0.0173514254 | [0.01693925331854492, 0.01777822427516094] | 0.046611536 | 0.372256031 | 0 | 0 |
| M1O | 0.00472820438 | [0.0045294001117633775, 0.004926474130079182] | 0.012701485 | 0.372256031 | 0 | 0 |
| M2O | 7.06466573e-05 | [6.623120812128818e-05, 7.52021634671879e-05] | 0.000189779752 | 0.372256031 | 0 | 0 |

Operational reductions: `{'R1': 0.727503402297179, 'R2': 0.9959284810422115, 'G_2_1': 0.9850584594739462, 'difference_1_0': -0.012623220983778962, 'difference_2_0': -0.01728077870225501, 'difference_2_1': -0.004657557718476052}`

Active-region W+ quantiles (P50/P90/P99):

- M0: [0.016903635601894784, 0.12347589847483853, 0.40049154409222076]
- M1O: [0.00023481819575343899, 0.03455163345317014, 0.18814575008056122]
- M2O: [1.3877787807814457e-17, 0.000319855535282354, 0.0033238506101254117]

### gamma = 1.0

Functional absolute LAD losses:

| model | loss | 95% bootstrap interval |
|---|---:|---:|
| M0 | 0.0361322782 | [0.0352849116987935, 0.037009118342837266] |
| M1F | 0.00967195986 | [0.00926917584138549, 0.01007298631490782] |
| M2F | 0.000145463958 | [0.00013664818437780196, 0.00015456913322316494] |

Functional reductions: `{'R1': 0.732318017217621, 'R2': 0.9959741271355143, 'G_2_1': 0.984960239674559, 'difference_1_0': -0.02646031831056299, 'difference_2_0': -0.035986814216615606, 'difference_2_1': -0.009526495906052618}`

Feasible-cost absolute disagreement losses:

| model | loss | 95% bootstrap interval | active loss | active mass | induced loss | induced-positive |
|---|---:|---:|---:|---:|---:|---:|
| M0 | 0.0359221654 | [0.03507361855984749, 0.036799223987701024] | 0.0942603655 | 0.381095121 | 0 | 0 |
| M1O | 0.00960281015 | [0.009199450807446588, 0.010005064219727479] | 0.0251979352 | 0.381095121 | 0 | 0 |
| M2O | 0.000142483331 | [0.00013365017743876225, 0.0001515791121808159] | 0.000373878654 | 0.381095121 | 0 | 0 |

Operational reductions: `{'R1': 0.7326773023629256, 'R2': 0.9960335539557933, 'G_2_1': 0.9851623297263308, 'difference_1_0': -0.026319355217347733, 'difference_2_0': -0.03577968203793824, 'difference_2_1': -0.009460326820590509}`

Active-region W+ quantiles (P50/P90/P99):

- M0: [0.03317296080474741, 0.25143615519057194, 0.8191152852203185]
- M1O: [0.0004639516875872829, 0.06819681174804648, 0.3765465256288896]
- M2O: [2.7755575615628914e-17, 0.0006296790343737202, 0.006542132370424003]

## Pre-exposed block

Configs 76--79 are reported separately as PRE-EXPOSED / NON-HOLDOUT. Only M0 and frozen primary-global M1 coefficients are evaluated. M2 is omitted because no exposed M2 coefficient was frozen and refitting is forbidden.

## Interpretation boundary

Use the preregistered A/B/C/D logic with absolute scale, bootstrap uncertainty, active/induced diagnostics, and configuration/trajectory heterogeneity. These synthetic fixed-grid results do not establish applied routing usefulness or performance under divergent policies.
