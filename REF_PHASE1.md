# Phase 1: Machine & Cloud Setup

In Phase 1, we configure our Google Cloud setup for deployment. 
Be sure you have completed all the tasks in [README.md](README.md) first.

You will need: 

- A GCP account (https://cloud.google.com).
- A GCP billing account (and link the billing account to your project).
- A GCP project (e.g., elytech-mosquito).

| Task                            | Purpose                                  |
|---------------------------------|------------------------------------------|
| Create GCP account              | Use [https://cloud.google.com](https://cloud.google.com) |
| Create a GCP billing account    | Create a general billing account                  |
| Create GCP project              | e.g. elytech-mosquito                             |
| Enable billing for the project  | Required so the project can use GKE Autopilot     |
| Install gcloud CLI              | See below       |
| Initialize gcloud               | See below       | 
| Install GKE Auth Plugin         | See below       |
| Set project default             | See below       |
| Enable APIs                     | See below       |

##  Install Google Cloud CLI

The `gcloud` CLI is the primary interface for interacting with GCP.

1. IMPORTANT: Change to your home directory (`~`). We do not want to install the Cloud SDK inside the project repo.
2. Download tar.gz file.
3. Extract to google-cloud-sdk/ directory in your current (home) folder. 
4. Run the installer at ./google-cloud-sdk/install.sh
5. Answer either Y or N, then Y, then Enter/Return. 
6. Add the `~/google-cloud-sdk/bin` to your path.
7. Update the environment.

```shell
cd ~
curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-linux-x86_64.tar.gz
tar -xf google-cloud-cli-linux-x86_64.tar.gz
./google-cloud-sdk/install.sh
echo 'export PATH="$HOME/google-cloud-sdk/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

Important: Kill your current terminal and open a new one (e.g., in VS Code Terminal / New Terminal) for the PATH changes to apply. 
Then verify. 

```shell
gcloud version
```

## Initialize Google Cloud CLI

Make Chrome your default browser if you typically sign in to Google via Chrome. 
You'll sign in and it will show you a verification code in your browser. 
Copy the verification code and paste it into your VS Code terminal when asked. 
Then, it will provide a numbered list of all your Google Projects. 
Enter the number of the associated project. 

```shell
gcloud init --no-launch-browser
```

Additional helpful commands (in case you want them later): 

- Run `gcloud --help` to see the Cloud Platform services you can interact with. And run `gcloud help COMMAND` to get help on any gcloud command.
- Run `gcloud topic --help` to learn about advanced features of the CLI like arg files and output formatting
- Run `gcloud cheat-sheet` to see a roster of go-to `gcloud` commands.

##  Install GKE Authentication Plugin

This plugin allows `kubectl` to authenticate with Google Kubernetes Engine (GKE).
The which command below should return something like `/home/yourname/google-cloud-sdk/bin/gke-gcloud-auth-plugin`.

```shell
gcloud components install gke-gcloud-auth-plugin
source ~/.bashrc
which gke-gcloud-auth-plugin
```

## Authenticate

```shell
gcloud auth application-default login --no-browser
```

Copy the URL to your browser. Choose an account. Allow. 
You should see a page saying `You are now authenticated with the gcloud CLI!`

## Enable Required GCP APIs

Enable Kubernetes Engine and Docker image hosting via Artifact Registry.
You must have created a GCP billing account, a GCP project, and associated your billing account with your GCP project first. 

```shell
gcloud services enable container.googleapis.com
gcloud services enable artifactregistry.googleapis.com
```

## Configure kubectl to use Google Cloud credentials

```shell
gcloud config set container/use_application_default_credentials true
```

Close the terminal. 

From the VS Code menu, use Terminal / New Terminal and activate .venv with the new environment (if needed.) 

```shell
source .venv/bin/activate
```