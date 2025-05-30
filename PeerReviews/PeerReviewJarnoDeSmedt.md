# Peer review: Jarno De Smedt 2ITAI

## Evaluator: Jesse Bracqué 2ITAI

## Totaal score: 7/12

### Voor ik begin

Voor ik start wou ik de volgende dingen nog zeggen:

- Het project valt moeilijk te starten op de manier die beschreven wordt in de README-file. Tijdens het bouwen komt er telkens een error. Dit zorgde voor de nodige frustratie.
- Het uitvoeren ervan gebeurd in een dev container. Dit is duidelijk voor development en niet productie.
- Veel files en commando's moeten nog handmatig worden uitgevoerd. Dit is verre van ideaal voor gebruik als we te maken krijgen met mensen die niet over de technische vaardigheden en kennis beschikken. Hoe meer code er zelf uitgevoerd moet worden, hoe meer fouten er gemaakt kunnen worden.

## Rubriek:

### Problem description

#### Score: 1/2

#### Reden voor score:

Ik vind dat deze metriek de volgende score verdient omwille van de volgende redenen:

- Het probleem wordt kort omschreven.
- Hij geeft in deze beschrijving aan wat er gebeurt, maar zegt niet direct wat voor verschil zijn applicatie zal maken. Het vergelijken van prijzen kan handig zijn, maar er is geen duidelijke uitleg over waarom dit zo zeer een probleem is momenteel.

### Experiment tracking & model registry

#### Score: 2/2

#### Reden voor score:

Ik vind dat deze metriek de volgende score verdient omwille van de volgende redenen:

- Na uitvoer van de deployment is het model duidelijk terug te vinden in MLFlow. Dit wordt in zowel de code, app.py en train_and_register_model.py, als in de docker compose file duidelijk in de code weergegeven. Dit is prima in orde en werkt. Registratie van de code gebeurd door:
  - mlflow.sklearn.log_model(..., registered_model_name="car-price-model", ...)
- Ook experiment tracking gebeurd volledig volgens wat er nodig is. Dit gebeurd in train_and_register_model.py door deze twee lijnen code:
  - mlflow.set_tracking_uri(...)
  - mlflow.set_experiment("CarPricePrediction")
- Tenslotte wordt ook de gebruikte parameters gelogd naar MLFlow.

Dit gedeelte is dus volledig in orde.

### Workflow orchestration

#### Score: 1/2

#### Reden voor score:

Ik vind dat deze metriek de volgende score verdient omwille van de volgende redenen:

- Er is workflow orchestration aanwezig via Prefect. De training_pipeline is als Prefect deploymeny geïmplementeerd en kan als workflow uitgevoerd worden.
- De workflow is echter niet volledig uitgewerkt of opgesplitst in aparte en herbruikbare componenten of taken. Alles zit in één script (train_and_register_model.py). Dit is dus niet volledig uitwerkt. De README geeft aan dat verdere opsplitsing in de src folder gepland was, maar niet is uitgevoerd. Dit heeft Jarno zelf ook vermeld. Dit komt door een gebrek aan tijd.

### Model deployment

#### Score: 1/2

#### Reden voor score:

Ik vind dat deze metriek de volgende score verdient omwille van de volgende redenen:

- Het model draait in een dev container. Hierdoor kan het niet direct naar een cloud gezet worden, omdat het deployment niet geautomatiseerd is.
- Ook de aanwijzingen in de README zijn gericht op lokaal deployment. Deze stappen zullen niet mogelijk zijn voor het deployen in een cloud omgeving. De stap richting een cloud deployment is klein, maar deze is niet volledig uitgewerkt.
- Het project maakt wel gebruik van containerisatie, maar lokale. Dit is goed, maar voldoet volgens de metriek slechts aan 1 van de 2 mogelijke punten.
- Om verdere verbetering mogelijk te maken, had een automatische pipeline gebruikt kunnen worden hiervoor.

### Model monitoring

#### Score: 1/2

#### Reden voor score:

Ik vind dat deze metriek de volgende score verdient omwille van de volgende redenen:

- Er wordt gebruikgemaakt van Evidently om een data drift rapport te genereren. Dit rapport wordt automatisch aangemaakt en opgeslagen in de map reports na het trainen van het model.
- Er is echter geen sprake van een dashboard (zoals Grafana) of van automatische alerting of acties wanneer er drift wordt vastgesteld. Het rapport moet handmatig bekeken worden en er is geen integratie met een monitoring- of notificatiesysteem.
- Monitoring is dus aanwezig op een basis niveau (rapportage), maar niet volledig uitgewerkt richting automatische opvolging of productie monitoring.
- Vermits er basis monitoring is, is een 1 hier in mijn opinie het juiste antwoord.

### Reproducibility

#### Score: 1/2

#### Reden voor score:

Ik vind dat deze metriek de volgende score verdient omwille van de volgende redenen:

- Meeste van de instructies zijn aanwezig, maar niet compleet. Ze laten twijfel over aan de gebruiker en zorgen ervoor dat de gebruiker zelf nog dingen moet uitzoeken zoals de volgende:
  - De gebruiker zelf moet files gaan aanmaken. Meestal zullen bepaalde files ontbreken, maar vermits dit een schoolopdracht is, is er geen nood om files zoals '.env' te laten ontbreken.
  - Er wordt gezegd dat 'prefect.yaml' mogelijk nog niet bestaat, terwijl deze file weldegelijk wordt geïmporteerd. Dit maakt de README onnodig verwarrend.
  - Het bouwen van de gebruikte dev container had meerdere keren errors tijdens het bouwproces. Dit kan aan mijn eigen laptop liggen, dus hiervoor trek ik geen punten af, maar kan mogelijk een probleem zijn dat ook bij andere voorkomt.
  - Er worden geen instructies gegeven over hoe de logs van de prefect agent container te checken zijn.
  - Bij het geven van het volgende commando:
    prefect deploy train_and_register_model.py:training_pipeline -n cars1 -p zoompool
  - Krijg ik:
    The following deployment(s) could not be found and will not be deployed: cars1
    Could not find any deployment configurations with the given name(s): cars1. Your flow will be deployed with a new deployment configuration.
    2025/05/29 12:25:09 INFO mlflow.tracking.fluent: Experiment with name 'CarPricePrediction' does not exist. Creating a new experiment.
  - Deze deployment zal uiteindelijk wel gecreëerd worden, maar kan mogelijk weer tot verdere verwarring leiden door de logs die op het scherm komen te staan. Er wordt hier wel duidelijk vermeld dat er moet gekozen worden voor 'n' wanneer dit gevraagd wordt, dus in principe is dit oké.
  - Het model bij de web app laadt niet en geeft een error.
- Er word gezegd dat unit tests uit te voeren zijn. Dit is echter een deel van development en is niet relevant hier.
- Ook de precommit hooks zijn niet relevant tijdens productie.
- De gebruikte library versies zijn inbegrepen in de requirements.txt in de meeste mappen, maar zo te zien niet map voor de web applicatie.

Ondanks de waslijst aan dingen die ik hier noteerde, is 1 punt hier terecht. De data is ook aanwezig.
