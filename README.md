# CDN code challenge 
## A Python/Flask microservice for reporting on CDN customer logs
<details>
  <summary><strong>Table of Contents</strong> </summary>

- [Features](#Features)
- [Project description](#Project-description)
- [Instructions](#Instructions)

### Features
 - Written in Python 3.8
 - Powered by Flask
 - GitHub Actions for CI/CD
 - CI includes unit tests and code style chekcing with Flake
 - Continous deployment with Docker image creation and hosting in DockerHub. 
 - Microservice can also be deployed locally with Minikube
 - API documentation with Swagger
### Project description
It is a web service deployed as a microservice. It provides the means to be deployed locally on Docker or on top of a single node Minikube cluster. Its main purpose is to generate some small reports on CDN logs from customers. When it receives a request for a report, before producing it, it imports the log file into a local `sqlite` DB and then generates and returns the report. The reason for this design is that storing the log in a DB makes it super easy to generate the reports by just using simple SQL queries. 
This app lacks any user interface, all the reports are returned in JSON.
The reports are serviced via two REST APIs:
|Endpoint| Description |
|--|--|
|[http://localhost:5000​/report​/bytes​/{cdn_request_result_type: hit or miss}](http://localhost:5000%E2%80%8B/report%E2%80%8B/bytes%E2%80%8B/%7Bcdn_request_result_type:%20hit%20or%20miss%7D) | Returns the number of bytes for a CDN hit result |
|[http://localhost:5000/report/success_vs_fails](http://localhost:5000/report/success_vs_fails) | Returns the number of successful requests vs number of failed requests |
For more information about the APIs, start the service and go to the [API documentation](http://127.0.0.1:5000/api/docs/).
### Instructions
After cloning the repository, just run `make help` on the root directory of the project: `CDN-cc`. That explains all the commands that you can use to test the application.
```
$ make help
Before testing make sure you run 'make run-app' to start the microservice
bytes-for-hits                 Throws a GET request at http://localhost:5000/report/bytes/hit 
bytes-for-miss                 Throws a GET request at http://localhost:5000/report/bytes/miss
minikube-deploy                Deploys microservice in Minikube 
run-app                        Runs the microservice in localhost:5000 on Docker on your localhost (no Minikube, for that run 'make minikube-deploy')
success-vs-fails               Throws a GET request at http://localhost:5000/report/success_vs_fails
```
Just run `make <command>` to test the app. Example:
```
$ make bytes-for-hits
+ bytes-for-hits
+ curl http://localhost:5000/report/bytes/hit
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    73  100    73    0     0    960      0 --:--:-- --:--:-- --:--:--   960
{
    "total_bytes": 1865568139,
    "x-edge-response-result-type": "Hit"
}
```
Also you may want to run the test suite by executing `pytest` in the root directory of the project. 
