FROM php:8.3.0-fpm-alpine

COPY --from=composer:latest /usr/bin/composer /usr/local/bin/composer

WORKDIR /var/www

RUN apk add --no-cache \
    bash \
    $PHPIZE_DEPS \
    linux-headers
