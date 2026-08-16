#!/bin/bash

set -e  # stop on error

PROD_VNET_PREFIX="10.0.0.0/16"
STAG_VNET_PREFIX="10.1.0.0/16"

PE_PROD_SUBNET_PREFIX="10.0.1.0/24"
PE_STAG_SUBNET_PREFIX="10.1.1.0/24"


PE_SUBNET_NAME="snet-pe"


PROJECT="mytestprj"
ACR_NAME="acr$PROJECT"

LOCATION="swedencentral"
RESOURCE_GROUP="rg-${PROJECT}-base-swedencentral"

TF_BE_STORAGE_NAME="sttfbe${PROJECT}"

az group create --name $RESOURCE_GROUP --location $LOCATION
az group create --name rg-$PROJECT-prod-$LOCATION --location $LOCATION

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
  --name "vnet-$PROJECT-prod-$LOCATION" \
  --resource-group rg-$PROJECT-prod-$LOCATION \
  --location $LOCATION \
  --address-prefix $PROD_VNET_PREFIX \
  --tags environment=prod project=${PROJECT}


echo "finished"