# Bases de données : communication et réplication

## Socket

## Network

## Sécurité

### Principe de moindre privilège

- niveau réseau / firewall / subnetworks (ip whitelisting, etc.)
- niveau base (accès à une seule base, seulement sur les actions nécéssaires)
- niveau table (accès à une seule base, seulement sur les actions nécéssaires)

### Accès en lecture seule

## Performance

### Stockage

- memoire vs filesystem
- logs et disques séparés (différent types de logs, données, etc). Limiter les accès concurrents.

### Replication

- accès en lecture seule pour consultation
- accès en lecture seule pour reporting