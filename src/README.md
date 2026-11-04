# src

Prototipo del núcleo de Vox-Causal AI: los componentes del C4 Nivel 3 que pueden probarse sin Azure.

| Módulo | Componente / decisión |
|---|---|
| `voxcausal/causal.py` | Estimador causal con ajuste backdoor (Anexo D del informe) |
| `voxcausal/guardian.py` | Guardián de latencia con efectos precalculados (D2) |
| `voxcausal/pii.py` | Filtro de datos personales antes del LLM |
| `voxcausal/latency.py` | Ventaneo y presupuesto de latencia (p95 < 250 ms) |
| `voxcausal/security.py` | Política de acceso a audio del incidente (D4) |

Los servicios completos (Media Ingest Gateway, Servicio de Inferencia, Worker y escritorio del agente) se construyen en la fase 1 si el directorio confirma el dictamen.
