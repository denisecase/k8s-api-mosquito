# Phase 2: Project Initialization

Scaffold and validate the app: set up local project structure and prepare files for development and deployment.
---

## Add Project Files

| File                  | Purpose |
|------------------------|---------|
| `README.md`            | Project description and structure |
| `requirements.txt`     | Standard: Python dependencies |
| `.gitignore`           | Standard: Things to keep out of GitHub |
| `app/main.py`          | FastAPI app entry point |
| `Dockerfile`           | Container build instructions |


## Run App Locally

Activate .venv if not already activated.
Run the app locally. VS Code will ask if you want to open in the browser, click Yes.
You should see: `{"message":"Mosquito API is alive!"}` or similar.  

```shell
source .venv/bin/activate
uvicorn app.main:app --reload
```

By default, the app will run at <http://127.0.0.1:8000/>.

## Build and Test Docker Image

Build and test a Docker image. 
Remember the dot at the end of the first command - it means "this folder right here".

```shell
docker build -t mosquito-api:latest .
docker run -p 8000:8000 mosquito-api:latest
```

By default, the docker app will run at <http://localhost:8000/>.
