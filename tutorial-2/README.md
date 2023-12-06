# Tutorial 02 (Using policies to generate dynamic users for databases)

## 1. Setup the database

1. Create a database user as vault user with permission to create,alter,read,delete users/tables.
2. Create a temporary database with some tables for the tutorial.

## 2. Setup vault configuration

```sh
# start the vault as dev server
vault server -dev -dev-root-token-id=root

export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_ADDR='http://127.0.0.1:8200'

vault secrets enable database
```
- Add the policy for database credential generation.

> dynamic-secrets-policy.hcl
```
path "database/creds/myrole" {
  capabilities = ["read"]
}
```

```sh
vault policy write dynamic-secrets-policy dynamic-secrets-policy.hcl
```

- Add database connection details to the vault server
```sh
vault write database/config/vault_test_db \
plugin_name=mysql-database-plugin \
allowed_roles=myrole \
connection_url="{{username}}:{{password}}@tcp(127.0.0.1:3306)/vault_test" \
username="dulan" \
password="good"
```

- Create database role associated with the policy
```sh
vault write database/roles/myrole \
db_name=vault_test_db \
creation_statements="CREATE USER '{{name}}'@'%' \
IDENTIFIED BY '{{password}}'; \
GRANT ALL PRIVILEGES ON vault_test.* \
TO '{{name}}'@'%';" \
default_ttl="1h" \
max_ttl="24h" \
policies="dynamic-secrets"
```

## 3. Run the application

1. Appication config. Set the below variables according to your setup.
```python
VAULT_ADDR = 'http://127.0.0.1:8200'
VAULT_TOKEN = 'root'
DB_ROLE = 'myrole'
```
2. Application will,
    - get newly generated db credentials from the vault
    - use those credentials to read the database tables

3. Run the application
```bash
python db_vault.py
```