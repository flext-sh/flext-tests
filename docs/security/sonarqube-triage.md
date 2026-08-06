# Triagem SonarCloud — flext-sh/flext-tests

Gerado do dump da plataforma SonarCloud (2026-08-06).

Bead de rastreio: `mro-2wjm.23`

## Resumo

**106 issues** — BLOCKER 15, CRITICAL 18, MAJOR 44, MINOR 29
Tipos: VULNERABILITY 48, BUG 0, CODE_SMELL 58

| regra | issues |
|---|---|
| `docker:S6506` | 20 |
| `docker:S8482` | 15 |
| `python:S3776` | 11 |
| `python:S7498` | 10 |
| `python:S3358` | 9 |
| `python:S108` | 9 |
| `docker:S6470` | 5 |
| `docker:S6471` | 5 |

## Issues

Coluna **Decisão**: `corrigir` / `falso-positivo` / `risco-aceito`.

| # | sev | tipo | regra | componente | linha | Decisão |
|---|---|---|---|---|---|---|
| 1 | BLOCKER | VULNERABILITY | `docker:S8482` | `tests/fixtures/ci/docker/alpine.Dockerfile` | 20 | |
| 2 | BLOCKER | VULNERABILITY | `docker:S8482` | `tests/fixtures/ci/docker/alpine.Dockerfile` | 23 | |
| 3 | BLOCKER | VULNERABILITY | `docker:S8482` | `tests/fixtures/ci/docker/alpine.Dockerfile` | 25 | |
| 4 | BLOCKER | VULNERABILITY | `docker:S8482` | `tests/fixtures/ci/docker/arch.Dockerfile` | 22 | |
| 5 | BLOCKER | VULNERABILITY | `docker:S8482` | `tests/fixtures/ci/docker/arch.Dockerfile` | 25 | |
| 6 | BLOCKER | VULNERABILITY | `docker:S8482` | `tests/fixtures/ci/docker/arch.Dockerfile` | 27 | |
| 7 | BLOCKER | VULNERABILITY | `docker:S8482` | `tests/fixtures/ci/docker/debian.Dockerfile` | 23 | |
| 8 | BLOCKER | VULNERABILITY | `docker:S8482` | `tests/fixtures/ci/docker/debian.Dockerfile` | 26 | |
| 9 | BLOCKER | VULNERABILITY | `docker:S8482` | `tests/fixtures/ci/docker/debian.Dockerfile` | 28 | |
| 10 | BLOCKER | VULNERABILITY | `docker:S8482` | `tests/fixtures/ci/docker/fedora.Dockerfile` | 22 | |
| 11 | BLOCKER | VULNERABILITY | `docker:S8482` | `tests/fixtures/ci/docker/fedora.Dockerfile` | 25 | |
| 12 | BLOCKER | VULNERABILITY | `docker:S8482` | `tests/fixtures/ci/docker/fedora.Dockerfile` | 27 | |
| 13 | BLOCKER | VULNERABILITY | `docker:S8482` | `tests/fixtures/ci/docker/ubuntu.Dockerfile` | 23 | |
| 14 | BLOCKER | VULNERABILITY | `docker:S8482` | `tests/fixtures/ci/docker/ubuntu.Dockerfile` | 26 | |
| 15 | BLOCKER | VULNERABILITY | `docker:S8482` | `tests/fixtures/ci/docker/ubuntu.Dockerfile` | 28 | |
| 16 | CRITICAL | CODE_SMELL | `python:S3776` | `src/flext_tests/_utilities/_files/_batch.py` | 16 | |
| 17 | CRITICAL | CODE_SMELL | `python:S3776` | `src/flext_tests/_utilities/_files/_info.py` | 109 | |
| 18 | CRITICAL | CODE_SMELL | `python:S3776` | `src/flext_tests/_utilities/_files/_reading.py` | 63 | |
| 19 | CRITICAL | CODE_SMELL | `python:S3776` | `src/flext_tests/_utilities/_matchers/_containment.py` | 21 | |
| 20 | CRITICAL | CODE_SMELL | `python:S3776` | `src/flext_tests/_utilities/_matchers/_that.py` | 532 | |
| 21 | CRITICAL | CODE_SMELL | `python:S3776` | `src/flext_tests/_utilities/_matchers/_that.py` | 607 | |
| 22 | CRITICAL | CODE_SMELL | `python:S3776` | `src/flext_tests/_utilities/make_contract.py` | 53 | |
| 23 | CRITICAL | CODE_SMELL | `python:S3776` | `src/flext_tests/_utilities/make_registry.py` | 132 | |
| 24 | CRITICAL | CODE_SMELL | `python:S3776` | `src/flext_tests/_utilities/make_rendering.py` | 155 | |
| 25 | CRITICAL | CODE_SMELL | `python:S3776` | `src/flext_tests/_utilities/workspace_cleanup_paths.py` | 94 | |
| 26 | CRITICAL | CODE_SMELL | `python:S3776` | `src/flext_tests/_validator/tests.py` | 60 | |
| 27 | CRITICAL | CODE_SMELL | `python:S1192` | `src/flext_tests/domains.py` | 15 | |
| 28 | CRITICAL | CODE_SMELL | `python:S1192` | `src/flext_tests/kube.py` | 56 | |
| 29 | CRITICAL | VULNERABILITY | `docker:S6470` | `tests/fixtures/ci/docker/alpine.Dockerfile` | 33 | |
| 30 | CRITICAL | VULNERABILITY | `docker:S6470` | `tests/fixtures/ci/docker/arch.Dockerfile` | 35 | |
| 31 | CRITICAL | VULNERABILITY | `docker:S6470` | `tests/fixtures/ci/docker/debian.Dockerfile` | 36 | |
| 32 | CRITICAL | VULNERABILITY | `docker:S6470` | `tests/fixtures/ci/docker/fedora.Dockerfile` | 35 | |
| 33 | CRITICAL | VULNERABILITY | `docker:S6470` | `tests/fixtures/ci/docker/ubuntu.Dockerfile` | 36 | |
| 34 | MAJOR | VULNERABILITY | `githubactions:S8264` | `.github/workflows/docs.yml` | 18 | |
| 35 | MAJOR | VULNERABILITY | `githubactions:S8233` | `.github/workflows/docs.yml` | 19 | |
| 36 | MAJOR | VULNERABILITY | `githubactions:S8233` | `.github/workflows/docs.yml` | 20 | |
| 37 | MAJOR | CODE_SMELL | `python:S8786` | `src/flext_tests/_constants/validator.py` | 205 | |
| 38 | MAJOR | CODE_SMELL | `python:S8786` | `src/flext_tests/_constants/validator.py` | 211 | |
| 39 | MAJOR | CODE_SMELL | `python:S3358` | `src/flext_tests/_utilities/_files/_comparison.py` | 36 | |
| 40 | MAJOR | CODE_SMELL | `python:S3358` | `src/flext_tests/_utilities/_files/_comparison_parts/comparison_part_01.py` | 35 | |
| 41 | MAJOR | CODE_SMELL | `python:S3358` | `src/flext_tests/_utilities/_files/_creation.py` | 171 | |
| 42 | MAJOR | CODE_SMELL | `python:S3358` | `src/flext_tests/_utilities/_files/_creation.py` | 186 | |
| 43 | MAJOR | CODE_SMELL | `python:S108` | `src/flext_tests/_utilities/_files/_info.py` | 143 | |
| 44 | MAJOR | CODE_SMELL | `python:S108` | `src/flext_tests/_utilities/_files/_info.py` | 151 | |
| 45 | MAJOR | CODE_SMELL | `python:S3358` | `src/flext_tests/_utilities/_matchers/_containment.py` | 64 | |
| 46 | MAJOR | CODE_SMELL | `python:S3358` | `src/flext_tests/_utilities/_matchers/_containment.py` | 110 | |
| 47 | MAJOR | CODE_SMELL | `python:S108` | `src/flext_tests/_utilities/_matchers/_result.py` | 166 | |
| 48 | MAJOR | CODE_SMELL | `python:S108` | `src/flext_tests/_utilities/_matchers/_result.py` | 439 | |
| 49 | MAJOR | CODE_SMELL | `python:S108` | `src/flext_tests/_utilities/_matchers/_that.py` | 586 | |
| 50 | MAJOR | CODE_SMELL | `python:S108` | `src/flext_tests/_utilities/_matchers/_that.py` | 635 | |
| 51 | MAJOR | CODE_SMELL | `python:S108` | `src/flext_tests/_utilities/_matchers/_that.py` | 660 | |
| 52 | MAJOR | CODE_SMELL | `python:S3358` | `src/flext_tests/_utilities/_matchers/_that.py` | 711 | |
| 53 | MAJOR | CODE_SMELL | `python:S108` | `src/flext_tests/_utilities/_matchers/_that.py` | 841 | |
| 54 | MAJOR | CODE_SMELL | `python:S108` | `src/flext_tests/_utilities/_matchers/_that.py` | 907 | |
| 55 | MAJOR | CODE_SMELL | `python:S3358` | `src/flext_tests/_utilities/_matchers/_that.py` | 921 | |
| 56 | MAJOR | CODE_SMELL | `python:S3358` | `src/flext_tests/_utilities/workspace_cleanup_plan.py` | 57 | |
| 57 | MAJOR | VULNERABILITY | `docker:S6506` | `tests/fixtures/ci/docker/alpine.Dockerfile` | 20 | |
| 58 | MAJOR | VULNERABILITY | `docker:S6506` | `tests/fixtures/ci/docker/alpine.Dockerfile` | 23 | |
| 59 | MAJOR | VULNERABILITY | `docker:S6506` | `tests/fixtures/ci/docker/alpine.Dockerfile` | 25 | |
| 60 | MAJOR | VULNERABILITY | `docker:S6506` | `tests/fixtures/ci/docker/alpine.Dockerfile` | 27 | |
| 61 | MAJOR | VULNERABILITY | `docker:S6506` | `tests/fixtures/ci/docker/arch.Dockerfile` | 22 | |
| 62 | MAJOR | VULNERABILITY | `docker:S6506` | `tests/fixtures/ci/docker/arch.Dockerfile` | 25 | |
| 63 | MAJOR | VULNERABILITY | `docker:S6506` | `tests/fixtures/ci/docker/arch.Dockerfile` | 27 | |
| 64 | MAJOR | VULNERABILITY | `docker:S6506` | `tests/fixtures/ci/docker/arch.Dockerfile` | 29 | |
| 65 | MAJOR | VULNERABILITY | `docker:S6506` | `tests/fixtures/ci/docker/debian.Dockerfile` | 23 | |
| 66 | MAJOR | VULNERABILITY | `docker:S6506` | `tests/fixtures/ci/docker/debian.Dockerfile` | 26 | |
| 67 | MAJOR | VULNERABILITY | `docker:S6506` | `tests/fixtures/ci/docker/debian.Dockerfile` | 28 | |
| 68 | MAJOR | VULNERABILITY | `docker:S6506` | `tests/fixtures/ci/docker/debian.Dockerfile` | 30 | |
| 69 | MAJOR | VULNERABILITY | `docker:S6506` | `tests/fixtures/ci/docker/fedora.Dockerfile` | 22 | |
| 70 | MAJOR | VULNERABILITY | `docker:S6506` | `tests/fixtures/ci/docker/fedora.Dockerfile` | 25 | |
| 71 | MAJOR | VULNERABILITY | `docker:S6506` | `tests/fixtures/ci/docker/fedora.Dockerfile` | 27 | |
| 72 | MAJOR | VULNERABILITY | `docker:S6506` | `tests/fixtures/ci/docker/fedora.Dockerfile` | 29 | |
| 73 | MAJOR | VULNERABILITY | `docker:S6506` | `tests/fixtures/ci/docker/ubuntu.Dockerfile` | 23 | |
| 74 | MAJOR | VULNERABILITY | `docker:S6506` | `tests/fixtures/ci/docker/ubuntu.Dockerfile` | 26 | |
| 75 | MAJOR | VULNERABILITY | `docker:S6506` | `tests/fixtures/ci/docker/ubuntu.Dockerfile` | 28 | |
| 76 | MAJOR | VULNERABILITY | `docker:S6506` | `tests/fixtures/ci/docker/ubuntu.Dockerfile` | 30 | |
| 77 | MAJOR | CODE_SMELL | `python:S5778` | `tests/unit/test_utilities.py` | 131 | |
| 78 | MINOR | CODE_SMELL | `python:S7504` | `conftest.py` | 20 | |
| 79 | MINOR | CODE_SMELL | `python:S7498` | `src/flext_tests/_models/batch.py` | 76 | |
| 80 | MINOR | CODE_SMELL | `python:S7498` | `src/flext_tests/_models/batch.py` | 81 | |
| 81 | MINOR | CODE_SMELL | `python:S7498` | `src/flext_tests/_models/make.py` | 95 | |
| 82 | MINOR | CODE_SMELL | `python:S7498` | `src/flext_tests/_models/make.py` | 105 | |
| 83 | MINOR | CODE_SMELL | `python:S7498` | `src/flext_tests/_models/matchers.py` | 391 | |
| 84 | MINOR | CODE_SMELL | `python:S7498` | `src/flext_tests/_models/matchers.py` | 399 | |
| 85 | MINOR | CODE_SMELL | `python:S7498` | `src/flext_tests/_models/matchers.py` | 407 | |
| 86 | MINOR | CODE_SMELL | `python:S7498` | `src/flext_tests/_utilities/_matchers/_that.py` | 521 | |
| 87 | MINOR | CODE_SMELL | `python:S7498` | `src/flext_tests/_utilities/_matchers/_that.py` | 529 | |
| 88 | MINOR | CODE_SMELL | `python:S2772` | `src/flext_tests/_validator/_types_parts/types_part_01.py` | 12 | |
| 89 | MINOR | CODE_SMELL | `python:S2772` | `src/flext_tests/_validator/_types_parts/types_part_02.py` | 15 | |
| 90 | MINOR | CODE_SMELL | `python:S2772` | `src/flext_tests/_validator/tests.py` | 18 | |
| 91 | MINOR | CODE_SMELL | `python:S116` | `src/flext_tests/validator.py` | 24 | |
| 92 | MINOR | CODE_SMELL | `python:S116` | `src/flext_tests/validator.py` | 26 | |
| 93 | MINOR | CODE_SMELL | `python:S7498` | `src/flext_tests/validator.py` | 45 | |
| 94 | MINOR | VULNERABILITY | `docker:S6471` | `tests/fixtures/ci/docker/alpine.Dockerfile` | 8 | |
| 95 | MINOR | CODE_SMELL | `docker:S7031` | `tests/fixtures/ci/docker/alpine.Dockerfile` | 12 | |
| 96 | MINOR | CODE_SMELL | `docker:S7018` | `tests/fixtures/ci/docker/alpine.Dockerfile` | 12 | |
| 97 | MINOR | VULNERABILITY | `docker:S6471` | `tests/fixtures/ci/docker/arch.Dockerfile` | 7 | |
| 98 | MINOR | CODE_SMELL | `docker:S7031` | `tests/fixtures/ci/docker/arch.Dockerfile` | 13 | |
| 99 | MINOR | VULNERABILITY | `docker:S6471` | `tests/fixtures/ci/docker/debian.Dockerfile` | 7 | |
| 100 | MINOR | CODE_SMELL | `docker:S7031` | `tests/fixtures/ci/docker/debian.Dockerfile` | 13 | |
| 101 | MINOR | CODE_SMELL | `docker:S7018` | `tests/fixtures/ci/docker/debian.Dockerfile` | 14 | |
| 102 | MINOR | VULNERABILITY | `docker:S6471` | `tests/fixtures/ci/docker/fedora.Dockerfile` | 7 | |
| 103 | MINOR | CODE_SMELL | `docker:S7031` | `tests/fixtures/ci/docker/fedora.Dockerfile` | 13 | |
| 104 | MINOR | VULNERABILITY | `docker:S6471` | `tests/fixtures/ci/docker/ubuntu.Dockerfile` | 7 | |
| 105 | MINOR | CODE_SMELL | `docker:S7031` | `tests/fixtures/ci/docker/ubuntu.Dockerfile` | 13 | |
| 106 | MINOR | CODE_SMELL | `docker:S7018` | `tests/fixtures/ci/docker/ubuntu.Dockerfile` | 14 | |

## Como triar

1. **BLOCKER e CRITICAL primeiro**, e todo VULNERABILITY independente de severidade.
2. Classificar: **corrigir**, **falso-positivo** (marcar na plataforma SonarCloud com justificativa), **risco-aceito** (com prazo).
3. CODE_SMELL em volume alto sugere padrão — corrigir a causa raiz, não issue a issue.

Dados brutos: `~/sonarqube-violations/by-repo/flext-sh__flext-tests.json`

