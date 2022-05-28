FROM nginx:stable

RUN apt-get update \
 && apt-get install --no-install-recommends --no-install-suggests -y gnupg1 apt-transport-https ca-certificates wget \
 && wget -O /etc/apt/trusted.gpg.d/php.gpg https://packages.sury.org/php/apt.gpg \
 && echo 'deb https://packages.sury.org/php/ stretch main' > /etc/apt/sources.list.d/deb.sury.org.list \
 && apt-get update \
 && apt-get install --no-install-recommends --no-install-suggests -y php7.2-fpm php5.6-fpm
