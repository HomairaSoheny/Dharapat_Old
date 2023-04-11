# dharapat_analytics_cib_analyzer_prime_bank_backend

## To view logs from azure portal

**For Analytics:**

```**
kubectl logs -f --selector app=cib-analyser -n dev-cib-analytics
```

**For AI:**

```
kubectl logs -f --selector app=cib-analyser-consumer -n cib-analyser-services
```

## Running rabbitmq locally

* Stop k8-analytics-backend-dev cluster from portal.azure.com dashboard.
* Run python consumer_rabbitmq.py on terminal.

## Deployment: GitHub Actions Secret Keys

* **AZURE_REGISTRY_2:** Azure Portal > Registry
* **AZURE_REGISTRY_USERNAME_2:** Azure Portal > Cluster > Credential > Username
* **AZURE_REGISTRY_PASSWORD_2:** Azure Portal > Cluster > Credential > Username
* **AZURE_CLUSTER_NAME_2:** Azure Portal > Cluster Name
* **AZURE_CREDENTIALS_2:**
  Format:

  ```{
  {
  	"clientId": "",
  	"clientSecret": "",
  	"subscriptionId": "",
  	"tenantId": "",
  	"activeDirectoryEndpointUrl": "https://login.microsoftonline.com",
  	"resourceManagerEndpointUrl": "https://management.azure.com/",
  	"activeDirectoryGraphResourceId": "https://graph.windows.net/",
  	"sqlManagementEndpointUrl": "https://management.core.windows.net:8443/",
  	"galleryEndpointUrl": "https://gallery.azure.com/",
  	"managementEndpointUrl": "https://management.core.windows.net/"
  }
  ```
  * **ClientID:** Azure Portal>App Registration>App>Client ID
  * **ClientSecret:** Azure Portal>App Registration>App>Client credentials>Client Secrets
  * **SubscriptionId:** Azure Portal>Container Registry> Container (Dharapat)> Subscription ID
  * **TenantId:** Azure Portal>App Registration>App>Tenant ID
* **AZURE_CLUSTER_TOKEN_2:** Azure Portal > Cluster > Cluster Token
* **AZURE_CLUSTER_URL_2:** Azure Portal > Cluster > URL
