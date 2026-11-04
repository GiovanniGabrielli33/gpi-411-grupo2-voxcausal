# Vox-Causal AI · Informe ERV para Alloxentric SpA

Repositorio oficial del **Grupo 2 – Sección 411** de la cátedra **Gestión de Proyectos Informáticos (GPI) 2026-II**, Universidad Tecnológica Metropolitana (UTEM).

**Caso de estudio PIA:** evaluación técnica y económica (Informe ERV) para integrar el prototipo **Vox-Causal AI**, un motor de inferencia causal y análisis prosódico, en la plataforma SaaS corporativa de **Alloxentric SpA** (Microsoft Azure, Londres).

| | |
|---|---|
| Docente | Dr. Oscar Magna Veloso |
| Integrantes | Giovanni Gabrielli · Martín Vera · Aylin Strajilevich · Cristóbal Muñoz |
| Dictamen | **GO condicionado** (VAN después de impuestos US$ 366.751 · TIR 91,9 % · Payback 1,82 años · B/C 1,54) |
| Drive de la Parte 1 | Carpeta `/GPI-Taller Arquitectura/`: https://drive.google.com/drive/folders/18HAemgvuCRbLo8SWjQS0V514eCEYORqd?usp=drive_link |

## Estructura

```
├── README.md
├── docs/
│   ├── erv/            Informe ERV (Word y PDF) y presentación del caso (entregable exigido)
│   │   └── figuras/    Gráficos de costos, flujo de caja, sensibilidad, latencia y ahorro
│   ├── arquitectura/   Diagramas C4 niveles 1, 2 y 3 y pipeline MLOps
│   └── gestion/        Curva S y cuadrante de desempeño EVM
├── src/voxcausal/      Prototipo del núcleo (motor causal, guardián de latencia, filtro PII, ventaneo, política D4)
├── tests/              28 pruebas pytest
└── pyproject.toml      Dependencias y configuración de pytest-cov y ruff
```

## Métricas de calidad (ISO/IEC 25010, Informe ERV sección 2.3)

| Métrica | Meta | Valor medido en el prototipo |
|---|---|---|
| Error de ATE (efecto real 8 pp, 200.000 llamadas sintéticas) | ≤ 0,05 | 0,0009 con ajuste backdoor (0,071 sin ajuste) |
| Latencia p95 (presupuesto por tramo) | < 250 ms | 175 ms |
| Cobertura de pruebas (líneas y ramas) | ≥ 80 % | 100 % |
| Deuda técnica (método SQALE, estimada con ruff y pylint) | ≤ 4 h por incremento | 0,3–1,5 h, rating A |

Para reproducirlas:

```bash
pip install -e ".[dev]"
pytest
```

## Flujo de trabajo

- `main`: versión entregada.
- `feature/*`: desarrollo; cada rama se integra a `main` mediante pull request revisado por otro integrante (PR #1 informe, PR #2 prototipo).

## Uso de IA

Los diagramas, gráficos, cálculos y el prototipo se elaboraron con asistencia de IA generativa (Claude Opus, Anthropic) y fueron revisados por el equipo. Cada figura indica su fuente.
