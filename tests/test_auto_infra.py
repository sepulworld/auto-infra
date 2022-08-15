import logging
import pytest
import os
import boto3

from auto_infra.main import app
from typer.testing import CliRunner
from moto import mock_s3, mock_sts, mock_dynamodb2

runner = CliRunner()


@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"


@pytest.fixture(scope="function")
def s3(aws_credentials):
    with mock_s3():
        yield boto3.client("s3", region_name="us-east-1")


@pytest.fixture(scope="function")
def sts(aws_credentials):
    with mock_dynamodb2():
        yield boto3.client("dynamodb", region_name="us-east-1")


def test_terraform_command_test_1_format(capfd, caplog):
    with caplog.at_level(logging.INFO):
        result = runner.invoke(
            app,
            [
                "terraform",
                "fmt",
                "test-auto-infra-app",
                "--directory",
                "tests/terraform/test_1",
            ],
        )
    assert result.exit_code == 0
    assert "terraform -chdir=tests/terraform/test_1 fmt -check -diff" in caplog.text


@mock_dynamodb2
@mock_s3
@mock_sts
def test_terraform_command_test_1_init(capfd, caplog):
    with caplog.at_level(logging.INFO):
        result = runner.invoke(
            app,
            [
                "terraform",
                "init",
                "test-auto-infra-app",
                "--directory",
                "tests/terraform/test_1",
            ],
        )
    assert result.exit_code == 0
    assert "-backend-config='dynamodb_table=auto-infra-lock-123456789012-us-east-1" in caplog.text
    assert "terraform -chdir=tests/terraform/test_1 init" in caplog.text
    assert "-backend-config='bucket=infra-state-123456789012-us-east-1" in caplog.text
    assert "-backend-config='key=dev/test-auto-infra-app" in caplog.text
    assert "-backend-config='region=us-east-1" in caplog.text


@mock_dynamodb2
@mock_s3
@mock_sts
def test_terraform_command_test_1_plan(capfd, caplog):
    with caplog.at_level(logging.INFO):
        result = runner.invoke(
            app,
            [
                "terraform",
                "plan",
                "test-auto-infra-app",
                "--directory",
                "tests/terraform/test_1",
            ],
        )
    assert result.exit_code == 0
    assert "-backend-config='dynamodb_table=auto-infra-lock-123456789012-us-east-1" in caplog.text
    assert "terraform -chdir=tests/terraform/test_1 plan" in caplog.text
    assert "-backend-config='bucket=infra-state-123456789012-us-east-1" in caplog.text
    assert "-backend-config='key=dev/test-auto-infra-app" in caplog.text
    assert "-backend-config='region=us-east-1" in caplog.text


@mock_dynamodb2
@mock_s3
@mock_sts
def test_terraform_command_test_1_apply(capfd, caplog):
    with caplog.at_level(logging.INFO):
        result = runner.invoke(
            app,
            [
                "terraform",
                "apply",
                "test-auto-infra-app",
                "--directory",
                "tests/terraform/test_1",
            ],
        )
    assert result.exit_code == 0
    assert "-backend-config='dynamodb_table=auto-infra-lock-123456789012-us-east-1" in caplog.text
    assert "terraform -chdir=tests/terraform/test_1 apply" in caplog.text
    assert "-backend-config='bucket=infra-state-123456789012-us-east-1" in caplog.text
    assert "-backend-config='key=dev/test-auto-infra-app" in caplog.text
    assert "-backend-config='region=us-east-1" in caplog.text


@mock_dynamodb2
@mock_s3
@mock_sts
def test_terraform_command_test_output_command(capfd, caplog):
    with caplog.at_level(logging.INFO):
        result = runner.invoke(
            app,
            [
                "terraform",
                "output",
                "test-auto-infra-app",
                "--directory",
                "tests/terraform/test_1",
            ],
        )
    assert result.exit_code == 0
    assert "-backend-config='dynamodb_table=auto-infra-lock-123456789012-us-east-1" in caplog.text
    assert "terraform -chdir=tests/terraform/test_1 output" in caplog.text
    assert "-backend-config='bucket=infra-state-123456789012-us-east-1" in caplog.text
    assert "-backend-config='key=dev/test-auto-infra-app" in caplog.text
    assert "-backend-config='region=us-east-1" in caplog.text


# Test Terraform command to explicitly show one output using terraform output command
@mock_dynamodb2
@mock_s3
@mock_sts
def test_terraform_command_output_with_output_name(capfd, caplog):
    with caplog.at_level(logging.INFO):
        result = runner.invoke(
            app,
            [
                "terraform",
                "output",
                "test-auto-infra-app",
                "--directory",
                "tests/terraform/test_1",
                "--tf-output-name",
                "random_pet_phoebe",
            ],
        )
    assert result.exit_code == 0
    assert "phoebe" in caplog.text
    assert "walter" not in caplog.text

