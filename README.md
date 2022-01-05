### Vinny expres

Basic flask web for Vinny expres

#### Run

```bash
$ pip install .
$ uwsgi --http 0.0.0.0:5000 uwsgi.ini
```

#### Run in development mode (autoreload)

```bash
$ uwsgi --http 0.0.0.0:5000 uwsgi.ini --py-autoreload 1
```

#### Apache and Docker

Run web in docker container

```bash
$ docker-compose -f docker/docker-compose.yml up -d
```

Install apache mod-proxy-uwsgi and enable vinny-expres.sk.conf

```bash
$ apt-get install -y libapache2-mod-proxy-uwsgi
$ cp apache/vinny-expres.sk.conf /etc/apache2/sites-available
$ a2ensite vinny-expres.sk.conf
```
