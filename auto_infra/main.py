import os
import typer
from enum import Enum
from .lib.terraform_command import TerraformCommand


app = typer.Typer(help="foundation infra CLI.")
terraform = typer.Typer(help="run terraform commands")
app.add_typer(terraform, name="terraform")


@terraform.command("fmt")
def terraform_format(
    application: str,
    directory: str = typer.Option("./", help="Directory to check"),
    stream_output: bool = typer.Option(
        True,
        help="Flag to stream command output, instead of returning results once process finishes",  # noqa
    ),
):
    """
    Run Terraform format check
    """
    tf = TerraformCommand(
        application=application, directory=directory, stream_output=stream_output
    )

    tf.tf_format()


@terraform.command("import")
def terraform_import(
    application: str,
    tf_address: str,
    tf_id: str,
    directory: str = typer.Option("./", help="Directory to check"),
    stream_output: bool = typer.Option(
        True,
        help="Flag to stream command output, instead of returning results once process finishes",  # noqa
    ),
):
    """
    Run Terraform import
    """
    tf = TerraformCommand(
        application=application,
        directory=directory,
        stream_output=stream_output,
        tf_address=tf_address,
        tf_id=tf_id,
    )

    tf.tf_import()


@terraform.command("init")
def terraform_init(
    application: str,
    aws_region: str = typer.Option(
        "us-east-1",
        help="The AWS region to associate Terraform AWS provider with",
        envvar=["AWS_REGION"],
    ),
    aws_profile: str = typer.Option(
        "",
        help="The AWS IAM Profile to use",
        envvar=["AWS_PROFILE"],
    ),
    directory: str = typer.Option(
        "./",
        help="The directory to run terraform in",
        envvar=["INFRA_DIR"],
    ),
    environment: str = typer.Option(
        "dev",
        help="The environment to operate within",
        envvar=["ENVIRONMENT"],
    ),
    stream_output: bool = typer.Option(
        True,
        help="Flag to stream command output, instead of returning results once process finishes",  # noqa
    ),
):
    """
    Proscribed and uniform Terraform init
    """
    tf = TerraformCommand(
        application=application,
        aws_region=aws_region,
        directory=directory,
        environment=environment,
        aws_profile=aws_profile,
        stream_output=stream_output,
    )

    tf.tf_init()


@terraform.command("plan")
def terraform_plan(
    application: str,
    aws_region: str = typer.Option(
        "us-east-1",
        help="The AWS region to associate Terraform AWS provider with",
        envvar=["AWS_REGION"],
    ),
    aws_profile: str = typer.Option(
        "",
        help="The AWS IAM Profile to use",
        envvar=["AWS_PROFILE"],
    ),
    auto_init: bool = typer.Option(
        True,
        help="Automatically init the terraform config and state",
        envvar=["TF_AUTO_INIT"],
    ),
    directory: str = typer.Option(
        "./",
        help="The directory to run terraform in",
        envvar=["INFRA_DIR"],
    ),
    destroy_plan: str = typer.Option(
        "",
        help="If you want the plan to be a destroy plan, provide a file system path for output",  # noqa
    ),
    environment: str = typer.Option(
        "dev",
        help="The environment to operate within",
        envvar=["ENVIRONMENT"],
    ),
    stream_output: bool = typer.Option(
        True,
        help="Flag to stream command output, instead of returning results once process finishes",  # noqa
    ),
    refresh_state: str = typer.Option(
        "true",
        help="Update state prior to checking for differences",
        envvar=["TF_STATE_REFRESH"],
    ),
):
    """
    Proscribed and uniform Terraform plan and optional
    """
    tf = TerraformCommand(
        application=application,
        aws_profile=aws_profile,
        aws_region=aws_region,
        auto_init=auto_init,
        destroy_plan=destroy_plan,
        directory=directory,
        environment=environment,
        stream_output=stream_output,
        tf_refresh=refresh_state,
    )

    tf.tf_plan()


@terraform.command("apply")
def terraform_apply(
    application: str,
    aws_region: str = typer.Option(
        "us-east-1",
        help="The AWS region to associate Terraform AWS provider with",
        envvar=["AWS_REGION"],
    ),
    aws_profile: str = typer.Option(
        "",
        help="The AWS IAM Profile to use",
        envvar=["AWS_PROFILE"],
    ),
    auto_init: bool = typer.Option(
        True,
        help="Automatically init the terraform config and state",
        envvar=["TF_AUTO_INIT"],
    ),
    directory: str = typer.Option(
        "./",
        help="The directory to run terraform in",
        envvar=["INFRA_DIR"],
    ),
    environment: str = typer.Option(
        "dev",
        help="The environment to operate within",
        envvar=["ENVIRONMENT"],
    ),
    stream_output: bool = typer.Option(
        True,
        help="Flag to stream command output, instead of returning results once process finishes",  # noqa
        envvar=["STREAM_OUTPUT"],
    ),
    refresh_state: str = typer.Option(
        "true",
        help="Update state prior to checking for differences",
        envvar=["TF_STATE_REFRESH"],
    ),
):
    """
    Proscribed and uniform Terraform apply
    """
    tf = TerraformCommand(
        application=application,
        aws_region=aws_region,
        aws_profile=aws_profile,
        auto_init=auto_init,
        directory=directory,
        environment=environment,
        stream_output=stream_output,
        tf_refresh=refresh_state,
    )

    tf.tf_apply()


@terraform.command("output")
def terraform_output(
    application: str,
    aws_region: str = typer.Option(
        "us-east-1",
        help="The AWS region to associate Terraform AWS provider with",
        envvar=["AWS_REGION"],
    ),
    aws_profile: str = typer.Option(
        "",
        help="The AWS IAM Profile to use",
        envvar=["AWS_PROFILE"],
    ),
    auto_init: bool = typer.Option(
        True,
        help="Automatically init the terraform config and state",
        envvar=["TF_AUTO_INIT"],
    ),
    directory: str = typer.Option(
        "./",
        help="The directory to run terraform in",
        envvar=["INFRA_DIR"],
    ),
    environment: str = typer.Option(
        "dev",
        help="The environment to operate within",
        envvar=["ENVIRONMENT"],
    ),
    stream_output: bool = typer.Option(
        True,
        help="Flag to stream command output, instead of returning results once process finishes",  # noqa
        envvar=["STREAM_OUTPUT"],
    ),
    refresh_state: str = typer.Option(
        "true",
        help="Update state prior to checking for differences",
        envvar=["TF_STATE_REFRESH"],
    ),
    tf_output_name: str = typer.Option(
        "",
        help="If an output NAME is specified, only the value of that output is printed",
    ),
):
    """
    Proscribed and uniform Terraform output
    """
    tf = TerraformCommand(
        application=application,
        aws_region=aws_region,
        aws_profile=aws_profile,
        auto_init=auto_init,
        directory=directory,
        environment=environment,
        stream_output=stream_output,
        tf_refresh=refresh_state,
        tf_output_name=tf_output_name,
    )

    tf.tf_output()


@terraform.command("ensure-state-bucket-config")
def terraform_ensure_state_bucket_config(
    aws_region: str = typer.Option(
        "us-east-1",
        help="The AWS region to associate Terraform AWS provider with",
        envvar=["AWS_REGION"],
    ),
    aws_profile: str = typer.Option(
        "",
        help="The AWS IAM Profile to use",
        envvar=["AWS_PROFILE"],
    ),
    s3_bucket_name: str = typer.Option(...),
):
    """
    Proscribed and uniform Terraform output
    """
    tf = TerraformCommand(aws_region=aws_region, aws_profile=aws_profile)
    tf.ensure_s3_state_bucket_config(s3_bucket_name)


@terraform.command("destroy")
def terraform_destroy(
    application: str,
    aws_region: str = typer.Option(
        "us-east-1",
        help="The AWS region to associate Terraform AWS provider with",
        envvar=["AWS_REGION"],
    ),
    aws_profile: str = typer.Option(
        "",
        help="The AWS IAM Profile to use",
        envvar=["AWS_PROFILE"],
    ),
    auto_init: bool = typer.Option(
        True,
        help="Automatically init the terraform config and state",
        envvar=["TF_AUTO_INIT"],
    ),
    directory: str = typer.Option(
        "./",
        help="The directory to run terraform in",
        envvar=["INFRA_DIR"],
    ),
    stream_output: bool = typer.Option(
        True,
        help="Flag to stream command output, instead of returning results once process finishes",  # noqa
        envvar=["STREAM_OUTPUT"],
    ),
    environment: str = typer.Option(
        "dev",
        help="The environment to operate within",
        envvar=["ENVIRONMENT"],
    ),
    refresh_state: str = typer.Option(
        "true",
        help="Update state prior to checking for differences",
        envvar=["TF_STATE_REFRESH"],
    ),
):
    """
    Proscribed and uniform Terraform destroy
    """
    tf = TerraformCommand(
        application=application,
        aws_region=aws_region,
        aws_profile=aws_profile,
        auto_init=auto_init,
        directory=directory,
        environment=environment,
        stream_output=stream_output,
        tf_refresh=refresh_state,
    )

    tf.tf_destroy()
