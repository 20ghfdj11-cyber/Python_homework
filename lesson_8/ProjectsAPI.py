import requests


class ProjectsAPI:
    def __init__(self, url: str) -> None:
        self.base_url = url.rstrip("/")
        self.token = None

    def _authenticate(self, login: str, password: str):
        body = {"login": login, "password": password}
        resp = requests.post(f"{self.base_url}/api-v2/auth/keys/get", json=body)

        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise ConnectionError(
                f"Ошибка авторизации ({resp.status_code}): {e.response.text}"
            ) from e

        data = resp.json()
        if isinstance(data, dict):
            key = data.get("key")
        elif isinstance(data, list):
            key = data[0].get("key") if data else None

        if not key:
            raise ValueError(f'Поле "key" отсутствует в ответе сервера: {data}')

        self.token = key

    def get_keys_list(self, login: str, password: str):
        self._authenticate(login, password)
        return self.token

    def create_project(self, title: str, token: str):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        payload = {"title": title}
        resp = requests.post(
            f"{self.base_url}/api-v2/projects", json=payload, headers=headers
        )

        try:
            j = resp.json()
            proj_id = j.get("id") if isinstance(j, dict) else None
        except Exception:
            proj_id = resp.text.strip('"')

        return resp, proj_id

    def update_project(self, project_id: str, new_title: str, token: str):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        payload = {"title": new_title}
        resp = requests.put(
            f"{self.base_url}/api-v2/projects/{project_id}",
            json=payload,
            headers=headers,
        )

        if resp.status_code in [401, 403]:
            resp = requests.put(
                f"{self.base_url}/api-v2/projects/{project_id}?key={token}",
                json=payload,
            )
        return resp

    def get_project_list(self, token: str):
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.get(f"{self.base_url}/api-v2/projects", headers=headers)
        if resp.status_code in [401, 403]:
            resp = requests.get(f"{self.base_url}/api-v2/projects?key={token}")
        return resp

    def get_project_id(self, project_id: str, token: str):
        urls_to_try = [
            f"{self.base_url}/api-v2/projects/{project_id}",
            f"{self.base_url}/api-v2/projects?id={project_id}",
        ]

        for u in urls_to_try:
            headers = {"Authorization": f"Bearer {token}"}
            resp = requests.get(u, headers=headers)
            if resp.status_code == 200 and self._contains_project(
                resp.json(), project_id
            ):
                return resp

            resp = requests.get(f"{u}?key={token}")
            if resp.status_code == 200 and self._contains_project(
                resp.json(), project_id
            ):
                return resp

        fake_resp = requests.Response()
        fake_resp.status_code = 404
        return fake_resp

    def delete_project(self, project_id: str, token: str):
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.delete(
            f"{self.base_url}/api-v2/projects/{project_id}", headers=headers
        )
        if resp.status_code in [401, 403]:
            resp = requests.delete(
                f"{self.base_url}/api-v2/projects/{project_id}?key={token}"
            )
        return resp

    def _contains_project(self, data, search_id):
        if not isinstance(data, dict):
            return False

        possible_keys = ["content", "result", "items", "projects", "project", "data"]

        for key in possible_keys:
            items = data.get(key)
            if isinstance(items, list):
                for item in items:
                    if isinstance(item, dict) and item.get("id") == search_id:
                        return True
            elif isinstance(items, dict) and items.get("id") == search_id:
                return True

        if data.get("id") == search_id:
            return True

        return False
