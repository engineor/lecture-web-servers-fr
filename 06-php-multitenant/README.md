# Executer PHP avec différents utilisateurs

Dans le chapitre précédent, nous avons vu l'utilisation de PHP-FPM pour executer PHP. En se basant sur le même concept, ce chapitre va montrer la mise en place d'un serveur web multi-site et multi-utilisateurs.

## Nginx comme pure proxy

La première méthode va consister à utiliser Nginx uniquement comme un proxy vers les différents PHP-FPM.

Cette méthode, bien que fonctionnelle pour des fichiers PHP, ne nous permettra pas de charger des fichiers statiques sans passer par le container php-fpm.

Les fichiers disponibles dans `06-php-multitenant/demo1` sont basés sur ceux de la démo Nginx du chapitre hôtes virtuels et ceux du chapitre FastCGI.

```
server {
    listen       80;
    server_name  demo-vhost;

    location / {
        fastcgi_pass   php-demo-vhost:9000;
        fastcgi_index  index.php;
        fastcgi_param  SCRIPT_FILENAME  /scripts$fastcgi_script_name;
        include        fastcgi_params;
    }
}

server {
    listen       80;
    server_name  localhost;

    location / {
        fastcgi_pass   php-localhost:9000;
        fastcgi_index  index.php;
        fastcgi_param  SCRIPT_FILENAME  /scripts$fastcgi_script_name;
        include        fastcgi_params;
    }
}
```

```
docker run --name php-localhost --user www-data -d --rm -p 9000 -v $(pwd)/06-php-multitenant/demo1/html/localhost:/scripts php:7.2-fpm
```

```
docker run --name php-demo-vhost --user nobody -d --rm -p 9000 -v $(pwd)/06-php-multitenant/demo1/html/demo-vhost:/scripts php:7.2-fpm
```

**Attention, les dossiers ci-dessus ne sont pas `:ro`**

```
docker run --rm -p 80:80 -v $(pwd)/06-php-multitenant/demo1/config:/etc/nginx/conf.d nginx:latest
```

Ici, les fichiers sont utilisés sur les containers, donc non accessibles d'un utilisateur à l'autre. On utilise par ailleurs des utilisateurs différent pour lancer le process Nginx.

## Un seul container Nginx + php

Pour cet exemple, on va utiliser un seul container Nginx + PHP.

```
FROM nginx:latest

RUN groupadd site1 &&  useradd -g site1 site1 && \
    groupadd site2 &&  useradd -g site2 site2

...
```

Pour le reste, il faut configurer des pools dans php-fpm comme indiqué dans cet article [https://www.digitalocean.com/community/tutorials/how-to-host-multiple-websites-securely-with-nginx-and-php-fpm-on-ubuntu-14-04](https://www.digitalocean.com/community/tutorials/how-to-host-multiple-websites-securely-with-nginx-and-php-fpm-on-ubuntu-14-04).

Les dossiers contenant les sites (`root` déclarés dans les server blocks) doivent être lisible par l'utilisateur qui lance Nginx :

```
docker run --rm nginx cat /etc/nginx/nginx.conf
```

> user  nginx;

[Documentation Nginx user (et groupe)](http://nginx.org/en/docs/ngx_core_module.html#user)

Il faut donc ajouter un groupe (`www-data` ?) dans la configuration, puis donner les droits en lecture sur les document roots à `www-data` pour la lecture, et les utilisateurs `site1` et `site2` en écriture.

Il faut ensuite configurer les pools FPM pour qu'ils s'éxecutent en tant que `site1` et `site2`.

**Attention** : mettre `site1` ou `site2` dans le groupe `www-data` ouvrirait une faille de sécurité, car `site2` aurait la possibilité de venir lire les fichiers de `site1`.

## Conclusion

Dans ce chapitre nous avons vu comment utiliser PHP-FPM pour faire un serveur multi-utilisateurs.

Le chapitre suivant couvre une autre possibilité : un serveur avec [plusieurs versions de PHP](/07-php-multiple-version).