# k8s-api-mosquito

## OPTIONAL. On Windows, Open and Update PowerShell (if needed)

We recommend keeping key tools like PowerShell updated to lastest versions. For example:

```PowerShell
winget search Microsoft.PowerShell
winget upgrade --id Microsoft.PowerShell --silent --accept-package-agreements --accept-source-agreements
```

---

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
6. Uninstall all prior WSL Dockder versions

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
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
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

Add your user to the docker group so you don't have to use `sudo` every time:

```shell
sudo usermod -aG docker $USER
```

Exit and restart WSL

```shell
exit
wsl
```

Verify that the installation is successful by running the hello-world image.

```shell
docker version
docker info
docker run hello-world
```

## Clone Project Repo and Open in Code

1. Change directory into ~/Repos.
2. Git clone into ~/Repos folder.
3. Change directory into new k8s-api-mosquito repo folder.
4. Start VS Code in the repo folder.

```shell
cd ~/Repos
git clone https://github.com/denisecase/pro-analytics-01-audio-guides
cd pro-analytics-01-audio-guides
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

## After Making Progress

```shell
git add .
git commit -m "did this"
git push -u origin main
```
