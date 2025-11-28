#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<EOF
Usage: $0 --rg <resource-group> --acr <acr-name> --webapp <webapp-name> [--location <location>]

This script creates an Azure Resource Group and an ACR, and creates a Service Principal
for GitHub Actions with access to the resource group. It prints a JSON that you can
copy to the `AZURE_CREDENTIALS` GitHub secret (or uses `gh` to set secrets if available).

EOF
}

RG="tinyurl-rg"
ACR_NAME="mytinyurlacr"
WEBAPP_NAME="tinyurl-app"
LOCATION="eastus"

while [[ $# -gt 0 ]]; do
  case $1 in
    --rg) RG="$2"; shift 2;;
    --acr) ACR_NAME="$2"; shift 2;;
    --webapp) WEBAPP_NAME="$2"; shift 2;;
    --location) LOCATION="$2"; shift 2;;
    *) echo "Unknown option: $1"; usage; exit 1;;
  esac
done

echo "Using: RG=$RG ACR=$ACR_NAME WEBAPP=$WEBAPP_NAME LOCATION=$LOCATION"

echo "Checking Azure CLI login..."
if ! az account show >/dev/null 2>&1; then
  echo "Not logged into Azure CLI. Please run 'az login' and re-run this script." >&2
  exit 1
fi

SUBSCRIPTION_ID=$(az account show --query id -o tsv)
echo "Subscription ID: $SUBSCRIPTION_ID"

echo "Creating resource group $RG..."
az group create --name "$RG" --location "$LOCATION"

echo "Creating ACR $ACR_NAME..."
az acr create --resource-group "$RG" --name "$ACR_NAME" --sku Basic --admin-enabled true

echo "Creating App Service Plan and Web App $WEBAPP_NAME (Linux) ..."
az appservice plan create --name ${WEBAPP_NAME}-plan --resource-group "$RG" --is-linux --sku B1
az webapp create --resource-group "$RG" --plan ${WEBAPP_NAME}-plan --name "$WEBAPP_NAME" --deployment-container-image-name "${ACR_NAME}.azurecr.io/tinyurl:latest" || true

echo "Creating service principal (GitHub Actions) with contributor role on resource group..."
SP_JSON=$(az ad sp create-for-rbac --name "github-actions-${ACR_NAME}" --role contributor --scopes "/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RG" --sdk-auth)

echo
echo "Service principal credentials (copy this for GitHub secret AZURE_CREDENTIALS):"
echo
echo "$SP_JSON"
echo

if command -v gh >/dev/null 2>&1; then
  echo "gh CLI found - attempting to set repo secrets (requires gh auth and repo permission)..."
  gh secret set AZURE_CREDENTIALS --body "$SP_JSON"
  gh secret set ACR_NAME --body "$ACR_NAME"
  gh secret set AZURE_WEBAPP_NAME --body "$WEBAPP_NAME"
  echo "Set GH secrets AZURE_CREDENTIALS, ACR_NAME, AZURE_WEBAPP_NAME if gh CLI had access." 
else
  echo "No gh CLI detected. Please set the following GitHub secrets manually in your repo:" 
  echo "- AZURE_CREDENTIALS (paste the JSON printed above)" 
  echo "- ACR_NAME = $ACR_NAME" 
  echo "- AZURE_WEBAPP_NAME = $WEBAPP_NAME" 
fi

echo "Done. You can now push to main to trigger CI/CD (if you added the secrets)." 
