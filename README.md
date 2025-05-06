# MLOps project 2025 June

## Intro and problem description

This README.md file will be used as a guiding file for those who want to reproduce or understand the files and structure of my project. Note that this project was created in VSCode and will be written in such a way that describes how to make everything run while using VSCode.

Throughout history gold has always been a valuable asset. It has been a big part of global currency to regulate empires and states. In this project i aim to develop and use a fully containerized MLOps application that uses machine learning to predict the price fluctiantions of gold. This application, if the model is sufficient, would be a tool that can be used for financial gain. Disclaimer: since i am no expert, please do not use this to try and predict the market values on a day to day basis. This model is not meant to be accurate, but merely show the possibilities of ML usage in a Dev Ops environment.

## Setup

The very first step we will take is start Docker Desktop. Docker will need to be running in the background to allow us to create and use the necessary containers. After Docker has been started we will go through the rest of the steps:

### Creating a .venv and installing the necessary libraries

The virtual environment comes first. Before making this note that the .venv used here uses Python 3.10.2. Using different versions might result in newer or older libraries which will cause problems later down the line with new or potentially depricated methods.

To make a venv execute the following steps: click on 'terminal' in the top left, select 'new terminal', and type `python -m venv MLOps-project-venv`. Afterwards, open the explorer, if this isn't open yet, and navigate to the 'train-and-deploy' folder. Open 'scripts', and select 'hpo.py'. While inside any Python file you will see 'select kernel' in the top right corner. Click it, chose 'select another kernel', chose 'Python Environments' and select 'MLOps-project-venv'. Any other Python file would've been sufficient for the last bit, but clear instructions are always nicer to have.

The next step is to install the required libraries. The library names and versions can be found inside of the 'requirements.txt' file and can be installed using the following command in the terminal we just opened: `pip install -r requirements.txt --upgrade`. The following command will install these libraries.












## VOOR MEZELF:

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
