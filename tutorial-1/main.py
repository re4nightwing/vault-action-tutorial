import hvac

VAULT_ADDR = 'http://127.0.0.1:8200'
APPROLE_ROLE_NAME = 'my-role'

client = hvac.Client(url=VAULT_ADDR)

def write_secret(path, data):
    response = client.secrets.kv.v2.create_or_update_secret(path=path, secret=data)
    return response

def patch_secret(path, data):
    response = client.secrets.kv.v2.patch(path=path, secret=data)
    return response

def read_secret(path):
    response = client.secrets.kv.v2.read_secret_version(path=path, raise_on_deleted_version=False)
    return response.get('data', {}).get('data', {})

def list_secrets(path):
    response = client.secrets.kv.v2.list_secrets(path=path)
    return response.get('data', {}).get('keys', [])

def delete_latest_secret(path):
    response = client.secrets.kv.v2.delete_latest_version_of_secret(path=path)
    return response

def delete_secret(path):
    response = client.secrets.kv.v2.delete_metadata_and_all_versions(path=path)
    return response

def get_approle_creds(role_name):
    response = client.read(f'auth/approle/role/{role_name}/role-id')
    role_id = response['data']['role_id'] if response and response.get('data') else None

    secret_id_response = client.write(f'auth/approle/role/{role_name}/secret-id')
    secret_id = secret_id_response['data']['secret_id'] if secret_id_response and secret_id_response.get('data') else None

    return role_id, secret_id

def login_with_approle(role_name):
    role_id, secret_id = get_approle_creds(role_name)
    if role_id and secret_id:
        login_response = client.auth.approle.login(role_id, secret_id)
        if login_response and login_response.get('auth'):
            client.token = login_response['auth']['client_token']
            print(f"Successfully logged in with AppRole. Token: {client.token}")
            return True
    print("AppRole authentication failed.")
    return False

if __name__ == "__main__":
    if login_with_approle(APPROLE_ROLE_NAME):
        print("=================")
        secret_path = 'kitty/hello'
        secret_data = {'username': 'new', 'password': 'life2'}

        # Write a secret
        #write_secret(secret_path, secret_data)
        #print(f"Secret written to {secret_path}")

        # Patch a secret
        #patch_secret(secret_path, secret_data)
        #print(f"Secret Patched to {secret_path}")

        # Read a secret
        #retrieved_secret = read_secret(secret_path)
        #print(f"Retrieved Secret: {retrieved_secret}")

        # List all secrets in a path
        all_secrets = list_secrets("kitty")
        print(f"All Secrets in 'secrets' path: {all_secrets}")

        # Delete latest secret
        #delete_latest_response = delete_latest_secret(secret_path)
        #print(f"Deletion Status: {delete_latest_response}")

        # Delete a secret
        #delete_response = delete_secret(secret_path)
        #print(f"Deletion Status: {delete_response}")
