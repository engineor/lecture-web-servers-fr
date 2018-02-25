# Executer PHP avec Apache httpd, les stratégies disponibles

Il existe au moins trois façons de rendre un site dynamique en utilisant PHP comme langage de programmation pour générer les pages :

- Apache httpd `mod_php` : une extension d'Apache httpd permettant de faire tourner un processus PHP dans le processus Apache httpd.
- `php-cgi` : faire démarrer un processus PHP à la demande pour l'interpretation de la ressource.
- `php-fpm` : avoir un serveur avec plusieurs threads capable de prendre en charge les requêtes envoyéees par le serrrveur http.

Dans cet chapitre, nous allons nous concentrer exclusivement sur la première solution, historiquement la plus utilisée car simple à mettre en oeuvre. Les autres solutions seront détaillées dans les chapitres suivants.

## Fonctionnement

Comme indiqué sur le [wiki d'Apache](https://wiki.apache.org/httpd/php), le `mod_php` pouvait s'executer en [`DSO`](https://httpd.apache.org/docs/2.4/fr/dso.html) jusqu'à Apache httpd 2.2, c'est à dire comme morceau de logiciel invocable par le programme principale.

Cette solution nécessite l'execution de PHP avec le prefork MPM, qui est une solution lourde d'execution sans thread d'Apache. Par ailleurs, PHP est chargé pour toutes les requêtes web et non séléctivement.

C'est cette solution qui a déclenché la rumeur qu'Apache httpd serait capable de recevoir moins de requêtes par seconde que d'autres serveurs comme Nginx, ce qui est vrai dans le contexte de cette configuration mais totalement faux le reste du temps.

À partir de la version 2.4 d'Apache httpd, il est possible d'utiliser PHP avec le `mpm event`, ce qui améliore les performances.

PHP reste dans ce scenario couplé à la machine executant le serveur http, il n'y a donc pas de possibilité d'évolutivité horizontale.

Concernant l'utilisateur responsable de l'execution, c'est dans tous les cas l'utilisateur d'Apache httpd, sauf dans deux cas précis :

- l'utilisation du [MPM ITK](http://mpm-itk.sesse.net/), un fork du MPM prefork qui permets de définir dans le virtualhost un utilisateur spécifique qui lancera le process forké executant la requête.
- l'utilisation de librairies comme [SuPHP](https://www.suphp.org/Home.html)

## Configuration

Il existe des images Docker contenant PHP installé sur Apache httpd avec `mod_php` : [PHP sur Docker hub](https://hub.docker.com/_/php/), versions `-apache`.

Tester l'execution d'un fichier simple (`index.php` contenant `<?php phpinfo(); ?>`) :

```
docker run --rm -p 80:80 -v $(pwd)/03-php-apache-httpd/demo1/html:/var/www/html php:7.2-apache
```

Regardons la configuration :

```
docker run --rm php:7.2-apache cat /etc/apache2/apache2.conf
```

>IncludeOptional mods-enabled/\*.load  
>IncludeOptional mods-enabled/\*.conf  
>
>IncludeOptional conf-enabled/\*.conf  
>
>IncludeOptional sites-enabled/\*.conf  

```
docker run --rm php:7.2-apache cat /etc/apache2/mods-enabled
```

>lrwxrwxrwx 1 root root 27 Feb 16 23:16 php7.load -> ../mods-available/php7.load

```
docker run --rm php:7.2-apache cat /etc/apache2/conf-enabled/docker-php.conf
```

```apache
<FilesMatch \.php$>
	SetHandler application/x-httpd-php
</FilesMatch>

DirectoryIndex disabled
DirectoryIndex index.php index.html

<Directory /var/www/>
	Options -Indexes
	AllowOverride All
</Directory>
```

`DirectoryIndex` indique à Apache d'utiliser le fichier `index.php` si un dossier est demandé dans le requête, et `index.html` si `index.php` n'existe pas.

`SetHandler` indique à Apache de faire une execution de PHP sur le fichier, si le fichier fini par `.php` (`FilesMatch \.php$`).

`AllowOverride All` indique qu'un fichier `.htaccess` peut surcharger les configurations du virtualhost.

En plus de ces configuration, la bibliothèque PHP est installée sur le système :

```
docker run --rm php:7.2-apache cat /etc/apache2/mods-available/php7.load
```

>LoadModule php7_module        /usr/lib/apache2/modules/libphp7.so

## Conclusion

Bien que n'étant pas particulièrement efficace, cette solution permets de mettre en place un serveur http / php rapidement et avec une infrastructure minimale.

Un certain nombre de restrictions concernant la gestion granulaire des utilisateurs et l'évolutivité n'en font pas la solution la plus adéquate pour tous les types de projets.

D'autres solutions existent tels que l'utilisation des [scripts CGI](/04-cgi) détaillée dans le chapitre suivant.