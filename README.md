### 项目：django rest_framework 框架下邮箱用户

#### 一、简介

该项目是针对与邮箱用户注册使用的，项目已经把基础的功能写好，直接在该基础上填写业务功能即可。基础功能如下：

- 1、邮箱注册；
- 2、用户激活：使用 Celery 发送邮件注册邮箱用户，用户在指定时间内点击链接激活账户；
- 3、邮箱用户登陆并返回 Token；
- 4、登陆用户根据 Token 访问 API；
- 5、管理员登陆后使用 Token 访问 API 管理用户信息；
- 6、用户修改登陆密码，修改成功后发送邮件到用户邮箱通知修改密码成功
  > Token 生成使用的是 django rest_framework_simpleJWT

### API

- 注册用户:
  - auth/registration/
  - 参数：
    - username
    - password
    - email
  - 返回值：
    - id
    - email
    - created_at
    - updated_at
  - Celery 处理验证通知短信
- 验证用户：auth/email-verify/，这个 API 不需要单独使用，注册用户后自动会调用
- 用户登陆：
  - auth/login/
  - 参数：
    - email: 用户名或者邮箱都可以
    - password
  - 返回值：username 和 refresh，refresh 字典形式，又包括 refresh 和 access
- 登陆用户密码重设
  - 权限为：登陆的管理员用户
    > 需要注意的是：headers 传递 Authorization 的值必须是 Bearer 类型的，格式为：Bearer access 值
  - auth/reset/
  - 参数
    - username
    - password
    - email
  - 返回值
    - id
    - email
    - created_at
    - updated_at
  - Celery 处理设置成功通知短信
- 管理员查询所有用户
  - auth/users/
  - 权限为：登陆的管理员用户
  - Authorization 同上
  - 返回值：用户列表信息
- 管理员查询、更新、删除指定的用户信息
  - auth/user/<str:id>/
    > 需要注意的是：为来安全考虑，在该项目中使用 uuid 字段来作为 id 的值，是字符串，不是数值类型
  - 方法：
    - retrieve：获取单个用户
    - update：更新指定的用户信息，包括修改用户为管理员
    - destroy：删除指定的用户信息

### 配置信息

在该项目中邮件、celery 等基础的信息都需要开发者自己配置，开发者在项目的根目录下创建.env 文件配置对应的变量即可。变量包括：

- SECRET_KEY
- DEBUG
- 邮箱配置
  - EMAIL_USER_TLS
  - EMAIL_HOST
  - EMAIL_PORT
  - EMAIL_HOST_USER
  - EMAIL_HOST_PASSWORD
  - DEFAULT_FROM_EMAIL
  - EMAIL_BACKEND
  - FIRST_MSG：验证用户邮件内容的前半部分
  - LAST_MSG：验证用户邮件内容的后半部分
- simpleJWT 配置
  - ACCESS_TOKEN_LIFETIME
  - REFRESH_TOKEN_LIFETIME
- Celery 配置
  - CELERY_BROKER_URL
  - CELERY_RESULT_BACKEND
  - CELERY_ACCEPT_CONTENT
  - CELERY_TASK_SERIALIZER
  - CELERY_IGNORE_RESULT
  - CELERY_TIMEZONE
  - CELERY_TASK_TRACK_STARTED
  - CELERY_TASK_TIME_LIMIT
