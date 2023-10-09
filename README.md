[![CircleCI](https://dl.circleci.com/status-badge/img/gh/eder/888spectate-challenger/tree/main.svg?style=svg&circle-token=63d47442a2880587f1fa5a9c1818e1a38c40f2f9)](https://dl.circleci.com/status-badge/redirect/gh/eder/888spectate-challenger/tree/main)

## Find internal nodes
Let's assume we have a generic tree composed of consecutive integers (so if there is a 6 all numbers starting from and including 0 up to it also need to exist on the tree), such as follows:

[code-challenger](https://github.com/eder/888spectate-challenger/tree/main/code-challenger)

# Sports Management System Documentation

## Overview

System is an application developed using the FastAPI framework and PostgreSQL database. The project allows for the management and querying of sports, associated events, and selections. Built following best development practices and the SOLID principles, this system is designed to be robust and easily extensible.


## System Design 
<img width="768" alt="Screenshot 2023-10-09 at 04 16 14" src="https://github.com/eder/888spectate-challenger/assets/28600/242ee079-2dda-4894-bdb2-8fc3864a39d1">


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
<img width="1515" alt="Screenshot 2023-10-09 at 04 10 37" src="https://github.com/eder/888spectate-challenger/assets/28600/49eef4a1-8c97-4cb8-832b-96db74f5da1d">



## Project Structure  

<img width="1016" alt="Screenshot 2023-10-09 at 03 49 17" src="https://github.com/eder/888spectate-challenger/assets/28600/d7f1df9b-bfbd-4122-9280-f148dd144452">

## Swagger
- The `swagger` all APIs.
- Visit `http://0.0.0.0:8000/docs#/ to access the playground
   <img width="1674" alt="Screenshot 2023-10-09 at 03 58 17" src="https://github.com/eder/888spectate-challenger/assets/28600/2743411b-c144-4dfa-992d-3cb7d2a6ce2d">

