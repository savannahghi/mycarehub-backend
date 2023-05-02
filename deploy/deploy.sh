#!/usr/bin/env sh

set -eux

# Create the namespace
kubectl create namespace $NAMESPACE || true

# Delete Kubernetes secret if exists
kubectl delete secret mycarehub-backend-service-account --namespace $NAMESPACE || true
# kubectl delete secret mycarehub-secrets  --namespace $NAMESPACE || true

# Create GCP service account file
cat $GOOGLE_APPLICATION_CREDENTIALS >> ./service-account.json

# Recreate service account file as Kubernetes secret
kubectl create secret generic mycarehub-backend-service-account  \
    --namespace $NAMESPACE \
    --from-file=key.json=./service-account.json

helm upgrade \
    --install \
    --debug \
    --create-namespace \
    --namespace "${NAMESPACE}" \
    --set service.port="${PORT}" \
    --set app.replicaCount="${APP_REPLICA_COUNT}" \
    --set app.container.image="${DOCKER_IMAGE_TAG}" \
    --set app.container.env.googleCloudProject="${GOOGLE_CLOUD_PROJECT}"\
    --set app.container.env.settingsName="${SETTINGS_NAME}"\
    --set app.container.env.databaseInstanceConnectionName="${DB_INSTANCE_NAME}"\
    --set app.container.env.djangoSettingsModule="${DJANGO_SETTINGS_MODULE}"\
    --set app.container.env.defaultOrgId="${DEFAULT_ORG_ID}"\
    --set networking.issuer.name="letsencrypt-prod"\
    --set networking.issuer.privateKeySecretRef="letsencrypt-prod"\
    --set networking.ingress.host="${APPDOMAIN}"\
    --wait \
    --timeout 900s \
    -f ./charts/mycarehub-backend/values.yaml \
    $APPNAME \
    ./charts/mycarehub-backend
