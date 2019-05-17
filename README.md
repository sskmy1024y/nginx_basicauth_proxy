# Nginx Basic Authentication Proxy

Nginxのauth_request_moduleでBasic認証を用いたプロキシをするやつ

## Try

```
docker-compose up -d

# Open http://0.0.0.0:8000 in browser

```


# api

## auth

権限の判断は全て `Basic認証` で行う。 
また権限パスの指定は、全て**前方一致**で行なっている。

#### Example
* `/auth/users`
  * [Get userdata](#get-users-list) も [Get users list](#get-users-list) も叩ける.
* `/auth/users/`
  * [Get userdata](#get-users-list) は叩けるが、 [Get users list](#get-users-list) は叩けない.
* `/private/`
  * `base_url/private/index.html` や `base_url/private/secret/` などにもアクセスできる


### is_auth

 | method | endopoint               | auth require |
 | :----: | ----------------------- | :----------: |
 |  GET   | `base_url/auth/is_auth` |      ×       |

権限があるかどうかを返すエンドポイント。基本的にnginxからのみ呼ばれ、権限がある場合にのみ `200 OK` を返す。



## users

### Get users list
  | method | endopoint             | auth require |
  | :----: | --------------------- | :----------: |
  |  GET   | `base_url/auth/users` |      ○       |
  
ユーザ情報一覧を返すエンドポイント

* response body sample:
  * success `200 OK`
  ```json
  [
    {
        "id": 1,
        "name": "admin",
        "pathlist": [
            "/"
        ]
      },
      {
          "id": 2,
          "name": "test",
          "pathlist": [
              "/private"
          ]
      }
  ]
  ```

### Register user

| method | endopoint             | auth require |
| :----: | --------------------- | :----------: |
|  POST  | `base_url/auth/users` |      ○       |
  

* request body sample:
```json
{
  "name": "hogehoge",
  "password": "password",
  "pathlist": "/private, /auth"
}
```

* response body sample:
  * success `201 Created`
  ```json
  {
    "id": 3,
    "name": "hogehoge",
    "pathlist": [
        "/private",
        "/auth"
    ]
  }
  ```

  * conflict user name `409 Conflict`
  ```json
  "409 Conflict"
  ```

### Get Userdata

| method | endopoint                 | auth require |
| :----: | ------------------------- | :----------: |
|  GET   | `base_url/auth/users/:id` |      ○       |

* response body sample:
  * success `200 OK`
  ```json
  {
    "id": 3,
    "name": "hogehoge",
    "pathlist": [
        "/private",
        "/auth"
    ]
  }
  ```

  * user is not found `404 Not found`
  ```json
  "User is not found"
  ```

### update Userdata

| method | endopoint                 | auth require |
| :----: | ------------------------- | :----------: |
|  PUT   | `base_url/auth/users/:id` |      ○       |
  
* request body sample:
```json
{
  "name": "hogehoge",
  "password": "password2",
  "pathlist": "/"
}
```

```json
{
  "pathlist": "/private, /auth"
}
```

* response body sample:
  * success `204 No Content`
  ```json
  ```

  * user is not found `404 Not found`
  ```json
  "User is not found"
  ```

### delete Userdata

| method | endopoint                 | auth require |
| :----: | ------------------------- | :----------: |
| DELETE | `base_url/auth/users/:id` |      ○       |
  
* response body sample:
  * success `204 No Content`
  ```json
  ```

  * user is not found `404 Not found`
  ```json
  "User is not found"
  ```

