### Vinny expres

[![CI](https://github.com/matofeder/vinnyexpres/actions/workflows/ci.yml/badge.svg)](https://github.com/matofeder/vinnyexpres/actions/workflows/ci.yml)
[![Release](https://github.com/matofeder/vinnyexpres/actions/workflows/release.yml/badge.svg)](https://github.com/matofeder/vinnyexpres/actions/workflows/release.yml)

Basic flask web for https://vinny-expres.sk/

#### Run

```bash
$ pip install .
$ uwsgi --http 0.0.0.0:5000 uwsgi.ini
```

#### Run in development mode (autoreload)

```bash
$ uwsgi --http 0.0.0.0:5000 uwsgi.ini --py-autoreload 1
```

#### Apache and Docker (legacy)

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

#### Container image

The root `Dockerfile` builds the image used in Kubernetes: uwsgi speaks plain HTTP on **8080**, runs as uid
10001 and works with a read-only root filesystem.

```bash
$ docker build -t vinnyexpres .
$ docker run --rm -p 8080:8080 --env-file .env vinnyexpres     # http://localhost:8080
```

#### Release

Releases are git tags `vMAJOR.MINOR.PATCH`. Pushing one runs `.github/workflows/release.yml`, which publishes,
in this order (each step only if the previous one succeeded):

1. image `ghcr.io/matofeder/vinnyexpres:X.Y.Z` (+ `X.Y`, `X`, `latest`), linux/amd64 + linux/arm64,
2. Helm chart `oci://ghcr.io/matofeder/charts/vinnyexpres` version `X.Y.Z`, appVersion `X.Y.Z` (runs image `X.Y.Z`),
3. the GitHub Release for the tag with auto-generated notes. Tags like `v1.3.0-rc.1` become pre-releases.

```bash
$ git switch main && git pull --ff-only
$ gh run list --workflow ci.yml --branch main --limit 1      # last CI must be green
$ VERSION=1.0.0
$ git tag -a "v$VERSION" -m "v$VERSION" && git push origin "v$VERSION"
$ gh run watch "$(gh run list --workflow release.yml --limit 1 --json databaseId --jq '.[0].databaseId')" --exit-status
```

Pull requests only build the image; pushes to `main` never publish anything. Don't move a published tag,
release the next patch instead.

#### Kubernetes (Helm)

The chart lives in `charts/vinnyexpres` (Deployment with 2 non-root replicas, Service, optional Ingress,
PodDisruptionBudget). The contact form needs the Gmail app password in a Secret:

```bash
$ NS=vinnyexpres
$ kubectl create namespace $NS
$ kubectl -n $NS create secret generic vinnyexpres-email --from-literal=EMAIL_FROM_PASS='<gmail app password>'
```

```yaml
# values-prod.yaml
email:
  to: info@example.com            # comma separated
  from: your-account@gmail.com
  existingSecret: vinnyexpres-email
ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt
  hosts:
    - host: vinny-expres.sk
      paths: [{ path: /, pathType: Prefix }]
    - host: www.vinny-expres.sk
      paths: [{ path: /, pathType: Prefix }]
  tls:
    - secretName: vinny-expres-sk-tls
      hosts: [vinny-expres.sk, www.vinny-expres.sk]
```

```bash
$ helm upgrade --install vinnyexpres oci://ghcr.io/matofeder/charts/vinnyexpres \
    --version "$VERSION" -n $NS -f values-prod.yaml --wait
$ helm -n $NS rollback vinnyexpres                            # previous revision
```

If the ghcr.io package is private, create a `docker-registry` pull secret and set
`imagePullSecrets: [{name: ghcr-pull}]`. All options: `charts/vinnyexpres/values.yaml`.
`Chart.yaml` stays at `0.0.0-dev`; the release workflow sets both versions from the tag.
