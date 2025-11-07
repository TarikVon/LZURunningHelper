# LZU Running Helper - 快速使用指南

> 最近更新：支持多账号、JSON配置、Rich进度条、默认无需参数

## 🚀 快速开始

### 1. 单账号运行（最简单）

```bash
# 只需这一条命令，无需任何参数
python main.py
```

### 2. 多账号运行

#### 方式一：交互选择账号
```bash
python main.py
# 程序会显示账号列表，输入序号选择要运行的账号
```

#### 方式二：运行所有账号
```bash
python main.py -a
```

#### 方式三：运行指定账号
```bash
python main.py -i 0  # 运行第一个账号（序号0）
```

### 3. 查看配置
```bash
python main.py -c
```

---

## ⚙️ 配置说明

### 配置文件位置
- 主配置文件：`config.json`
- 示例文件：`config.example.json`

### 最小化配置（单账号）

```json
{
  "Base": {
    "APP": "Joyrun",
    "debug": true
  },
  "accounts": [
    {
      "name": "我的账号",
      "StudentID": "320250935091",
      "Password": "123456",
      "suffix": "@lzu.edu.cn",
      "record_type": "random",
      "record_number": 1,
      "distance": 4.8,
      "pace": 4.55,
      "stride_frequncy": 176
    }
  ]
}
```

### 多账号配置示例

```json
{
  "accounts": [
    {
      "name": "小王",
      "StudentID": "320250935091",
      "Password": "password1",
      "record_type": "random",
      ...
    },
    {
      "name": "小张",
      "StudentID": "320250935092",
      "Password": "password2",
      "record_type": "dongcao",
      ...
    }
  ]
}
```

### 配置参数详解

| 参数 | 说明 | 示例 |
|------|------|------|
| `name` | 账号显示名称 | `小王` |
| `StudentID` | 学号（不含@后缀） | `320250935091` |
| `Password` | 登录密码 | `123456` |
| `suffix` | 邮箱后缀 | `@lzu.edu.cn` |
| `Phone` | 验证码用手机号 | `13800138000` |
| `record_type` | 跑步路径选择 | `random`、`dongcao`、`xicao` |
| `record_number` | 具体路径号 | `0`(随机)、`1`(第1条)、`2`(第2条)... |
| `distance` | 跑步距离(km) | `4.8` |
| `pace` | 每公里用时(分钟) | `4.55` |
| `stride_frequncy` | 步幅(步/分钟) | `176` |

---

## 📋 命令参考

```bash
# 默认运行（推荐）
python main.py

# 显示配置信息
python main.py -c, --check

# 运行所有账号
python main.py -a, --all

# 运行指定账号（索引从0开始）
python main.py -i 0, --index 0
```

---

## ✨ 新功能特性

### 🎨 美观的进度条
上传时会显示彩色进度条，更直观地了解上传进度

### 📱 多账号支持
- 在一个配置文件中管理多个账号
- 灵活地选择运行哪个或哪些账号
- 每个账号可配置不同的跑步参数

### 🎯 默认执行上传
- 无需输入 `-s` 参数
- 默认直接执行上传操作
- 更加便捷高效

### 📄 JSON 配置格式
- 更加清晰易读的配置格式
- 支持注释说明
- 更容易扩展功能

---

## 🔧 常见问题

### Q1: 如何添加新账号？
**A:** 编辑 `config.json`，在 `accounts` 数组中添加新的账号对象即可。

### Q2: 运行时提示"账号验证失败"怎么办？
**A:** 
1. 检查学号和密码是否正确
2. 确保网络连接正常
3. 如有新设备登录，需要输入手机号进行短信验证

### Q3: 可以配置不同的跑步路径吗？
**A:** 可以。每个账号可独立配置：
- `record_type`: `dongcao`(东操)、`xicao`(西操)、`random`(随机)
- `record_number`: `0`(随机路径) 或 `1-N`(特定路径)

### Q4: 如何修改跑步距离或速度？
**A:** 编辑对应账号的配置：
- `distance`: 跑步距离(km)
- `pace`: 每公里用时(分钟)
- `stride_frequncy`: 步幅(步/分钟)

### Q5: 后台需要输入验证码怎么办？
**A:** 程序会提示输入手机号和验证码，按照提示操作即可。

---

## 📦 依赖安装

### 使用 UV（推荐）
```bash
uv sync
```

### 使用 pip
```bash
pip install -r requirements.txt
```

### 依赖列表
- `requests >= 2.32.0` - HTTP 请求库
- `rich >= 13.0.0` - 美观的终端输出

---

## 🧪 测试功能

验证所有新功能是否正常工作：

```bash
python test_features.py
```

预期输出：
```
✅ JSON 配置加载测试
✅ 多账号支持测试
✅ 客户端账号索引测试
✅ Rich 库集成测试
✅ 主脚本导入测试

Total: 5/5 tests passed
```

---

## 📝 使用示例

### 示例1：单账号自动上传
```bash
$ python main.py

[INFO] main, 2025-11-07 10:30:45, Running Joyrun Client [2024.01.01]
⠙ 上传 账号1 的跑步记录 ████████████████ 100%
[INFO] main, 2025-11-07 10:30:50, upload record success !
```

### 示例2：多账号交互选择
```bash
$ python main.py

                    请选择要执行的账号
┏━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ 序号 ┃ 账号名 ┃ 学号       ┃
┡━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━┩
│ 0    │ 小王   │ 320250935091 │
│ 1    │ 小张   │ 320250935092 │
└──────┴─────────┴─────────────┘

请输入账号序号 (0-1): 0
⠙ 上传 小王 的跑步记录 ████████████████ 100%
✓ 账号 小王 上传成功
```

### 示例3：运行所有账号
```bash
$ python main.py -a

开始执行所有账号（共 2 个）

(1/2) 正在执行账号: 小王
⠙ 上传 小王 的跑步记录 ████████████████ 100%
✓ 账号 小王 上传成功

(2/2) 正在执行账号: 小张
⠙ 上传 小张 的跑步记录 ████████████████ 100%
✓ 账号 小张 上传成功

所有账号执行完毕！
```

---

## 🐛 故障排除

### 问题：模块导入失败
```
ModuleNotFoundError: No module named 'requests'
```
**解决方案：**
```bash
uv sync  # 或 pip install -r requirements.txt
```

### 问题：配置文件找不到
```
FileNotFoundError: 配置文件未找到: config.json
```
**解决方案：**
```bash
# 复制示例配置文件
cp config.example.json config.json
# 编辑 config.json，填入你的账号信息
```

### 问题：登录失败
- 检查学号和密码是否正确
- 确保网络连接正常
- 查看是否需要短信验证

---

## 📚 更多信息

- 详细更新日志：见 `UPDATE_LOG.md`
- 原始项目文档：见 `README.md`
- 代码示例：见 `config.example.json`

---

## 💡 小提示

1. **首次使用**：从 `config.example.json` 复制配置后修改
2. **多账号提速**：使用 `python main.py -a` 一次性上传所有账号
3. **调试模式**：在 `config.json` 中设置 `"debug": true` 查看详细日志
4. **定时运行**：可以配合系统定时任务实现自动上传

---

**最后更新**：2025-11-07  
**项目版本**：v0.2.0
