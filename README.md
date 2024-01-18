Projeto criado para criação de APIs para um site protótipo.

Instalação das dependências:
    Foi utilizado a ferramenta Anaconda para gerenciar bibliotecas, ela pode ser obtida no seguinte site: https://www.anaconda.com/download
    Foi utilizado a versão 3.11 do Python. Para criar um ambiente virtual para o projeto foi utilizado o comando:
    
    conda create -n projeto_simples python=3.11 anaconda
    conda activate projeto_simples

    As dependências requeridas para o projeto, podem ser encontradas no arquivo requirements.txt, e o comando para instalação é:

    pip install -r requirements.txt

Instalação do banco de dados:

    No diretório raíz do projeto, existe um arquivo chamado create_db.py. Esse arquivo cria o nosso banco de dados(SQLite) e também cria um primeiro usuário desse banco de dados. Para rodá-lo basta abrir a pasta no seu terminal(Lembre-se de estar com o venv ativado) e digitar:
    python create_db.py

    As credenciais criadas como padrão são: usuário felipechinen e senha password.

Rodar o FastAPI:
    
    Após rodar todos os comandos até aqui, basta então rodar o arquivo main.py no seu terminal, utilizando:
    python main.py

    O FastAPI cria uma documentação web automaticamente, no qual você pode utilizar as APIs pelo navegador, bastando acessar: 127.0.0.1:8000/docs

Endpoints:

POST /token :
    Esse endpoint faz a autenticação, verificando no banco de dados se o usuário passado é válido, utilizando uma hash SHA-256 gerada a partir do arquivo ./pem_files/user_pwd_secret.txt
    Além disso, essa authenticação expira após 60 minutos.

POST /users :
    Endpoint para inserir novos usuários no banco de dados.
    Como input necessita de um login, senha e se o usuário é válido. É feito um hash da senha(Conforme descrito anteriormente) e então armazenada no banco de dados.

GET /users :
    Esse endpoint retorna uma lista que contém todos os usuários do banco de dados(username, is_valid, email). E foi utilizado basicamente para verificar se a criação está ocorrendo de maneira correta.

POST /genre_type:
    Adiciona um novo tipo de genero na tabela GenreType no banco de dados. Essa tabela contém um id e um nome e será utilizado como tabela lookup para os generos dos filmes

GET /genre_type:
    Obtém todos os gêneros adicionados na tabela GenreType

PUT /genre_type:
    Modifica o gênero de uma tupla do banco de dados. Deve-se passar o genre_id do gênero e seu novo nome.

DELETE /genre_type:
    Deleta 1 ou mais generos se tiverem nomes duplicados no banco. Pode-se passar tanto o genre_id quanto o genre_name.

GET /movie
    Lê do banco, todos os filmes do banco(Contém filtro de offset e limit). Volta apenas as informações gerais do filme(Nome, Data de lançamento e o id do gênero)
    Se passar o parametro genre_id diferente de 0, o banco irá procurar os filmes daquele gênero, senão irá pegar todos os filmes.

GET /full_movie
    Lê do banco o filme do id que você passar. Retorna todas as informações do filme(Contendo nome, data de lançamento, id do gênero, nota, elenco, diretor e sinopse).

POST /full_movie
    Adiciona no banco um filme completo.
    Esse endpoint popula 2 tabelas, uma que contém apenas informações gerais do filme e outra que contém informações de descrição.

DELETE /full_movie
    Remove do banco um filme. Deve-se passar o id do filme para removê-lo. Ele remove também a descrição desse filme.

PUT /movie_description
    Modifica apenas a descrição de um filme. Para isso, deve-se passar o movie_id do filme.