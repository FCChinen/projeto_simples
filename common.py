import hashlib


def hash_password(password: str):
    #  TODO: Criar um gerador de salt para cada usuário,
    # para melhoria de segurança
    with open("./pem_files/user_pwd_secret.txt", "r") as f:
        salt = f.read()
    pwd = salt+password
    pwd = pwd.encode('ascii')
    return hashlib.sha256(pwd).hexdigest()


if __name__ == '__main__':
    print(hash_password('password'))
