# MLOps project 2025 June

## Intro

This README.md file will be used as a guiding file for those who want to reproduce or understand the files and structure of my project.

## Setup

To start off, we need to install the necessary libraries in order for our files to be executable and make a virtual environment.

The virtual environment comes first. This can simply be

The library names and versions can be found inside of the 'requirements.txt' file and can be installed using the following command: `pip install -r requirements.txt --upgrade`. The following command will install or update, depending on if these have been previously installed, these libraries. To execute this command, simply open a terminal inside the rootfolder of the project. However, i recommend using a virtual environment file so avoid conflicting library versions from clashing.























## VOOR MEZELF:

### Initialiseren venv:

- maak venv
source .venv/Scripts/activate
pip install -r requirements.txt


### labo2 gedeelte

mlflow ui --backend-store-uri sqlite:///mlflow.db
surf naar localhost:5000

### labo3 gedeelte:

- Starten prefect server:

docker compose up --build -d
docker images => onder repo naam pakken van map en tag
prefect init => kies docker => geef naam repo en tag die genoteerd staan voor initialisatie

- gebruiken server:

prefect server start --host 0.0.0.0 --port 4200

- workpool creëren:

prefect work-pool create --type process work-pool-1 --overwrite

- worker starten:

prefect worker start --pool <name-of-my-workpool>

ga naar einde prefect stuk => zie hoe daar moet, maak van alles flows en tasks en probeer uit!


