# System Specification
## Data Poisoning Canary System for ML Pipelines (PoC)

---
### Scope Constraint (PoC)
This specification intentionally limits scope to:
- batch tabular data
- offline comparison
- explainable statistical signals

Any feature not required to demonstrate end-to-end canary behavior is deferred.


## 1. Problem Statement

Machine learning systems are vulnerable to silent dataset degradation prior to model training. Such degradation may arise from statistical distribution shifts, data pipeline malfunctions, or accidental or intentional data poisoning.

In this system, **data drift** is defined as:

Any statistically observable deviation between two versions of the same tabular dataset that plausibly indicates corruption, pipeline failure, or poisoning, independent of downstream model behavior.

The system detects symptoms, not intent, and provides early, explainable warnings before model training occurs.

---

## 2. Inputs

### 2.1 Dataset Definition
- Input datasets are tabular.
- Rows represent observations.
- Columns represent features.
- An optional label column may be present.

Non-tabular formats are out of scope.

### 2.2 Dataset Versioning
- Each ingestion creates a new immutable dataset version.
- Versions are identified by dataset name and version identifier.
- Dataset versions must not be modified once ingested.

### 2.3 Reference vs Current Dataset
- Drift analysis is defined as a comparison between two dataset versions.
- Default baseline is the immediately preceding version.
- Users may optionally specify an explicit baseline version.

Time-based windows and rolling baselines are out of scope.

---

## 3. Processing Model

### 3.1 Statistical Fingerprinting
For each dataset version, the system computes deterministic and reproducible statistical fingerprints, including:
- Dataset-level summaries
- Feature-level summaries
- Label distribution summaries (if applicable)

Fingerprints must be significantly smaller than raw datasets.

### 3.2 Statistical Sketches (Deferred)
Statistical sketches are out of scope for the initial PoC and may be introduced in later iterations for scalability experiments.

### 3.3 Signal Computation
Multiple drift and corruption signals are computed, including but not limited to:
- Distribution shift metrics
- Entropy change
- Variance collapse
- Missingness spikes
- Duplicate rate increases
- Label imbalance changes

Each signal produces a normalized abnormality measure.

#### 3.3.a Signal Computation (Cycle 1)
In the initial implementation, the system computes a minimal set of explainable drift signals:
- KS test for numerical features
- Population Stability Index (PSI)
- Categorical frequency shift (L1 distance)

Additional signals (entropy, variance collapse, missingness, duplicates) are explicitly deferred.


### 3.4 Signal Aggregation
- Weak signals are aggregated to estimate evidence strength.
- Certain signals may be designated as fatal.
- Fatal signals may independently trigger failure.

---

## 4. Outputs

### 4.1 Canary States
The system emits one of three advisory canary states:
- OK: No significant abnormalities.
- WARN: Evidence of abnormality with insufficient confidence.
- FAIL: High-confidence abnormality detected.

### 4.2 Stored Artifacts
The system persists:
1. Statistical fingerprints
2. Statistical sketches (if generated)
3. Comparison artifacts including canary state and explanation

Raw dataset copies are not stored as artifacts.

---

## 5. Architecture

### 5.1 FastAPI
Responsible for ingestion orchestration, versioning, async task triggering, and artifact retrieval. No statistical computation is performed.

### 5.2 Celery
Responsible for fingerprinting, sketching, signal computation, aggregation, and canary evaluation. Tasks must be idempotent and replayable.

### 5.3 Redis
Acts as a transient task broker and coordination layer. Not a system of record.

### 5.4 MinIO
System of record for dataset versions, fingerprints, sketches, and comparison artifacts.

---

## 6. Explicit Non-Goals
- No UI or dashboards
- No streaming or real-time detection
- No model drift analysis
- No automated remediation
- No domain-specific semantics

---

## 7. External API

- `POST /datasets/{name}/ingest`
  - Accepts tabular data
  - Creates immutable dataset version

- `POST /datasets/{name}/compare`
  - Compares latest version against baseline
  - Triggers canary evaluation

- `GET /datasets/{name}/artifacts/{version}`
  - Retrieves stored fingerprints and canary result
