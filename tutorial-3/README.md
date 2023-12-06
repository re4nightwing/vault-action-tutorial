# Tutorial 03 (Using vault with github actions)

## 1. Get needed files
```bash
git clone https://github.com/hashicorp-education/learn-vault-github-actions.git
cd learn-vault-github-actions/vault-github-action
```

## 2. Create Docker image

```bash
.
├── config.ru
├── Dockerfile
├── Gemfile
└── lib
    └── service.rb
```

Dockerfile
```docker
FROM ruby:3.0
MAINTAINER HashiCorp Vault Education <team-vault-education@hashicorp.com>

ARG app_secret="THIS_IS_A_HARDCODED_SECRET"

RUN apt-get update
RUN apt-get install -y net-tools

# Install gems
ENV APP_HOME /app
ENV HOME /root
RUN mkdir $APP_HOME
WORKDIR $APP_HOME
COPY tutorial-3/Gemfile* $APP_HOME/
RUN bundle install

# Upload source
COPY tutorial-3/config.ru $APP_HOME
RUN mkdir $APP_HOME/lib
COPY tutorial-3/lib/* $APP_HOME/lib

# Start server
ENV PORT 8080
EXPOSE 8080

RUN /bin/bash -c "echo '$app_secret' > ./app_secret"
CMD ["rackup", "--port", "8080", "--env", "production" ]
```

- create the docker container
```bash
docker build . --file tutorial-3/Dockerfile -t vault-action-example --network=host
```

- check current secret key
```bash
docker run vault-action-example /bin/bash -c "cat ./app_secret"
```

## 3. Start vault (dev mode)

```bash
vault server -dev -dev-root-token-id=root
export VAULT_ADDR=http://127.0.0.1:8200
export VAULT_TOKEN=root
```

- create a secret in vault
```bash
vault kv put secret/ci app_secret=SecretProvidedByVault
vault kv get secret/ci
```

- create a policy with read access to the secret path
```bash
vault policy write ci-secret-reader - <<EOF
path "secret/data/ci" {
    capabilities = ["read"]
}
EOF
```

- Export an environment variable GITHUB_REPO_TOKEN to capture the token value created with the ci-secret-reader policy attached.
```bash
GITHUB_REPO_TOKEN=$(vault token create -policy=ci-secret-reader -format json | jq -r ".auth.client_token")
```

- Retrieve the secret at the path using the GITHUB_REPO_TOKEN.(check if the token is working)
```bash
VAULT_TOKEN=$GITHUB_REPO_TOKEN vault kv get secret/ci
```

**Add all files to a github repo.**

## 4. Setup auth credential in gihub repo secrets

1. Go to repository settings
2. Go to secrets and variables > actions
3. Create a new Repository secrets as `VAULT_TOKEN`. (VAULT_TOKEN should be the $GITHUB_REPO_TOKEN varibale created using the policy)

## 5. Setup the GitHub self-hosted runner

1. Go to repository settings
2. Go to Actions>Runners
3. Click on "New self-hosted runner" and follow the instructions to create a new runner.

## 6. Create github workflow for the actions

1. In local repo location create the workflow directory.
```bash
mkdir -p .github/workflows
```

.github/workflows/image-builder.yml
```yml
name: ImageBuilder
# Run this workflow every time a new commit pushed to your repository
on: push
jobs:
  build:
    runs-on: self-hosted
    steps:
      - uses: actions/checkout@v3
      - name: Import Secrets
        uses: hashicorp/vault-action@v2
        with:
          url: http://127.0.0.1:8200
          tlsSkipVerify: true
          token: ${{ secrets.VAULT_TOKEN }}
          secrets: |
            secret/data/ci app_secret
      - name: Build Docker Image
        run: docker build . --file tutorial-3/Dockerfile --build-arg app_secret="${{ env.APP_SECRET }}" -t vault-action-example
```

## 7. Finally

1. Push the repo changes to the remote to trigger the action workflow.
2. Check the local runner or github actions tab for process status.
3. Check the secret change using,
```bash
docker run vault-action-example /bin/bash -c "cat ./app_secret"
```
