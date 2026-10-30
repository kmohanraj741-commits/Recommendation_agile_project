# Recommendation System – 24MIS0464

Three Flask versions:
- V1: Show List – display recommendation items.
- V2: Filter – filter by Electronics, Fashion, or Home.
- V3: Sort – sort by name, price, or recommendation score.

## Folder structure
Each `v1`, `v2`, and `v3` folder contains `app.py`, `templates/index.html`,
`requirements.txt`, `Dockerfile`, and `k8s-deployment.yaml`.
The root contains `Jenkinsfile`, `.gitignore`, and this README.

## Run locally
Install Python 3.10 or later. In a terminal from the project root:

V1:
    cd v1
    python -m pip install -r requirements.txt
    python app.py
Open http://localhost:5000

Stop with Ctrl+C, then V2:
    cd ..\v2
    python -m pip install -r requirements.txt
    python app.py
Open http://localhost:5000

Stop with Ctrl+C, then V3:
    cd ..\v3
    python -m pip install -r requirements.txt
    python app.py
Open http://localhost:5000

Only run one version at a time locally because all use port 5000.

## Docker images
Create a DockerHub repository named `recommendation-system`, then run from the root
(replace YOUR_DOCKERHUB_USERNAME):

    docker build -t YOUR_DOCKERHUB_USERNAME/recommendation-system:v1 ./v1
    docker push YOUR_DOCKERHUB_USERNAME/recommendation-system:v1
    docker build -t YOUR_DOCKERHUB_USERNAME/recommendation-system:v2 ./v2
    docker push YOUR_DOCKERHUB_USERNAME/recommendation-system:v2
    docker build -t YOUR_DOCKERHUB_USERNAME/recommendation-system:v3 ./v3
    docker push YOUR_DOCKERHUB_USERNAME/recommendation-system:v3

## Kubernetes
Enable Kubernetes in Docker Desktop and check `kubectl get nodes`.
Replace YOUR_DOCKERHUB_USERNAME in each manifest, then run:

    kubectl apply -f v1/k8s-deployment.yaml
    kubectl apply -f v2/k8s-deployment.yaml
    kubectl apply -f v3/k8s-deployment.yaml

Check `kubectl get deployments`, `kubectl get pods`, and `kubectl get services`.
NodePorts: V1 http://localhost:30001, V2 http://localhost:30002, V3 http://localhost:30003.

## Jenkins
This Jenkinsfile is for a Windows Jenkins agent (uses `bat`).
Create three Pipeline jobs using Pipeline script from SCM and the root `Jenkinsfile`:

| Job name | Git branch |
| Recommendation-System-V1 | */v1 |
| Recommendation-System-V2 | */v2 |
| Recommendation-System-V3 | */v3 |

Use `- none -` for GitHub credentials if the repository is public.
Add DockerHub credential:
- Kind: Username with password
- ID: `dockerhub-recommendation`
- Username: DockerHub username
- Password: DockerHub access token

Add kubeconfig as a Secret file credential with ID `recommendation-kubeconfig`.
The Jenkins agent needs Git, Python, Docker CLI, and kubectl available in PATH, plus access to Docker Desktop and Kubernetes.
