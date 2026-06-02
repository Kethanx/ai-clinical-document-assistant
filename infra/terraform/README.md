# Terraform Infrastructure

This folder contains the Terraform configuration for the Azure infrastructure used by the Cardiology Assistant project.

The goal of this Terraform configuration is to document and reproduce the cloud infrastructure required to run the application, including storage, search, container registry, and Kubernetes resources.

---

## Managed Azure Resources

This Terraform configuration defines:

- Azure Resource Group
- Azure Storage Account
- Azure Blob Storage container for uploaded PDFs
- Azure Queue Storage queue for document ingestion jobs
- Azure AI Search service for vector search
- Azure Container Registry for Docker images
- Azure Kubernetes Service cluster
- Role assignment allowing AKS to pull images from ACR

Azure OpenAI is currently treated as an existing external dependency because model deployments and quota availability can vary by region and subscription.

---

## Folder Structure

```text
infra/terraform/
├── providers.tf
├── main.tf
├── variables.tf
├── outputs.tf
├── terraform.tfvars.example
└── README.md
```

---

## Prerequisites

Install:

- Terraform
- Azure CLI
- An active Azure subscription

Login to Azure:

```bash
az login
```

Confirm the active subscription:

```bash
az account show
```

---

## Configuration

Copy the example variables file:

```bash
cp terraform.tfvars.example terraform.tfvars
```

Update `terraform.tfvars` with your real Azure resource names:

```hcl
location                = "East US"
resource_group_name     = "ai-clinical-rg"
project_name            = "cardiology"

storage_account_name    = "youruniquestorageacct"
container_registry_name = "youruniqueacrname"
search_service_name     = "youruniqueaisearch"

aks_cluster_name        = "cardiology-aks"
aks_node_count          = 1
aks_node_size           = "Standard_B2s"
```

Do not commit `terraform.tfvars` because it is environment-specific.

---

## Terraform Commands

Initialize Terraform:

```bash
terraform init
```

Format files:

```bash
terraform fmt
```

Validate configuration:

```bash
terraform validate
```

Preview the infrastructure plan:

```bash
terraform plan
```

Apply the infrastructure:

```bash
terraform apply
```

Destroy the infrastructure:

```bash
terraform destroy
```

---

## Important Note About Existing Resources

The current Azure environment for this project was initially created manually through the Azure Portal and Azure CLI.

Because of that, running `terraform apply` without importing existing resources may cause Terraform to attempt to create duplicate resources with the same names.

For the current project state, this Terraform configuration is primarily used as an Infrastructure-as-Code representation of the target Azure architecture.

To fully manage the existing environment with Terraform, existing Azure resources should first be imported into Terraform state using `terraform import`.

---

## Cost Considerations

This configuration is designed for a low-cost development/demo environment.

Cost-conscious choices include:

- Azure AI Search Free tier
- Azure Container Registry Basic tier
- Single-node AKS cluster
- `Standard_B2s` AKS node size
- Standard LRS storage

AKS can still create ongoing compute charges while running. Stop or delete the AKS cluster when it is not being used for demos.

Stop AKS:

```bash
az aks stop \
  --resource-group ai-clinical-rg \
  --name cardiology-aks
```

Start AKS:

```bash
az aks start \
  --resource-group ai-clinical-rg \
  --name cardiology-aks
```

---

## Outputs

Terraform outputs include:

- Resource group name
- Storage account name
- Azure Container Registry login server
- Azure AI Search service name
- AKS cluster name
- AKS credentials command

Example:

```bash
terraform output
```

---

## Future Improvements

Potential improvements:

- Import existing Azure resources into Terraform state
- Add Azure OpenAI resource and model deployments
- Add Azure Key Vault for secret management
- Add Application Insights and Azure Monitor
- Add remote Terraform state using Azure Storage
- Add separate environments for dev and production
- Add private networking for production-style security

---

## Purpose

This Terraform layer demonstrates Infrastructure as Code practices for the Cardiology Assistant project and supports reproducible deployment of the Azure infrastructure used by the application.
