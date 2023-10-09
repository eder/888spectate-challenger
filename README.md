[![CircleCI](https://dl.circleci.com/status-badge/img/gh/eder/888spectate-challenger/tree/main.svg?style=svg&circle-token=63d47442a2880587f1fa5a9c1818e1a38c40f2f9)](https://dl.circleci.com/status-badge/redirect/gh/eder/888spectate-challenger/tree/main)




# Sports Management System Documentation

## Overview

System is an application developed using the FastAPI framework and PostgreSQL database. The project allows for the management and querying of sports, associated events, and selections. Built following best development practices and the SOLID principles, this system is designed to be robust and easily extensible.


## System Design 
<img width="768" alt="Screenshot 2023-10-09 at 04 16 14" src="https://github.com/eder/888spectate-challenger/assets/28600/ef372138-69ae-4e56-b193-2d29170c8a41">

## Requirements

-   [docker](https://docs.docker.com/engine/installation/#supported-platforms)

## Starting 
In the project root directory, run the command
```bash
$ make up
```

### Tests

# Run Tests in Docker
```
$ make test
```
<img width="1515" alt="Screenshot 2023-10-09 at 04 10 37" src="https://github.com/eder/888spectate-challenger/assets/28600/e9828b5b-62f5-4adc-b2b8-6e979ef24bca">


## Project Structure  

<img width="1016" alt="Screenshot 2023-10-09 at 03 49 17" src="https://github.com/eder/888spectate-challenger/assets/28600/8ff8cd5f-4af5-47cf-a2b8-f94be55c4ec9">

## Swagger
- The `swagger` all APIs.
- Visit `http://0.0.0.0:8000/docs#/ to access the playground
  <img width="1674" alt="Screenshot 2023-10-09 at 03 58 17" src="https://github.com/eder/888spectate-challenger/assets/28600/d13b9f2e-9a6a-42db-927d-9ca96a4a3bc4">
