# 安装指南

## 系统要求

### 操作系统
- macOS 10.15+
- Linux (Ubuntu 20.04+, Debian 11+, CentOS 8+)
- Windows 10+ (WSL2 推荐)

### 软件依赖
- Python 3.9 或更高版本
- Git 2.25 或更高版本
- pip 21.0 或更高版本

### 硬件要求
- CPU: 2 核心及以上
- 内存: 4GB 及以上
- 磁盘空间: 500MB 及以上

## 安装步骤

### 1. 安装 Python

#### macOS
```bash
# 使用 Homebrew 安装
brew install python@3.11

# 验证安装
python3 --version
```

#### Linux (Ubuntu/Debian)
```bash
# 更新包列表
sudo apt update

# 安装 Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip

# 验证安装
python3.11 --version
```

#### Windows
1. 从 [Python 官网](https://www.python.org/downloads/) 下载 Python 3.11 安装包
2. 运行安装程序，勾选 "Add Python to PATH"
3. 验证安装：
```cmd
python --version
```

### 2. 安装 Git

#### macOS
```bash
# 使用 Homebrew 安装
brew install git

# 验证安装
git --version
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt install git

# 验证安装
git --version
```

#### Windows
1. 从 [Git 官网](https://git-scm.com/download/win) 下载 Git 安装包
2. 运行安装程序，使用默认设置
3. 验证安装：
```cmd
git --version
```

### 3. 安装 Agently

#### 从 PyPI 安装
```bash
# 创建虚拟环境（推荐）
python3 -m venv agently-env
source agently-env/bin/activate  # Linux/Mac
# 或
agently-env\Scripts\activate  # Windows

# 安装 Agently
pip install agently

# 验证安装
agently --version
```

#### 从源码安装
```bash
# 克隆仓库
git clone https://github.com/yunlongwen/agently.git
cd agently

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -e .

# 验证安装
agently --version
```

### 4. 配置 API 密钥

Agently 需要访问云端大模型 API，支持以下模型：

#### OpenAI
```bash
# 设置环境变量
export OPENAI_API_KEY="your_openai_api_key"

# 或在配置文件中设置
agently config set openai.api_key "your_openai_api_key"
```

#### Anthropic
```bash
# 设置环境变量
export ANTHROPIC_API_KEY="your_anthropic_api_key"

# 或在配置文件中设置
agently config set anthropic.api_key "your_anthropic_api_key"
```

#### Google Gemini
```bash
# 设置环境变量
export GOOGLE_API_KEY="your_google_api_key"

# 或在配置文件中设置
agently config set google.api_key "your_google_api_key"
```

### 5. 验证安装

```bash
# 运行版本检查
agently --version

# 运行健康检查
agently doctor

# 测试基本功能
agently chat "Hello, Agently!"
```

## 配置文件

Agently 的配置文件位于：

- **Linux/macOS**: `~/.agently/config.yaml`
- **Windows**: `%USERPROFILE%\.agently\config.yaml`

### 配置示例

```yaml
# 模型配置
models:
  default: openai
  openai:
    api_key: "your_openai_api_key"
    model: "gpt-4"
    temperature: 0.7
  anthropic:
    api_key: "your_anthropic_api_key"
    model: "claude-3-opus-20240229"
    temperature: 0.7
  google:
    api_key: "your_google_api_key"
    model: "gemini-pro"
    temperature: 0.7

# 性能配置
performance:
  max_memory: 4096  # MB
  max_concurrent_contexts: 3
  timeout: 120  # 秒

# 日志配置
logging:
  level: INFO
  file: ~/.agently/logs/agently.log
```

## 升级

### 升级到最新版本
```bash
# 激活虚拟环境
source agently-env/bin/activate  # Linux/Mac
# 或
agently-env\Scripts\activate  # Windows

# 升级 Agently
pip install --upgrade agently

# 验证版本
agently --version
```

### 升级到特定版本
```bash
pip install agently==1.0.0
```

## 卸载

```bash
# 激活虚拟环境
source agently-env/bin/activate  # Linux/Mac
# 或
agently-env\Scripts\activate  # Windows

# 卸载 Agently
pip uninstall agently

# 删除虚拟环境（可选）
deactivate
rm -rf agently-env  # Linux/Mac
# 或
rmdir /s agently-env  # Windows
```

## 故障排查

### 问题：Python 版本不兼容
**错误信息**: `Python version 3.9 or higher required`

**解决方案**:
```bash
# 检查 Python 版本
python3 --version

# 安装兼容的 Python 版本
# 参考 "安装 Python" 部分
```

### 问题：pip 安装失败
**错误信息**: `pip install agently` 失败

**解决方案**:
```bash
# 升级 pip
pip install --upgrade pip

# 使用国内镜像源
pip install agently -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 问题：API 密钥无效
**错误信息**: `Invalid API key`

**解决方案**:
```bash
# 检查环境变量
echo $OPENAI_API_KEY

# 重新设置 API 密钥
agently config set openai.api_key "your_correct_api_key"

# 验证 API 密钥
agently doctor
```

### 问题：内存不足
**错误信息**: `MemoryError` 或程序崩溃

**解决方案**:
```bash
# 调整内存限制
agently config set performance.max_memory 4096

# 减少并发上下文
agently config set performance.max_concurrent_contexts 2
```

## 下一步

安装完成后，请阅读 [快速入门指南](quickstart.md) 开始使用 Agently。

---

**相关文档**:
- [快速入门](quickstart.md)
- [CLI 使用](cli_usage.md)
- [常见问题](faq.md)
