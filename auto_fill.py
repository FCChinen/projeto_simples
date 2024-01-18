import requests
import json

class Management:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000"
        self.username = "felipechinen"
        self.password = "password"
        self.token = self.login()

    def login(self) -> str:
        url = f"{self.base_url}/token"

        payload = f'username={self.username}&password={self.password}'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code != 200:
            response.raise_for_status()

        return response.json()['access_token']
    
    def add_genre_type(self, genre_name: str) -> dict:
        url = f"{self.base_url}/genre_type"

        payload = {}
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        params = {
            "genre_name": genre_name
        }

        response = requests.request("POST", url, headers=headers, data=payload, params=params)
        if response.status_code != 200:
            response.raise_for_status()

        return response.json()

    def get_genre_types(self) -> list:
        url = f"{self.base_url}/genre_type"
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.request("GET", url, headers=headers)
        if response.status_code != 200:
            response.raise_for_status()
        return response.json()

    def add_movie(self, payload) -> dict:
        url = f"{self.base_url}/full_movie"
        payload = payload
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.request("POST", url=url, headers=headers, json=payload)

        if response.status_code != 200:
            print(response.text)
            response.raise_for_status()

        return response.json()  

    def get_all_movie(self) -> dict:
        url = f"{self.base_url}/movie"
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.request("GET", url=url, headers=headers)

        if response.status_code != 200:
            response.raise_for_status()

        return response.json()
    
if __name__ == "__main__":
    m = Management()
    with open('auto_fill.json', 'r') as f:
        a = f.read()
        movies_pl = json.loads(a)
    genre_name = []
    genre_dict = {}
    for mv in movies_pl:
        if mv['movie']['genre_name'] not in genre_name:
            response = m.add_genre_type(mv['movie']['genre_name'])
            genre_dict[response['genre_name']] = response['genre_id']
            genre_name.append(mv['movie']['genre_name'])
        mv['movie']['fk_genre_id'] = genre_dict[mv['movie']['genre_name']]
        m.add_movie(payload=mv)

    print(f"Gêneros no banco de dados: {m.get_genre_types()}")
    print(f"Filmes no banco: {m.get_all_movie()}")