<div align="center">

# 🏃 LZU Running Helper

**兰州大学悦跑圈智能助手**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

*让跑步打卡变得更简单、更智能*

[快速开始](#-快速开始) • [功能特性](#-功能特性) • [使用指南](#-使用指南) • [定时任务](#-定时任务) • [常见问题](#-常见问题)

</div>

---

## 📖 项目简介

LZU Running Helper 是为兰州大学学生设计的悦跑圈自动打卡工具，基于 [PKURunningHelper](https://github.com/RinCloud/PKURunningHelper) 改进，专门适配兰大跑步路线。

### ✨ 主要特性

| 功能 | 描述 |
|------|------|
| 🔐 **多账号管理** | 一个配置文件管理多个账号，支持批量执行 |
| 📊 **进度可视化** | Rich 库美化输出，实时显示总进度条 |
| ⚙️ **灵活配置** | 支持多配置文件切换（早晚不同配置）|
| ⏰ **定时任务** | 内置定时脚本，支持每日自动运行 |
| 🎯 **智能调度** | 账号间隔执行，防止 API 限流 |
| 🎨 **交互友好** | 彩色输出、表格选择、清晰的状态提示 |

---

## 🚀 快速开始

### 方式一：UV 包管理器（推荐）

```bash
# 克隆项目
git clone https://github.com/tangfenga/LZURunningHelper.git
cd LZURunningHelper

# 同步依赖
uv sync

# 配置账号
cp config.example.json config.json
nano config.json  # 编辑配置文件

# 运行
python main.py
```

### 方式二：传统 pip 方式

```bash
# 克隆项目
git clone https://github.com/tangfenga/LZURunningHelper.git
cd LZURunningHelper

# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或 .venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 配置并运行
cp config.example.json config.json
python main.py
```

---

## 💡 使用指南

### 基本命令

```bash
# 默认执行（单账号直接运行，多账号交互选择）
python main.py

# 运行所有账号
python main.py -a

# 运行指定账号（索引从 0 开始）
python main.py -i 0

# 使用指定配置文件
python main.py -f config.morning.json

# 查看配置
python main.py -c
```

### 配置文件说明

#### 基本配置 (`config.json`)

```json
{
  "Base": {
    "APP": "Joyrun",
    "debug": false,
    "account_interval": 5
  },
  "accounts": [
    {
      "name": "账号1",
      "StudentID": "320250935091",
      "Password": "123456",
      "suffix": "@lzu.edu.cn",
      "Phone": "",
      "record_type": "random",
      "record_number": 1,
      "distance": 4.8,
      "pace": 4.55,
      "stride_frequncy": 176
    }
  ]
}
```

#### 配置参数说明

| 参数 | 说明 | 可选值 |
|------|------|--------|
| `name` | 账号显示名称 | 任意字符串 |
| `StudentID` | 学号（不含@后缀） | 你的学号 |
| `Password` | 密码 | 你的密码 |
| `suffix` | 邮箱后缀 | `@lzu.edu.cn` |
| `Phone` | 手机号（验证码用） | 选填 |
| `record_type` | 跑步路径 | `dongcao` / `xicao` / `random` |
| `record_number` | 具体路径 | `0`(随机) / `1-N` |
| `distance` | 跑步距离(km) | `2.0` - `10.0` |
| `pace` | 配速(分钟/km) | `4.0` - `6.0` |
| `stride_frequncy` | 步频(步/分钟) | `160` - `190` |
| `account_interval` | 账号间隔(秒) | 建议 `3-10` |

### 多账号示例

```json
{
  "Base": {
    "APP": "Joyrun",
    "debug": false,
    "account_interval": 5
  },
  "accounts": [
    {
      "name": "小王",
      "StudentID": "320250935091",
      "record_type": "dongcao",
      "distance": 3.0,
      ...
    },
    {
      "name": "小张",
      "StudentID": "320250935092",
      "record_type": "xicao",
      "distance": 4.8,
      ...
    }
  ]
}
```

运行效果：

```
                    请选择要执行的账号
┏━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ 序号 ┃ 账号名  ┃ 学号        ┃
┡━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━┩
│ 0    │ 小王    │ 320250935091 │
│ 1    │ 小张    │ 320250935092 │
└──────┴─────────┴─────────────┘

请输入账号序号 (0-1): 
```

---

## ⏰ 定时任务

### Linux/Mac 自动执行

#### 1. 配置脚本

编辑 `auto_run.sh`，修改项目路径：

```bash
PROJECT_DIR="/path/to/LZURunningHelper"  # 改为实际路径
```

#### 2. 赋予权限

```bash
chmod +x auto_run.sh
```

#### 3. 测试运行

```bash
./auto_run.sh morning  # 测试早上任务
./auto_run.sh evening  # 测试晚上任务
```

#### 4. 配置 Crontab

```bash
crontab -e
```

添加以下内容：

```cron
# 每天早上 9:00 执行
0 9 * * * /path/to/LZURunningHelper/auto_run.sh morning

# 每天晚上 19:00 执行
0 19 * * * /path/to/LZURunningHelper/auto_run.sh evening
```

#### 5. 查看日志

```bash
# 日志位置
ls logs/
cat logs/morning_2025-11-12.log
cat logs/evening_2025-11-12.log

# 实时查看
tail -f logs/morning_$(date +%Y-%m-%d).log
```

### Windows 定时任务

使用 **任务计划程序**：

1. 打开"任务计划程序"
2. 创建基本任务
3. 触发器：每天 9:00 / 19:00
4. 操作：启动程序
   - 程序：`python.exe`
   - 参数：`main.py -f config.morning.json -a`
   - 起始于：项目目录路径

---

## 🎨 功能演示

### 多账号批量执行

```bash
$ python main.py -a

开始执行所有账号（共 3 个）

(1/3) 正在执行账号: 小王
✓ 账号 小王 上传成功

等待 5 秒后执行下一个账号...

(2/3) 正在执行账号: 小张
✓ 账号 小张 上传成功

等待 5 秒后执行下一个账号...

(3/3) 正在执行账号: 小李
✓ 账号 小李 上传成功

总进度 ████████████████ 100%

✓ 所有账号执行完毕！
```

### 使用不同配置文件

```bash
# 早上使用轻松配置
python main.py -f config.morning.json -a

# 晚上使用标准配置
python main.py -f config.evening.json -a
```

---

## 🔧 高级功能

### 自定义路径

跑步路径文件位于 `Joyrun/data/`：
- `dongcao.joyrun.json` - 东操路径
- `xicao.joyrun.json` - 西操路径

格式：
```json
[
    [纬度1, 经度1],
    [纬度2, 经度2],
    ...
]
```

可以添加自己的路径文件并在配置中引用。

### 调试模式

开启调试模式查看详细日志：

```json
{
  "Base": {
    "debug": true
  }
}
```

---

## ❓ 常见问题

<details>
<summary><b>Q: 提示"配置文件未找到"</b></summary>

**A:** 确保 `config.json` 存在于项目根目录。可以从 `config.example.json` 复制：

```bash
cp config.example.json config.json
```
</details>

<details>
<summary><b>Q: 登录失败或需要验证码</b></summary>

**A:** 
1. 检查学号和密码是否正确
2. 如果账号绑定了手机，需要在配置中填写 `Phone` 字段
3. 按照提示输入验证码
</details>

<details>
<summary><b>Q: 多账号如何设置不同的跑步参数？</b></summary>

**A:** 每个账号都可以独立配置 `distance`、`pace`、`record_type` 等参数：

```json
{
  "accounts": [
    {
      "name": "Account1",
      "distance": 3.0,
      "record_type": "dongcao"
    },
    {
      "name": "Account2",
      "distance": 4.8,
      "record_type": "xicao"
    }
  ]
}
```
</details>

<details>
<summary><b>Q: 定时任务没有执行</b></summary>

**A:** 
1. 检查 crontab 配置：`crontab -l`
2. 查看系统日志：`grep CRON /var/log/syslog`
3. 确保脚本有执行权限：`chmod +x auto_run.sh`
4. 检查项目路径是否正确
</details>

<details>
<summary><b>Q: 如何避免被检测？</b></summary>

**A:** 
1. 设置合理的 `account_interval`（建议 5-10 秒）
2. 使用 `random` 路径类型
3. 配置合理的速度和距离
4. 避免同一时间大量账号执行
</details>

---

## 📝 更新日志

### v2.0.0 (2025-11-07)

**新增功能：**
- ✨ 多账号支持
- 📊 Rich 进度条
- ⚙️ 配置文件选择 (`-f` 参数)
- ⏰ 定时任务脚本
- 🎯 账号间隔执行

**改进：**
- 🔄 配置格式从 INI 迁移到 JSON
- 🎨 交互界面美化
- 📈 总进度条显示
- 🐛 Bug 修复和性能优化

### v1.0.0 (2024-10-01)

- 🎉 初始版本发布
- 基于 PKURunningHelper 改编
- 适配兰州大学路径

---

## 📄 许可证

本项目基于 MIT 许可证开源。

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 开发指南

```bash
# 克隆项目
git clone https://github.com/tangfenga/LZURunningHelper.git
cd LZURunningHelper

# 安装开发依赖
uv sync

# 运行测试
python test_features.py
python test_progress_features.py

# 提交前检查
python main.py -c
```

---

## 🙏 致谢

- 原项目：[PKURunningHelper](https://github.com/RinCloud/PKURunningHelper)
- 感谢所有贡献者和用户的支持

---

## ⚠️ 免责声明

本项目仅供学习交流使用，请遵守学校相关规定。使用本工具产生的任何后果由使用者自行承担。

---

<div align="center">

**如果这个项目对你有帮助，请给个 ⭐ Star！**

Made with ❤️ for LZU students

</div>
