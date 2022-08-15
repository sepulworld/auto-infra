### auto-infra

foundation-infra cli for pipeline and daily tasks


### Prerequisite

##### pyenv
```
brew install pyenv
pyenv init
pyenv install 3.9.2
pyenv global 3.9.2
```

##### pipx
```
python -m pip install pipx
```

##### poetry
```
pipx install poetry
```

### Install

```
poetry install
```

### Docker Releases

### Development

This CLI uses [Typer](https://typer.tiangolo.com/)

##### Development for Terraform commands

```
git clone git@github.com:sepulworld/auto-infra.git
cd auto-infra
poetry install
poetry shell
```

#### Updating README

```
poetry shell
typer auto_infra.main utils docs --name auto-infra --output COMMANDS.md
```

Generally 'commands' should have their code in thier own Module under `./lib`


#### [Commands Doc](./COMMANDS.md)

