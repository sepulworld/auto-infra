# `auto-infra`

foundation infra CLI.

**Usage**:

```console
$ auto-infra [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `terraform`: run terraform commands

## `auto-infra terraform`

run terraform commands

**Usage**:

```console
$ auto-infra terraform [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `apply`: Proscribed and uniform Terraform apply
* `destroy`: Proscribed and uniform Terraform destroy
* `ensure-state-bucket-config`: Proscribed and uniform Terraform output
* `fmt`: Run Terraform format check
* `import`: Run Terraform import
* `init`: Proscribed and uniform Terraform init
* `output`: Proscribed and uniform Terraform output
* `plan`: Proscribed and uniform Terraform plan and...

### `auto-infra terraform apply`

Proscribed and uniform Terraform apply

**Usage**:

```console
$ auto-infra terraform apply [OPTIONS] APPLICATION
```

**Arguments**:

* `APPLICATION`: [required]

**Options**:

* `--aws-region TEXT`: The AWS region to associate Terraform AWS provider with  [env var: AWS_REGION; default: us-east-1]
* `--aws-profile TEXT`: The AWS IAM Profile to use  [env var: AWS_PROFILE; default: ]
* `--auto-init / --no-auto-init`: Automatically init the terraform config and state  [env var: TF_AUTO_INIT; default: True]
* `--directory TEXT`: The directory to run terraform in  [env var: INFRA_DIR; default: ./]
* `--environment TEXT`: The environment to operate within  [env var: ENVIRONMENT; default: dev]
* `--stream-output / --no-stream-output`: Flag to stream command output, instead of returning results once process finishes  [env var: STREAM_OUTPUT; default: True]
* `--s3-bucket TEXT`: The S3 bucket to store Terraform state in  [env var: S3_BUCKET; default: ]
* `--refresh-state TEXT`: Update state prior to checking for differences  [env var: TF_STATE_REFRESH; default: true]
* `--help`: Show this message and exit.

### `auto-infra terraform destroy`

Proscribed and uniform Terraform destroy

**Usage**:

```console
$ auto-infra terraform destroy [OPTIONS] APPLICATION
```

**Arguments**:

* `APPLICATION`: [required]

**Options**:

* `--aws-region TEXT`: The AWS region to associate Terraform AWS provider with  [env var: AWS_REGION; default: us-east-1]
* `--aws-profile TEXT`: The AWS IAM Profile to use  [env var: AWS_PROFILE; default: ]
* `--auto-init / --no-auto-init`: Automatically init the terraform config and state  [env var: TF_AUTO_INIT; default: True]
* `--directory TEXT`: The directory to run terraform in  [env var: INFRA_DIR; default: ./]
* `--stream-output / --no-stream-output`: Flag to stream command output, instead of returning results once process finishes  [env var: STREAM_OUTPUT; default: True]
* `--s3-bucket TEXT`: The S3 bucket to store Terraform state in  [env var: S3_BUCKET; default: ]
* `--environment TEXT`: The environment to operate within  [env var: ENVIRONMENT; default: dev]
* `--refresh-state TEXT`: Update state prior to checking for differences  [env var: TF_STATE_REFRESH; default: true]
* `--help`: Show this message and exit.

### `auto-infra terraform ensure-state-bucket-config`

Proscribed and uniform Terraform output

**Usage**:

```console
$ auto-infra terraform ensure-state-bucket-config [OPTIONS]
```

**Options**:

* `--aws-region TEXT`: The AWS region to associate Terraform AWS provider with  [env var: AWS_REGION; default: us-east-1]
* `--aws-profile TEXT`: The AWS IAM Profile to use  [env var: AWS_PROFILE; default: ]
* `--s3-bucket-name TEXT`: [required]
* `--help`: Show this message and exit.

### `auto-infra terraform fmt`

Run Terraform format check

**Usage**:

```console
$ auto-infra terraform fmt [OPTIONS] APPLICATION
```

**Arguments**:

* `APPLICATION`: [required]

**Options**:

* `--directory TEXT`: Directory to check  [default: ./]
* `--stream-output / --no-stream-output`: Flag to stream command output, instead of returning results once process finishes  [default: True]
* `--help`: Show this message and exit.

### `auto-infra terraform import`

Run Terraform import

**Usage**:

```console
$ auto-infra terraform import [OPTIONS] APPLICATION TF_ADDRESS TF_ID
```

**Arguments**:

* `APPLICATION`: [required]
* `TF_ADDRESS`: [required]
* `TF_ID`: [required]

**Options**:

* `--directory TEXT`: Directory to check  [default: ./]
* `--stream-output / --no-stream-output`: Flag to stream command output, instead of returning results once process finishes  [default: True]
* `--help`: Show this message and exit.

### `auto-infra terraform init`

Proscribed and uniform Terraform init

**Usage**:

```console
$ auto-infra terraform init [OPTIONS] APPLICATION
```

**Arguments**:

* `APPLICATION`: [required]

**Options**:

* `--aws-region TEXT`: The AWS region to associate Terraform AWS provider with  [env var: AWS_REGION; default: us-east-1]
* `--aws-profile TEXT`: The AWS IAM Profile to use  [env var: AWS_PROFILE; default: ]
* `--directory TEXT`: The directory to run terraform in  [env var: INFRA_DIR; default: ./]
* `--environment TEXT`: The environment to operate within  [env var: ENVIRONMENT; default: dev]
* `--s3-bucket TEXT`: The S3 bucket to store Terraform state in  [env var: S3_BUCKET; default: ]
* `--stream-output / --no-stream-output`: Flag to stream command output, instead of returning results once process finishes  [default: True]
* `--help`: Show this message and exit.

### `auto-infra terraform output`

Proscribed and uniform Terraform output

**Usage**:

```console
$ auto-infra terraform output [OPTIONS] APPLICATION
```

**Arguments**:

* `APPLICATION`: [required]

**Options**:

* `--aws-region TEXT`: The AWS region to associate Terraform AWS provider with  [env var: AWS_REGION; default: us-east-1]
* `--aws-profile TEXT`: The AWS IAM Profile to use  [env var: AWS_PROFILE; default: ]
* `--auto-init / --no-auto-init`: Automatically init the terraform config and state  [env var: TF_AUTO_INIT; default: True]
* `--directory TEXT`: The directory to run terraform in  [env var: INFRA_DIR; default: ./]
* `--environment TEXT`: The environment to operate within  [env var: ENVIRONMENT; default: dev]
* `--stream-output / --no-stream-output`: Flag to stream command output, instead of returning results once process finishes  [env var: STREAM_OUTPUT; default: True]
* `--s3-bucket TEXT`: The S3 bucket to store Terraform state in  [env var: S3_BUCKET; default: ]
* `--refresh-state TEXT`: Update state prior to checking for differences  [env var: TF_STATE_REFRESH; default: true]
* `--tf-output-name TEXT`: If an output NAME is specified, only the value of that output is printed  [default: ]
* `--help`: Show this message and exit.

### `auto-infra terraform plan`

Proscribed and uniform Terraform plan and optional

**Usage**:

```console
$ auto-infra terraform plan [OPTIONS] APPLICATION
```

**Arguments**:

* `APPLICATION`: [required]

**Options**:

* `--aws-region TEXT`: The AWS region to associate Terraform AWS provider with  [env var: AWS_REGION; default: us-east-1]
* `--aws-profile TEXT`: The AWS IAM Profile to use  [env var: AWS_PROFILE; default: ]
* `--auto-init / --no-auto-init`: Automatically init the terraform config and state  [env var: TF_AUTO_INIT; default: True]
* `--directory TEXT`: The directory to run terraform in  [env var: INFRA_DIR; default: ./]
* `--destroy-plan TEXT`: If you want the plan to be a destroy plan, provide a file system path for output  [default: ]
* `--environment TEXT`: The environment to operate within  [env var: ENVIRONMENT; default: dev]
* `--s3-bucket TEXT`: The S3 bucket to store Terraform state in  [env var: S3_BUCKET; default: ]
* `--stream-output / --no-stream-output`: Flag to stream command output, instead of returning results once process finishes  [default: True]
* `--refresh-state TEXT`: Update state prior to checking for differences  [env var: TF_STATE_REFRESH; default: true]
* `--help`: Show this message and exit.
