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