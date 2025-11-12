# 🏃‍♂️ LZURunningHelper

**兰大悦跑圈智能助手**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

_让跑步打卡变得更简单、更智能_

---

## 📘 项目简介

本项目改写自 [PKURunningHelper](https://github.com/RinCloud/PKURunningHelper)，在原基础上适配兰州大学校园跑步路径。

> 鉴于本校二手群中有人使用类似项目盈利，打着人工代跑的旗号，实际上利用虚拟定位提供路径严重偏差的低劣服务，因此将这个自己用的小工具开源。

---

## ✨ 功能特性

| 功能             | 描述                                   |
| ---------------- | -------------------------------------- |
| 🔐 **多账号管理** | 一个配置文件管理多个账号，支持批量执行 |
| 📊 **进度可视化** | Rich 库美化输出，实时显示总进度条      |
| ⚙️ **灵活配置**   | 支持多配置文件切换（早晚不同配置）     |
| ⏰ **定时任务**   | 支持每日自动运行                       |
| 🎯 **智能调度**   | 账号间隔执行，防止 API 限流            |
| 🎨 **交互友好**   | 彩色输出、表格选择、清晰状态提示       |

---

## 🚀 环境配置

> **推荐 Python 3.9+**
>
> 若已有 Python 3.9 环境，可跳过以下安装步骤。

### 🧩 方式一：pip 安装（**入门推荐 ✅**）

1. 从官网下载 [Python 3.9.x](https://www.python.org/ftp/python/3.9.13/python-3.9.13-amd64.exe)
2. 安装时请务必勾选 **“Add Python 3.9 to PATH”**
   ![Python 安装路径示例](images/image.png)
3. 克隆项目并进入目录：

    ```bash
    git clone https://github.com/TarikVon/LZURunningHelper.git
    cd LZURunningHelper
    ```

4. 创建虚拟环境（仅限 CMD）：

    ```bash
    "%LOCALAPPDATA%\Programs\Python\Python39\python.exe" -m venv .venv
    ```

5. 激活虚拟环境：

    ```bash
    .\.venv\Scripts\activate.bat
    ```

6. 安装依赖：

    ```bash
    pip install -r requirements.txt
    ```

---

### 🧠 方式二：UV 包管理器（**进阶推荐 ✅**）

若你使用 [UV](https://github.com/astral-sh/uv) 包管理器，可一键同步依赖：

```bash
git clone https://github.com/TarikVon/LZURunningHelper.git
cd LZURunningHelper

uv sync
python main.py
```

---

## 🪄 使用指南

### ⚙️ 账号配置

1. 编辑 `config.json` 文件：

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
                "record_type": "random",
                "distance": 4.8,
                "pace": 4.55,
                "stride_frequncy": 176
            }
        ]
    }
    ```

2. 运行：

    ```bash
    python main.py -s
    ```

    或批量执行：

    ```bash
    python main.py -a
    ```

3. 若控制台输出：

    ```plaintext
    [DEBUG] joyrun, 2025-05-01 02:37:20, response.json = {
        "ret": "0",
        "msg": "发布成功",
        ...
    ```

    表示上传成功，可前往悦跑圈 APP 验证。

---

### 💻 基本命令

```bash
python main.py           # 默认执行
python main.py -a        # 运行所有账号
python main.py -i 0      # 指定账号
python main.py -f config.morning.json  # 使用早晨配置
python main.py -c        # 查看配置
```

---

### 🧾 配置参数说明

| 参数               | 说明             | 可选值                   |
| ------------------ | ---------------- | ------------------------ |
| `StudentID`        | 学号             | 必填                     |
| `Password`         | 密码             | 必填                     |
| `suffix`           | 邮箱后缀         | @lzu.edu.cn              |
| `record_type`      | 跑步路径         | dongcao / xicao / random |
| `distance`         | 跑步距离         | 2.0 - 10.0               |
| `pace`             | 配速             | 4.0 - 6.0                |
| `stride_frequncy`  | 步频             | 160 - 190                |
| `account_interval` | 账号间隔执行时间 | 3 - 10 秒                |

---

## ⏰ 定时任务设置

### Linux / Mac

```bash
chmod +x auto_run.sh
crontab -e
```

### Windows

1. 打开“任务计划程序”
2. 创建基本任务
3. 设置触发时间：9:00 / 19:00
4. 操作：

    - 程序：`python.exe`
    - 参数：`main.py -f config.morning.json -a`

---

## 🏃‍♀️ 自定义跑步路径

跑步路径文件在 `Joyrun/data/` 路径下，格式为：

```
[
    [纬度1, 经度1], 
    [纬度2, 经度2],
    ...
]
```

悦跑圈底层调用的是高德地图 API，所以需要使用高德地图坐标拾取器获取跑步路径经纬度：
[https://lbs.amap.com/tools/picker](https://lbs.amap.com/tools/picker)

注意高德地图复制的经纬度格式是 `[经度, 纬度]`，
而本软件所使用的经纬度格式为 `[纬度, 经度]`，
需要经纬度互换以及去除小数点（可以编写程序实现修改）。

---

## 🎬 功能演示

### 🔁 多账号批量执行

```
开始执行所有账号（共 3 个）
(1/3) 正在执行账号: 小王
✓ 上传成功
等待 5 秒后执行下一个账号...
```

### 📂 不同配置文件切换

```bash
python main.py -f config.morning.json -a
python main.py -f config.evening.json -a
```

### 💡 高级功能

-   🧭 自定义路径 (`Joyrun/data/`)
-   🧪 调试模式 (`"debug": true`)
-   🕓 多账号间隔执行（防限流）
-   🗂️ 多配置文件适配早晚任务

---

## ❓ 常见问题 FAQ

<details>
<summary><b>Q: 配置文件未找到？</b></summary>
A: 确认存在 `config.ini` 或 `config.json`。
</details>

<details>
<summary><b>Q: 登录失败或需要验证码？</b></summary>
A: 输入手机号后按提示填写验证码。
</details>

<details>
<summary><b>Q: 定时任务无效？</b></summary>
A: 检查 crontab / 任务计划程序路径权限。
</details>

<details>
<summary><b>Q: 如何避免被检测？</b></summary>
A:
- 账号间隔 ≥ 5 秒；
- 使用 random 路径；
- 合理设置配速与距离。
</details>

---

## 📄 许可证与贡献

本项目基于 **MIT License** 开源。
欢迎提交 Issue 与 Pull Request！

> 若发现问题，请提交 issue，将在第一时间修复。

---

## 🙏 致谢

-   原项目：[PKURunningHelper](https://github.com/RinCloud/PKURunningHelper)
-   感谢所有贡献者的维护与改进！

---

## ⚠️ 免责声明

本项目仅供学习与交流使用。
请遵守学校相关规定，使用本工具产生的任何后果由使用者自行承担。

---

<div align="center">

⭐ **若项目对你有帮助，请给个 Star！**

Made with ❤️ for LZU Students

</div>
