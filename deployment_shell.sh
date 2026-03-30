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
az group create --name rg-$PROJECT-stag-$LOCATION --location $LOCATION

az acr create \
  --name $ACR_NAME \
  --resource-group $RESOURCE_GROUP \
  --sku Basic \
  --admin-enabled false \
  --public-network-enabled true \
  --zone-redundancy Disabled \
  --dnl-scope TenantReuse \
  --tags environment=prod project=$PROJECT

az keyvault create \
  --name "kv-${PROJECT}-prod" \
  --resource-group $RESOURCE_GROUP \
  --location swedencentral \
  --enabled-for-disk-encryption false \
  --retention-days 30 \
  --enable-rbac-authorization true \
  --sku standard \
  --default-action Allow \
  --bypass AzureServices \
  --tags environment=prod project=${PROJECT}

az keyvault create \
  --name "kv-${PROJECT}-stag" \
  --resource-group $RESOURCE_GROUP \
  --location swedencentral \
  --enabled-for-disk-encryption false \
  --retention-days 30 \
  --enable-rbac-authorization true \
  --sku standard \
  --default-action Allow \
  --bypass AzureServices \
  --tags environment=stag project=${PROJECT}


# az storage account create \
#   --name $TF_BE_STORAGE_NAME \
#   --resource-group $RESOURCE_GROUP \
#   --location $LOCATION \
#   --sku Standard_LRS \
#   --allow-shared-key-access false \
#   --public-network-access Disabled \
#   --allow-blob-public-access false \
#   --default-action Deny \
#   --https-only true \
#   --tags environment=prod project=$PROJECT \
#   --min-tls-version TLS1_2


az network private-dns zone create \
  --resource-group $RESOURCE_GROUP \
  --name "privatelink.vaultcore.azure.net"


az network vnet create \
  --name "vnet-$PROJECT-prod-$LOCATION" \
  --resource-group rg-$PROJECT-prod-$LOCATION \
  --location $LOCATION \
  --address-prefix $PROD_VNET_PREFIX \
  --tags environment=prod project=${PROJECT}

az network vnet subnet create \
  --name $PE_SUBNET_NAME-prod \
  --resource-group rg-$PROJECT-prod-$LOCATION \
  --vnet-name "vnet-$PROJECT-prod-$LOCATION" \
  --address-prefix $PE_PROD_SUBNET_PREFIX

az network vnet create \
  --name "vnet-$PROJECT-stag-$LOCATION" \
  --resource-group rg-$PROJECT-stag-$LOCATION \
  --location $LOCATION \
  --address-prefix $STAG_VNET_PREFIX \
  --tags environment=stag project=${PROJECT}

az network vnet subnet create \
  --name $PE_SUBNET_NAME-stag \
  --resource-group rg-$PROJECT-stag-$LOCATION \
  --vnet-name "vnet-$PROJECT-stag-$LOCATION" \
  --address-prefix $PE_STAG_SUBNET_PREFIX

echo "finished"