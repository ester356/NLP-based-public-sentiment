# NLP-based-public-sentiment

# services - 系统服务层 / System Service Layer

该目录包含系统提供的核心**业务服务模块**。  
每个模块负责处理具体业务逻辑，与控制器（如 API 接口）解耦，提升系统的模块化与可维护性。

This directory contains core **business service modules** for the system.  
Each module is responsible for processing business logic and serving APIs or controllers.

---

## 📌 当前功能 / Implemented Features

| 功能模块         | 简要说明 / Description                                         |
|------------------|---------------------------------------------------------------|
| 用户注册与登录   | 普通用户通过 `user` 表注册与验证登录信息                       |
| 管理员注册与登录 | 管理员通过 `admin` 表注册，限制 ID 只能为 1、2、3、4           |
| 用户管理（1号管理员） | 增加、删除用户，修改用户权限，仅允许管理员 ID 为 1 操作          |
| 文章管理（2号管理员） | 删除指定文章，仅允许管理员 ID 为 2 操作                        |
| （预留）评论管理（3号管理员） | 预留功能，暂无实现                                          |
| （预留）日记及舆情分析查看（4号管理员） | 预留功能，暂无实现                                   |

---

## 🧑‍💻 用户注册与登录 / User Registration & Login

### 📄 功能说明：

- 普通用户通过 `register(username, password)` 注册账号，注册时：
  - 生成当前时间 `create_time`
  - 默认权限 `permission = 0`
  - 绑定默认管理员 ID `admi_id = 1`
- 使用 `login(id, password)` 验证用户身份。

### ✅ 使用示例：

```python
# 用户注册
register("user123", "password123")

# 用户登录
login("user123", "password123")
```

## 👨‍💼 管理员注册与登录 / Admin Registration & Login

### 📄 功能说明：
- 管理员注册函数为 `register(id, password)`，但限制管理员 ID 只能为 1、2、3、4。  
- 管理员登录同样使用 `login(id, password)` 进行身份验证。  
- 系统会保存管理员的注册时间 `create_time`。

### ✅ 使用示例：

```python
# 管理员注册（ID 必须是 1~4）
register(2, "adminpass")

# 管理员登录
login("2", "adminpass")
```
## 👤 用户管理（1号管理员权限） / User Management by Admin #1

### 📄 功能说明：
仅管理员 ID 为 1 的账号允许进行以下操作：

- `add_user(user_id, password, permission, admin_id)`：新增用户，需传入管理员 ID（必须为 1）  
- `delete_user(user_id, admin_id)`：删除指定用户  
- `change_user_permission(user_id, new_permission, admin_id)`：修改用户权限  

增删改操作均会先检查用户是否存在，且所有操作会保持数据库连接。

### 示例代码：

```python
# 添加用户
add_user('6', '6', '1', 1)

# 删除用户
delete_user('6', 1)

# 修改用户权限
change_user_permission('1', 1, 1)
```
## 📝 文章管理（2号管理员权限） / Article Management by Admin #2

### 📄 功能说明：
仅管理员 ID 为 2 的账号允许删除文章：

- `delete_article(article_id, admin_id)`：删除指定文章

操作前会检查文章是否存在。

### 示例代码：

```python
# 删除文章
delete_article(5062309233296726, 2)
```
