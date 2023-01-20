# Seed

Em `scripts/seed.py` são criados alguns dados para facilitar o desenvolvimento
e alguns testes manuais. Dados como universidade, unidades consumidoras, 
contratos e etc. Leia o script para entender como eles se relacionam.

Para popular o banco execute **dentro do container da API** o seguinte:

```sh
./scripts/seed.sh
```

Note que o script executado no comando anterior é um script em bash. Ele faz 
pipe do conteúdo de `seed.py` para o shell do Django.

Para apagar os dados do banco de dados você pode usar:

```sh
./scripts/dbflush.sh
```

**Execute o comando anterior com cuidado!**. Esse script pula o prompt de 
confirmação e apaga todos os dados diretamente.

## Seed de Demonstação

O seed de demonstração da entrega do projeto pode ser carregado executando o seguinte comando:

```sh
./scripts/seed.sh
```

Esse comando também deve ser executado dentro do container da api (mec-energia-api).

## Usuários

Para acessar dados da API e a documentação, você deve criar um usuário. O script
`seed.py` já cria um _usuário de universidade_. Logar com esse usuário te dá a
perspectiva de um usuário de universidade. As credenciais desse usuário estão
em `seed.py`.

Além desse usuário, você pode criar um super usuário. Para isso basta rodar

```sh
./scripts/create-superuser.sh
```

A senha e o email estão `scripts/create-superuser.sh`. Você deve usá-los para
logar na API.
