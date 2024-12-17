terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=4.1.0"
    }
  }
}

# Configure the Microsoft Azure Provider
provider "azurerm" {
  features {}
  subscription_id = "bb3a08b1-9f3f-4a7d-a7bd-44998976010d"
}


# Create a container for all resources
resource "azurerm_resource_group" "resource_container" {
    name = "satire-project-rg"
    location = var.LOCATION
}

# Create an account to hold required data
resource "azurerm_storage_account" "storage_container" {
    name = "satireprojectsa"
    location = var.LOCATION
    resource_group_name = azurerm_resource_group.resource_container.name
    account_replication_type = "LRS"
    account_tier = "Standard"
}


