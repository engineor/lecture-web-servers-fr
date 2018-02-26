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

## Demo / Exercice : PHP-FPM distant

Pour cet exercice, nous aurons besoin d'un serveur http et d'un serveur FastCGI (`php-fpm`).

Pour l'exemple, nous utiliserons le script php suivant :

```php
<!Doctype html>
<html>
    <head>
        <title>PHP-FPM</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h1>PHP-FPM</h1>
        <h2><?= PHP_VERSION ?></h2>
    </body>
</html>
```

### Avec Apache httpd

Récupérer la configuation d'Apache httpd :

```
docker run --rm httpd cat /usr/local/apache2/conf/httpd.conf > 05-fastcgi/demo1/config/httpd.conf
```

Activer le mode `proxy_fcgi`

```
LoadModule proxy_module modules/mod_proxy.so
LoadModule proxy_fcgi_module modules/mod_proxy_fcgi.so
```

Configurer ensuite la délégation des fichiers `.php` à PHP-FPM :

```
ProxyPassMatch ^/(.*\.php(/.*)?)$ fcgi://php:9000/var/www/html/$1
<Directory "/usr/local/apache2/htdocs">
    DirectoryIndex index.php
</Directory>
```

Il faut maintenant lancer le container PHP-FPM (avec le code dans `/var/www/html` comme indiqué dans la directive `ProxyPassMatch`) : 

```
docker run --name php-05-02 --rm -p 9000:9000 -v $(pwd)/05-fastcgi/demo1/html:/var/www/html:ro php:7.2-fpm
```

Il reste à lancer le container Apache httpd :

```
docker run --rm --link php-05-02:php -p 80:80 -v $(pwd)/05-fastcgi/demo1/config/httpd.conf:/usr/local/apache2/conf/httpd.conf:ro -v $(pwd)/05-fastcgi/demo1/html:/scripts:ro httpd
```

Si on arrête le container PHP-FPM et on recharge la page, on aura une erreur 503 car Apache httpd n'arrive plus à communiquer avec le serveur PHP.

### Avec Nginx

Récupérer la configuration du bloc serveur d'Nginx :

```
docker run --rm nginx cat /etc/nginx/conf.d/default.conf > 05-fastcgi/demo2/config/default.conf
```

Modifier la configuration pour faire passer la requête à PHP-FPM lors de l'execution d'un fichier finissant en `.php` :

```nginx
location / {
    root   /usr/share/nginx/html;
    index  index.html index.htm;
}

# proxy the PHP scripts to Apache listening on 127.0.0.1:80
#
#location ~ \.php$ {
#    proxy_pass   http://127.0.0.1;
#}

# pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
#
location ~ \.php$ {
    root           html;
    fastcgi_pass   127.0.0.1:9000;
    fastcgi_index  index.php;
    fastcgi_param  SCRIPT_FILENAME  /scripts$fastcgi_script_name;
    include        fastcgi_params;
}
```

Lançons ensuite le serveur nginx seul (sans lancer PHP-FPM), et regardons comment la page [http://localhost/index.php](http://localhost/index.php) réagis :

```
docker run --rm -p 80:80 -v $(pwd)/05-fastcgi/demo2/config/default.conf:/etc/nginx/conf.d/default.conf:ro -v $(pwd)/05-fastcgi/demo2/html:/code:ro nginx
```

En regardant les logs, on trouve la ligne suivante, qui nous indique que la redirection vers un serveur local a échoué.

> 2018/02/26 06:25:16 [error] 5#5: *1 connect() failed (111: Connection refused) while connecting to upstream, client: 172.17.0.1, server: localhost, request: "GET /index.php HTTP/1.1", upstream: "fastcgi://127.0.0.1:9000", host: "localhost"

Comme nous executons l'environnement dans un environnement Docker, nous devrons utiliser le nom du container à la place de l'IP locale pour communiquer avec PHP-FPM :

```
#fastcgi_pass   127.0.0.1:9000;
fastcgi_pass   php-05-02:9000;
```

Redémarrons le serveur Nginx, toujours avec le code dans `/code`, mais en ajoutant un lien vers `php-05-02`, le container PHP-FPM que nous allons démarrer par la suite (`--link php-05-02:php`).

```
docker run --rm -p 80:80 --link php-05-02:php -v $(pwd)/05-fastcgi/demo2/config/default.conf:/etc/nginx/conf.d/default.conf:ro -v $(pwd)/05-fastcgi/demo2/html:/code:ro nginx
```

Charger la page resulte toujours dans une erreur 502 car nous n'avons toujours pas démarré PHP-FPM.

```
docker run --name php-05-02 --rm -p 9000:9000 -v $(pwd)/05-fastcgi/demo2/html:/scripts:ro php:7.2-fpm
```

Notez le point de montage `/scripts`, qui correspond à la configuration disponible sous la clé `fastcgi_param` dans Nginx.

Rechargez la page et tout fonctionne.

## Demo / Exercice : PHP-FPM en local

La démonstration de l'exercice précédent montre l'utilisation de PHP-FPM sur un serveur tiers (ou du moins un container tiers dans notre cas).

Il est aussi possible d'executer PHP-FPM sur la même machine que le serveur http, et de s'y connecter sans passer par le réseau grâce aux sockets fichiers.

### Avec Apache httpd

Ajouter PHP-FPM à l'image `httpd` grâce à un `Dockerfile`.

Modifier la configuration de PHP-FPM pour écouter sur un socket fichier :

```
listen = /var/run/php7-fpm/DOMAINNAME.socket
```

Changer le `ProxyPassMatch` en conséquence.

### Avec Nginx

Voir la documentation sur Rackspace : [Nginx avec PHP-FPM sur un socket UNIX fichier](https://support.rackspace.com/how-to/install-nginx-and-php-fpm-running-on-unix-file-sockets/)

Ajouter PHP-FPM à l'image `nginx` grâce à un `Dockerfile`.

Modifier la configuration de PHP-FPM pour écouter sur un socket fichier :

```
listen = /var/run/php7-fpm/DOMAINNAME.socket
```

## Profiter des avantages d'un serveur FastCGI en PHP

[`fastcgi_finish_request `](https://secure.php.net/manual/fr/function.fastcgi-finish-request.php)

>Cette fonction affiche toutes les données de la réponse au client et termine la requête. Ceci permet pour les tâches consommatrices en temps d'être effectuées sans laisser la connexion avec le client ouverte.

## Conclusion

FastCGI est une évolution pratique de CGI qui nous permet une meilleure évolutivité et une gestion des processus plus granulaire.

Dans le chapitre suivant, nous verrons comment profiter de ces avantages pour mettre en place un serveur d'hébergement en [exécutant PHP avec différents utilisateurs](/06-php-multitenant).