# Dharapat PBL CIB Analyzer Analytics

## How to Load an Instance of the CIB Data Class
```
import json
from cib_data_class import cib_class

cib_path = '...'
with open(cib_path) as f:
	cib_data = cib_class(json.load(f))
	cib_data.perform_sanity_check()
```

## Map of CIB data class variables

|Field Name in CIB Report|Variable Name|Return Type|
|---|---|---|
|Credit Information Bureau - Bangladesh Bank|cib_header|<class 'pandas.core.frame.DataFrame'>|
|INQUIRED|inquired|<class 'dict'>|
|SUBJECT INFORMATION|subject_info|<class 'dict'>|
|ADDRESS|address|<class 'pandas.core.frame.DataFrame'>|
|OWNERS LIST|owners_list|<class 'pandas.core.frame.DataFrame'>|
|COMPANY(S) LIST|company_list|<class 'pandas.core.frame.DataFrame'>|
|LINKED PROPRIETORSHIP(S) LIST|linked_prop_list|<class 'list'>|
|1. SUMMARY OF FACILITY(S) AS BORROWER & CO-BORROWER|summary_1|<class 'dict'>|
|1.(A) SUMMARY OF THE FUNDED FACILITIES AS BORROWER & CO-BORROWER|summary_1A|<class 'pandas.core.frame.DataFrame'>|
|1.(B) SUMMARY OF THE NON-FUNDED FACILITIES AS BORROWER & CO-BORROWER|summary_1B|<class 'pandas.core.frame.DataFrame'>|
|2. SUMMARY OF FACILITY(S) AS GUARANTOR|summary_2|<class 'dict'>|
|2.(A) SUMMARY OF THE FUNDED FACILITIES AS GUARANTOR|summary_2A|<class 'pandas.core.frame.DataFrame'>|
|2.(B) SUMMARY OF THE NON-FUNDED FACILITIES AS GUARANTOR|summary_2B|<class 'pandas.core.frame.DataFrame'>|
|REQUESTED CONTRACT DETAILS|req_contracts|<class 'pandas.core.frame.DataFrame'>|
|DETAILS OF INSTALLMENT FACILITY(S)|installment_facility|<class 'list'>|
|DETAILS OF CREDIT CARD FACILITY(S)|credit_card_facility|<class 'list'>|
|DETAILS OF NONINSTALLMENT FACILITY(S)|noninstallment_facility|<class 'list'>|


## Creating Production/UAT Image:

* Change rabbitmq connection address from `consumer_rabbitmq.py`
* Go to `build.sh` and change the image version.
* Run `sh build.sh` in terminal.

## Check Azure Portal Log:

### **For Analytics:**

* Django
  ```
  kubectl logs -f --selector app=cib-analyser -n dev-cib-analytics --container worker

  ```
* RabbitMQ
  ```
  kubectl logs -f --selector app=cib-analyser -n dev-cib-analytics --container cib-analyser
  ```

### **For AI:**

```
kubectl logs -f --selector app=cib-analyser-consumer -n cib-analyser-services
```

## Running it locally:

* Change rabbitmq connection address to blank from `consumer_rabbitmq.py` then push to GitHub and deploy in the Azure Cluster. It will turn the repository off from online.
* Fix the rabbitmq connection address to blank from `consumer_rabbitmq.py` but don't push it or deploy it.
* Run `python consumer_rabbitmq.py` in terminal.
* To deploy it again undu the previous steps and then push to GitHub and deploy to Azure Cluster.

## Deployment: GitHub Actions Secret Keys

* **AZURE_REGISTRY_2:** Azure Portal > Registry
* **AZURE_REGISTRY_USERNAME_2:** Azure Portal > Cluster > Credential > Username
* **AZURE_REGISTRY_PASSWORD_2:** Azure Portal > Cluster > Credential > Username
* **AZURE_CLUSTER_NAME_2:** Azure Portal > Cluster Name
* **AZURE_CREDENTIALS_2 :**
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
