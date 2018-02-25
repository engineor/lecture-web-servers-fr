# Virtualhost

Le principe des virtualhosts, ou serveurs virtuels en français, est de permettre l'hébergement de plusieurs sites web sur un même serveur, sur une même machine.

Pour savoir quelle page servir, nous aurons la possibilité de différencier les requêtes sur le nom ou sur l'IP.

Les exemples disponibles sur cette page peuvent être reproduits en utilisant le fichier `hosts` de votre ordinateur pour faire pointer les noms sur votre container.

## Virtualhost basé sur le nom

Pour les virtualhosts basés sur le nom, il faut éditer votre fichier `hosts` : `/etc/hosts` ou `C:\Windows\System32\drivers\etc`.

Ajoutons une ligne pour que `http://demo-vhost` pointe sur notre propre machine :

```
127.0.0.1    localhost
127.0.0.1    demo-vhost
```

### Apache httpd

Comme dans [le chapitre précédent](01-101-server-web-theory), il s'agit de démarrer Apache httpd avec une configuration personnalisée. En regardant dans le fichier `httpd.conf`, on retrouve les lignes suivantes :

```
docker run --rm httpd cat /usr/local/apache2/conf/httpd.conf | grep vhost
```

> \#LoadModule vhost_alias_module modules/mod_vhost_alias.so
> \#Include conf/extra/httpd-vhosts.conf

Dans notre cas, nous voulons utiliser les configurations complémentaires pour les virtualhosts, et allons donc décommenter la ligne `Include`.

> Include conf/extra/httpd-vhosts.conf

À noter, il est possible d'utiliser un joker (*wildcard*), ici \* pour charger plusieurs fichiers de configuration d'hôtes virtuels, par exemple `Include vhosts/*.conf`.

Pour cette démonstration, nous avons copié le fichier de configuration (`conf/extra/httpd-vhosts.conf`) dans le dossier `02-virtualhost/demo1/config` avec la commande suivante :

```
docker run --rm httpd cat /usr/local/apache2/conf/extra/httpd-vhosts.conf > 02-virtualhost/demo1/config/httpd-vhosts.conf
```

Ces configurations par défaut sont basés sur les noms. On retrouve donc une directive `ServerName` dans chaque `VirtualHost`, ainsi que l'accès au `VirtualHost` pour n'importe quelle adresse IP (`*:80`).

```apache
<VirtualHost *:80>
    ServerAdmin webmaster@dummy-host.example.com
    DocumentRoot "/usr/local/apache2/docs/dummy-host.example.com"
    ServerName dummy-host.example.com
    ServerAlias www.dummy-host.example.com
    ErrorLog "logs/dummy-host.example.com-error_log"
    CustomLog "logs/dummy-host.example.com-access_log" common
</VirtualHost>

<VirtualHost *:80>
    ServerAdmin webmaster@dummy-host2.example.com
    DocumentRoot "/usr/local/apache2/docs/dummy-host2.example.com"
    ServerName dummy-host2.example.com
    ErrorLog "logs/dummy-host2.example.com-error_log"
    CustomLog "logs/dummy-host2.example.com-access_log" common
</VirtualHost>
```

Il faut donc modifier cette configuration pour utiliser nos noms :

```apache
<VirtualHost *:80>
    DocumentRoot "/usr/local/apache2/htdocs/demo-vhost"
    ServerName demo-vhost
</VirtualHost>

<VirtualHost *:80>
    DocumentRoot "/usr/local/apache2/htdocs/localhost"
    ServerName localhost
</VirtualHost>
```

Des fichiers html sont disponibles dans `02-virtualhost/demo1/html/localhost` et `02-virtualhost/demo1/html/demo-vhost`.

```
docker run --rm -p 80:80 -v $(pwd)/02-virtualhost/demo1/config/httpd.conf:/usr/local/apache2/conf/httpd.conf:ro -v $(pwd)/02-virtualhost/demo1/config/httpd-vhosts.conf:/usr/local/apache2/conf/extra/httpd-vhosts.conf:ro -v $(pwd)/02-virtualhost/demo1/html:/usr/local/apache2/htdocs:ro httpd
```

Vous pouvez maintenant accèder aux différents sites avec les adresses [http://localhost](http://localhost) et [http://demo-vhost](http://demo-vhost).

### Nginx

Comme pour Apache httpd ci-dessus, il est possible de créer des hôtes virtuels sur Nginx. Ces hôtes virtuels sont appelés `server blocks`.

La configuration Nginx, qui pour mémoire est disponible à l'adresse `/etc/nginx/nginx.conf` dans l'image Nginx, est la suivante :

```
docker run --rm nginx:latest cat /etc/nginx/nginx.conf
```

```json
user  nginx;
worker_processes  1;

error_log  /var/log/nginx/error.log warn;
pid        /var/run/nginx.pid;


events {
    worker_connections  1024;
}


http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    keepalive_timeout  65;

    #gzip  on;

    include /etc/nginx/conf.d/*.conf;
}
```

La dernière ligne indique de charger n'importe quel fichier de configuration existant dans le dossier `conf.d`.

```
docker run --rm nginx:latest ls /etc/nginx/conf.d
```

>default.conf

```
docker run --rm nginx:latest cat /etc/nginx/conf.d/default.conf
```

```json
server {
    listen       80;
    server_name  localhost;

    #charset koi8-r;
    #access_log  /var/log/nginx/host.access.log  main;

    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
    }

    #error_page  404              /404.html;

    # redirect server error pages to the static page /50x.html
    #
    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }

    # proxy the PHP scripts to Apache listening on 127.0.0.1:80
    #
    #location ~ \.php$ {
    #    proxy_pass   http://127.0.0.1;
    #}

    # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
    #
    #location ~ \.php$ {
    #    root           html;
    #    fastcgi_pass   127.0.0.1:9000;
    #    fastcgi_index  index.php;
    #    fastcgi_param  SCRIPT_FILENAME  /scripts$fastcgi_script_name;
    #    include        fastcgi_params;
    #}

    # deny access to .htaccess files, if Apache's document root
    # concurs with nginx's one
    #
    #location ~ /\.ht {
    #    deny  all;
    #}
}
```

L'illustration ci-dessus montre un `server block`. On retrouve dedans la clé `server_name` (nom du serveur), qui est donc similaire au `ServerName` d'Apache httpd.

Remplaçons cette configuration par une configuration personnalisée. Nous utiliserons un fichier par hôte virtuel :

localhost.conf:

```json
server {
    listen       80;
    server_name  localhost;

    location / {
        root   /usr/share/nginx/html/localhost;
        index  index.html;
    }
}
```

demo-vhost.conf

```json
server {
    listen       80;
    server_name  demo-vhost;

    location / {
        root   /usr/share/nginx/html/demo-vhost;
        index  index.html;
    }
}
```

```
docker run --rm -p 80:80 -v $(pwd)/02-virtualhost/demo2/config:/etc/nginx/conf.d -v $(pwd)/02-virtualhost/demo2/html:/usr/share/nginx/html nginx:latest
```


## Virtualhost basé sur l'adresse

Pour des raisons techniques, nous ne verrons pas l'utilisation d'hôtes virtuels basés sur les IP.

De manière générale, le fonctionnement est similaire à celui décrit ci-dessus pour les noms, sauf que la configuration se fait au niveau réseau, c'est à dire dans le tag `VirtualHost` pour Apache httpd :

```
<VirtualHost adresse_ip:80>
	DocumentRoot "/usr/local/apache2/htdocs/adresse_ip"
</VirtualHost>
```


## Conclusion

Il existe plusieurs façons de faire coexister des sites sur un même serveur. En plus des solutions vues ici, on peut penser au mode `userdir` d'Apache httpd qui permets d'exposer des dossiers dans un répertoire spécifique de chaque utilisateur du système (traditionnellement `public_html`), mais de manière générale ces solutions sont laissées à l'écart en faveur de solutions plus modernes et plus containerisées.

Maintenant que nous avons bien compris les différentes configurations possible permettant d'exposer des sites statiques, nous allons voir comment [rendre les sites dynamiques avec PHP sur Apache httpd](03-php-apache-httpd).