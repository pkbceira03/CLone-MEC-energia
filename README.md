# MEC Energia API

## Ferramentas

Para acessar o banco, é recomendado que você tenha 
[Docker Compose](https://docs.docker.com/compose/install/) instalado em
sua máquina.

Copie o arquivo `.env.dev` para `.env`:

```
cp .env.dev .env 
```

Então levante os containeres da API e do banco de dados com:

```sh
docker-compose up -d
```
