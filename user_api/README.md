# Serviço User_API

Este serviço é responsável por listar, exibir, criar, alterar e excluir usuários.

Ele é totalmente independente de outros serviços e seu container contém seu webservice (**FastAPI**), seu banco de dados (**PostgreSQL**) e seu serviço de cache em memória (**Redis**).

Para funcionamento com o serviço de ordens, é necessário que ambos estejam na mesma rede para comunicação, por este motivo, é necessário criar uma interface de rede no **Docker** com o seguinte comando:

`docker network create containers-shared`

Feito isto, basta subir o container do serviço executando o comando a seguir dentro da pasta `user_api`:

`docker compose up`

O serviço é iniciado na porta `8080` e seu acesso na máquina host pode ser realizado por http://localhost:8080.


Obs:
O serviço é iniciado com alguns dados fictícios que podem ser removidos/desabilitados posteriormente.



## Endpoints

O serviço possuí os seguintes endpoints:

| Método HTTP | Endpoint            | Descrição                                              |
|-------------|---------------------|--------------------------------------------------------|
| GET         | /                   | Redireciona a conexão para o endpoint `/users`         |
| GET         | /users              | Lista todos usuários, ordenados pelo `id` decrescente. |
| GET         | /users/{id}         | Exibe o usuário filtrando pelo campo `{id}`            |
| GET         | /users/{id}/orders/ | Lista todas as ordens para o usuário filtrado `{id}`   |
| POST        | /users              | Cria um novo usuário                                   |
| PATCH       | /users/{id}         | Atualiza o usuário pelo campo `{id}`                   |
| DELETE      | /users/{id}         | Deleta o usuário pelo campo `{id}`                     |

Obs: o método HTTP `PUT` foi desabilitado nesse serviço devido ao método HTT `PATCH` atendenter a necessidade de atualizações.

### GET
O método GET retorna as informações a respeito de um usuário específico, ou todos, em formato **JSON** conforme exemplo abaixo:
```json
{
    "id": 1, 
    "name": "Bruno Baehr", 
    "cpf": "123.456.789-98", 
    "email": "email@email.com", 
    "phone_number": "(47) 9999-9999", 
    "created_at": "2022-06-05 13:57:40.721212", 
    "updated_at": null
}
```
`id`: Id do usuário (Campo gerado pelo banco de dados).
\
`name`: Nome do usuário (Campo obrigatório);
\
`cpf`: CPF do usuário (Campo obrigatório);
\
`email`: Email do usuário (Campo opcional, exibe `null` caso não exista);
\
`phone_number`: Telefone do usuário (Campo opcional, exibe `null` caso não exista);
\
`created_at`: Data e hora de criação do usuário (Campo gerado pelo banco de dados);
\
`updated_at`: Data e hora da última atualização do usuário (Campo gerado pelo banco de dados, exibe `null` caso não exista);

### GET - Orders
O endpoint `users/{id}/orders` retorna todas as ordens para o usuário filtrado. 
\
Ela comunica diretamente com o serviço **Order_API**, em outro container, para listar as ordens em formato **JSON**, conforme exemplo abaixo:
```json
[
    {
        "id": 3, 
        "user_id": 1, 
        "item_description": "Grampeador", 
        "item_quantity": "1", 
        "item_price": "15", 
        "total_value": "15", 
        "created_at": "2022-06-05 20:11:35.474559", 
        "updated_at": null
    }
]
```
`id`: Id da ordem.
\
`user_id`: Id do usuário;
\
`item_description`: Descrição do item;
\
`item_quantity`: Quantidade;
\
`item_price`: Preço;
\
`total_value`: Total;
\
`created_at`: Data e hora de criação da ordem;
\
`updated_at`: Data e hora da última atualização da ordem;


### POST
O método POST é responsável por criar um usuário no serviço e necessita das seguintes informações em formato **JSON**
```json
{
    "name": "nome",
    "cpf": "cpf",
    "email": "email",
    "phone_number": "telefone"
}
```
`nome`: Nome do usuário em formato **string** (Não permite vazio);
\
`cpf`: CPF do usuário em formato **string** (Não permite vazio);
\
`email`: Nome do usuário em formato **string** (Campo opcional);
\
`phone_number`: Telefone em formato **string** (Campo opcional);


O retorno do método POST após executado retorna o usuário criado.
```json
{
    "id": 99, 
    "name": "Novo Cadastro", 
    "cpf": "123.456.789-33", 
    "email": "teste@email.com", 
    "phone_number": null, 
    "created_at": "2022-06-05 13:57:40.721212", 
    "updated_at": null
}
```



Obs: Não é realizada nenhuma validação nos dados se os campos são válidos.
\
Obs2: Os campos `name`, `cpf` e `phone_number` são salvos no banco de dados criptografados (ofuscados).


### PATCH
O método PATCH é responsável por atualizar os dados do usuário no serviço e necessita das seguintes informações em formato **JSON**
```json
{
    "name": "nome",
    "cpf": "cpf",
    "email": "email",
    "phone_number": "telefone"
}
```
`nome`: Nome do usuário em formato **string** (Campo opcional, não permite vazio);
\
`cpf`: CPF do usuário em formato **string** (Campo opcional, não permite vazio);
\
`email`: Nome do usuário em formato **string** (Campo opcional);
\
`phone_number`: Telefone em formato **string** (Campo opcional);

O retorno do método PATCH após executado retorna o usuário alterado.
```json
{
    "id": 99, 
    "name": "Novo Cadastro (Alterado)", 
    "cpf": "123.456.789-33", 
    "email": "teste@email.com", 
    "phone_number": "(47 8888-8888)", 
    "created_at": "2022-06-05 13:57:40.721212", 
    "updated_at": "2022-06-05 13:59:13.773712"
}
```

Obs: Os campos não informados serão ignorados na atualização.
\
Obs2: Não é realizada nenhuma validação nos dados se os campos são válidos.
\
Obs3: Os campos `name`, `cpf` e `phone_number` são salvos no banco de dados criptografados (ofuscados).

### DELETE
O método DELETE é responsável por deletar usuários e não necessita nenhuma informação, apenas a chamada ao endpoint passando o `id` do usuário.

O método DELETE retorna o **JSON** abaixo quando concluído com sucesso.
```json
{'detail': 'User deleted!'}
```

### ERROS
Caso ocorra algum erro em algum endpoint, será retornado o **JSON** abaixo com mais informações sobre o erro.
\
Exemplo 1:
```json
{'detail': 'User not found!'}
```

Exemplo 2:
```json
{"detail":"HTTPConnectionPool(host='localhost', port=8080): Max retries exceeded with url: /users/1 (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x7f6a19dadf40>: Failed to establish a new connection: [Errno 111] Connection refused'))"}
```





