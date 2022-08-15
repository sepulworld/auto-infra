FROM python:3.10.0-slim-buster

ENV PATH="${PATH}:/root/.asdf/shims:/root/.asdf/bin:/root/.tctl/bin:/root/bin:/root/bin/grpcurl"
SHELL ["/bin/bash", "-c"]

ARG TERRAFORM_VERSION=1.2.6
ARG KUBECTL_VERSION=1.19.9
ARG AWS_IAM_AUTHENTICATOR=1.19.6

WORKDIR /auto-infra

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential

COPY bootstrap.sh /root/bootstrap.sh
RUN chmod +x /root/bootstrap.sh
RUN /root/bootstrap.sh

# Install Poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN pip install 'poetry==1.1.5'
COPY poetry.lock pyproject.toml /auto-infra/
COPY . /auto-infra/

RUN poetry config virtualenvs.create false 
RUN poetry install --no-dev --no-interaction --no-ansi


RUN mkdir -p ~/.ssh && chmod 700 ~/.ssh


## Depending on pipeline setup with action workers, might need to introdue assume role logic
## ENTRYPOINT ["./aws_sts_assume_role.sh"]