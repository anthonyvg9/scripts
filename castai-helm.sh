CASTAI_API_URL="${CASTAI_API_URL:-https://api.cast.ai}"


echo "Adding helm repositories for CAST AI required charts."
helm repo add castai-helm https://castai.github.io/helm-charts
if [[ $INSTALL_NVIDIA_DEVICE_PLUGIN = "true" ]]; then
  helm repo add nvdp https://nvidia.github.io/k8s-device-plugin
fi
helm repo update
echo "Finished adding helm charts repositories."

echo "Installing castai-cluster-controller."
helm upgrade -i cluster-controller castai-helm/castai-cluster-controller -n castai-agent \
  --set castai.apiKey=$CASTAI_API_TOKEN \
  --set castai.apiURL=$CASTAI_API_URL \
  --set castai.clusterID=$CASTAI_CLUSTER_ID
echo "Finished installing castai-cluster-controller."

echo "Installing castai-spot-handler."
helm upgrade -i castai-spot-handler castai-helm/castai-spot-handler -n castai-agent \
  --set castai.apiURL=$CASTAI_API_URL \
  --set castai.clusterID=$CASTAI_CLUSTER_ID \
  --set castai.provider=aws
echo "Finished installing castai-spot-handler."

echo "Installing castai-evictor."
helm upgrade -i castai-evictor castai-helm/castai-evictor -n castai-agent --set replicaCount=0
echo "Finished installing castai-evictor."

if [[ $INSTALL_NVIDIA_DEVICE_PLUGIN = "true" ]]; then
  echo "Installing NVIDIA device plugin required for GPU support."
  helm upgrade -i nvdp nvdp/nvidia-device-plugin -n castai-agent \
    --set-string nodeSelector."nvidia\.com/gpu"=true \
    --set \
tolerations[0].key=CriticalAddonsOnly,tolerations[0].operator=Exists,\
tolerations[1].effect=NoSchedule,tolerations[1].key="nvidia\.com/gpu",tolerations[1].operator=Exists,\
tolerations[2].key="scheduling\.cast\.ai/spot",tolerations[2].operator=Exists,\
tolerations[3].key="scheduling\.cast\.ai/scoped-autoscaler",tolerations[3].operator=Exists,\
tolerations[4].key="scheduling\.cast\.ai/node-template",tolerations[4].operator=Exists
  echo "Finished installing NVIDIA device plugin."
fi

if [[ $INSTALL_KVISOR = "true" ]]; then
  helm upgrade -i castai-kvisor castai-helm/castai-kvisor -n castai-agent \
    --set castai.apiURL=$CASTAI_API_URL \
    --set castai.apiKey=$CASTAI_API_TOKEN \
    --set castai.clusterID=$CASTAI_CLUSTER_ID \
    --set structuredConfig.provider=eks
  echo "Finished installing castai-kvisor."
fi
