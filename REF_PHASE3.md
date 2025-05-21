# Phase 3: Vertical Slice Deployment

Implement a minimal API, package it into a container, and deploy it using Kubernetes on Google Kubernetes Engine (GKE) Autopilot.

## Prerequisites

Before continuing, ensure:

- You have completed README.md, Phase 1, and Phase 2.
- Your FastAPI app builds and runs locally.
- You have authenticated with GCP (`gcloud auth application-default login`).
- Your Docker image is ready to be tagged and pushed.

## Step 1: Add Kubernetes Deployment Files

| File                   | Purpose |
|------------------------|---------|
| `k8s/deployment.yaml`  | Defines how the app runs in Kubernetes |
| `k8s/service.yaml`     | Exposes the app to the cluster (or internet) |


## Step 2: Build and Tag Docker Image

Build and tag your Docker image for Artifact Registry given PROJECT-ID=elytech-mosquito and REPO-ID=mosquito-repo.

```shell
PROJECT_ID=elytech-mosquito
REPO_ID=mosquito-repo
docker build -t us-central1-docker.pkg.dev/$PROJECT_ID/$REPO_ID/mosquito-api-ca:latest .
```

## Step 3: Push Image to Artifact Registry

```shell
docker push us-central1-docker.pkg.dev/$PROJECT_ID/$REPO_ID/mosquito-api-ca:latest
```

## Step 4: Update k8s/deployment.yaml

Open `k8s/deployment.yaml` and update the container image to match the one pushed.

```yaml
image: us-central1-docker.pkg.dev/elytech-mosquito/mosquito-repo/mosquito-api-ca:latest
```

## Step 5: Create a GKE Autopilot Cluster

```shell
gcloud container clusters create-auto mosquito-cluster \
  --region us-central1 \
  --project elytech-mosquito
```

## Step 6: Get Your GKE Cluster Name

Get your cluster name:

```shell
gcloud container clusters list --region us-central1 --project elytech-mosquito
```

This will return a table. The value under NAME is your cluster name. 
You will use `CLUSTER_NAME` in the command in the next step. 

## Step 7: Connect kubectl to Your GKE Cluster

Use `CLUSTER_NAME` in the following command to connect your Kubernetes CLI to your GKE cluster.

```bash
gcloud container clusters get-credentials CLUSTER_NAME \
  --region us-central1 \
  --project elytech-mosquito
```

For example:

```bash
gcloud container clusters get-credentials mosquito-cluster \
  --region us-central1 \
  --project elytech-mosquito
```

## Step 8. Apply Kubernetes manifests to GKE

If needed, re-authenticate with: `gcloud auth application-default login --no-browser` as we did before.

Then apply your deployment and service definitions: `kubectl apply -f k8s/`

## Step 9: Verify Deployment

Check that your deployment and service were created:

```shell
kubectl get deployments
kubectl get services
```

To get the external IP address of your service:

```shell
kubectl get service mosquito-api-service
```

It may take a few minutes to get an EXTERNAL-IP address assigned. 
Once available, visit the external IP address in your browser to verify the API is live. 
You should see a message like:

{"message": "Mosquito API is alive!"}
