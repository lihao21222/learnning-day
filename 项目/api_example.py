import requests
import json


class APIClient:
    def __init__(self, base_url="https://jsonplaceholder.typicode.com"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json"
        })

    def get_posts(self):
        url = f"{self.base_url}/posts"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_post(self, post_id):
        url = f"{self.base_url}/posts/{post_id}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def create_post(self, title, body, user_id):
        url = f"{self.base_url}/posts"
        data = {
            "title": title,
            "body": body,
            "userId": user_id
        }
        response = self.session.post(url, data=json.dumps(data))
        response.raise_for_status()
        return response.json()

    def update_post(self, post_id, title=None, body=None):
        url = f"{self.base_url}/posts/{post_id}"
        data = {}
        if title:
            data["title"] = title
        if body:
            data["body"] = body
        response = self.session.put(url, data=json.dumps(data))
        response.raise_for_status()
        return response.json()

    def delete_post(self, post_id):
        url = f"{self.base_url}/posts/{post_id}"
        response = self.session.delete(url)
        response.raise_for_status()
        return response.status_code == 200


def main():
    client = APIClient()

    print("=== API调用示例 ===\n")

    print("1. 获取所有文章:")
    posts = client.get_posts()
    print(f"成功获取 {len(posts)} 篇文章")
    print(f"第一篇文章: {json.dumps(posts[0], indent=2, ensure_ascii=False)}\n")

    print("2. 获取单篇文章 (ID: 1):")
    post = client.get_post(1)
    print(json.dumps(post, indent=2, ensure_ascii=False), "\n")

    print("3. 创建新文章:")
    new_post = client.create_post(
        title="测试标题",
        body="这是测试内容",
        user_id=1
    )
    print(json.dumps(new_post, indent=2, ensure_ascii=False), "\n")

    print("4. 更新文章 (ID: 1):")
    updated_post = client.update_post(
        post_id=1,
        title="更新后的标题"
    )
    print(json.dumps(updated_post, indent=2, ensure_ascii=False), "\n")

    print("5. 删除文章 (ID: 1):")
    deleted = client.delete_post(1)
    print(f"删除成功: {deleted}")


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.RequestException as e:
        print(f"API调用出错: {e}")
