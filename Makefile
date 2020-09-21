FAUSTO_CONTAINER=faustodsm/cdn-cc:latest

all: help

run-app: ## Runs the microservice in localhost:8000
	@echo "+ $@"
	@docker run --rm -d -p 5000:5000 ${FAUSTO_CONTAINER}

bytes-for-hits: ## Throws a GET request at http://localhost:5000/report/bytes/hit 
	@echo "+ $@"
	@curl http://localhost:5000/report/bytes/hit

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
