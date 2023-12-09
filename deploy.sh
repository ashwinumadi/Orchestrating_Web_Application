kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml
kubectl apply -f deploy_app.yaml
kubectl apply -f deploy_service.yaml
kubectl apply -f deploy_backend.yml
kubectl apply -f deploy_service_backend.yaml
kubectl apply -f ingress.yml
kubectl apply -f ingress_backend.yml