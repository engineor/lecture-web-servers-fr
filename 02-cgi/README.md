# Un site dynamique avec CGI

## Qu'est-ce que CGI - Common Gateway Interface

### Définition

D'après [Wikipedia](https://fr.wikipedia.org/wiki/Common_Gateway_Interface) :

>La Common Gateway Interface (littéralement « Interface de passerelle commune »), généralement abrégée CGI, est une interface utilisée par les serveurs HTTP. Elle a été normalisée par la RFC 38751.

![](02-cgi/images/cgi-wikipedia.png)

La CGI permets donc au serveur http de lancer l'exécution d'un logiciel sur la machine et d'en récupérer le résultat.

![](02-cgi/images/cgi-sequence.png)

### Limitations

La CGI créé un nouveau processus sur la machine à chaque requête, ce qui a donc un coup d'exécution assez lourd.

Elle ne permet pas non plus une gestion granulaire des droits, les scripts étant executés avec l'utilisateur du serveur http.

Enfin, elle ne permets pas une évolutivité horizontale, car les processus sont créés sur la machine du serveur http.

### TL;DR

La Common Gateway Interface permet d'ajouter au serveur http la capacité d'utiliser un logiciel.

Facile à mettre en place et pratique pour un site à forte charge, elle est lente et lourde et ne permets pas une évolutivité horizontale.

## Créer l'environnement

Pour commencer, nous allons construire un environnement contenant :

- Apache httpd
- Python3
- PHP (version 5 cgi pour faire simple)
- Apache httpd mod_cgi actif

### L'image Docker

Pour se faire, en partant de l'image Docker `httpd:latest`, nous allons utiliser un Dockerfile pour ajouter `python3`, `php5-cgi` et le mode CGI qui manquent à notre liste.

```
FROM httpd:latest

RUN apt-get update && apt-get install -y python3 php5-cgi
```

Ce fichier est disponible dans le dossier `02-cgi/config`, et nous appellerons l'image `serveur-web-cgi`.

```
docker build -t serveur-web-cgi 02-cgi/config
```

Nous pouvons maintenant utiliser l'image `serveur-web-cgi` qui contient les executables pour PHP et python :

```
docker run --rm serveur-web-cgi which php-cgi
```

>/usr/bin/php-cgi

```
docker run --rm serveur-web-cgi which python3
```

>/usr/bin/python3

```
docker run --rm serveur-web-cgi ls /usr/local/apache2/modules/mod_cgi.so
```

>/usr/local/apache2/modules/mod_cgi.so

### Configuration d'Apache httpd

Le mode CGI est activé sur Apache httpd, comme énoncé dans les instructions précédemment énoncées.

L'image `serveur-web-cgi` étant basé sur `httpd:latest`, les configurations se trouvent dans les répertoires indiqués dans le chapitre [Théorie des serveurs web](01-101-server-web-theory)

Dans le fichier `httpd.conf`, il faut trouver la ligne `#LoadModule cgi_module modules/mod_cgi.so` et la décommenter (enlever le `#`).

La configuration que nous allons charger devra donc contenir cette version modifiée du fichier `httpd.conf`. Ce fichier changera selon les exemples, on le créera donc dans chaque section à venir.

## Demo / Exercice : écriture d'un CGI servant une page simple

### Afficher une page HTML simple

Le fichier de configuration modifié est disponible dans le dossier `02-cgi/config`, avec `mod_cgi` activé.

Les configurations à changer sont les suivantes :

```apache
LoadModule mpm_event_module modules/mod_mpm_event.so
#LoadModule mpm_prefork_module modules/mod_mpm_prefork.so

<IfModule mpm_prefork_module>
	#LoadModule cgi_module modules/mod_cgi.so
</IfModule>

LoadModule alias_module modules/mod_alias.so

<IfModule alias_module>
    #
    # ScriptAlias: This controls which directories contain server scripts. 
    # ScriptAliases are essentially the same as Aliases, except that
    # documents in the target directory are treated as applications and
    # run by the server when requested rather than as documents sent to the
    # client.  The same rules about trailing "/" apply to ScriptAlias
    # directives as to Alias.
    #
    ScriptAlias /cgi-bin/ "/usr/local/apache2/cgi-bin/"

</IfModule>

<Directory "/usr/local/apache2/cgi-bin">
    AllowOverride None
    Options None
    Require all granted
</Directory>

<IfModule mime_module>
    #
    # AddHandler allows you to map certain file extensions to "handlers":
    # actions unrelated to filetype. These can be either built into the server
    # or added with the Action directive (see below)
    #
    # To use CGI scripts outside of ScriptAliased directories:
    # (You will also need to add "ExecCGI" to the "Options" directive.)
    #
    #AddHandler cgi-script .cgi
</IfModule>
```

La première chose à faire est de changer le [module multi-processus](https://httpd.apache.org/docs/2.4/fr/mpm.html). En effet, CGI fonctionnant avec des créations de multiples processus, il faut utiliser le mode prefork à la place du mode evènement. Il faut donc commenter la première ligne du script ci-dessus et décommenter la seconde.

Ensuite, il faut activer le `mod_cgi`. Ceci se fait à l'interieur de la condition sur le module prefork activé précedemment.

Les autres configurations ne sont pas à changer pour le moment, mais permettent d'executer des scripts CGI en dehors du dossier défini dans l'alias.

Le fichier `python3` servant à générer la page est disponible dans le dossier `02-cgi/script`. Il doit être executable par l'utilisateur d'Apache httpd (`daemon` dans notre cas).

```python
#!/usr/bin/python3

import cgitb
import getpass
cgitb.enable()

print("Content-Type: text/html;charset=utf-8")
print()

print("<!Doctype html>")
print("<html>")
print("    <head>")
print("        <title>CGI Apache httpd demo Python</title>")
print("    </head>")
print("    <body>")
print("        <h1>CGI Apache httpd demo Python</h1>")
print("        <p>Welcome " + getpass.getuser() + "</p>")
print("    </body>")
print("</html>")
```

Le script CGI Python va juste afficher une page html simple :

```
docker run --rm -v $(pwd)/02-cgi/demo1/config/httpd.conf:/usr/local/apache2/conf/httpd.conf:ro -v $(pwd)/02-cgi/demo1/script/script.py:/usr/local/apache2/cgi-bin/script.py -p 80:80 serveur-web-cgi
```

Rendez-vous donc sur l'url [http://localhost/cgi-bin/script.py](http://localhost/cgi-bin/script.py).

### Afficher une page HTML avec la date courante

Le dossier `02-cgi/demo2` contient les mêmes fichiers que `02-cgi/demo1`, à l'exception du fichier `script/script.py` qui est modifié de sorte à ajouter la date et l'heure courante (à la seconde prêt de sorte à voir le changement en rafraichissant la page).

Voici quelques indications si vous désirez réaliser vous-même le test :

```
# importer la gestion des dates
import datetime

# mettre la date et le temps courants dans une variable
currentTime = datetime.datetime.now()

# créer une string avec la date (utc) en langue naturelle
currentTime.strftime("We are the %d, %b %Y %I:%M:%S %p")
```

### Afficher une page HTML avec formulaire

Pour réaliser cette tâche, vous aurez besoin de cette documentation : [Python 3: Common Gateway Interface support](https://docs.python.org/3/library/cgi.html).


## Demo / Exercice : écriture d'un CGI en php

### Afficher une page HTML simple

De la même façon qu'en Python, il s'agit de créer un script en indiquant le type en début de fichier :

```php
#!/usr/bin/php-cgi

<?php header('Content-Type: text/html;charset=utf-8') ?>
<!Doctype html>
<html>
    <head>
        <title>CGI Apache httpd demo PHP</title>
    </head>
    <body>
        <h1>CGI Apache httpd demo PHP</h1>
        <p>Welcome <?= get_current_user() ?>!</p>
    </body>
</html>
```

```
docker run --rm -v $(pwd)/02-cgi/demo4/config/httpd.conf:/usr/local/apache2/conf/httpd.conf:ro -v $(pwd)/02-cgi/demo4/script/script.php:/usr/local/apache2/cgi-bin/script.php:ro -v $(pwd)/02-cgi/demo4/config/force-redirect.ini:/etc/php5/cgi/conf.d/30-force-redirect.ini:ro -p 80:80 serveur-web-cgi
```

### Afficher une page HTML avec la date courante

Utiliser l'exemple précédent ainsi que les `DateTimeImmutable` pour réaliser cet exemple.

```php
$currentTime = new DateTimeImmutable;
```

```php
<p>We are the <?= $currentTime->format("d, M Y h:i:s A") ?></p>
```

```
docker run --rm -v $(pwd)/02-cgi/demo5/config/httpd.conf:/usr/local/apache2/conf/httpd.conf:ro -v $(pwd)/02-cgi/demo5/script/script.php:/usr/local/apache2/cgi-bin/script.php:ro -v $(pwd)/02-cgi/demo5/config/force-redirect.ini:/etc/php5/cgi/conf.d/30-force-redirect.ini:ro -p 80:80 serveur-web-cgi
```

### Afficher une page HTML avec formulaire

Pour réaliser cette tâche, vous aurez besoin d'utiliser les variables superglobales `$_GET`, `$_POST` ou `$_REQUEST`.

## Demo / Exercice : écriture d'un CGI en C++

### Afficher une page HTML simple

C++ est un langage compilé, il faut donc écrire le script, puis le compiler dans un executable que l'on donnera au CGI.

Le code suivant est disponible dans le fichier `02-cgi/demo7/script/main.cpp` :

```cpp
#include <iostream>
#include <stdlib.h>
using namespace std;
 
int main()
{
	cout<<"Content-type: text/html"<<endl;
    cout<<endl;
    cout<<"<!Doctype>"<<endl;
	cout<<"<html>"<<endl;
    cout<<"    <head>"<<endl;
    cout<<"        <title>CGI Apache httpd demo C++</title>"<<endl;
    cout<<"    </head>"<<endl;
    cout<<"    <body>"<<endl;
    cout<<"        <h1>CGI Apache httpd demo C++</h1>"<<endl;
    cout << getenv("USER") << endl;
    cout<<"    </body>"<<endl;
    cout<<"</html>"<<endl;
 
	return 0;
}
```

Pour le compiler, nous allons utiliser un container docker (`gcc`) et plus précisément le compilateur `g++` :

```
docker run --rm -v $(pwd)/02-cgi/demo7/script:/code -w /code gcc g++ main.cpp -o script.cgi
```

Maintenant que le fichier est compilé dans le binary `02-cgi/demo7/script/script.cgi`, il reste à le monter dans le container docker et tester :

```
docker run --rm -v $(pwd)/02-cgi/demo7/config/httpd.conf:/usr/local/apache2/conf/httpd.conf:ro -v $(pwd)/02-cgi/demo7/script/script.cgi:/usr/local/apache2/cgi-bin/script.cgi:ro -p 80:80 serveur-web-cgi
```

### Afficher une page HTML avec formulaire et nom

Pour réaliser cette tâche, vous aurez besoin de cette documentation : [C++ Web Programming](https://www.tutorialspoint.com/cplusplus/cpp_web_programming.htm)

## Conclusion

Grâce à cette technique, il est possible de créer des scripts et logiciels permettant de rendre dynamique les pages web, et ce dans notre langage de préférence, et de préférence dans le langage le plus performant pour la tâche à réaliser.

Dans le chapitre suivant, nous allons voir une autre technique un peu plus moderne et plus légère : l'[utilisation de FastCGI](03-fastcgi).