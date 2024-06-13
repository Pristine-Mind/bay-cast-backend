## Setting up Local Development

Install [pyenv](https://github.com/pyenv/pyenv) and  [poetry](https://github.com/python-poetry/poetry)

Install python version in `pyproject.toml` which is `3.11`:
```
pyenv install 3.11
```
Install dependencies:
```
poetry install
```

Copy .env.sample file to .env and override there.
```
touch .env
cp .env.sample .env
```

Also install [flake8](https://github.com/PyCQA/flake8) locally.

## Runing Development Server

```bash
docker compose build
docker compose up
```
