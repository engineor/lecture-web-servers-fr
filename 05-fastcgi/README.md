# Un site dynamique avec FastCGI

## Qu'est-ce que FastCGI - Fast Common Gateway Interface

### Définition

D'après [Wikipedia](https://fr.wikipedia.org/wiki/FastCGI) :


>FastCGI est une technique permettant la communication entre un serveur HTTP et un logiciel indépendant, c'est une évolution de Common Gateway Interface, abrégée en CGI, signifiant en anglais « Interface passerelle commune ».
>
>Créée en 1996 pour gérer les applications dynamiques des applications du World Wide Web (souvent abrégé en Web), la Common Gateway Interface permet l’exécution d'un nouveau processus à chaque requête, permettant ainsi la génération dynamique des pages.
>
>Dans le cas de CGI, chaque requête lance une nouvelle instance de CGI, qui appellera le programme à exécuter. Le binaire cgi recrée à chaque appel le contexte de l'environnement d'exécution et ne permet pas de limiter le nombre de processus simultanés. Le nombre de processus simultanés sera donc dépendant du nombre de processus simultanés du serveur web.
>
>Avec FastCGI, les applications générant les pages dynamiques peuvent se situer sur un ou des serveur(s) différent(s) du ou des serveur(s) hébergeant le service HTTP. Une variable est introduite permettant de déterminer le nombre minimum et maximum de processus CGI à exécuter, indépendamment du nombre de processus HTTP maximum.

Concrêtement, FastCGI donne donc la possibilité d'executer la génération des pages sur des serveurs physique ou virtuels différent du serveur hébergeant le serveur http, et est configurable indépendamment du serveur http.

Pour le reste, le diagramme de séquence ne prennant pas en compte la séparation des processus ni la séparation réseau de l'exécution des programmes, on retrouve un schema similaire.

Pour ce chapitre, nous prendrons l'exemple de `php-fpm` (`PHP FastCGI Process Manager`), qui est l'implémentation FastCGI la plus répandue actuellement dans l'écosystème PHP.

![](05-fastcgi/images/php-fpm.png)

Pour exécuter du Python3 en FastCGI, il est possible d'utiliser des serveurs comme [uWSGI](https://www.digitalocean.com/community/tutorials/how-to-deploy-python-wsgi-applications-using-uwsgi-web-server-with-nginx) ou [CherryPy](https://www.digitalocean.com/community/tutorials/how-to-deploy-python-wsgi-applications-using-a-cherrypy-web-server-behind-nginx).

### Évolutivité

Un chapitre complet sera dédié à l'évolutivité horizontale de l'infrastructure grâce à PHP-FPM plus tard dans le cours.

## Demo / Exercice : PHP-FPM en local

### Avec Apache httpd

### Avec Nginx

## Demo / Exercice : PHP-FPM distant

### Avec Apache httpd

### Avec Nginx

## Profiter des avantages d'un serveur FastCGI en PHP

[`fastcgi_finish_request `](https://secure.php.net/manual/fr/function.fastcgi-finish-request.php)

>Cette fonction affiche toutes les données de la réponse au client et termine la requête. Ceci permet pour les tâches consommatrices en temps d'être effectuées sans laisser la connexion avec le client ouverte.

## Conclusion

FastCGI est une évolution pratique de CGI qui nous permet une meilleure évolutivité et une gestion des processus plus granulaire.

Dans le chapitre suivant, nous verrons comment profiter de ces avantages pour mettre en place un serveur d'hébergement en [exécutant PHP avec différents utilisateurs](/06-php-multitenant).