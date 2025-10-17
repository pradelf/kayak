# kayak
Bloc1 : Construction et alimentation d'une infrastructure de gestion de données (Build &amp; Manage a Data Infrastructure).

![alt text](Media/Kayak-FPr.png)
## Sujet du projet d'évaluation : 
L’équipe marketing de Kayak a besoin d’aide pour un nouveau projet. Après avoir mené une étude auprès des utilisateurs, l’équipe a découvert que 70 % des utilisateurs qui prévoient un voyage souhaitent obtenir plus d’informations sur leur destination.

De plus, l’étude montre que les gens ont tendance à se méfier des informations qu’ils lisent s’ils ne connaissent pas la marque qui a produit le contenu.

Par conséquent, l’équipe marketing de Kayak souhaite créer une application qui recommandera aux utilisateurs où planifier leurs prochaines vacances. L’application devra se baser sur des données réelles concernant :

La météo
Les hôtels dans la région
L’application devra ensuite être capable de recommander les meilleures destinations et les meilleurs hôtels en fonction de ces variables, à tout moment.
## Evaluation

| Numéro du bloc| Nom du bloc (Français)|Nom du bloc (Anglais)	|Projets* | Durée durant l'examen de certification |
| :---------------: |:---------------:| :--------:|:---------------:|:---------------:|
|1	|Construction et alimentation d'une infrastructure de gestion de données|Build & Manage a Data Infrastructure	|Présenter 1 projet  - Fullstack Data Science - Data Collection & Management Project (Projet Kayak)	|10 minutes réparties comme suit : - 5 minutes de présentation - 5 minutes de questions-réponses |

## Execution du projet.

En premier lieu, la liste des villes ou lieux cibles pour un projet de vacances est créée.
Puis pour chacun d'eux;  nous récupérons leur coordonnées GPS grâce à l'API web service de nomitim.

## Process you have in mind for the project : Kayak
For a project like Kayak, it might look something like this:

 [ ]  Use a geolocalisation API to get latitude and longitude for my list of cities (such as nominatim)
 [ ] Use a weather API to get weather information on my cities, thanks to the coordinates (such as open weather api)
 [ ] Use my weather information to select the 5 most attractive cities for a holiday
 [ ]Use Scrapy to scrape booking.com information on 25 information for each city
 [ ] Upload all my raw data to an S3 bucket using boto3
Retrieve the data locally using boto3
 [ ] Clean and structure the data into a tabular format with python and pandas
 [ ] Upload my tabular data to an RDS with sqlalchemy
Run a few SQL requests on my data using sqlalchemy

## concrete goals

* What tools do you have to use?

* What processes do you need to put into place?

* What questions do you need to answer?

* What problems do you need to solve?

* What specific files do you need hand in for the certification?