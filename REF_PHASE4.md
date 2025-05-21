# Phase 4: Add Real Data and Endpoints

In Phase 4, we transform a basic FastAPI service into a functional mosquito surveillance API. 
We load real data, store it in a local DuckDB database, and expose meaningful endpoints.

## Prerequisites

Before continuing, ensure:

- You have completed README.md, Phase 1, Phase 2, and Phase 3.
- Your app is running in GKE Autopilot and accessible via external IP.
- Your repo includes app/, requirements.txt, and Dockerfile.
- You have a basic understanding of working with CSV files and FastAPI routes.

## Step 1: Add Sample Data

| File                   | Purpose |
|------------------------|---------|
| `data/`                             | Stores source CSV files |
| `data/san_diego_mosquito_traps.csv` | Sample mosquito trap data |

Example CSV header and data:

```csv
_id,Record ID,City,State,Zip Code,Community,Date Collected,Mosquito Species,Count
1,DEH2016-CVLAB-003207,Vista,CA,92083,Vista,2016-07-31T00:00:00,Culex quinquefasciatus - Southern House Mosquito,4
2,DEH2014-CVLAB-000002,Carlsbad,CA,92008,Carlsbad,2015-03-17T00:00:00,Culex tarsalis - Western Encephalitis Mosquito,15
```

## Step 2: Create a DuckDB Loader & Generate the Database

Step 2.1 Create a script to convert CSV data to DuckDB format.

| File                     | Purpose |
|--------------------------|---------|
| `scripts/load_duckdb.py` | Reads the CSV and saves a DuckDB database |
| `db/mosquito.duckdb`     | Output DuckDB file (can be versioned) |

Step 2.2. Generate the DuckDB database.

- Activate the virtual environment (if not already activated)
- Run the loader script from a terminal in the root project folder:

```shell
python3 scripts/load_duckdb.py
```

The generated DuckDB database is not human-readable. Use queries or Python code to inspect it.
Feature engineering and column cleaning were applied in `load_duckdb.py`  
to produce the simplified and query-friendly [Phase 4 DATA](REF_PHASE4+DATA.md).

## Step 3: Add DuckDB Access Logic and Test the Service Functions

Step 3.1. Add a lightweight database utility module to query DuckDB.

| File            | Purpose |
|-----------------|---------|
| `app/db.py`     | Opens connection, returns records |

Step 3.2. Run the script to test the service functions.

- Activate the virtual environment (if not already activated)
- Run the db script from a terminal in the root project folder:

```shell
python3 app/db.py
```

## Step 4: Add API Endpoints and Test Locally

Step 4.1. Edit `app/main.py` and add routes that return real data. For example:

| Route                          | Purpose                                         |
|-------------------------------|-------------------------------------------------|
| GET /                         | Return API status message                       |
| GET /traps                    | Return up to `{limit}` traps (default: 100)     |
| GET /traps/{trap_id}          | Return a specific trap by ID                    |
| GET /species                  | Return list of distinct mosquito species        |
| GET /species/{species_name}   | Return traps matching the given species         |
| GET /dates?start=...&end=...  | Return traps within a date range (YYYY-MM-DD)   |

Step 4.2 Run and Test the App Locally

Activate .venv if not already activated.
Run the app locally. VS Code will ask if you want to open in the browser, click Yes.
You should see: `{"message":"Mosquito API is alive!"}` or similar.  

```shell
uvicorn app.main:app --reload
```

It will run in the browser at <ttp://127.0.0.1:8000/>.

Step 4.3 Test the API Endpoints

| URL | Description |
|-----|-------------|
| http://127.0.0.1:8000/              | Root endpoint – confirms the API is running |
| http://127.0.0.1:8000/traps         | Returns the first 100 traps |
| http://127.0.0.1:8000/traps?limit=5 | Returns the first 5 traps |
| http://127.0.0.1:8000/traps/1 | Returns the trap with ID 1 |
| http://127.0.0.1:8000/species | Returns the list of distinct species |
| http://127.0.0.1:8000/species/Culex%20quinquefasciatus%20-%20Southern%20House%20Mosquito | Returns traps for the given species |
| http://127.0.0.1:8000/species/INVALID                       | Returns an error with valid species list |
| http://127.0.0.1:8000/dates?start=2016-01-01&end=2016-12-31 | Returns traps within the date range |
| http://127.0.0.1:8000/dates?start=1990-01-01&end=2100-01-01 | Returns error showing valid date range |


## Step 5: Update Dockerfile

Verify Dockerfile copies in the CSV and DuckDB files as needed.
Update Dockerfile:

```text
COPY ./data/ /app/data
COPY ./db/ /app/db
COPY ./app /app/app
COPY requirements.txt .
```

## Step 6: Rebuild and Push

After making changes, rebuild and redeploy.

OPTIONAL: If the docker build command doesn't work, you may need to re-authenticate for both Docker and GKE. Run the following, copy and paste the provided URL into Chrome.
Pick your account and authorize. Copy the authorization code and paste it back into the VS Code terminal to authenticate. 

```shell
gcloud auth application-default login --no-launch-browser
```

1. Rebuild and re-push the image and restart the deployment.
2. OPTIONAL: Delete and re-apply the manifests for a clean start (NOT optional if Kubernetes yaml files change)
3. Restart the deployment to apply the new image
4. OPTIONAL: Describe the service to get more information
5. OPTIONAL: Use pods info to get hash.
6. OPTIONAL: Use hash to view logs. 
7. Check the service. 

```shell
docker build -t us-central1-docker.pkg.dev/elytech-mosquito/mosquito-repo/mosquito-api-ca:latest .
docker push us-central1-docker.pkg.dev/elytech-mosquito/mosquito-repo/mosquito-api-ca:latest

kubectl delete -f k8s/
kubectl apply -f k8s/

kubectl rollout restart deployment mosquito-api

kubectl describe service mosquito-api-service
kubectl get pods
kubectl logs mosquito-api-78c478cfb-t4kfp
```

## Step 7: Verify Deployment

1. Verify the deployment was created.
2. Verify the service was created.
2. Get the external IP address of your service.

```shell
kubectl get deployments
kubectl get services
kubectl get service mosquito-api-service
```

It may take 5-10 minutes to get an EXTERNAL-IP address assigned. 
Once available, visit the external IP address in your browser to verify the API is live. 
You should see a message like:

{"message": "Mosquito API is alive!"}

Visit http://<ExternalIP/>, for example <http://34.118.235.124/>

## Step 8. Test the Deployed API Endpoints

| URL | Description |
|-----|-------------|
| http://34.118.235.124/              | Root endpoint – confirms the API is running |
| http://34.118.235.124/traps         | Returns the first 100 traps |
| http://34.118.235.124/traps?limit=5 | Returns the first 5 traps |
| http://34.118.235.124/traps/1 | Returns the trap with ID 1 |
| http://34.118.235.124/species | Returns the list of distinct species |
| http://34.118.235.124/species/Culex%20quinquefasciatus%20-%20Southern%20House%20Mosquito | Returns traps for the given species |
| http://34.118.235.124/species/INVALID                       | Returns an error with valid species list |
| http://34.118.235.124/dates?start=2016-01-01&end=2016-12-31 | Returns traps within the date range |
| http://34.118.235.124/dates?start=1990-01-01&end=2100-01-01 | Returns error showing valid date range |
