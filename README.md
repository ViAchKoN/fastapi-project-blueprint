# FastApi Project Blueprint
___

### Description
The project blueprint based on FastAPI. 
It already includes examples of migrations, tests and API.
It can be cloned and modified according to the requirements.

___

### How to run 
 
Set env variables in .env file

Open a Terminal window and run:
```bash
echo "DATABASE_USERNAME=postgres" >> .env
echo "DATABASE_PASSWORD=postgres" >> .env
echo "DATABASE_PORT=5432" >> .env
echo "DATABASE_NAME=project_base" >> .env
```

**Python**: 

```bash
python3 -m venv .venv

source .venv/bin/activate

pip install poetry

poetry install

alembic upgrade head

uvicorn core.main:app --host 0.0.0.0
```

**Docker**

```bash
docker-compose up -d

#use --build flag if you want to rebuild image after changes

docker-compose up --build
```
