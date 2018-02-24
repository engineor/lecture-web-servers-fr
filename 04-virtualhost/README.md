# Virtualhost

Prérequis : 

- docker installé et fonctionnel
- docker-compose installé et fonctionnel
- savoir éditer son fichier host

Pratique :

- avoir `nginx:latest` (`docker pull nginx:latest`)
- avoir `php:7.2-fpm` (`docker pull php:7.2-fpm`)

## Démarrer un nginx sans configuration spécifique

`docker run --rm -p 80:80 nginx:latest`

## Exposer un fichier `index.html` :

### Lire la config *(découverte du document root)*
`docker run --rm nginx:latest cat /etc/nginx/conf.d/default.conf`

### Monter le document root en volume

#### Fichier `demo1/index.html`
```
<!Doctype html>
<html>
	<head>
		<title>Nginx demo</title>
	</head>
	<body>
		<h1>Nginx demo</h1>
	</body>
</html>
```

### Charger le dossier `demo1` dans le container

`docker run --rm -p 80:80 -v $(pwd)/demo1:/usr/share/nginx/html nginx:latest`

## Changer le document root

### Monter le document root en volume

#### Fichier `demo2/nginx/default.conf`

```
server {
    listen       80;
    server_name  localhost;

    location / {
        root   /root;
    }
}
```

#### Fichier `demo2/public/index.html`

```
<!Doctype html>
<html>
	<head>
		<title>Nginx demo 2</title>
	</head>
	<body>
		<h1>Nginx demo 2</h1>
	</body>
</html>
```

### Charger le dossier `demo2` (`nginx` et `public`) dans le container

`docker run --rm -p 80:80 -v $(pwd)/demo2/nginx:/etc/nginx/conf.d/ -v $(pwd)/demo2/public/:/root nginx:latest`


## Virtualhost basé sur le nom
## Virtualhost basé sur l'adresse