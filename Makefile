FAUSTO_CONTAINER=faustodsm/cdn-cc:latest

all: help

run-app: ## Runs the microservice in localhost:5000 on Docker on your localhost (no minikube, for that run 'make minikube-deploy')
	@echo "+ $@"
	@docker run --rm -d -p 5000:5000 ${FAUSTO_CONTAINER}

bytes-for-hits: ## Throws a GET request at http://localhost:5000/report/bytes/hit 
	@echo "+ $@"
	@echo "+ curl http://localhost:5000/report/bytes/hit"
	@curl http://localhost:5000/report/bytes/hit

minikube-deploy: ## Deploys microservice in minikube 
	@echo "+ $@"
	@kubectl apply -f cdn-deployment.yml 
	@kubectl expose deployment  fausto-cdn-deploy --type=LoadBalancer --name=fausto-cdn-service
	@echo "***NOW OPEN ANOTHER TERMINAL OR A BROWSER AND TEST THE SERVICE, E.G. curl http://<IP and port described in the table below>/report/bytes/hit ***"
	@minikube service fausto-cdn-service

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
