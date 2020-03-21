Simple nginx setup with full vhosts flexibility
===============================================

The role does install main nginx conf file, but the vhost configs shall be provided by the user in the form
of a template. The current vhost config is passed into the template as `item` var.

```
nginx_vhosts:
  - name: name_of_host
    config_template: "shared/nginx/vhost.conf"
```

## Special feature

The role makes sure that there are no other vhosts than configured. This means that when you remove or rename
a vhost you don't have to clean it up manually on the server.

You can disable this feature with `nginx_remove_extra_vhosts: no`

## Other vars 

Look into `defaults/main.yml`.

## Example vhost file for a PHP app with front controller

```jinja
server {
    listen 80;
    server_name {{ item.hostname }} www.{{ item.hostname }};
    return 301 https://{{ item.hostname }}$request_uri;
}

server {
    listen 443 ssl http2;

    server_name {{ item.hostname }};

    root {{ item.public_dir }};

    index index.php index.html;

    access_log {{ item.log_dir }}/access.log;
    error_log {{ item.log_dir }}/error.log error;

    ssl_certificate {{ nginx_cert_directory }}/{{ item.ssl_cert | basename }};
    ssl_certificate_key {{ nginx_cert_directory }}/{{ item.ssl_key | basename }};

    location / {
        try_files $uri /front_controller_script_name.php$is_args$args;
    }

    location ~ ^/front_controller_script_name\.php(/|$) {
        fastcgi_pass 127.0.0.1:9000;
        fastcgi_split_path_info ^(.+\.php)(/.*)$;
        include fastcgi_params;

        fastcgi_param SCRIPT_FILENAME $realpath_root$fastcgi_script_name;
        fastcgi_param DOCUMENT_ROOT $realpath_root;

        internal;
    }
}
```


