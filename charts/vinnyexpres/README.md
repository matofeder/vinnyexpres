# vinnyexpres

Helm chart for [vinny-expres.sk](https://vinny-expres.sk): the Flask app served by uwsgi (plain HTTP on 8080).
Chart version = app version = image tag.

```sh
kubectl create namespace vinnyexpres
kubectl -n vinnyexpres create secret generic vinnyexpres-email --from-literal=EMAIL_FROM_PASS='<gmail app password>'

helm upgrade --install vinnyexpres oci://ghcr.io/matofeder/charts/vinnyexpres --version <X.Y.Z> \
  -n vinnyexpres -f values-prod.yaml --wait
```

`values-prod.yaml` and every option: see the repository [README](https://github.com/matofeder/vinnyexpres#kubernetes-helm).
