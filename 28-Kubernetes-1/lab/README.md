# Installation local kubernetes cluster

## Install and configuring minikube

### Windows host
If you are working on Windows or on a Virtual Machine on a Windows computer install minikube on Windows: 

1. Install Virtualbox from [here](https://www.virtualbox.org/)
2. Install Chocolatey from [here](https://chocolatey.org/install) with administrative PowerShell
2. Install [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/#install-on-windows-using-chocolatey-or-scoop) with administrative Command Prompt using Chocolatey
3. Install [minikube](https://kubernetes.io/docs/tasks/tools/install-minikube/) with administrative Command Prompt using Chocolatey
4. Run minikube:
```
minikube start --driver=virtualbox
```

### MacOS
If you are using MacOS, you can also install minikube.
If you already installed docker, you do not have to install virtualbox, as docker on Mac installs its own hypervisor hyperkit (that works better than virtualbox).

1. Install [minikube](https://kubernetes.io/docs/tasks/tools/install-minikube/)
2. Install [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl)
3. Run minikube:
```
minikube start --driver=hyperkit
```

### Linux host (Ubuntu)

If you are using Ubuntu, you can also install minikube. 
   
1. Install Virtualbox from [here](https://www.virtualbox.org/)
2. Install [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/#install-using-native-package-management)
3. Install [minikube](https://kubernetes.io/docs/tasks/tools/install-minikube/) from [here](https://github.com/kubernetes/minikube/releases/download/v1.11.0/minikube_latest_amd64.deb)
4. Run minikube:
```
minikube start --driver=virtualbox
```

# Kubernetes basics

First thing as usual, check the version you are running:

```
kubectl version
```

Check if and on which IP-address our cluster is running:

```
kubectl cluster-info
```

For Windows 10, open a git Bash and run the commands with Linux syntax.

Enable autocomplete as explained [here](https://kubernetes.io/docs/reference/kubectl/cheatsheet/#kubectl-autocomplete) by running the following:
```
source <(kubectl completion bash) # setup autocomplete in bash into the current shell, bash-completion package should be installed first.
echo "source <(kubectl completion bash)" >> ~/.bashrc # add autocomplete permanently to your bash shell.
```

# Excercise 1

Deploy Flask API.

See subfolder and file `exercise1/exercise1.md`

# Excercise 2

Deploy message-app.

See subfolder and file `exercise2/exercise2.md`
