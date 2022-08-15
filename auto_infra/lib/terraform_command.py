import boto3
import os

from dataclasses import dataclass

from .common import run_command
from .setup_logger import logger


@dataclass
class TerraformCommand:
    """Class for defining Terraform actions"""

    # Application should be the name of the source control repo,
    # ideally unique across org
    application: str = ""
    stream_output: bool = True
    aws_region: str = ""
    aws_profile: str = ""
    auto_init: bool = True
    destroy_plan: str = ""
    directory: str = ""
    environment: str = "dev"
    product: str = ""
    s3_bucket: str = ""
    team: str = ""
    tf_refresh: str = "true"
    tf_init_return: str = ""
    tf_plan_return: str = ""
    tf_apply_return: str = ""
    tf_destroy_return: str = ""
    tf_fmt_return: str = ""
    tf_address: str = ""
    tf_id: str = ""
    tf_output_name: str = ""

    def tf_init(self) -> str:
        aws_acct = self._get_aws_account_number_and_set_env_profile()
        if not self.s3_bucket:
            bucket = self._ensure_s3_state_bucket(
                aws_acct=aws_acct, aws_region=self.aws_region
            )
        else:
            bucket = self.s3_bucket
        lock_table = self._ensure_dynamodb_lock_table(
            aws_acct=aws_acct, aws_region=self.aws_region
        )
        terraform_init = (
            f"terraform -chdir={self.directory} init "
            f"-reconfigure "
            f"-backend-config='bucket={bucket}' "
            f"-backend-config='key={self.environment}/{self.application}' "
            f"-backend-config='region={self.aws_region}' "
            f"-backend-config='profile={self.aws_profile}' "
            f"-backend-config='dynamodb_table={lock_table}'"
        )
        logger.info(f"initializing Terraform...{terraform_init}")
        # don't stream init command, Buildkite doesn't handle this well, need to debug
        # if you stream it will skip right to next command, not same behavior on laptop
        self.tf_init_return = run_command(
            terraform_init, stream_output=self.stream_output
        )
        logger.info(self.tf_init_return)

    def tf_plan(self) -> str:
        self._auto_init()
        terraform_plan = f"terraform -chdir={self.directory} plan -refresh={self.tf_refresh} "  # noqa
        if self.destroy_plan:
            terraform_destroy_plan = (
                terraform_plan + f"-destroy -out {self.destroy_plan}"
            )
            logger.info(f"generting plan for destroy...{terraform_destroy_plan}")
            self.tf_plan_return = run_command(
                terraform_destroy_plan, stream_output=self.stream_output
            )
        else:
            logger.info(f"terraform plan...{terraform_plan}")
            self.tf_plan_return = run_command(
                terraform_plan, stream_output=self.stream_output
            )

    def tf_apply(self) -> str:
        self._auto_init()
        terraform_apply = (
            f"terraform -chdir={self.directory} apply -refresh={self.tf_refresh} "
            f"-auto-approve"
        )  # noqa
        logger.info(f"terraform apply...{terraform_apply}")
        self.tf_apply_return = run_command(
            terraform_apply, stream_output=self.stream_output
        )

    def tf_output(self) -> str:
        self._auto_init()
        terraform_output = f"terraform -chdir={self.directory} output"  # noqa
        if self.tf_output_name:
            terraform_tf_output_name = terraform_output + f" {self.tf_output_name}"
            logger.info(
                f"display requested output of a resource...{terraform_tf_output_name}"
            )
            self.tf_plan_return = run_command(
                terraform_tf_output_name, stream_output=self.stream_output
            )
        else:
            logger.info(f"terraform output...{terraform_output}")
            self.tf_output_return = run_command(
                terraform_output, stream_output=self.stream_output
            )

    def tf_format(self) -> str:
        terraform_format = (
            f"terraform -chdir={self.directory} fmt " f"-check " f"-diff "
        )

        logger.info("terraform format...")
        self.tf_format_return = run_command(terraform_format)

    def tf_import(self) -> str:
        self._auto_init()
        terraform_import = (
            f"terraform -chdir={self.directory} import {self.tf_address} {self.tf_id}"
        )

        logger.info("terraform import...")
        self.tf_format_return = run_command(terraform_import)

    def tf_destroy(self) -> str:
        self._auto_init()
        terraform_destroy = (
            f"terraform -chdir={self.directory} destroy -refresh={self.tf_refresh} "
            f"-auto-approve "
        )
        logger.info(f"terraform destroy...{terraform_destroy}")
        self.tf_destroy_return = run_command(
            terraform_destroy, stream_output=self.stream_output
        )

    def _auto_init(self) -> None:
        """
        Run _load_env_vars and check to see if end user wants to
        also automatically run terraform init (tf_init)
        """
        self._load_env_vars()
        if self.auto_init:
            self.tf_init()

    def _load_env_vars(self) -> None:
        """
        Load OS env vars for TF to use
        """
        os.environ["TF_VAR_app"] = self.application
        os.environ["TF_VAR_aws_profile"] = self.aws_profile
        os.environ["TF_VAR_environment"] = self.environment
        os.environ["TF_VAR_product"] = self.product
        os.environ["TF_VAR_aws_region"] = self.aws_region
        os.environ["TF_VAR_team"] = self.team
        logger.info(f"env_var: TF_VAR_app={os.environ['TF_VAR_app']}")
        logger.info(f"env_var: TF_VAR_aws_profile={os.environ['TF_VAR_aws_profile']}")
        logger.info(f"env_var: TF_VAR_environment={os.environ['TF_VAR_environment']}")
        logger.info(f"env_var: TF_VAR_product={os.environ['TF_VAR_product']}")
        logger.info(f"env_var: TF_VAR_aws_region={os.environ['TF_VAR_aws_region']}")
        logger.info(f"env_var: TF_VAR_team={os.environ['TF_VAR_team']}")

    def _set_boto3_session(self):
        if self.aws_profile:
            session = boto3.session.Session(profile_name=self.aws_profile)
        else:
            session = boto3.session.Session()

        return session

    def _get_aws_account_number_and_set_env_profile(self) -> str:
        session = self._set_boto3_session()
        return session.client("sts").get_caller_identity()["Account"]

    def ensure_s3_state_bucket_config(self, bucket: str) -> None:
        """
        Ensure that the state bucket has appropriate ACL and tags
        configuration.
        """
        session = self._set_boto3_session()
        s3 = session.resource("s3")
        bucket_tagging = s3.BucketTagging(bucket)
        response = bucket_tagging.put(
            Tagging={
                "TagSet": [
                    {
                        "Key": "Team",
                        "Value": "product-infra",
                    },
                    {
                        "Key": "Product",
                        "Value": "infra-pipleline",
                    },
                    {
                        "Key": "Service",
                        "Value": "auto-infra",
                    },
                ],
            }
        )
        logger.info(f"set bucket tags on {bucket}: aws response {response}")
        s3_client = session.client("s3")
        response = s3_client.put_bucket_encryption(
            Bucket=bucket,
            ServerSideEncryptionConfiguration={
                "Rules": [
                    {
                        "ApplyServerSideEncryptionByDefault": {
                            "SSEAlgorithm": "aws:kms",
                        }
                    }
                ]
            },
        )
        logger.info(f"set bucket encryption {bucket}: aws response {response}")
        bucket_versioning = s3.BucketVersioning(bucket)
        response = bucket_versioning.enable()
        logger.info(f"set bucket versioning {bucket}: aws response {response}")
        response = s3_client.put_public_access_block(
            Bucket=bucket,
            PublicAccessBlockConfiguration={
                "BlockPublicAcls": True,
                "IgnorePublicAcls": True,
                "BlockPublicPolicy": True,
                "RestrictPublicBuckets": True,
            },
        )
        logger.info(f"set bucket acl {bucket}: aws response {response}")


    def _ensure_s3_state_bucket(self, aws_acct, aws_region) -> str:
        """Ensure that the AWS account has the appropreiate s3 bucket
        to use for Terraform state with secure settings."""

        session = self._set_boto3_session()
        bucket_name = f"infra-state-{aws_acct}-{aws_region}"
        logger.debug(f"ensuring AWS account tf state bucket = {bucket_name}")
        s3 = session.resource("s3")

        if s3.Bucket(bucket_name).creation_date is None:
            logger.info(
                f"creating default s3 state bucket {bucket_name} for account {aws_acct}"
            )
            if aws_region == "us-east-1":
                s3.create_bucket(Bucket=bucket_name)
            else:
                s3.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={"LocationConstraint": aws_region},
                )
            self.ensure_s3_state_bucket_config(bucket_name)

        else:
            logger.info(f"default s3 Terraform state bucket exists {bucket_name}")

        return bucket_name

    def _ensure_dynamodb_lock_table(self, aws_acct, aws_region) -> str:
        """Ensure that the AWS account has the appropriate dynamodb
        terraform lock table to use for Terraform state locking."""

        session = self._set_boto3_session()
        table_name = f"auto-infra-lock-{aws_acct}-{aws_region}"
        logger.debug(f"ensuring AWS account dynamodb table = {table_name}")

        dynamodb = session.client("dynamodb", region_name=aws_region)
        try:
            dynamodb.describe_table(TableName=table_name)
        except dynamodb.exceptions.ResourceNotFoundException:
            logger.info(f"creating lock table: {table_name}")
            dynamodb.create_table(
                AttributeDefinitions=[
                    {
                        "AttributeName": "LockID",
                        "AttributeType": "S",
                    },
                ],
                KeySchema=[
                    {
                        "AttributeName": "LockID",
                        "KeyType": "HASH",
                    },
                ],
                BillingMode="PAY_PER_REQUEST",
                TableName=table_name,
                Tags=[
                    {
                        "Key": "Team",
                        "Value": "product-infra",
                    },
                    {
                        "Key": "Product",
                        "Value": "infra-pipleline",
                    },
                    {
                        "Key": "Service",
                        "Value": "auto-infra",
                    },
                ],
            )
            pass

        logger.info(f"using Dynamodb table for locking = {table_name}")

        return table_name

    def tf_output_kubeconfig(self) -> str:
        tf_output = f"terraform -chdir={self.directory} output -raw kubeconfig_path"
        return run_command(tf_output, stream_output=False)
