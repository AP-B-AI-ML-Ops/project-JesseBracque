# Peer review: Vincent Heyndrickx 2ITAI

## Evaluator: Jesse Bracqué 2ITAI

## Totaal score: 3/12

### Voor ik begin

Voor ik start wou ik de volgende dingen nog zeggen:

- Vincent vertelde mij dat, door een gebrek aan tijd door zijn legeropleiding, hij geen tijd heeft gehad om dit project te maken. Hierdoor zullen meeste dingen ontbreken.

## Rubriek:

### Problem description

#### Score: 0/2

#### Reden voor score:

Ik vind dat deze metriek de volgende score verdient omwille van de volgende redenen:

- Er is geen probleemstelling geformuleerd.
- Het is niet duidelijk waar exact deze applicatie gebruikt kan worden.
  Er wordt dus duidelijk niet voldaan aan eender welk van de twee criteria. Hierdoor kan ik niet anders dan een 0/2 geven hier.

### Experiment tracking & model registry

#### Score: 1/2

#### Reden voor score:

Ik vind dat deze metriek de volgende score verdient omwille van de volgende redenen:

- Beide zaken gebeuren wel, in model.py, maar zitten in 1 file. Dit is slecht opgesplitst en de code zelf kan niet gecheckt worden op werking. Ik vind dat er hier 1 punt voor gegeven kan worden, puur omdat het wel in de code staat.
- Kijk bij de laatste metriek voor meer uitleg. Ik licht hiet nog iets beter toe wat mijn algemen probleem met dit project is.

### workflow orchestration

#### Score: 1/2

#### Reden voor score:

Ik vind dat deze metriek de volgende score verdient omwille van de volgende redenen:

- Ook hier is er code aanwezig voor een workflow, maar het gebruik kan niet gecheckt worden. Deze is kort en slecht uitgewerkt. Met moeite kan ik hier 1 punt voor geven, puur omdat er een pipepline is opgezet en deze via een worker, als de docker-compose niet fout was geweest, uitgevoerd had kunnen worden. Alleen weten we dus niet OF deze ook effectief zou werken.
- Kijk bij de laatste metriek voor meer uitleg. Ik licht hiet nog iets beter toe wat mijn algemen probleem met dit project is.

### Model deployment

#### Score: 0/2

#### Reden voor score:

Ik vind dat deze metriek de volgende score verdient omwille van de volgende redenen:

- Zelfs op lokale omgeving werkt er hier niets, dus in een cloud omgeving zou dit gegarandeerd voor problemen zorgen. Hierdoor ben ik genoodzaakt om geen punten te geven, want deze rubriek heeft tenslotte betrekking tot het gebruiken van de applicatie.
- Kijk bij de laatste metriek voor meer uitleg. Ik licht hiet nog iets beter toe wat mijn algemen probleem met dit project is.

### Model monitoring

#### Score: 1/2

#### Reden voor score:

Ik vind dat deze metriek de volgende score verdient omwille van de volgende redenen:

- Er gebeurd wel monitoring in de 'Batch' map. Deze is het absolute minimum wat nodig is. Hierdoor schraap ik nog 1 punt bijeen. Deze is het absolute begin van batch monitoring, dus zoals vermeld in de rubriek voor 1/2 zal ik hier dus een punt geven.
- Kijk bij de laatste metriek voor meer uitleg. Ik licht hiet nog iets beter toe wat mijn algemen probleem met dit project is.

### Reproducibility

#### Score: 0/2

#### Reden voor score:

Ik vind dat deze metriek de volgende score verdient omwille van de volgende redenen:

- Er worden, buiten het bouwen van het project, compleet geen instructies gegeven over hoe het project gebruikt of uitgevoerd moet worden. Hierdoor wordt er dus niet voldaan aan de volgende zaken:
  - Duidelijke instructies
  - Makkelijke te runnen code => Geen instructies over hun werking, want die ontbreken
- Na het bouwen testte ik de volgende zaken en kwam tot de volgende conclusies:
  - De docker-compose.yml is fout. Hierdoor werkt niks van de services en kan er bijgevolg dus ook niet gekeken worden of en hoe de service werking is.
- Het enige positieve, maar hier ga ik geen punt op geven, is dat de versies van de gebruikte libraries wel inbegrepen zijn per map waar python scripts worden gebruikt.
  In conclusie: Hier kan ik geen punten op geven, want niets werkt. Ik weet dat het de bedoeling is dat we onze mening goed onderbouwen, maar dit project schreeuwt echt dat het een ramp is als ZELFS het bouwen ervan al niet werkt. Fouten worden gemaakt, maar het werkend krijgen van dit soort zaken, zeker als een groot deel van de services ontbreken, is niet onmogelijk en zelfs vrij doenbaar. Ik heb mijn best gedaan om punten te geven waar mogelijk, maar zelfs met een hoop door de vingers te zien valt er hier absoluut niets hoger dan een 3/12 te geven. Zelfs deze score is in mijn ogen al te hoog, maar ik heb geprobeerd om eerlijk en correct te anaylseren wat er in de code gebeurd. De data is ook aanwezig.
