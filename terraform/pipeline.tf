resource "azurerm_service_plan" "onion-service-plan" {
  name                = "satire-onion-service-plan"
  resource_group_name = azurerm_resource_group.resource_container.name
  location            = azurerm_resource_group.resource_container.location
  os_type             = "Linux"
  sku_name            = "Y1"
}

resource "azurerm_linux_function_app" "onion-pipeline" {
  name                = "satire-onion-scraper"
  resource_group_name = azurerm_resource_group.resource_container.name
  location            = azurerm_resource_group.resource_container.location

  storage_account_name       = azurerm_storage_account.storage_container.name
  storage_account_access_key = azurerm_storage_account.storage_container.primary_access_key
  service_plan_id            = azurerm_service_plan.onion-service-plan.id
 
  site_config {}
}

# Compress the function app
data "archive_file" "onion_pipeline_compressed" {
  type        = "zip"
  source_dir  = "../onion_pipeline"
  output_path = "onion_pipeline.zip"
}

# # Upload the compressed app to storage
# resource "azurerm_storage_blob" "onion_pipeline_blob" {
#   name = "${filesha256(var.)}.zip"
#   storage_account_name = azurerm_storage_account.storage_account.name
#   storage_container_name = azurerm_storage_container.storage_container.name
#   type = "Block"
#   source = var.archive_file.output_path
# }