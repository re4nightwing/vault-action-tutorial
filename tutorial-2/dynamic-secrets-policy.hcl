# dynamic-secrets-policy.hcl
path "database/creds/myrole" {
  capabilities = ["read"]
}
