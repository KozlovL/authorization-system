# Authorization System (Система аутентификации и авторизации)

## Автор

**Козлов Леонид** [GitHub](https://github.com/KozlovL)

---

## Описание проекта

Проект представляет собой **собственную систему аутентификации и авторизации**, реализованную на Python 3.12 с использованием Django и Django REST Framework.
Основная цель — показать, как можно реализовать **свою систему разграничения прав доступа** к различным ресурсам, не полагаясь полностью на "из коробки" решения. В проекте настроен линтер ruff для улучшения читаемости кода.

## Функциональность

1. **Аутентификация пользователей**

   * Регистрация нового пользователя с email, паролем и именем.
   * Login: пользователи входят в систему по email и паролю.
   * Logout: удаление refresh токена.
   * Обновление профиля: пользователь может редактировать свои данные.
   * Мягкое удаление: при удалении аккаунта `is_active` выставляется в `False`.

2. **Авторизация и разграничение прав**

   * Реализована через **роли пользователей** (`Admin`, `Manager`, `User`) и **правила доступа** (`AccessRule`), которые определяют:

     * доступ к ресурсам (read, create, update, delete);
     * права на все объекты (`*_all_permission`) или только на свои (`*_owned_permission`).
   * Минимальные бизнес-ресурсы:

     * `BusinessResource` (например, товары, заказы, магазины)
     * `BusinessObject` — объекты ресурсов с владельцем (`owner`).
   * При запросе проверяется:

     * Если пользователь не авторизован → ошибка 401
     * Если доступ запрещён → ошибка 403
   * Администратор может менять роли пользователей и управлять правилами доступа через API.

3. **Тестовые данные**

   * В проекте есть фикстуры в директории `fixtures`:

     * Пользователи (`users.json`)
     * Роли (`roles.json`)
     * Правила доступа (`access_rules.json`)
     * Бизнес-ресурсы (`business_resources.json`)
     * Бизнес-объекты (`business_objects.json`)
   * Это позволяет быстро поднять проект для демонстрации работы системы.

---

## Структура проекта

```
authorization-system
├─ access             # Модуль управления ролями и правилами доступа
├─ api                # API эндпоинты и кастомные пермишены
├─ backend            # Настройки Django
├─ business_objects   # Бизнес-ресурсы и объекты
├─ fixtures           # Фикстуры для наполнения базы
├─ users              # Пользователи и сериализаторы
├─ docker-compose.yml
├─ Dockerfile
├─ manage.py
├─ requirements.txt
└─ pyproject.toml
```

---

## Docker и запуск

Проект полностью работает в **Docker Compose**.

### 1. Клонирование репозитория

```bash
git clone https://github.com/KozlovL/authorization-system
cd authorization-system
```

### 2. Копирование .env файла

```bash
cp .env.example .env
```

### 3. Сборка и запуск сервисов

```bash
docker compose up -d --build
```

> В контейнерах поднимается Django и Postgres для хранения данных.

> Документация доступна по адресам: http://127.0.0.1:8000/redoc/ и http://127.0.0.1:8000/swagger/

---

## Основные API эндпоинты

### Пользователи

| Метод  | URL                            | Назначение                                    |
| ------ | ------------------------------ | --------------------------------------------- |
| POST   | `/api/users/`                  | Регистрация пользователя                      |
| GET    | `/api/users/`                  | Получение списка пользователей (только админ) |
| GET    | `/api/users/{id}/`             | Получение профиля пользователя                |
| PATCH  | `/api/users/{id}/`             | Обновление данных профиля                     |
| PATCH  | `/api/users/{id}/update-role/` | Смена роли пользователя (только админ)        |
| DELETE | `/api/users/{id}/`             | Мягкое удаление пользователя                  |

### Аутентификация

| Метод | URL                  | Назначение            |
| ----- | -------------------- | --------------------- |
| POST  | `/api/auth/login/`   | Вход пользователя     |
| POST  | `/api/auth/logout/`  | Выход пользователя    |
| POST  | `/api/auth/refresh/` | Обновление JWT токена |

### Бизнес-ресурсы и объекты

| Метод  | URL                                      | Назначение                          |
| ------ | ---------------------------------------- | ----------------------------------- |
| GET    | `/api/business-objects/?resource=<name>` | Получение объектов ресурса (list)   |
| POST   | `/api/business-objects/`                 | Создание объекта ресурса            |
| PATCH  | `/api/business-objects/{id}/`            | Обновление объекта (partial_update) |
| DELETE | `/api/business-objects/{id}/`            | Удаление объекта                    |

> Для `list` обязательно указывать query-параметр `resource`.  
> Для `create` параметр `resource` передаётся в теле запроса JSON.

### Правила доступа (Access Rules)

| Метод | URL                  | Назначение                                |
| ----- | -------------------- | ----------------------------------------- |
| GET   | `/api/access-rules/` | Получение списка правил доступа (только админ) |
| PATCH | `/api/access-rules/{id}/` | Обновление правила доступа (только админ) |

---

## Схема прав доступа

* Таблица **Roles** — роли пользователей (`Admin`, `Manager`, `User`)
* Таблица **BusinessResource** — бизнес-ресурсы (товары, заказы, магазины)
* Таблица **BusinessObject** — объекты ресурсов с владельцем (`owner`)
* Таблица **AccessRule** — правила доступа для каждой роли к ресурсу

  * `read_all_permission`, `read_owned_permission`
  * `create_permission`
  * `update_all_permission`, `update_owned_permission`
  * `delete_all_permission`, `delete_owned_permission`

> Все столбцы `_all_permission` и `_owned_permission` имеют тип bool и определяют, может ли пользователь действовать со всеми объектами или только со своими.

---


## Примеры данных (Fixtures) для authorization-system

Ниже приведены примеры данных, используемых в системе для демонстрации работы аутентификации, авторизации и доступа к бизнес-ресурсам. Полные JSON-файлы находятся в папке `fixtures/`.

---

### Роли пользователей

| ID | Название роли |
| -- | ------------- |
| 1  | Admin         |
| 2  | Manager       |
| 3  | User          |

---

### Пользователи

| ID | Email               | Username | Роль     | Активен |
| -- | ------------------ | -------- | -------- | ------- |
| 1  | admin@example.com   | admin    | Admin    | true    |
| 2  | manager@example.com | manager  | Manager  | true    |
| 3  | user@example.com    | user     | User     | true    |

> Пароли хэшированы и безопасно хранятся в базе.

> У каждого пользователя пароль `Password_123`

---

### Бизнес-ресурсы

| ID | Имя      | Описание |
| -- | -------- | -------- |
| 1  | products | Товары   |
| 2  | orders   | Заказы   |
| 3  | shops    | Магазины |

---

### Бизнес-объекты

| ID | Название     | Ресурс    | Владелец |
| -- | ----------- | -------- | -------- |
| 1  | Товар 1     | products | admin    |
| 2  | Товар 2     | products | admin    |
| 3  | Товар 3     | products | manager  |
| 4  | Заказ 1     | orders   | manager  |
| 5  | Заказ 2     | orders   | user     |
| 6  | Заказ 3     | orders   | user     |
| 7  | Магазин 1   | shops    | admin    |
| 8  | Магазин 2   | shops    | manager  |
| 9  | Магазин 3   | shops    | user     |

---

### Правила доступа (Access Rules)

| ID | Роль     | Ресурс   | Read All | Read Owned | Create | Update All | Update Owned | Delete All | Delete Owned |
| -- | -------- | -------- | -------- | ---------- | ------ | ---------- | ------------ | ---------- | ------------ |
| 1  | Admin    | products | true     | true       | true   | true       | true         | true       | true         |
| 2  | Manager  | products | false    | true       | true   | false      | true         | false      | false        |
| 3  | User     | products | false    | true       | false  | false      | false        | false      | false        |
| 4  | Admin    | orders   | true     | true       | true   | true       | true         | true       | true         |
| 5  | Manager  | orders   | false    | true       | true   | false      | true         | false      | false        |
| 6  | User     | orders   | false    | true       | false  | false      | false        | false      | false        |
| 7  | Admin    | shops    | true     | true       | true   | true       | true         | true       | true         |
| 8  | Manager  | shops    | false    | true       | true   | false      | true         | false      | false        |
| 9  | User     | shops    | false    | true       | false  | false      | false        | false      | false        |

> `Read All`, `Update All`, `Delete All` — права на любые объекты ресурса.  
> `Read Owned`, `Update Owned`, `Delete Owned` — права только на свои объекты.

---





# Примеры запросов к API

## Аутентификация

### POST `/api/auth/login/`

Вход пользователя, получение пары JWT токенов (access + refresh).

**Пример запроса:**

```json
{
  "email": "user@example.com",
  "password": "Password_123"
}
```

**Пример ответа (200 OK):**

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJh...",
  "access": "eyJ0eXAiOiJKV1QiLCJh..."
}
```

**Ошибка при деактивированном пользователе:**

```json
{
  "non_field_errors": ["Пользователь деактивирован."]
}
```

---

### POST `/api/auth/refresh/`

Обновление access токена по refresh токену.

**Пример запроса:**

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJh..."
}
```

**Пример ответа (200 OK):**

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJh..."
}
```

---

### POST `/api/auth/logout/`

Выход пользователя, добавление refresh токена в blacklist.

**Пример запроса:**

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJh..."
}
```

**Пример ответа (204 No Content):**

```json
{
  "detail": "Успешный логаут."
}
```

**Ошибки:**

```json
{
  "detail": "Требуется refresh токен."
}
```

или

```json
{
  "detail": "Неверный refresh токен."
}
```


## Работа с пользователями

### Регистрация пользователя

**URL:** `/api/users/`
**Метод:** POST
**Права:** доступно всем (AllowAny)

**Пример запроса:**

```json
{
  "email": "newuser@example.com",
  "username": "newuser",
  "first_name": "Новый",
  "last_name": "Пользователь",
  "password": "Password_123",
  "password_confirm": "Password_123"
}
```

**Пример ответа:**

```json
{
  "id": 4,
  "email": "newuser@example.com",
  "username": "newuser",
  "first_name": "Новый",
  "last_name": "Пользователь",
  "role": {
    "id": 3,
    "name": "User"
  }
}
```

---

### Получение списка пользователей

**URL:** `/api/users/`
**Метод:** GET
**Права:** только админ

**Пример ответа:**

```json
[
  {
    "id": 1,
    "email": "admin@example.com",
    "username": "admin",
    "first_name": "Админ",
    "last_name": "Админов",
    "role": {"id": 1, "name": "Admin"}
  },
  {
    "id": 2,
    "email": "manager@example.com",
    "username": "manager",
    "first_name": "Менеджер",
    "last_name": "Менеджеров",
    "role": {"id": 2, "name": "Manager"}
  }
]
```

---

### Получение профиля пользователя

**URL:** `/api/users/{id}/`
**Метод:** GET
**Права:** админ или владелец профиля

**Пример ответа:**

```json
{
  "id": 3,
  "email": "user@example.com",
  "username": "user",
  "first_name": "Пользователь",
  "last_name": "Пользователей",
  "role": {"id": 3, "name": "User"}
}
```

---

### Обновление профиля пользователя

**URL:** `/api/users/{id}/`
**Метод:** PATCH
**Права:** админ или владелец профиля

**Пример запроса:**

```json
{
  "first_name": "Иван",
  "last_name": "Иванов"
}
```

**Пример ответа:**

```json
{
  "id": 3,
  "email": "user@example.com",
  "username": "user",
  "first_name": "Иван",
  "last_name": "Иванов",
  "role": {"id": 3, "name": "User"}
}
```

---

### Смена роли пользователя

**URL:** `/api/users/{id}/update-role/`
**Метод:** PATCH
**Права:** только админ

**Пример запроса:**

```json
{
  "role": "Manager"
}
```

**Пример ответа:**

```json
{
  "id": 3,
  "email": "user@example.com",
  "username": "user",
  "first_name": "Пользователь",
  "last_name": "Пользователей",
  "role": {"id": 2, "name": "Manager"}
}
```

---

### Мягкое удаление пользователя

**URL:** `/api/users/{id}/`
**Метод:** DELETE
**Права:** админ или владелец профиля

**Пример запроса:**

```json
{
  "refresh": "<refresh_token>"
}
```

**Пример ответа:**

```
204 No Content
```


## Работа с бизнес-объектами

### CRUD для бизнес-объектов конкретного ресурса

Все действия требуют аутентификацию (JWT access token). Для `list` обязательно передавать query-параметр `resource`.

---

### Получение списка объектов ресурса (list)

**Метод:** GET
**URL:** `/api/business-objects/?resource=<name>`
**Пример запроса:**

```bash
curl -H "Authorization: Bearer <access_token>" \
     http://localhost:8000/api/business-objects/?resource=products
```

**Пример ответа:**

```json
[
  {
    "id": 1,
    "name": "Товар 1",
    "description": "Описание товара 1",
    "resource": {
      "id": 1,
      "name": "products",
      "description": "Товары"
    },
    "owner": {
      "id": 1,
      "email": "admin@example.com",
      "username": "admin",
      "first_name": "Админ",
      "last_name": "Админов",
      "role": {
        "id": 1,
        "name": "Admin"
      }
    }
  }
]
```

---

### Получение одного объекта (retrieve)

**Метод:** GET
**URL:** `/api/business-objects/{id}/`
**Пример запроса:**

```bash
curl -H "Authorization: Bearer <access_token>" \
     http://localhost:8000/api/business-objects/1/
```

**Пример ответа:**

```json
{
  "id": 1,
  "name": "Товар 1",
  "description": "Описание товара 1",
  "resource": {
    "id": 1,
    "name": "products",
    "description": "Товары"
  },
  "owner": {
    "id": 1,
    "email": "admin@example.com",
    "username": "admin",
    "first_name": "Админ",
    "last_name": "Админов",
    "role": {
      "id": 1,
      "name": "Admin"
    }
  }
}
```

---

### Создание объекта (create)

**Метод:** POST
**URL:** `/api/business-objects/`
**Пример запроса:**

```bash
curl -X POST http://localhost:8000/api/business-objects/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
        "name": "Товар 10",
        "description": "Описание нового товара",
        "resource": "products"
      }'
```

**Пример ответа:**

```json
{
  "id": 10,
  "name": "Товар 10",
  "description": "Описание нового товара",
  "resource": {
    "id": 1,
    "name": "products",
    "description": "Товары"
  },
  "owner": {
    "id": 2,
    "email": "manager@example.com",
    "username": "manager",
    "first_name": "Менеджер",
    "last_name": "Менеджеров",
    "role": {
      "id": 2,
      "name": "Manager"
    }
  }
}
```

---

### Обновление объекта (partial_update)

**Метод:** PATCH
**URL:** `/api/business-objects/{id}/`
**Пример запроса:**

```bash
curl -X PATCH http://localhost:8000/api/business-objects/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
        "description": "Обновленное описание"
      }'
```

**Пример ответа:**

```json
{
  "id": 1,
  "name": "Товар 1",
  "description": "Обновленное описание",
  "resource": {
    "id": 1,
    "name": "products",
    "description": "Товары"
  },
  "owner": {
    "id": 1,
    "email": "admin@example.com",
    "username": "admin",
    "first_name": "Админ",
    "last_name": "Админов",
    "role": {
      "id": 1,
      "name": "Admin"
    }
  }
}
```

---

### Удаление объекта (destroy)

**Метод:** DELETE
**URL:** `/api/business-objects/{id}/`
**Пример запроса:**

```bash
curl -X DELETE http://localhost:8000/api/business-objects/1/ \
  -H "Authorization: Bearer <access_token>"
```

**Пример ответа:**

```http
HTTP 204 No Content
```

---

> **Примечания:**
>
> * Для `list` обязательно указывать query-параметр `resource`.
> * Для `create` поле `resource` передается в JSON (`"products"`, `"orders"`, `"shops"`).
> * Все действия требуют аутентифицированного пользователя. Права доступа проверяются через `BusinessResourcePermission`.


## Работа с правилами доступа

Эндпоинт для администраторов для управления правилами доступа ролей к бизнес-ресурсам.

> Все действия доступны только для пользователей с ролью **Admin**.

### Получение всех правил доступа

**GET** `/api/access-rules/`

**Пример запроса (c URL query не требуется)**:

```bash
curl -X GET "http://localhost:8000/api/access-rules/" \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

**Пример ответа:**

```json
[
  {
    "id": 1,
    "role": "Admin",
    "business_resource": "products",
    "read_owned_permission": true,
    "read_all_permission": true,
    "create_permission": true,
    "update_owned_permission": true,
    "update_all_permission": true,
    "delete_owned_permission": true,
    "delete_all_permission": true
  },
  {
    "id": 2,
    "role": "Manager",
    "business_resource": "products",
    "read_owned_permission": true,
    "read_all_permission": false,
    "create_permission": true,
    "update_owned_permission": true,
    "update_all_permission": false,
    "delete_owned_permission": false,
    "delete_all_permission": false
  }
]
```

---

### Обновление правил доступа

**PATCH** `/api/access-rules/{id}/`

**Пример запроса:**

```bash
curl -X PATCH "http://localhost:8000/api/access-rules/2/" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "create_permission": false,
    "update_owned_permission": false
  }'
```

**Пример ответа:**

```json
{
  "id": 2,
  "role": "Manager",
  "business_resource": "products",
  "read_owned_permission": true,
  "read_all_permission": false,
  "create_permission": false,
  "update_owned_permission": false,
  "update_all_permission": false,
  "delete_owned_permission": false,
  "delete_all_permission": false
}
```

---

> Примечания:
>
> * Все запросы требуют JWT токен администратора в заголовке `Authorization: Bearer <ACCESS_TOKEN>`.
> * Только PATCH и GET методы поддерживаются.



---

## Технологии

* Python 3.12
* Django
* Django REST Framework
* PostgreSQL
* Docker + Docker Compose
* JWT для аутентификации

---

## Как работает система

1. При логине пользователю выдается JWT токен.
2. Каждый запрос проверяет `Authorization: Bearer <token>`.
3. Пермишены (`BusinessResourcePermission`) проверяют права пользователя на ресурс. По умолчанию правила таковы:

   * Админ имеет доступ ко всем объектам.
   * Менеджер/пользователь может работать только со своими объектами или с тем, на что есть разрешение.
4. Для бизнес-объектов `list` требует `resource` в query-параметре, `create` — в теле JSON.
5. Все изменения ролей и прав доступны только администраторам через соответствующие эндпоинты.
6. В проекте не предусмотрено создание новых бизнес-ресурса, роли, правила через API.
7. Рекомендуется тестировать приложение через `Postman`
---
