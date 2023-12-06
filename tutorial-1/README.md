# Tutorial 01 (Using vault approles to generate dynamic tokens for applications)

## 1. Setup vault server
```sh
# start the vault as dev server
vault server -dev -dev-root-token-id=root

export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_ADDR='http://127.0.0.1:8200'

vault auth enable approle
```
## 2. Add a new policy to the vault server

create kv-policy.hcl
```js
path "secret/*" {
  capabilities = ["read", "create", "update", "list", "delete"]
}

```

```sh
#Add new policy
vault policy write kv-policy kv-policy.hcl

#List all policies
vault policy list

#View configs of a policy
vault read sys/policies/acl/kv-policy
```

## 3. Add new approle attached with the policy

```sh
#Add new approle
vault write auth/approle/role/my-role \
policies=kv-policy \
secret_id_ttl=10m \
token_num_uses=10 \
token_ttl=20m \
token_max_ttl=30m \
secret_id_num_uses=40

#List all approles
vault list auth/approle/role
#View configs of an approle
vault read auth/approle/role/my-role
```

## 4. Run the application

1. Appication config. Set the below variables according to your setup.
```python
VAULT_ADDR = 'http://127.0.0.1:8200'
APPROLE_ROLE_NAME = 'my-role'
```
2. Application contains several use cases.
    - Write secrets
    - Patch secrets
    - Read secrets
    - List secrets
    - Delete the latest secret version
    - Delete a specific secret version

3. Run the application
```bash
python main.py
```