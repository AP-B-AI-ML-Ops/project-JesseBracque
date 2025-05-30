# Peer review: Mauro Demey 2ITAI

## Evaluator: Jesse Bracqué 2ITAI

## Totaal score: 9/12

### Voor ik begin

Voor ik start wou ik de volgende dingen nog zeggen:

- Het project was goed, maar ontbrak kleine details.

## Rubriek:

### Problem description

#### Score: 1/2

#### Reden voor score:

Ik vind dat deze metriek de volgende score verdient omwille van de volgende redenen:

- Er wordt kort uitgelegd waarvoor het gebruikt kan worden, de gezondheidszorg, maar benadrukt dit niet. De focus ligt vooral op het ML gedeelte en de werking hiervan. Daardoor is er wel duidelijkheid daar rond, maar is er gebrek aan een diepgaandere uitleg. Deze uitleg voldoet volgens mij niet aan een rubriek voor een 2/2 hierdoor.

### Experiment tracking & model registry

#### Score: 2/2

#### Reden voor score:

Ik vind dat deze metriek de volgende score verdient omwille van de volgende redenen:

- Beide zijn hier zowel in de code, wat natuurlijk nodig is, als duidelijk in MLFlow te zien onder hun respectievelijke experimenten. Hierdoor is alles mooi en overzichtelijk.

Concreet is alles in orde en is hier niets op aan te merken.

### Workflow orchestration

#### Score: 2/2

#### Reden voor score:

Ik vind dat deze metriek de volgende score verdient omwille van de volgende redenen:

- split_data.py had ook met een flow kunnen gebeuren, want dit had netter geweest en minder ruimte tot fouten toegelaten. Dit is echter maar 1 commando, dus het is een bijna verwaarloosbaar detail.
- De main flow is mooi uitgewerkt en runt vlotjes.
- Ook batch predict runt vlot en is mooi uitgewerkt.

Uiteindelijk werkt alles proper en doet het wat het moet doen. Omdat ik hiervoor een punt heb afgetrokken, zie laatste rubriek hieronder, zal ik dit hier niet doen.

### Model deployment

#### Score: 2/2

#### Reden voor score:

Ik vind dat deze metriek de volgende score verdient omwille van de volgende redenen:

- Alle nodige stappen zijn genomen in de code van de verschillende files om cloud deployment mogelijk te maken. Dit is wat nodig is. Veel meer valt hier niet over te zeggen na het kijken naar de project files.

### Model monitoring

#### Score: 1/2

#### Reden voor score:

Ik vind dat deze metriek de volgende score verdient omwille van de volgende redenen:

- Het evidently rapport wordt mooi gemaakt en komt verzorgd terecht maar het terecht moet komen.
- De resultaten op grafana zijn duidelijk weergegeven en makkelijk bereikbaar.
- Alerts ontbreken hier wel duidelijk. Dit is het enige duidelijke minpunt.

### Reproducibility

#### Score: 1/2

#### Reden voor score:

Ik vind dat deze metriek de volgende score verdient omwille van de volgende redenen:

- De data zelf is niet aanwezig, maar moet gedownload worden. Deze is vrij klein, 316.97kb, dus zou in principe gewoon uit de .gitignore gelaten kunnen zijn. Hier trek ik niks voor af, maar ik merk het wel op. Voor andere projecten met grote datasets is dit namelijk een idee, maar uiteindelijk moet deze toch gedownload worden. Hierdoor blijft dit een persoonlijke voorkeur.
- Ook hier ontbreken de .env files, wat volgens de industriestandaard eigenlijk moet, maar hier eigenlijk niet persé had moeten ontbreken. Opnieuw goed dat daar rekening mee gehouden wordt.
- Alle links naar de verschillende services zijn duidelijk en proper weergegeven. Dit is verzorgd en makkelijk om te volgen.
- Tijdens het volgen van instructie nr. 4 wordt er gezegd dat er naar 'train/data' genavigeert moet worden. Deze map bestaat echter niet en heet 'training/data'. Relatief makkelijk recht te zetten, maar kan mogelijk voor verwarring zorgen bij mensen die geen technische voorkennis hebben.
- In alle requirements.txt files doorheen het project ontbreken de library versies. Er is duidelijk vermeld in de rubriek voor 2/2 dat deze aanwezig moeten zijn.

Algemeen gezien is het in orde, maar er ontbreken details hier en daar. Ik zelf vind het moeilijk om dan te beslissen of er hier een 1 of 2 gegeven wordt, want als het van mij af hing zou ik een 1.5/2 geven. Ik zal hier dus uiteindelijk een 1 geven en zachter zijn op andere criteria om niet onnodig veel punten af te trekken. Over deze beslissing zou gediscussieerd kunnen worden en hiervan ben ik mezelf bewust, maar ik heb mijn best gedaan om mijn gedachtengoed zo helder mogelijk te verwoorden.
