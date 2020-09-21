FAUSTO_IMAGE=faustodsm/cdn-cc:latest

all: help

run-app: ## Runs the microservice in localhost:5000 on Docker on your localhost (no Minikube, for that run 'make minikube-deploy')
	@echo "+ $@"
	@docker run --rm -d -p 5000:5000 ${FAUSTO_IMAGE}

bytes-for-hits: ## Throws a GET request at http://localhost:5000/report/bytes/hit 
	@echo "+ $@"
	@echo "+ curl http://localhost:5000/report/bytes/hit"
	@curl http://localhost:5000/report/bytes/hit | python -m json.tool

bytes-for-miss: ## Throws a GET request at http://localhost:5000/report/bytes/miss
	@echo "+ $@"
	@echo "+ curl http://localhost:5000/report/bytes/miss"
	@curl http://localhost:5000/report/bytes/miss | python -m json.tool

success-vs-fails: ## Throws a GET request at http://localhost:5000/report/success_vs_fails
	@echo "+ $@"
	@echo "+ curl http://localhost:5000/report/success_vs_fails"
	@curl http://localhost:5000/report/success_vs_fails | python -m json.tool

minikube-deploy: ## Deploys microservice in Minikube 
	@echo "+ $@"
	@kubectl apply -f cdn-deployment.yml 
	@kubectl expose deployment  fausto-cdn-deploy --type=LoadBalancer --name=fausto-cdn-service
	@echo "***NOW OPEN ANOTHER TERMINAL OR A BROWSER AND TEST THE SERVICE, E.G. curl http://<IP and port described in the table below>/report/bytes/hit ***"
	@minikube service fausto-cdn-service

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
