variable "location" {
  description = "Azure region for resources."
  type        = string
  default     = "East US"
}

variable "resource_group_name" {
  description = "Resource group name."
  type        = string
  default     = "ai-clinical-rg"
}

variable "project_name" {
  description = "Short project name used for resource naming."
  type        = string
  default     = "cardiology"
}

variable "storage_account_name" {
  description = "Globally unique Azure Storage Account name."
  type        = string
}

variable "container_registry_name" {
  description = "Globally unique Azure Container Registry name."
  type        = string
}

variable "search_service_name" {
  description = "Globally unique Azure AI Search service name."
  type        = string
}

variable "aks_cluster_name" {
  description = "AKS cluster name."
  type        = string
  default     = "cardiology-aks"
}

variable "aks_node_count" {
  description = "Number of AKS nodes."
  type        = number
  default     = 1
}

variable "aks_node_size" {
  description = "VM size for AKS nodes."
  type        = string
  default     = "Standard_B2s"
}