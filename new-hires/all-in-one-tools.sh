# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install iTerm2
brew install --cask iterm2

# Install Docker Desktop
brew install --cask docker

# Install kubectl
brew install kubectl

# Install minikube
brew install minikube

# Install Terraform
brew install terraform

# Configure Vim for YAML editing
echo "syntax on" >> ~/.vimrc
echo "filetype plugin indent on" >> ~/.vimrc

# Install krew
(
  set -x; cd "$(mktemp -d)" &&
  curl -fsSLO "https://github.com/kubernetes-sigs/krew/releases/latest/download/krew.tar.gz" &&
  tar zxvf krew.tar.gz &&
  KREW=./krew-"$(uname | tr '[:upper:]' '[:lower:]')_amd64" &&
  "$KREW" install krew
)

# Install kubectl node-shell plugin
kubectl krew install node-shell

# Install ktop
kubectl krew install ktop

# Install tmux
brew install tmux

# Install Azure CLI
brew install azure-cli

# Install AWS CLI
brew install awscli

# Install eksctl
brew tap weaveworks/tap
brew install weaveworks/tap/eksctl

# Install Google Cloud SDK
brew install --cask google-cloud-sdk

# Install openshift-cli
brew install openshift-cli

