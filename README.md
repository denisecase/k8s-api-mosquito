# k8s-api-mosquito

A public-health data microservice deployed to GKE Autopilot using FastAPI, Docker, and Kubernetes.

[![Deploy to GKE](https://img.shields.io/badge/deploy-GKE-green)](https://console.cloud.google.com/)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org/downloads/release/python-3110/)

## Deployed API Endpoints

| URL | Description |
|-----|-------------|
| http://34.122.47.29/              | Root endpoint – confirms the API is running |
| http://34.122.47.29/traps         | Returns the first 100 traps |
| http://34.122.47.29/traps?limit=5 | Returns the first 5 traps |
| http://34.122.47.29/traps/1 | Returns the trap with ID 1 |
| http://34.122.47.29/species | Returns the list of distinct species |
| http://34.122.47.29/species/Culex%20quinquefasciatus%20-%20Southern%20House%20Mosquito | Returns traps for the given species |
| http://34.122.47.29/species/INVALID                       | Returns an error with valid species list |
| http://34.122.47.29/dates?start=2016-01-01&end=2016-12-31 | Returns traps within the date range |
| http://34.122.47.29/dates?start=1990-01-01&end=2100-01-01 | Returns error showing valid date range |


About the data:

- MIN_DATE_COLLECTED=2015-01-07
- MAX_DATE_COLLECTED=2018-08-28
- Fetched 11925 traps
- See [Phase 4 DATA](REF_PHASE4+DATA.md) for a list of species

## Local Machine Setup

For professional Python, Git, and VS Code setup and workflow, see [pro-analytics-01](https://github.com/denisecase/pro-analytics-01). 

We need to install some additional tools to support containerization and Kubernetes deployments.

| Tool             | Purpose                             | Notes |
|------------------|-------------------------------------|----------------|
| `Docker`         | Build and run containers            | Use Docker Engine (avoid Docker Desktop) |
| `kubectl`        | Command-line interface to Kubernetes| [Install](https://kubernetes.io/docs/tasks/tools/) |
| `gh`             | GitHub CLI                          | Helpful for repo management |

## OPTIONAL. On Windows, Open and Update PowerShell (if needed)

We recommend keeping key tools like PowerShell updated to lastest versions. For example:

```PowerShell
winget search Microsoft.PowerShell
winget upgrade --id Microsoft.PowerShell --silent --accept-package-agreements --accept-source-agreements
```

## On Windows Machines Use WSL

Use Windows Subsystem for Linux. Update (if needed) and launch WSL. 

```powershell
wsl --update
wsl
```

## Check Ubuntu version - use Ubuntu 22.04+ if possible.

```shell
lsb_release -a
```

## Tool Installation (Python 3.11)

1. Update package lists.
2. Install Python 3.11 and Development Tools.
3. Install helpful tools: curl, unzip
4. Install GitHub CLI (Command Line Interface)
5. Install Kubernetes
6. Uninstall all prior WSL Docker versions

```shell
sudo apt-get update -y
sudo apt-get install -y python3.11 python3.11-venv python3.11-dev build-essential
sudo apt-get install -y git curl unzip
sudo apt-get install -y gh
sudo apt-get install -y kubectl
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
```

Add Docker's official GPG key:

```shell
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings

curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo tee /usr/share/keyrings/cloud.google.gpg > /dev/null

sudo chmod a+r /usr/share/keyrings/cloud.google.gpg
```

Add the repository to Apt sources:

```shell
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

Install Docker for WSL

```shell
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

Add your user to the docker group so we don't need `sudo` every time:

```shell
sudo usermod -aG docker $USER
```

Exit and restart WSL

```shell
exit
wsl
```

Verify that the installation is successful and run the hello-world image.

```shell
docker version
docker info
docker run hello-world
```

## Clone Project Repo and Open in Code

1. Change directory into ~/Repos.
2. Git clone into ~/Repos folder.
3. Change directory into new repo folder.
4. Start VS Code in the repo folder.

```shell
cd ~/Repos
git clone https://github.com/denisecase/k8s-api-mosquito
cd k8s-api-mosquito
code .
```


## Manage Python Virtual Environment: Repeatable Setup

Use VS Code menu Terminal / New Terminal to run the following commands.
Click yes to use the new .venv after creating it. 

1. Create a new virtual environment using Python 3.11.
2. Activate the new virtual environment.
3. Install and upgrade key packages.
4. Install packages from requirements.txt.
5. Run pip check.
6. Save installed versions to req-installed.txt.


```shell
python3.11 -m venv .venv
source .venv/bin/activate

python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install -r requirements.txt --timeout 300 --progress-bar on --no-cache-dir

python3 -m pip check
python3 -m pip list > req-installed.txt
```



## Before Making Changes

```shell
git pull
```

## After Making Progress

```shell
git add .
git commit -m "did this"
git push -u origin main
```

## Project Phases

This project is organized into development phases:

- [Phase 1: Machine & Cloud Setup](./ref_phase1.md)
- [Phase 2: Project Initialization](./ref_phase2.md)
- [Phase 3: Vertical Slice Deployment](./ref_phase3.md)

## Data Set Links

- [CivicData](https://www.civicdata.com/)
- [San Diego Mosquito Traps Data](https://www.civicdata.com/dataset/county-of-san-diego-deh-routine-mosquito-surveillance-traps/resource/2c88678b-39b0-48a5-b071-d526d994fc42)

Cite: Routine Mosquito Surveillance Traps

> URL: https://www.civicdata.com/api/3/action/datastore_search?resource_id=2c88678b-39b0-48a5-b071-d526d994fc42

> This dataset provides information from approximately 130 active routine surveillance traps set on a weekly or bi-weekly basis for adult mosquitos across San Diego County for the years **2015-current**. After collection, an ecologist counts and classifies the mosquitos. Mosquitos of the appropriate species are then tested in a laboratory for viruses that can be transmitted to people. This data is managed by the San Diego County Vector Control Program and is extracted from the land use and environment database, Accela. This dataset is intended for public access, use, and education. For a description of this data, see Routine Mosquito Surveillance Trap metadata. If additional information is needed please see our [Public Records Request webpage] (https://www.sandiegocounty.gov/content/sdc/deh/doing_business/records.html).

> Note: San Diego County’s Vector Control Program strives to provide complete and accurate data, however, it does not guarantee, either expressed or implied, the accuracy, completeness, or timeliness of the information. The Department of Environmental Health will not be responsible for any error or omission, or for the use of, or the results obtained from the use of this information.

> Metadata Created Data: July 2, 2018