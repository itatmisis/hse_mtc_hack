# deep misis | HSE-MTS Hack

## PSA

All further commits by 0xb1b1 are to be available in [0xb1b1/telewatcher](https://github.com/0xb1b1/telewatcher).

## Deploy the service

### Docker Compose

```bash
docker compose up -d
```

### Kubernetes

Apply all files inside `kube-common`, then apply all microservices' K8s files (typically located in `<microservice name>/kube`)

### Helm

Coming soon (see PSA)
