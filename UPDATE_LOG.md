# LZU Running Helper - 项目更新说明

## 更新内容概览

本次更新实现了您提出的所有四个需求，使项目功能更加完整和用户友好。

---

## 1. ✅ 配置文件转为 JSON 格式

### 变更内容
- **原配置方式**：`config.ini` (INI 格式)
- **新配置方式**：`config.json` (JSON 格式)
- **配置文件位置**：`./config.json`

### 配置结构

```json
{
  "Base": {
    "APP": "Joyrun",
    "debug": true
  },
  "accounts": [
    {
      "name": "account1",
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

### 配置项说明

| 字段 | 说明 | 示例值 |
|------|------|--------|
| `name` | 账号名称（用于显示） | `account1` |
| `StudentID` | 学号（不含邮箱后缀） | `320250935091` |
| `Password` | 密码 | `123456` |
| `suffix` | 邮箱后缀 | `@lzu.edu.cn` |
| `Phone` | 手机号（可选，需要验证码时） | 空或手机号 |
| `record_type` | 跑步路径 | `dongcao` \| `xicao` \| `random` |
| `record_number` | 具体路径 | `0`(随机) \| `1-N` |
| `distance` | 跑步距离（km） | `4.8` |
| `pace` | 每公里用时（分钟） | `4.55` |
| `stride_frequncy` | 步幅（步/分钟） | `176` |

---

## 2. ✅ 增加多账号功能

### 实现方式

#### 配置多个账号
在 `config.json` 的 `accounts` 数组中添加多个账号对象：

```json
{
  "accounts": [
    {
      "name": "account1",
      "StudentID": "320250935091",
      ...
    },
    {
      "name": "account2",
      "StudentID": "320250935092",
      ...
    }
  ]
}
```

#### 修改文件清单
- `util/class_.py`：Config 类已支持 JSON 格式读取
- `Joyrun/client.py`：JoyrunClient 添加 `account_index` 参数支持
- `main.py`：完整的多账号交互界面

---

## 3. ✅ 集成 Rich 库进度条

### 功能特性

✨ **美观的进度条显示**
- 在上传跑步记录时显示进度条
- 使用旋转加载动画 + 进度条 + 百分比显示
- 支持彩色输出和格式化文本

### 实现位置
- **文件**：`Joyrun/client.py`
- **方法**：`upload_record()`

### 依赖
- `rich >= 13.0.0` （已在 `pyproject.toml` 中配置）

### 效果预览
```
⠙ 上传 account1 的跑步记录 ████████████████ 100%
```

---

## 4. ✅ 默认无需输入 -s 参数

### 行为变更

| 命令 | 行为 | 说明 |
|------|------|------|
| `python main.py` | 默认执行上传 | 如只有一个账号则直接运行；多个账号则交互选择 |
| `python main.py -c` | 显示配置 | 查看当前配置（检查配置） |
| `python main.py -a` | 运行所有账号 | 依次执行所有已配置的账号 |
| `python main.py -i 0` | 运行指定账号 | 运行索引为 0 的账号 |

### 主要改进
- ✅ **无需 `-s` 参数**：默认直接执行上传操作
- ✅ **智能账号选择**：单账号自动运行，多账号交互选择
- ✅ **美观的交互界面**：使用 Rich 库的 Table 组件展示账号列表
- ✅ **友好的提示信息**：彩色的成功/失败提示，清晰的进度显示

### 交互示例

**有多个账号时的选择界面：**
```
                    请选择要执行的账号
┏━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ 序号 ┃ 账号名 ┃ 学号       ┃
┡━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━┩
│ 0    │ account1 │ 320250935091 │
│ 1    │ account2 │ 320250935092 │
└──────┴─────────┴─────────────┘

请输入账号序号 (0-1): 
```

---

## 文件变更清单

### 修改文件
1. **`main.py`** - 完整重写，支持多账号交互和默认执行
2. **`Joyrun/client.py`** - 添加账号索引支持和 Rich 进度条
3. **`config.json`** - JSON 格式配置（已存在但结构调整）
4. **`test_features.py`** - 创建完整的功能测试脚本

### 配置文件
- **`config.json`** - JSON 格式配置（已支持多账号）
- **`pyproject.toml`** - 已包含 `rich >= 13.0.0` 依赖

---

## 快速开始

### 1. 单账号使用
```bash
# 配置 config.json 中的账号信息
python main.py  # 直接运行上传，无需任何参数
```

### 2. 多账号使用
```bash
# 在 config.json 中配置多个账号
# 运行时会自动显示账号列表供选择
python main.py

# 或运行所有账号
python main.py -a

# 或运行指定账号
python main.py -i 0
```

### 3. 查看配置
```bash
python main.py -c
```

---

## 功能测试

所有功能已通过完整的集成测试：

```
✅ JSON 配置加载测试
✅ 多账号支持测试
✅ 客户端账号索引测试
✅ Rich 库集成测试
✅ 主脚本导入测试

Total: 5/5 tests passed
```

运行测试：
```bash
python test_features.py
```

---

## 技术细节

### 代码改进

#### 1. Config 类 (`util/class_.py`)
- 已原生支持 JSON 格式
- 提供 `get()`, `getint()`, `getfloat()`, `getboolean()` 方法
- 完全向后兼容

#### 2. JoyrunClient 类 (`Joyrun/client.py`)
- 添加 `account_index` 参数
- 从指定账号读取配置
- 集成 Rich 进度条显示

#### 3. 主程序 (`main.py`)
- 完整的命令行参数处理
- 默认上传行为
- 多账号交互选择
- Rich 库美化输出

---

## 依赖说明

### 项目依赖
```toml
[project]
dependencies = [
    "requests>=2.32.0",
    "rich>=13.0.0",  # ← 新增的依赖
]
```

### 安装依赖
```bash
# 使用 UV 包管理器
uv sync

# 或使用 pip
pip install -r requirements.txt
```

---

## 常见问题

**Q: 如何添加新账号？**  
A: 在 `config.json` 的 `accounts` 数组中添加新的对象即可。

**Q: 如何修改默认的跑步参数？**  
A: 修改 `config.json` 中对应账号的 `distance`, `pace`, `stride_frequncy` 等字段。

**Q: 运行 `-a` 参数时某个账号失败会怎样？**  
A: 会停止执行并显示错误信息。这样确保您能及时发现问题。

**Q: 进度条显示有问题？**  
A: 确保终端支持 ANSI 颜色输出。某些老旧的终端可能不支持。

---

## 后续建议

1. **日志功能增强** - 添加上传结果日志记录
2. **定时执行** - 支持定时自动上传
3. **重试机制** - 失败自动重试
4. **数据备份** - 自动备份上传的数据

---

## 支持

如有问题，请：
1. 查看 `config.json` 配置是否正确
2. 运行 `python test_features.py` 进行功能测试
3. 运行 `python main.py -c` 查看当前配置
4. 检查日志输出中的错误信息

---

**更新完成日期**：2025-11-07  
**更新版本**：v0.2.0
