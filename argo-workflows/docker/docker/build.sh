cd ./src

eval $(minikube docker-env)
docker build -t nasa-hsi-argo:latest .

cd ~-