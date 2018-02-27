# Rendre l'execution de PHP évolutive (scalable)

## Multiplier les workers PHP avec Nginx

### Demo 1 : laisser faire docker

```
version: "3.3"
services:
    app:
        image: nginx:latest
        ports:
            - 80:80
        volumes:
            - ./html:/var/www/html:ro
    php:
        image: php:7.2-fpm
        ports:
            - 9000
        volumes:
            - ./html:/var/www/html
```

```
docker-compose -f 08-php-scalability/demo1/docker-compose.yml up -d --scale php=3
```

Rechargez la page pour voir changer la ligne `System`.

Dans ce cas précis, Docker (docker-compose et son réseau privé) s'occupe de distribuer sur les 3 containers PHP.

### Demo 2 : configurer Nginx

Manuellement, il faut changer la config Nginx (voir fichiers demo2)

```
docker-compose -f 08-php-scalability/demo2/docker-compose.yml up -d
```

## Sessions

Voir demo3 pour le problème

Voir demo4 pour la solution avec Redis en session handler

## Génération de fichiers

Read only file system + data volume

## Varnish

Si vous désirez tester une installation incluant un cache http (varnish), rendez-vous sur ce tutoriel : [https://blog.nicolargo.com/2014/10/infra-lemp-docker.html](https://blog.nicolargo.com/2014/10/infra-lemp-docker.html)