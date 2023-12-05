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
COPY Gemfile* $APP_HOME/
RUN bundle install

# Upload source
COPY config.ru $APP_HOME
RUN mkdir $APP_HOME/lib
COPY lib/* $APP_HOME/lib

# Start server
ENV PORT 8080
EXPOSE 8080

RUN /bin/bash -c "echo '$app_secret' > ./app_secret"
CMD ["rackup", "--port", "8080", "--env", "production" ]
