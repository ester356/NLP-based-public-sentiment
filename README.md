# NLP-based-public-sentiment

# services - 系统服务层 / System Service Layer

该目录包含系统提供的核心**业务服务模块**。  
每个模块负责处理具体业务逻辑，与控制器（如 API 接口）解耦，提升系统的模块化与可维护性。

This directory contains core **business service modules** for the system.  
Each module is responsible for processing business logic and serving APIs or controllers.

---

## 📌 当前功能 / Implemented Features

| 功能模块         | 简要说明 / Description                         |
|------------------|-----------------------------------------------|
| 用户注册与登录   | 普通用户通过 `user` 表注册与验证登录信息       |
| 管理员注册与登录 | 限定 ID 的管理员可通过 `admin` 表注册与登录    |

---

## 🧑‍💻 用户注册与登录 / User Registration & Login

### 📄 功能说明：

- 用户通过 `register(username, password)` 注册账号。
- 登录使用 `login(id, password)` 进行身份验证。
- 注册成功后，默认：
  - `permission = 0`（普通用户权限）
  - `admi_id = 1`（默认归属于管理员 ID 为 1）

### ✅ 使用示例：

```python
from services.user_service import register, login

# 用户注册
register("user123", "password123")

# 用户登录
login("user123", "password123")

```
## 👨‍💼 管理员注册与登录 / Admin Registration & Login

### 📄 功能说明：

- 管理员通过 `register(id, password)` 进行注册，ID 必须为 1、2、3 或 4。  
- 登录使用 `login(id, password)` 验证身份。  
- 系统最多支持 4 位管理员，ID 由系统限定。  
- 注册时会记录注册时间 `create_time`。

### ✅ 使用示例：

```python
from services.admin_db_manage import register, login

# 管理员注册（仅限 ID 为 1~4）
register(2, "adminpass")

# 管理员登录
login("2", "adminpass")
```

