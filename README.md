# Cours : Serveurs web

[![Build Status](https://travis-ci.org/engineor/lecture-web-servers-fr.svg?branch=master)](https://travis-ci.org/engineor/lecture-web-servers-fr)

Ce cours en français est conçu à destination d'élèves de 5ème année à l'[IPSSI](https://www.ecole-ipssi.com/). Il a cependant vocation à évoluer, comme indiqué à la fin de cette documentation (rubrique `Contribuer`).

Le contenu et les exemples sont principalement basés sur PHP et son écosystème, bien que les concepts soient les mêmes avec tous les langages et systèmes d'exploitation.

## Plan du cours

0. [Prérequis](00-prerequisites)
1. [Web, requête http et serveurs web, les bases](01-101-server-web-theory)
2. [Virtualhost : mettre plusieurs sites sur un même serveur](02-virtualhost)
3. [Executer PHP avec Apache httpd, les stratégies disponibles](03-php-apache-httpd)
4. [Mettre du contenu dynamique dans une page web avec CGI](04-cgi)
5. [Mettre du contenu dynamique dans une page web avec FastCGI](05-fastcgi)
6. [Executer PHP avec différents utilisateurs](06-php-multitenant)
7. [Executer différentes versions de PHP dans le cadre d'une requête web](07-php-multiple-versions)
8. [Rendre l'execution de PHP évolutive (scalable)](08-php-scalability)
9. [Sécurité : les concepts de base](09-security)
10. [Bases de données : communication et réplication](10-databases)
11. [L'hébergement web](11-web-hosting)

## Contribuer

Pour contribuer, merci de faire un fork puis une PR directement sur la master.

Toute contribution doit être intégralement rédigée en français.

Pour chaque proposition, il faut inclure à la fois la théorie et la pratique associée

Les exemples doivent :

- être basés sur Docker, de préférence sur une ou des images déjà utilisées dans les autres exercices / démos
- être réalisables en copiant collant les lignes sans réfléchir
- être facilement lisible, les extraits de code long (fichiers html) doivent être extraits et mis dans des dossiers `demoX`
- contenir des commandes et des images dont les liens sont relatifs à la racine du projet

Toutes ces règles sont ici à titre d'indication, toute PR est la bienvenue mais ces règles seront discutées dans les PR respectivement.
