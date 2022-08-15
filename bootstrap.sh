#!/bin/bash

# Set the default shell to bash, otherwise it is dash and won't work correctly with the asdf tools
rm /bin/sh
ln -s /bin/bash /bin/sh

apt update && \
    apt install -y autoconf dnsutils libtool m4 automake bash build-essential curl gettext git unzip wget tar && \
    apt install -y apt-transport-https ca-certificates curl gnupg2 software-properties-common && \
    apt install -y libssl-dev libffi-dev cargo &&

python -m ensurepip --upgrade
pip install "poetry==$POETRY_VERSION"
git clone https://github.com/asdf-vm/asdf.git /root/.asdf --branch v0.8.0 && \
    echo -e '\n. /root/.asdf/asdf.sh' >> /root/.bashrc && \
    echo -e '\n. /root/.asdf/asdf.sh' >> /root/.profile && \
    source /root/.bashrc && \
    mkdir -p /root/.asdf/toolset

asdf plugin-add kubectl https://github.com/Banno/asdf-kubectl.git
asdf install kubectl 1.19.9
asdf install kubectl 1.18.17
asdf global kubectl $KUBECTL_VERSION

# Add asdf-vm plugin for terraform
asdf plugin-add terraform https://github.com/Banno/asdf-hashicorp.git

# Install supported versions of Terraform
asdf install terraform 0.13.6
asdf install terraform 0.14.9
asdf install terraform 0.15.1
asdf install terraform 1.0.8
asdf global terraform $TERRAFORM_VERSION

# install tctl
mkdir -p /root/.tctl/bin
curl -Lo /root/.tctl/bin/tctl https://binaries.dl.tetrate.io/public/raw/versions/linux-amd64-${TCTL_VERSION}/tctl
chmod +x /root/.tctl/bin/tctl

# install aws-iam-authenticator
mkdir -p /root/bin
curl -Lo /root/bin/aws-iam-authenticator https://amazon-eks.s3.us-west-2.amazonaws.com/1.19.6/2021-01-05/bin/linux/amd64/aws-iam-authenticator
chmod +x /root/bin/aws-iam-authenticator

# install grpcurl
mkdir -p /root/bin/grpcurl
wget https://github.com/fullstorydev/grpcurl/releases/download/v1.8.1/grpcurl_1.8.1_linux_x86_64.tar.gz
tar -xvf grpcurl_1.8.1_linux_x86_64.tar.gz --directory /root/bin/grpcurl
chmod +x /root/bin/grpcurl/grpcurl

# install jq
curl -Lo /root/bin/jq https://github.com/stedolan/jq/releases/download/jq-1.6/jq-linux64
chmod +x /root/bin/jq

 # install Teleport Terraform Provider
 mkdir -p ${HOME?}/.terraform.d/plugins/gravitational.com/teleport/teleport/8.0.5/linux_amd64
 curl -L -O https://get.gravitational.com/terraform-provider-teleport-v8.0.5-linux-amd64-bin.tar.gz
 tar -zxvf terraform-provider-teleport-v8.0.5-linux-amd64-bin.tar.gz -C ${HOME?}/.terraform.d/plugins/gravitational.com/teleport/teleport/8.0.5/linux_amd64