#!/bin/bash

set -e  # stop on error

PROD_VNET_PREFIX="10.0.0.0/16"

ENVIRONMENT="prod"
PROJECT="mytestprj"
ACR_NAME="acr${PROJECT}123"

LOCATION="swedencentral"
RESOURCE_GROUP="rg-${PROJECT}-${ENVIRONMENT}-${LOCATION}"


az group create --name $RESOURCE_GROUP --location $LOCATION

az acr create \
  --name $ACR_NAME \
  --resource-group $RESOURCE_GROUP \
  --sku Basic \
  --admin-enabled false \
  --public-network-enabled true \
  --zone-redundancy Disabled \
  --dnl-scope TenantReuse \
  --tags environment=prod project=$PROJECT


az network vnet create \
  --name "vnet-$PROJECT-$ENVIRONMENT-$LOCATION" \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --address-prefix $PROD_VNET_PREFIX \
  --tags environment=prod project=${PROJECT}

echo "finished"