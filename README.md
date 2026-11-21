<!-- Profile README for github.com/santoshmyakala -->

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/header-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="./assets/header-light.svg">
  <img alt="Santoshkumar Myakala — Cloud Architect | DevOps & SRE | Platform Engineering | MLOps & AI Infrastructure" src="./assets/header-dark.svg" width="100%">
</picture>

<a href="https://github.com/santoshmyakala">
  <img alt="Cloud & Infrastructure Architecture · DevOps and Site Reliability Engineering · Platform Engineering · MLOps and AI Infrastructure · Kubernetes and Cloud Automation" src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=500&size=20&duration=2800&pause=1200&color=58A6FF&center=true&vCenter=true&width=620&lines=Cloud+%26+Infrastructure+Architecture;DevOps+and+Site+Reliability+Engineering;Platform+Engineering;MLOps+and+AI+Infrastructure;Kubernetes+and+Cloud+Automation">
</a>

<br>

<a href="https://www.linkedin.com/in/santoshkumar-myakala-b3456021/"><img alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-Santoshkumar%20Myakala-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white"></a>
<a href="https://github.com/santoshmyakala?tab=repositories"><img alt="GitHub repositories" src="https://img.shields.io/badge/GitHub-Repositories-24292f?style=for-the-badge&logo=github&logoColor=white"></a>
<img alt="Location: Stockholm, Sweden" src="https://img.shields.io/badge/Based%20in-Stockholm%2C%20Sweden-2ea043?style=for-the-badge">
<img alt="Open to AI Platform, MLOps and Cloud Architecture roles" src="https://img.shields.io/badge/Open%20to-AI%20Platform%20·%20MLOps%20·%20Cloud%20Architecture-8250df?style=for-the-badge">

<br><br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/impact-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="./assets/impact-light.svg">
  <img alt="15+ years in IT; 12 years DevOps and cloud; 13 tested project repos; 13 Terraform stacks tested; 191 automated tests in CI; 100% of images signed with SBOM" src="./assets/impact-dark.svg" width="100%">
</picture>

</div>

---

## About

I design and build the platforms engineers ship on — **multi-account AWS and Azure foundations, Kubernetes with GitOps, large-scale CI/CD** (cloud, embedded and hardware-in-the-loop at Scania), and increasingly **GPU and AI infrastructure**. 15+ years in IT, 12 in DevOps and cloud, across Sweden, Belgium, France, Germany and India.

I work from architecture to production: ADRs, workshops, PoCs and technology evaluations, then hands-on delivery. My public repositories are built the same way — **every claim below is backed by code with passing CI**.

<div align="center">
<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/capabilities-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="./assets/capabilities-light.svg">
  <img alt="Capability map: Cloud foundation, Secure delivery, AI infrastructure, MLOps and agentic AI" src="./assets/capabilities-dark.svg" width="100%">
</picture>

</div>

**Current focus:** AI-driven DevOps (agentic CI-failure triage, alert analysis), AI platform engineering and MLOps.

## Tech stack

<div align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/stack-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="./assets/stack-light.svg">
  <img alt="Tech stack — Cloud: AWS, Azure, Google Cloud; Containers and GitOps: Docker, Kubernetes, Helm, Argo CD; CI/CD: Jenkins, GitLab CI, GitHub Actions, Azure DevOps, Bitbucket, JFrog; IaC and security: Terraform, Ansible, Trivy, Falco; Monitoring and tracing: Prometheus, Grafana, OpenTelemetry, Datadog, Power BI; Logging: Loki, Elasticsearch, Logstash, Kibana; AI, GPU and ML: NVIDIA, PyTorch, MLflow, DVC, scikit-learn, FastAPI, Claude; Operating systems: Linux, Red Hat, SUSE, Ubuntu, Debian, Kali Linux, QNX; Languages: Python, Bash, C, C++, Java, Groovy, JavaScript, Go, Rust; Python data stack: pandas, NumPy, Matplotlib, Jupyter; Data engineering: Hadoop, Hive, Spark, Kafka, Airflow, NiFi, Databricks; Databases and servers: PostgreSQL, MySQL, MongoDB, Redis, DynamoDB, Cosmos DB, Nginx" src="./assets/stack-dark.svg" width="100%">
</picture>
</div>


## Featured projects

#### ☁️ Cloud & platform architecture

<table>
<tr>
<td colspan="2" valign="top">

### [cloud-solution-architectures](https://github.com/santoshmyakala/cloud-solution-architectures)
**AWS and Azure side by side**: landing-zone guardrails (SCPs / Azure Policy), hub-and-spoke inspection networking (Transit Gateway + Network Firewall / Azure Firewall Premium), serverless event-driven intake, Kubernetes platform and multi-region DR — with ADRs and Well-Architected mapping.

`Terraform` `AWS` `Azure` `Network Firewall` `Azure Policy` `Lambda` `Functions`

<sub>6 Terraform stacks with offline <code>terraform test</code> · blocking Trivy IaC gate · identical validation logic on both clouds</sub>

</td>
</tr>
<tr>
<td width="50%" valign="top">

### [aws-saas-production-platform](https://github.com/santoshmyakala/aws-saas-production-platform)
A production AWS platform **designed from failure domains**: per-AZ NAT and VPC endpoints, N+1 AZ capacity math, CloudFront + WAF, ECS Fargate **canary deploys rolled back by SLO alarms**, Aurora + RDS Proxy, SQS + DLQ, burn-rate alerting and **warm-standby DR** (Aurora Global, Route 53 failover).

`Terraform` `AWS` `ECS Fargate` `Aurora` `RDS Proxy` `CloudFront` `WAF` `Route 53`

<sub>18 plan-time tests prove zonal isolation, AZ-loss capacity, edge lockdown, rollback alarms and DR · GitHub Actions: OIDC plans on PRs, staged deploys with approval, nightly drift issues</sub>

</td>
<td width="50%" valign="top">

### [resilience-patterns-lab](https://github.com/santoshmyakala/resilience-patterns-lab)
The code behind the diagram words: **exactly-once effects on an at-least-once queue** (idempotency keys, transactional outbox, ack-after-commit), deadlines, **retry budgets**, circuit breakers and load shedding.

`Python` `FastAPI` `PostgreSQL` `SQS` `ElasticMQ` `Prometheus`

<sub>Weekly GitHub Actions game day: dependency outage, overload and a worker SIGKILL mid-batch → 200/200 captured, none twice · 27× retry amplification measured and fixed</sub>

</td>
</tr>
<tr>
<td colspan="2" valign="top">

### [azure-hybrid-manufacturing-platform](https://github.com/santoshmyakala/azure-hybrid-manufacturing-platform)
**Hybrid cloud for a factory**: ExpressRoute primary / VPN backup into an Azure Firewall Premium hub, **OT/IT segmentation as IEC 62443 zones and conduits** (nothing in Azure can reach the control network), private-only PaaS with Entra ID auth, private AKS, hybrid DNS, Azure Policy + FinOps budgets, SQL failover-group DR.

`Terraform` `Azure` `ExpressRoute` `Azure Firewall` `AKS` `Event Hubs` `Azure Policy` `FinOps`

<sub>12 offline tests prove inspection of every flow, OT conduits, private endpoints, policy and budgets · GitHub Actions with OIDC federated credentials · ADRs + runbooks</sub>

</td>
</tr>
<tr>
<td width="50%" valign="top">

### [aws-three-tier-platform](https://github.com/santoshmyakala/aws-three-tier-platform)
HA **web → app → MongoDB replica set** across three AZs with WireGuard VPN, least-privilege security groups and SSM-only access (no SSH).

`Terraform` `AWS` `ALB` `Auto Scaling` `MongoDB` `WireGuard`

<sub>5 plan-level tests with a mocked AWS provider · IMDSv2 · encrypted volumes</sub>

</td>
<td width="50%" valign="top">

### [ansible-elk-stack](https://github.com/santoshmyakala/ansible-elk-stack)
Secured **Elastic Stack 9**: auth on, least-privilege Logstash writer, Kibana only behind an Nginx TLS proxy, Vault-managed secrets.

`Ansible` `Elasticsearch` `Logstash` `Kibana` `Docker`

<sub>Deployed for real in CI · idempotent (changed=0) · end-to-end verify playbook</sub>

</td>
</tr>
</table>

#### ⚙️ Platform services & tooling — Go · Java · Rust

<table>
<tr>
<td colspan="2" valign="top">

### [k8s-guardrails-webhook](https://github.com/santoshmyakala/k8s-guardrails-webhook)
A **Kubernetes validating admission webhook** in Go that admits only **digest-pinned images from trusted registries**, with FinOps labels, resource requests/limits and a non-root, unprivileged runtime. Ratchets on `UPDATE`, audited break-glass, warn-then-enforce rollout, Prometheus metrics; **fails closed**, TLS 1.3 with cert-manager hot-reload and no API access.

`Go` `Kubernetes` `Admission webhook` `cert-manager` `kustomize` `Prometheus` `cosign`

<sub>21 unit/HTTP tests + a 9-check kind e2e against a real API server (incl. fail-closed) · distroless image, signed by digest with cosign (SBOM + SLSA provenance)</sub>

</td>
</tr>
<tr>
<td width="50%" valign="top">

### [production-orders-service](https://github.com/santoshmyakala/production-orders-service)
A **Spring Boot 4 / Java 21** service for plant production orders: idempotent creation, ETag/If-Match optimistic locking, **transactional outbox** (`SKIP LOCKED` relay), ERP calls behind timeouts, retries and a **circuit breaker**, OAuth2 JWT roles — the kind of workload the Azure hybrid platform hosts.

`Java 21` `Spring Boot 4` `PostgreSQL` `Flyway` `Resilience4j` `Testcontainers` `Docker`

<sub>22 tests incl. Testcontainers PostgreSQL + a real ERP stub, 92% line coverage · distroless layered image · manifests pass the guardrails webhook</sub>

</td>
<td width="50%" valign="top">

### [ci-failure-triage](https://github.com/santoshmyakala/ci-failure-triage)
A **Rust CLI and GitHub Action** that reads a CI log and says **why a job failed and whether a retry is worth it**: 35 weighted rules across 10 categories, root-cause-over-symptom scoring, GitHub / GitLab / Jenkins logs.

`Rust` `clap` `regex` `GitHub Actions` `cosign`

<sub>20 tests · streams 500 MB in ~6 s (84 MB/s), constant memory · signed Linux / macOS / Windows releases</sub>

</td>
</tr>
</table>

#### 🔐 DevSecOps & software supply chain

<table>
<tr>
<td width="50%" valign="top">

### [devsecops-gitops-pipeline](https://github.com/santoshmyakala/devsecops-gitops-pipeline)
Central **reusable secure-delivery workflow** (gitleaks → Semgrep → Trivy → SBOM → image gate → keyless Sigstore signing), signature-gated GitOps promotion, Argo CD, and **Kyverno 1.20** policies admitting only pipeline-signed images.

`GitHub Actions` `Sigstore` `Syft` `Trivy` `Argo CD` `Kyverno` `kind`

<sub>kind e2e: signed image admitted · unsigned, privileged, root and <code>:latest</code> denied</sub>

</td>
<td width="50%" valign="top">

### [devsecops-reference-architectures](https://github.com/santoshmyakala/devsecops-reference-architectures)
Eight DevSecOps architectures across platforms and lifecycle stages: GitHub, **GitLab**, **Azure DevOps** (Notation/Ratify), **AWS-native** (CodePipeline, Inspector, Signer), OPA/Conftest, **OWASP ZAP DAST**, External Secrets, **Falco**.

`GitLab CI` `Azure DevOps` `AWS Signer` `OPA` `ZAP` `Falco` `External Secrets`

<sub>19 Rego tests · schema-validated pipelines · live ZAP scan: 118 rules passed, 2 findings fixed at source</sub>

</td>
</tr>
</table>

#### 🧠 AI infrastructure & agentic AI

<table>
<tr>
<td colspan="2" valign="top">

### [ansible-llm-platform](https://github.com/santoshmyakala/ansible-llm-platform)
A **self-hosted LLM platform provisioned end to end with Ansible**:
- hardened nodes with an inventory-generated nftables firewall;
- **llama.cpp and vLLM** chosen per node (CPU, NVIDIA, AMD/Intel), with every model file checked against its published SHA-256;
- an **in-house gateway**: team keys stored only as hashes, per-team request and token limits, least-in-flight routing with **failover**;
- Prometheus SLO alerts and Grafana.

`Ansible` `llama.cpp` `vLLM` `Python` `nftables` `Prometheus` `Grafana` `Open WebUI`

<sub>CI installs every role on a fresh VM with a real model, re-runs it (0 changes), then verifies answers, 401/429 and failover with a server stopped · 26 gateway tests · ansible-lint production profile</sub>

</td>
</tr>
<tr>
<td width="50%" valign="top">

### [ai-infrastructure-hpc-gpu](https://github.com/santoshmyakala/ai-infrastructure-hpc-gpu)
**GPU training platform** on Kubernetes (GPU Operator, MIG/time-slicing, Kueue, PyTorchJob, DCGM alerts) and **Slurm HPC** (GRES, IB topology, Pyxis), on **EKS p5 + EFA + FSx Lustre** and **AKS ND H100 v5 + Managed Lustre**, plus an NVIDIA licensing guide.

`NVIDIA GPU Operator` `Slurm` `Kueue` `Kubeflow` `NCCL` `DCGM` `EFA` `Terraform`

<sub>Real 2-process DDP training in CI · real <code>slurmctld</code> accepts the config · PyTorchJob validated against Kubeflow CRD</sub>

</td>
<td width="50%" valign="top">

### [agentic-genai-platform](https://github.com/santoshmyakala/agentic-genai-platform)
**Ops Copilot**: a retrieval-grounded **Claude** agent for platform operations — runbook RAG with citations, live tools (DCGM, CI, model API), human-approved side effects, prompt-injection fencing and secret redaction, evals.

`Claude API` `Agents` `Tool use` `RAG` `FastAPI` `Prometheus`

<sub>31 deterministic tests with a scripted model client · 7-case behavioural eval set · ships via the signed pipeline</sub>

</td>
</tr>
</table>

#### 📈 MLOps & machine learning

<table>
<tr>
<td width="50%" valign="top">

### [wine-quality-mlops](https://github.com/santoshmyakala/wine-quality-mlops)
Reproducible ML lifecycle: **DVC → MLflow tracking & registry → FastAPI + Prometheus → hardened container → Helm**, delivered through the central DevSecOps pipeline.

`DVC` `MLflow` `scikit-learn` `FastAPI` `Helm` `Sigstore`

<sub>Test RMSE 0.598 vs 0.874 baseline · signed image promoted to dev</sub>

</td>
<td width="50%" valign="top">

### [wave-energy-farm-ml](https://github.com/santoshmyakala/wave-energy-farm-ml)
Wave-farm power from 16-buoy layouts at four sites: **gradient boosting vs MLP vs a permutation-equivariant set transformer**, with a data-leakage audit.

`PyTorch` `scikit-learn` `MLflow`

<sub>Set transformer R² 0.992 (Perth) · 27k duplicate rows found · blocked split exposes leakage</sub>

</td>
</tr>
<tr>
<td colspan="2" valign="top">

### [fashion-mnist-neural-networks](https://github.com/santoshmyakala/fashion-mnist-neural-networks)
**Softmax regression → MLP → CNN** in PyTorch under one pipeline, so each architectural step is measured.

`PyTorch` `NumPy` `MLflow`

<sub>Test accuracy 84.1% → 90.6% → 93.5%</sub>

</td>
</tr>
</table>

### Live build status

Proof, not claims — every featured repository is tested on every push:

| Repository | CI |
|---|---|
| [ansible-llm-platform](https://github.com/santoshmyakala/ansible-llm-platform) | [![ci](https://github.com/santoshmyakala/ansible-llm-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/santoshmyakala/ansible-llm-platform/actions/workflows/ci.yml) |
| [k8s-guardrails-webhook](https://github.com/santoshmyakala/k8s-guardrails-webhook) | [![ci](https://github.com/santoshmyakala/k8s-guardrails-webhook/actions/workflows/ci.yml/badge.svg)](https://github.com/santoshmyakala/k8s-guardrails-webhook/actions/workflows/ci.yml) |
| [production-orders-service](https://github.com/santoshmyakala/production-orders-service) | [![ci](https://github.com/santoshmyakala/production-orders-service/actions/workflows/ci.yml/badge.svg)](https://github.com/santoshmyakala/production-orders-service/actions/workflows/ci.yml) |
| [ci-failure-triage](https://github.com/santoshmyakala/ci-failure-triage) | [![ci](https://github.com/santoshmyakala/ci-failure-triage/actions/workflows/ci.yml/badge.svg)](https://github.com/santoshmyakala/ci-failure-triage/actions/workflows/ci.yml) |
| [azure-hybrid-manufacturing-platform](https://github.com/santoshmyakala/azure-hybrid-manufacturing-platform) | [![ci](https://github.com/santoshmyakala/azure-hybrid-manufacturing-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/santoshmyakala/azure-hybrid-manufacturing-platform/actions/workflows/ci.yml) |
| [aws-saas-production-platform](https://github.com/santoshmyakala/aws-saas-production-platform) | [![ci](https://github.com/santoshmyakala/aws-saas-production-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/santoshmyakala/aws-saas-production-platform/actions/workflows/ci.yml) |
| [resilience-patterns-lab](https://github.com/santoshmyakala/resilience-patterns-lab) | [![ci](https://github.com/santoshmyakala/resilience-patterns-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/santoshmyakala/resilience-patterns-lab/actions/workflows/ci.yml) |
| [cloud-solution-architectures](https://github.com/santoshmyakala/cloud-solution-architectures) | [![ci](https://github.com/santoshmyakala/cloud-solution-architectures/actions/workflows/ci.yml/badge.svg)](https://github.com/santoshmyakala/cloud-solution-architectures/actions/workflows/ci.yml) |
| [devsecops-gitops-pipeline](https://github.com/santoshmyakala/devsecops-gitops-pipeline) | [![ci](https://github.com/santoshmyakala/devsecops-gitops-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/santoshmyakala/devsecops-gitops-pipeline/actions/workflows/ci.yml) |
| [devsecops-reference-architectures](https://github.com/santoshmyakala/devsecops-reference-architectures) | [![ci](https://github.com/santoshmyakala/devsecops-reference-architectures/actions/workflows/ci.yml/badge.svg)](https://github.com/santoshmyakala/devsecops-reference-architectures/actions/workflows/ci.yml) |
| [ai-infrastructure-hpc-gpu](https://github.com/santoshmyakala/ai-infrastructure-hpc-gpu) | [![ci](https://github.com/santoshmyakala/ai-infrastructure-hpc-gpu/actions/workflows/ci.yml/badge.svg)](https://github.com/santoshmyakala/ai-infrastructure-hpc-gpu/actions/workflows/ci.yml) |
| [agentic-genai-platform](https://github.com/santoshmyakala/agentic-genai-platform) | [![ci](https://github.com/santoshmyakala/agentic-genai-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/santoshmyakala/agentic-genai-platform/actions/workflows/ci.yml) |
| [wine-quality-mlops](https://github.com/santoshmyakala/wine-quality-mlops) | [![ci](https://github.com/santoshmyakala/wine-quality-mlops/actions/workflows/ci.yml/badge.svg)](https://github.com/santoshmyakala/wine-quality-mlops/actions/workflows/ci.yml) |
| [aws-three-tier-platform](https://github.com/santoshmyakala/aws-three-tier-platform) | [![terraform](https://github.com/santoshmyakala/aws-three-tier-platform/actions/workflows/terraform.yml/badge.svg)](https://github.com/santoshmyakala/aws-three-tier-platform/actions/workflows/terraform.yml) |
| [ansible-elk-stack](https://github.com/santoshmyakala/ansible-elk-stack) | [![ci](https://github.com/santoshmyakala/ansible-elk-stack/actions/workflows/ci.yml/badge.svg)](https://github.com/santoshmyakala/ansible-elk-stack/actions/workflows/ci.yml) |
| [wave-energy-farm-ml](https://github.com/santoshmyakala/wave-energy-farm-ml) | [![ci](https://github.com/santoshmyakala/wave-energy-farm-ml/actions/workflows/ci.yml/badge.svg)](https://github.com/santoshmyakala/wave-energy-farm-ml/actions/workflows/ci.yml) |
| [fashion-mnist-neural-networks](https://github.com/santoshmyakala/fashion-mnist-neural-networks) | [![ci](https://github.com/santoshmyakala/fashion-mnist-neural-networks/actions/workflows/ci.yml/badge.svg)](https://github.com/santoshmyakala/fashion-mnist-neural-networks/actions/workflows/ci.yml) |

<sub>Every project ships with CI, tests, results from real runs, SHA-pinned actions, secret scanning and Dependabot. Data sources are cited with their licences. The ML projects began as coursework from my PG Diploma in Machine Learning and were rebuilt as production-style reference implementations.</sub>

## Experience

**Scania (TRATON)** · **Play'n GO** · **ECARX / Volvo Cars** · **Hexagon** · Roller Gaming · ALTEN · Cyient

<details>
<summary><b>Show roles and highlights</b></summary>

| Period | Role | Organisation | Highlights |
|---|---|---|---|
| 2024 – present | DevOps Engineer, Driver System Software Factory | **Scania Group** (TRATON) | GitLab CI/CD and developer-platform architecture across cloud, Android, QNX, embedded and VM environments; automated HIL/SIL pipelines (build → deploy → flash → validate); targeted CI workflows improved by ~40–50%; standardised DevContainers; CI/platform observability with Datadog, OpenTelemetry, Prometheus/Grafana and Loki, plus Power BI CI reporting |
| 2023 – 2024 | Infrastructure Specialist | **Play'n GO** | AWS infrastructure with Terraform; networking, connectivity and SSL/TLS certificate lifecycle; Bitbucket delivery workflows |
| 2022 – 2023 | Cloud Engineer (consultant) | **ECARX Europe / Volvo Cars** via Explipro | AWS with Terraform (networking, IAM, compute, Kubernetes); GitOps with Argo CD; Helm charts; CI/CD traceability; GitLab/JFrog upgrades via GitOps; OAuth 2.0, MFA, Microsoft Entra ID; DevSecOps |
| 2017 – 2022 | Senior Product Development Engineer | **Hexagon Manufacturing Intelligence** | Enterprise CI/CD for multiple desktop and web products; led Perforce → GitLab migration |
| 2021 – 2022 | DevOps Engineer (remote) | **Roller Gaming UK** | AWS infrastructure automation with Terraform |
| 2012 – 2017 | Engineer → Senior Engineer | ALTEN · AMM Enterprise · Cyient · AXISCADES | GitLab CI/Jenkins pipelines, Azure deployments, Terraform, PostgreSQL data pipelines, automation |

</details>

<sub>Full history on <a href="https://www.linkedin.com/in/santoshkumar-myakala-b3456021/">LinkedIn</a>.</sub>

## Skills matrix

<details>
<summary><b>Show the full skills matrix (Production · Projects · Exploring)</b></summary>

> **Production** = used in the professional roles above. **Projects** = demonstrated in the public repositories below. **Exploring** = currently learning.

<table>
<tr><th align="left" width="18%">Area</th><th align="left">Production</th><th align="left" width="26%">Projects</th><th align="left" width="16%">Exploring</th></tr>
<tr>
<td><b>Cloud platforms</b></td>
<td>AWS (multi-account, VPC & networking, IAM, compute, storage) · Microsoft Azure · Microsoft Entra ID · Cloud networking · SSL/TLS</td>
<td>Multi-AZ VPC design · WireGuard VPN · SSM-only access</td>
<td>Google Cloud · Hybrid cloud</td>
</tr>
<tr>
<td><b>DevOps & platform</b></td>
<td>GitLab CI/CD · Jenkins · GitHub Actions · Bitbucket · Docker · DevContainers · Kubernetes · Helm · Argo CD / GitOps · Terraform · Ansible · JFrog Artifactory · Python · Bash · C · C++ · Groovy (Jenkins pipelines) · Java · JavaScript · Go · Rust · Linux (Red Hat, SUSE, Ubuntu, Debian, Kali) · QNX</td>
<td>Go validating admission webhook · distroless multi-stage images · kind e2e · Reusable workflows · Argo CD app-of-apps · <code>terraform test</code> with mocked providers</td>
<td>Internal developer platforms</td>
</tr>
<tr>
<td><b>Observability & reliability</b></td>
<td>SRE practices · Datadog · OpenTelemetry · Prometheus · Grafana · Loki · ELK stack · Power BI CI reporting · Monitoring & alerting</td>
<td>Elastic Stack 9 · Prometheus metrics in services · DCGM GPU alerts</td>
<td>LLM observability</td>
</tr>
<tr>
<td><b>Security</b></td>
<td>DevSecOps · IAM · OAuth 2.0 · MFA · Access control in CI/CD</td>
<td>Sigstore keyless signing · SBOM attestation · Kyverno (CEL) & custom Go (fail-closed) admission · Trivy · Semgrep · gitleaks</td>
<td>SLSA provenance</td>
</tr>
<tr>
<td><b>Architecture</b></td>
<td>CI/CD design · Build & release systems · Infrastructure architecture · ADRs, PoCs & technology evaluation · Cloud migration & legacy modernisation</td>
<td>Threat modelling (STRIDE) · signature-gated promotion</td>
<td>Bazel · Large-scale distributed systems</td>
</tr>
<tr>
<td><b>Data engineering</b></td>
<td>Data pipelines · Kafka · Airflow · NiFi · dbt · Databricks · Hadoop · Hive · Spark · PostgreSQL · MySQL · Redis · pandas · NumPy</td>
<td>DVC data pipelines · DynamoDB / Cosmos DB designs · MongoDB replica set · data-quality audits (pandas)</td>
<td>—</td>
</tr>
<tr>
<td><b>MLOps & AI infrastructure</b></td>
<td>AI-assisted CI log / failure triage (AIOps)</td>
<td>MLflow · DVC · FastAPI model serving · Helm · PyTorch DDP · NVIDIA GPU Operator · Slurm · Kueue · Claude API agents (tool use, RAG, evals)</td>
<td>Model / drift monitoring · LLM observability</td>
</tr>
</table>

</details>



## How I typically build platforms

A generalised view of the delivery platforms I have designed — not a specific employer's system.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/diagrams/platform-dark.svg">
  <img alt="Delivery platform: developer pushes to GitLab; CI builds in a DevContainer, runs unit, integration and HIL/SIL tests and security scans, publishes to Artifactory and bumps a GitOps repo; Argo CD deploys Helm releases to Kubernetes on AWS EKS provisioned with Terraform; Prometheus, OpenTelemetry, Datadog, Loki, Grafana and Power BI CI reports feed AI-assisted triage that sends recommendations back to developers." src="assets/diagrams/platform-light.svg" width="100%">
</picture>

## Certifications & education

Software Architecture of Large-Scale Systems · Cloud Security Lead & Cloud Leader AWS (Scania) · AWS VPC & Networking · Google SRE Culture · IIT Roorkee Big Data Engineering · IBM Big Data & ML

<details>
<summary><b>Show all certifications and education</b></summary>

<table>
<tr><td valign="top" width="50%">

**Cloud, architecture & reliability**
- Software Architecture & Technology of Large-Scale Systems — NewTechWays (2025)
- Cloud Security Lead — Scania Group (2024)
- Cloud Leader AWS — Scania Group (2024)
- AWS VPC and Networking in Depth — Udemy (2023)
- DevOps Specialization — CloudxLab (2022)
- Developing a Google SRE Culture — Coursera / Google Cloud (2021)
- Google Cloud Platform Fundamentals: Core Infrastructure — Coursera (2021)

</td><td valign="top" width="50%">

**Data & machine learning**
- Big Data Engineering with Hadoop & Spark — EICT, IIT Roorkee (2019)
- Big Data & Machine Learning Professional Degree — IBM (2019)
- Data Science Professional Degree — NSDC (2019)
- Deploying Scalable Machine Learning for Data Science — LinkedIn Learning (2021)
- Machine Learning with Python — IBM / Cognitive Class (2021)

**Education**
- Master of Computer Applications — Andhra University
- B.Tech, Aeronautical Engineering — JNTU (university top-5 rank)

</td></tr>
</table>

</details>

## GitHub activity

<div align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/santoshmyakala/santoshmyakala/output/activity-dark.svg">
  <img alt="GitLab-style activity calendar covering every day since joining GitHub; a snake eats each contribution day from oldest to newest while the view pans to today" src="https://raw.githubusercontent.com/santoshmyakala/santoshmyakala/output/activity-light.svg" width="100%">
</picture>
<br>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/santoshmyakala/santoshmyakala/output/languages-dark.svg">
  <img alt="Most used languages across my own public repositories, by bytes of code" src="https://raw.githubusercontent.com/santoshmyakala/santoshmyakala/output/languages-light.svg" width="100%">
</picture>
<br>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/santoshmyakala/santoshmyakala/output/stats-dark.svg?v=2">
  <img alt="All-time GitHub stats since joining: total contributions, commits, pull requests, reviews, issues and repositories, with longest and current streak and stars earned" src="https://raw.githubusercontent.com/santoshmyakala/santoshmyakala/output/stats-light.svg?v=2" width="100%">
</picture>
</div>

---

<div align="center">
<sub>Open to conversations about platform engineering, AI infrastructure and cloud architecture — reach out on <a href="https://www.linkedin.com/in/santoshkumar-myakala-b3456021/">LinkedIn</a>.</sub>
</div>
