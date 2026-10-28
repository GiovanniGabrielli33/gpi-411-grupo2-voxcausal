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
├── src/                Código de la solución (se incorpora si el dictamen es GO)
└── tests/              Pruebas (se incorporan si el dictamen es GO)
```

## Flujo de trabajo

- `main`: versión entregada.
- `feature/erv`: desarrollo del Informe ERV; se integra a `main` mediante pull request revisado por otro integrante.

## Uso de IA

Los diagramas, gráficos y cálculos se elaboraron con asistencia de IA generativa (Claude Opus, Anthropic) y fueron revisados por el equipo. Cada figura indica su fuente.
