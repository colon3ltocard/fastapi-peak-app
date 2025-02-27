# Introduction

This is a POC for a mountain peak application made using fastapi.

# Installation - developer

Requires python >= 3.7.
Using [pyenv](https://github.com/pyenv/pyenv-installer) and a virtualenv. First install pyenv.

```shell script
pyenv install 3.8.3
pyenv virtualenv 3.8.3 peakenv
pyenv activate peakenv
pip install -r requirements.txt
```

# Running the app - developer

```shell script
(peakenvnew) bash-5.0$ uvicorn peakapp.main:app --reload
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [9942] using statreload
INFO:     Started server process [9979]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

You can play with the following endpoints:
* http://127.0.0.1:8000/generate_data - inject some data in the sqlite db
* http://127.0.0.1:8000/docs - see the docs generated by fastapi
* http://127.0.0.1:8000 - see the leaflet map generated by folium.

