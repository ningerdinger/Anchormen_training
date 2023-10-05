# Helm Lab

## Install minikube

1. Install Virtualbox from [here](https://www.virtualbox.org/)
2. Install kubectl from [here](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
3. Install Minikube from [here](https://github.com/kubernetes/minikube)

## Install helm
For windows users, you can install helm using chocolatey (see [here](https://helm.sh/docs/using_helm/)):
```
%% Open a command line with administrative rights
%% If chocolatey is not installed, uncomment the following line:
%% @"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
%% If minikube is not installed, uncomment the following line:
%% choco install minikube
choco install kubernetes-helm
exit
```

** From now on, Windows 10 users should open a git Bash AS ADMINISTRATOR and run the commands with Linux syntax. **

For linux users, you can install helm using Snap (see [here](https://helm.sh/docs/using_helm/)):

```
curl https://baltocdn.com/helm/signing.asc | sudo apt-key add -
sudo apt-get install apt-transport-https --yes
echo "deb https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
sudo apt-get update
sudo apt-get -y install helm
```

For macOS users, you can install helm using Homebrew (see [here](https://helm.sh/docs/using_helm/)):

```
brew install kubernetes-helm
```

## Check that helm is properly installed.
Run the following:

```
# If minikube is not started, uncomment and run the following line:
# minikube start --driver=virtualbox
helm version 
```
Helm should be installed.

## Auto-completion.
Run the following:

```
# setup autocomplete in bash into the current shell, bash-completion package should be installed first.
source <(helm completion bash) 
# add autocomplete permanently to your bash shell.
echo "source <(helm completion bash)" >> ~/.bashrc 

```

## Update and add repositories in helm
A new repository named [Helm Hub](https://hub.helm.sh/) has been created similar to docker hub but for helm:

```
helm search hub prometheus
```

[Bitnami](https://bitnami.com/) has a library for helm charts as well, which might be interesting. To add a new repository to helm, run the following:

```
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
```

To search for a chart, for example the prometheus-operator, just run the following

```
helm search repo prometheus
```

## Install a chart

We will install nginx from the bitnami repository, see [here](https://github.com/bitnami/charts/tree/master/bitnami/nginx)

If we are only interested in installing the repository, the following code should be run (DO NOT RUN IT):

```
# helm install bitnami/nginx o
# If some parameters should be changed, add them with the --set argument, for example
# helm install bitnami/nginx --set imagePullPolicy=Always 
```

However, we usually want to make some changes. To fetch the repository, but not install it, run:

```
cd  ~/Documents # Or any other folder
mkdir mynginx
cd mynginx
helm fetch --untar bitnami/nginx
```

The previous command will also uncompress the repository, although it is not needed for helm to work.


To install the repository, run the following:

```
cd nginx
helm install mynginx .
```

To check the installation procedure, run:

``` 
kubectl get pods -w
```

Once installed, run:

```
kubectl get svc
```

and 

```
minikube service mynginx
```
It should return the nginx welcome page.

## Update a chart and rollback

1. Change version in Chart.yaml file to a superior one, for example

``` 
version: 9.3.1
```
2. Open the values.yaml file and edit server block to:

``` 
serverBlock: |-
  # example PHP-FPM server block
  server {
    listen 8080;
    root /app;
    location / {
      add_header Content-Type text/plain; # Prevents download
      return 200 "hello!";
    }
  }
```

Check the release name with the following command:

```
helm ls
```

Upgrade the helm chart as follows:

```
helm upgrade mynginx .
```

Check the history of the release with:

```
helm status mynginx
helm history mynginx
```

Image that you don't want the new version. Just roll it back using the following command:

```
helm rollback mynginx 
```

# Uninstall and delete a release

The following command removes all the components installed in Kubernetes and deletes the release. 

```
helm uninstall mynginx 
```

# Use a github repository to track changes and share releases

By running the following command, a compressed version of the release is created to be shared:

```
cd ..
helm package nginx
```

To generate an index file based on the charts found, run:

```
helm repo index .
```

Create a new github repository called, for example, helm-test  **WITHOUT README** as explained [here](https://docs.github.com/en/github/getting-started-with-github/quickstart/create-a-repo)

Then, add, commit and push the files to github:

```
git init
git remote add origin <REPO_URL>
git checkout -b gh-pages
git add index.yaml nginx-9.3.1.tgz
git commit -m "First commit"
git push --set-upstream origin gh-pages
```

To add a repository to helm, run the following:

```
helm repo add myrepo https://<ningerdinger>.github.io/helm-test
helm repo update
```

Check with 

```
helm repo list
```
Search for the new nginx chart added by:

```
helm search repo nginx
```

and install it:

```
helm install nginx-from-repo myrepo/nginx
```

Check the installation using:

```
helm ls
```
Remove the release by running the following command:
```
helm uninstall nginx-from-repo 
```

## Exercise, try to install prometheus in minikube from [here](https://github.com/prometheus-community/helm-charts)
