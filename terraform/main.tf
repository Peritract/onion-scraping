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
    location = "UK South"
}

# Make a PG server
resource "azurerm_postgresql_flexible_server" "satire_pg_server" {
  name                = "satire-pg-server"
  location            = azurerm_resource_group.resource_container.location
  resource_group_name = azurerm_resource_group.resource_container.name
  zone = 1

  storage_mb                   = 32768
  storage_tier = "P4"
  sku_name = "B_Standard_B1ms"

  backup_retention_days        = 7
  geo_redundant_backup_enabled = false
  auto_grow_enabled            = false

  administrator_login          = var.DB_USERNAME
  administrator_password = var.DB_PASSWORD

  version                      = "16"
}

# Put a database in it
resource "azurerm_postgresql_flexible_server_database" "satire_db" {
  name                = "satire-db"
  server_id         = azurerm_postgresql_flexible_server.satire_pg_server.id
  charset             = "UTF8"
  collation           = "en_US.utf8"
}

resource "azurerm_postgresql_flexible_server_firewall_rule" "database_access" {
    name                        = "satire-db-firewall"
    server_id                 = azurerm_postgresql_flexible_server.satire_pg_server.id
    start_ip_address            = "0.0.0.0"
    end_ip_address              = "255.255.255.255"
}

resource "null_resource" "db_setup" {

  provisioner "local-exec" {

    command = "psql -h $DB_HOST -U $DB_USER -d $DB_NAME -p $DB_PORT -f ../database/schema.sql"

    environment = {
      DB_HOST = "${azurerm_postgresql_flexible_server.satire_pg_server.name}.postgres.database.azure.com"
      DB_USER = var.DB_USERNAME
      PGPASSWORD = var.DB_PASSWORD
      DB_NAME = azurerm_postgresql_flexible_server_database.satire_db.name
      DB_PORT = 5432
    }
  }
}
