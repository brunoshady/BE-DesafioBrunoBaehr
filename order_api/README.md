# Serviço Order_API

Este serviço é responsável por listar, exibir, criar, alterar e excluir ordens.

Ele é totalmente independente de outros serviços e seu container contém seu webservice (**FastAPI**), seu banco de dados (**PostgreSQL**) e seu serviço de cache em memória (**Redis**).

Para funcionamento com o serviço de users, é necessário que ambos estejam na mesma rede para comunicação, por este motivo, é necessário criar uma interface de rede no **Docker** com o seguinte comando:

`docker network create containers-shared`

Feito isto, basta subir o container do serviço executando o comando a seguir dentro da pasta `order_api`:

`docker compose up`

O serviço é iniciado na porta `8090` e seu acesso na máquina host pode ser realizado por http://localhost:8090.


Obs:
O serviço é iniciado com alguns dados fictícios que podem ser removidos/desabilitados posteriormente.



## Endpoints

O serviço possuí os seguintes endpoints:

| Método HTTP | Endpoint               | Descrição                                                 |
|-------------|------------------------|-----------------------------------------------------------|
| GET         | /                      | Redireciona a conexão para o endpoint `/orders`           |
| GET         | /orders                | Lista todas as ordens, ordenadas pelo `id` decrescente.   |
| GET         | /orders/{id}           | Exibe a ordem filtrando pelo campo `{id}`                 |
| GET         | /orders/user/{user_id} | Lista todas as ordens para o usuário filtrado `{user_id}` |
| POST        | /orders                | Cria uma nova ordem                                       |
| PATCH       | /orders/{id}           | Atualiza a ordem pelo campo `{id}`                        |
| DELETE      | /orders/{id}           | Deleta a ordem pelo campo `{id}`                          |

Obs: o método HTTP `PUT` foi desabilitado nesse serviço devido ao método HTT `PATCH` atendenter a necessidade de atualizações.

### GET
O método GET retorna as informações a respeito de uma ordem específico, ou todos, em formato **JSON** conforme exemplo abaixo:
```json
{
    "id": 3, 
    "user_id": 1, 
    "item_description": "Grampeador", 
    "item_quantity": 1, 
    "item_price": 15.0, 
    "total_value": 15.0, 
    "created_at": "2022-06-06T02:10:20.600226", 
    "updated_at": null
}
```
`id`: Id da ordem (Campo gerado pelo banco de dados).
\
`user_id`: Id do usuário da ordem (Campo obrigatório);
\
`item_description`: Descrição da ordem (Campo obrigatório);
\
`item_quantity`: Quantidade da ordem (Campo obrigatório);
\
`item_price`: Preço da ordem (Campo obrigatório);
\
`total_value`: Total da ordem (Campo calulado automaticamente com a multiplicação da dos campos `item_quantity` e `item_price`);
\
`created_at`: Data e hora de criação da ordem (Campo gerado pelo banco de dados);
\
`updated_at`: Data e hora da última atualização da ordem (Campo gerado pelo banco de dados, exibe `null` caso não exista);

### GET - Orders
O endpoint `orders/user/{user_id}` retorna todas as ordens para o usuário filtrado. 
\
Ela comunica diretamente com o serviço **User_API**, em outro container, para listar as ordens em formato **JSON**, conforme exemplo abaixo:
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
O método POST é responsável por criar uma ordem no serviço e necessita das seguintes informações em formato **JSON**
```json
{
    "user_id": 0,
    "item_description": "descrição",
    "item_quantity": 0,
    "item_price": 0
}
```
`user_id`: Id do usuário da ordem em formato **inteiro** (Campo obrigatório);
\
`item_description`: Descrição da ordem em formato **string** (Campo obrigatório, não permite vazio);
\
`item_quantity`: Quantidade da ordem em formato **inteiro** (Campo obrigatório);
\
`item_price`: Preço da ordem em formato **numérico** (Campo obrigatório);


O retorno do método POST após executado retorna a ordem criada.
```json
{
    "id": 99, 
    "user_id": 9, 
    "item_description": "Nova Ordem", 
    "item_quantity": "1", 
    "item_price": "100", 
    "total_value": "100", 
    "created_at": "2022-06-05 22:11:35.474559", 
    "updated_at": null
}
```
Obs: O campo `user_id` é validado junto ao serviço **User_API** para verificar se o usuário realmente existe, e caso o usuário não exista, é retornado um erro.



### PATCH
O método PATCH é responsável por atualizar os dados da ordem no serviço e necessita das seguintes informações em formato **JSON**
```json
{
    "user_id": 0,
    "item_description": "descrição",
    "item_quantity": 0,
    "item_price": 0
}
```
`user_id`: Id do usuário da ordem em formato **inteiro** (Campo opcional);
\
`item_description`: Descrição da ordem em formato **string** (Campo opcional, não permite vazio);
\
`item_quantity`: Quantidade da ordem em formato **inteiro** (Campo opcional);
\
`item_price`: Preço da ordem em formato **numérico** (Campo opcional);


O retorno do método PATCH após executado retorna a ordem alterada.
```json
{
    "id": 99, 
    "user_id": 9, 
    "item_description": "Nova Ordem Alterada", 
    "item_quantity": "1", 
    "item_price": "100", 
    "total_value": "100", 
    "created_at": "2022-06-05 22:11:35.474559", 
    "updated_at": "2022-06-05 22:12:37.412539"
}
```

Obs: Os campos não informados serão ignorados na atualização.
Obs2: O campo `user_id` é validado junto ao serviço **User_API** para verificar se o usuário realmente existe, e caso o usuário não exista, é retornado um erro.

### DELETE
O método DELETE é responsável por deletar ordens e não necessita nenhuma informação, apenas a chamada ao endpoint passando o `id` da ordem.

O método DELETE retorna o **JSON** abaixo quando concluído com sucesso.
```json
{'detail': 'Order deleted!'}
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





