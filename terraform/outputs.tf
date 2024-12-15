output "satire-db-host" {
    value = "${azurerm_postgresql_flexible_server.satire_pg_server.name}.postgres.database.azure.com"
}