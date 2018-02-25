# Théorie des serveurs web

## Définition

Wikipedia FR :

> Un serveur web est spécifiquement un serveur multi-service utilisé pour publier des sites web sur Internet ou un intranet. L'expression « serveur Web » désigne également le logiciel utilisé sur le serveur pour exécuter les requêtes HTTP, le protocole de communication employé sur le World Wide Web.  
> Un serveur web diffuse généralement des sites web, il peut contenir d'autres services liés comme l'envoi d'e-mails, du streaming, le transfert de fichiers par FTP, etc.  

Dans notre contexte :

- Logiciel (on ne parle pas ici du serveur matériel)
- Executer les requêtes http
  - servir un fichier statique
  - servir un fichier généré dynamiquement
    - interagir avec une base de donnée
    - interagir avec un système de fichier
  - servir un fichier dynamique de façon statique (cache http)


## Role (de base) du serveur http

![](01-101-server-web-theory/images/chrome-request.png)

Le serveur http recoit une requête http qui lui vient du navigateur web (ou tout autre client http). Selon les demandes exprimées dans la requête (verbe, en-têtes, etc.), il génère une réponse qu'il renvoit au client.

![](01-101-server-web-theory/images/http-request-simple.png)

### 1. Requête http

```bash
curl -Lvso /dev/null http://localhost
```

> GET / HTTP/1.1  
> Host: localhost  
> User-Agent: curl/7.54.0  
> Accept: &ast;/&ast;  

Ici, on utilise `curl` comme client http pour voir la requête envoyée. Pour débugger une requête http, il est aussi possible de passer par des services comme [RequestBin](https://requestb.in/).

Ce message demande une ressource spécifique via son url (la racine du site dans le cas présent). Toujours dans cet exemple précis, on constate que le client demande n'importe quel type de contenu, le serveur décidera donc ce qu'il doit servir basé sur sa valeur par défaut.

### 2. Réponse http

```bash
curl -I http://localhost
```
> HTTP/1.1 200 OK  
> Date: Sat, 24 Feb 2018 10:50:40 GMT  
> Server: Apache/2.4.29 (Unix)  
> Last-Modified: Sat, 24 Feb 2018 10:37:38 GMT  
> ETag: "88-565f2dd9b8080"  
> Accept-Ranges: bytes  
> Content-Length: 136  
> Content-Type: text/html  

```bash
curl http://localhost
```

```html
<!Doctype>  
<html>  
    <head>
        <title>Hello World</title>
    </head>
    <body>
        <h1>Hello World</h1>
    </body>
</html>
```

Les commandes ci-dessus nous montrent les en-têtes et le contenu de la réponse http renvoyée par le serveur http. Le `Content-Type` explique à notre client http comment interpréter la ressource, ici avec `curl` il traitera donc le contenu comme du texte qu'il affichera dans la console malgré le `Content-Type: text/html`. Un navigateur web interpreterait ce contenu pour afficher une page web.

### 3. Execution de la requête

Notre serveur est relativement simple pour le moment, et sert du contenu statique. L'exécution de la requête consiste donc à chercher sur le système de fichier si il existe un fichier ayant le nom donné dans l'url, en lire le contenu et le retourner avec les en-têtes requises.

## Ports par défaut pour les requêtes web

Les ports par défaut pour les requêtes web sont les suivantes :

- http : port 80
- https : port 443

Pour utiliser un port non standard, il suffit de mettre `:` et le numéro du port après le nom de domaine ou l'adresse IP.

# Rappel : les DNS

On accède à un serveur via son adresse IP (v4 ou v6)

Un nom de domaine a une **zone**, qui définit pour chaque entrée un type et une destination.

![](01-101-server-web-theory/images/cloudflare.png)

Pour la résolution de nom dans le cadre d'une requête http, seuls les champs `CNAME`, `A` et `AAAA` nous intéressent. Pour `A` et `AAAA` on associe un nom à une adresse. Pour le `CNAME`, on associe un nom à un autre nom, qui est lui même associé à une adresse.

Pour en savoir plus sur les DNS, vous pouvez vous réferrer au [cours d'OpenClassroom sur le fonctionnement des réseaux TCP/IP](https://openclassrooms.com/courses/apprenez-le-fonctionnement-des-reseaux-tcp-ip/le-service-dns).

Exemple de zone DNS (extrait de la zone de `scotlandphp.co.uk`) :

>;; CNAME Records  
>webmail.scotlandphp.co.uk.      300	IN	CNAME  business.zoho.com.  
>conference.scotlandphp.co.uk.   300	IN	CNAME  scotlandphp.github.io.  
>www.slack.scotlandphp.co.uk.	   300	IN	CNAME  slack.scotlandphp.co.uk.  
>
>;; A Records (IPv4 addresses)  
>2017.conference.scotlandphp.co.uk. 300	IN  A  149.202.172.54  
>wallace.scotlandphp.co.uk.	      300 IN  A  149.202.175.239  

La résolution DNS la plus simple : `/etc/hosts` ou `C:\Windows\System32\drivers\etc` (par défaut).

```
##
# Host Database
#
# localhost is used to configure the loopback interface
# when the system is booting.  Do not change this entry.
##
127.0.0.1	localhost keycloak.local
255.255.255.255	broadcasthost
::1             localhost 
```

Il est possible d'ajouter des lignes dans ce fichier pour résoudre arbitrairement un nom de domaine, notamment faire pointer un site sur la version de développement local.

## Exemples de serveurs HTTP

- [Apache2](https://httpd.apache.org/) (attention, Apache est une fondation, Apache2 est le nom courant du serveur http qui est en fait Apache http server project)
- [Nginx](https://nginx.org/)
- [IIS](https://www.iis.net/)
- [Caddy](https://caddyserver.com/)
- [Lighttp](https://www.lighttpd.net/)
- ...
- n'importe quelle boucle infinie qui écoute un port, prends la requête et renvoit une réponse http

## Demo / Exercice : démarrer Apache et Nginx

### Démarrer un serveur httpd sans configuration spécifique

```
docker run --rm -p 80:80 httpd:latest
```

Rendez-vous sur la page [http://localhost](http://localhost) pour voir la page par défaut.

Eteignez ensuite le serveur en utilisant `Ctrl+C` dans votre ligne de commande dans laquelle le serveur a été lancé.

### Démarrer un serveur nginx sans configuration spécifique

```
docker run --rm -p 80:80 nginx:latest
```

Rendez-vous sur la page [http://localhost](http://localhost) pour voir la page par défaut.

Eteignez ensuite le serveur en utilisant `Ctrl+C` dans votre ligne de commande dans laquelle le serveur a été lancé.

## Demo / Exercice : servir une page html statique

L'exercice consiste à utiliser notre propre page html à la place de celle par défaut fournie par le serveur web.

Pour cela, étant donné que nous utilisons Docker, nous allons monter notre fichier dans le container créé pour écraser le fichier par défaut.

Dans une production, il faudrait écraser le fichier lors du build, et dans un environnement de développement dans Docker on remplacerait le fichier à la main.

### Apache

Dans le container Apache httpd, le dossier par défaut dans lequel on trouve le fichier `index.html` est `/usr/local/apache2/htdocs`.

```bash
docker run --rm httpd ls -la /usr/local/apache2/htdocs
```

Le fichier `index.html` que l'on veut utiliser contient le contenu suivant :

```html
<!Doctype>  
<html>  
    <head>
        <title>Httpd : Hello World</title>
    </head>
    <body>
        <h1>Httpd</h1>
        <h2>Hello World</h2>
    </body>
</html>
```

Il est disponible dans le dossier `01-101-server-web-theory/demo2`, que nous allons donc monter pour remplacer `/usr/local/apache2/htdocs` dans le container.

```bash
docker run --rm -p 80:80 -v $(pwd)/01-101-server-web-theory/demo2:/usr/local/apache2/htdocs httpd
```

Ouvrez votre navigateur web sur l'url [http://localhost](http://localhost) et vous devriez voir votre page.

### Nginx

Dans le container Apache httpd, le dossier par défaut dans lequel on trouve le fichier `index.html` est `/usr/share/nginx/html`.

```bash
docker run --rm nginx ls -la /usr/share/nginx/html
```

Le fichier `index.html` que l'on veut utiliser contient le contenu suivant :

```html
<!Doctype>  
<html>  
    <head>
        <title>Nginx : Hello World</title>
    </head>
    <body>
        <h1>Nginx</h1>
        <h2>Hello World</h2>
    </body>
</html>
```

Il est disponible dans le dossier `01-101-server-web-theory/demo3`, que nous allons donc monter pour remplacer `/usr/share/nginx/html` dans le container.

```bash
docker run --rm -p 80:80 -v $(pwd)/01-101-server-web-theory/demo3:/usr/share/nginx/html:ro nginx
```

Ouvrez votre navigateur web sur l'url [http://localhost](http://localhost) et vous devriez voir votre page.

## DocumentRoot

Les dossiers dans lesquels nous avons fait les volumes Docker dans le chapitre précédent sont les `DocumentRoot` ou `root`, c'est à dire la racine du projet exposé par le serveur http.

Pour trouver ces chemins, il faut donc trouver la configuration du serveur web, dans laquelle ces racines sont indiquées.

### Apache

Dans le container httpd la configuration se trouve dans `/usr/local/apache2/conf/httpd.conf` d'après la documentation disponible sur le [Docker Hub de l'image httpd](https://hub.docker.com/_/httpd/).

```bash
docker run --rm httpd cat /usr/local/apache2/conf/httpd.conf
```

Comme vous pouvez le constater la documentation d'Apache httpd est assez longue (et commentée). Parmis toutes les options et configurations, nous sommes uniquement intéressé par le `DocumentRoot` pour le moment.

Vous pouvez donc utiliser la commande suivante pour filtrer uniquement la valeur de la racine :

```bash
docker run --rm httpd cat /usr/local/apache2/conf/httpd.conf | grep DocumentRoot
```

Il est donc maintenant possible de surcharger cette configuration avec notre configuration personnalisée.

Le contenu de la configuration du container a été copié dans le dossier `01-101-server-web-theory/demo4/config` grâce à la commande suivante :

```bash
docker run --rm httpd cat /usr/local/apache2/conf/httpd.conf > 01-101-server-web-theory/demo4/config/httpd.conf
```

Dans le fichier `01-101-server-web-theory/demo4/config/httpd.conf`, la valeur de `DocumentRoot` a été changé pour `/code` :

```xml
DocumentRoot "/code"
<Directory "/code">
    ...
</Directory>    
```

Notez que la valeur de l'instruction `Directory` suivante est aussi mise à jour, car elle défini les règles d'exécution pour ce répertoire.

Il reste ensuite à monter notre fichier html dans le dossier `/code` et notre configuration dans le dossier `/usr/local/apache2/conf/httpd.conf`.

```
docker run --rm -p 80:80 -v $(pwd)/01-101-server-web-theory/demo4/config/httpd.conf:/usr/local/apache2/conf/httpd.conf:ro -v $(pwd)/01-101-server-web-theory/demo4/html:/code:ro httpd
```

### Nginx

Dans le container nginx la configuration se trouve dans `/etc/nginx/nginx.conf` d'après la documentation disponible sur le [Docker Hub de l'image nginx](https://hub.docker.com/_/nginx/).

```bash
docker run --rm nginx cat /etc/nginx/nginx.conf
```

Comme vous pouvez le constater la documentation de nginx est assez courte (et non commentée). Parmis toutes les options et configurations, nous sommes uniquement intéressé par le `include /etc/nginx/conf.d/*.conf;` pour le moment. Celui-ci nous indique que les fichiers de configuration du dossier `conf.d` sont chargés automatiquement.

```bash
docker run --rm nginx ls /etc/nginx/conf.d
```

> default.conf

```bash
docker run --rm nginx cat /etc/nginx/conf.d/default.conf
```

Comme vous pouvez le constater, ce fichier contient les lignes suivantes :

```json
location = / {  
    root   /usr/share/nginx/html;  
}
```

Il est donc maintenant possible de surcharger cette configuration avec notre configuration personnalisée.

Le contenu de la configuration du container a été copié dans le dossier `01-101-server-web-theory/demo5/config` grâce à la commande suivante :

```bash
docker run --rm nginx cat /etc/nginx/conf.d/default.conf > 01-101-server-web-theory/demo5/config/default.conf
```

Dans le fichier `01-101-server-web-theory/demo5/config/default.conf`, la valeur de `root` a été changé pour `/code` :

```json
location = / {  
    root   /code;  
}   
```

Il reste ensuite à monter notre fichier html dans le dossier `/code` et notre configuration dans le dossier `/etc/nginx/conf.d/`.

```
docker run --rm -p 80:80 -v $(pwd)/01-101-server-web-theory/demo5/config/default.conf:/etc/nginx/conf.d/default.conf:ro -v $(pwd)/01-101-server-web-theory/demo5/html:/code:ro nginx
```

## Conclusion

Dans ce chapitre, nous avons vu les bases des serveurs web, comment charger une page html statique et comment personnaliser la configuration de sorte à mettre notre projet à l'endroit qui nous convient sur la machine.

Si vous utilisez une solution pre-packagé (WAMP, MAMP, etc.), je vous invite à aller consulter les fichiers de configuration pour mieux comprendre comment ces ensembles applicatifs fonctionnent.

Le chapitre suivant couvrira une technique permettant de servir des pages différentes selon l'origine de la requête à l'aide des [virtualhost](02-virtualhost).

