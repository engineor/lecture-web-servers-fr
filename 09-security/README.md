# Sécurité : les concepts de base

- Réseau :
  - firewall
  - réseau virtuel ([AWS VPC](https://aws.amazon.com/fr/vpc/), [OVH vRack](https://www.ovh.com/fr/solutions/vrack/))
  - https
- Filesystem
  - read only
  - object storage
- Serveur
  - hardening (less software, specific servers, chown and chmod, limit multitenants, 2FA)
  - http
     - Directory/Filematch et deny
     - location et deny  all;

```
<Files ".ht*">
    Require all denied
</Files>
```

```
location ~ /\.ht {
    deny  all;
}
```