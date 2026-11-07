# Feature Drift Radar

> Detecta si los datos que alimentan un modelo han cambiado antes de que el modelo empiece a fallar.

**Feature Drift Radar** es una CLI ligera y explicable para comparar dos CSV: un conjunto de referencia (entrenamiento) y uno actual (producción). Calcula *Population Stability Index* (PSI) para columnas numéricas y distancia de Jensen–Shannon para categóricas.

## Why it matters

Un modelo puede seguir respondiendo aunque los datos hayan cambiado: nuevos clientes, estacionalidad, cambios de producto o errores en el pipeline. Este proyecto permite tener una primera alarma de drift sin depender de una plataforma externa.

## Funcionalidades

- Detecta y clasifica columnas numéricas/categóricas automáticamente.
- PSI por columna numérica con bins construidos desde el dataset de referencia.
- Distancia Jensen–Shannon para distribuciones categóricas.
- Semáforo: **stable**, **watch** o **drift**.
- Informe JSON exportable y salida de terminal legible.
- Sin dependencias externas: solo Python estándar.

## Instalación

```bash
git clone https://github.com/alvaroalcalaa/feature-drift-radar.git
cd feature-drift-radar
python radar.py examples/reference.csv examples/current.csv --report report.json
```

Requiere Python 3.10+.

## Demo

```text
Feature                Type         Score    Status
------------------------------------------------------
monthly_spend          numeric      0.284    drift
plan                   categorical 0.061    stable

2 features analysed · 1 drift alert
```

## Uso

```bash
python radar.py reference.csv current.csv
python radar.py reference.csv current.csv --bins 8 --report drift-report.json
```

Los umbrales por defecto son PSI ≥ 0.25 y Jensen–Shannon ≥ 0.15 para marcar `drift`.

## Estructura

```text
feature-drift-radar/
├── radar.py
├── tests.py
├── examples/
│   ├── reference.csv
│   └── current.csv
└── README.md
```

## English

Feature Drift Radar is a dependency-free Python CLI that compares a reference CSV against a current CSV. It flags distribution shifts with PSI for numeric features and Jensen–Shannon distance for categorical features, producing an explainable terminal and JSON report.

## License

MIT © 2026 Álvaro Alcalá
