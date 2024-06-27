# Url shortener translator
This service will shorten complex URLs into simpler ones and redirect users to the original URLs when accessed.

## Features
- Create a shorten translation equivalence.
- Get translation from a short URL.
- Measure the times the url has been visited or translated.
- Manage the url shortener translation

## Install
0.- Clone the repository
1.- Create an environment
```sh
pip install virtualenv
```
2.- Install/Upgrade pip
```sh
python -m pip install --upgrade pip
```
3.- Install virtual enviroment:
```sh
python 3.11 -m venv <virtual-environment-name>
```
4.-Activate the environment
```sh
source env/bin/activate
```
6.- Install requirements.
```sh
pip install -r requirements.txt
```
7.- Run the service in main folder
```sh
uvicorn main:app --reload
```

## Swagger 
To access the swagger go for at it carry to the documentations of the endpoints:
```sh
http://127.0.0.1:8000/docs
```
## Use
Put any url path. If it is exist i will redirect to the equivalent you added
```sh
 http://127.0.0.1:8000/{path} 
```
## Tests
You can run the test by running the following command:
```sh
 pytest test_crud.py --capture=no
```
