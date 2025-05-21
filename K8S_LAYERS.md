# Kubernetes: Layered Mental Model

- [Learn Kubernetes Basics](https://kubernetes.io/docs/tutorials/kubernetes-basics/) (Official interactive tutorial for the **Kubernetes cluster orchestration system**)

## Layer 1: Cluster Level

| Term            | Description                                                                 |
|-----------------|-----------------------------------------------------------------------------|
| Cluster         | A collection of machines (nodes) managed as a single unit by Kubernetes.   |
| Control Plane   | Manages the cluster: schedules pods, handles updates, monitors health.     |
| GKE             | Google Kubernetes Engine – a *hosted* Kubernetes service by Google Cloud.   |
| Minikube        | A *local*, single-node Kubernetes cluster for development/testing.         |

> This layer is the computing environment. GKE is remote; Minikube is local.

The Minikube CLI and Kubernetes CLI (kubectl) provide basic bootstrapping operations for working with a cluster, including start, stop, status, and delete.

---

## Layer 2: Node Level

| Term        | Description                                                    |
|-------------|----------------------------------------------------------------|
| Node        | A machine (VM or physical) in the cluster that runs workloads. |
| Kubelet     | An agent on each node that communicates with the control plane.|

> This is the execution layer – the workloads run on nodes.

---

## Layer 3: Pod Level

| Term        | Description                                                             |
|-------------|-------------------------------------------------------------------------|
| Pod         | The *smallest deployable unit* in Kubernetes. Runs one or more containers. |
| Container   | An application, typically built from a Dockerfile, runs inside a pod. |

> This is the "what actually runs" layer. We write containers, Kubernetes runs pods.

---

## Layer 4: Application Management

| Term                       | Description                                                             |
|----------------------------|-------------------------------------------------------------------------|
| Deployment                 | Defines desired state (e.g., number of pods, update strategy).          |
| Service                    | Exposes the pods inside/outside the cluster (via ClusterIP, NodePort, or LoadBalancer). |
| Ingress                    | Optional. Smart HTTP routing (e.g., based on domain/path).              |
| Horizontal Pod Autoscaler  | Scales pods up/down based on CPU/memory or custom metrics.              |

> This layer controls how apps behave and scale over time.

---

## Layer 5: Configuration and Storage

| Term        | Description                                                              |
|-------------|--------------------------------------------------------------------------|
| ConfigMap   | Store environment variables and config files (non-sensitive).            |
| Secret      | Store passwords, keys, or sensitive config values.                       |
| Volume      | Attach persistent or ephemeral storage to pods.                          |

> This layer separates configuration/data from code.

---

## Example: Kubernetes YAML File Organization

| File/Filename             | Purpose                                             |
|---------------------------|-----------------------------------------------------|
| `k8s/deployment.yaml`     | Defines how the app is deployed                    |
| `k8s/service.yaml`        | Defines how the app is exposed                     |
| `k8s/configmap.yaml`      | Application-level configuration                     |
| `k8s/secret.yaml`         | Sensitive values (e.g., passwords, tokens)          |
| `k8s/ingress.yaml`        | Domain-based routing (optional)                     |
| `k8s/hpa.yaml`            | Autoscaling rules (optional)                        |

Typically, yaml files are organized into folders like `k8s/` or environment-specific folders like:

```
k8s/
├── base/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   └── secret.yaml
├── overlays/
│   ├── dev/
│   │   └── kustomization.yaml
│   ├── staging/
│   │   └── kustomization.yaml
│   └── prod/
│       └── kustomization.yaml
```

---

## Interchangeable Components and Tools

| Concept             | Alternatives / Notes                                                       |
|---------------------|----------------------------------------------------------------------------|
| Container Engine    | Docker, **containerd**, CRI-O (Kubernetes supports anything with CRI).         |
| Cluster Platform    | Minikube (local), GKE, AKS (Azure), EKS (AWS), kind, k3s (lightweight).    |
| YAML Tools          | `kubectl apply`, Helm (templating), Kustomize (patching), Skaffold (build + deploy). |

