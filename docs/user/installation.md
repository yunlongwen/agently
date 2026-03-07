# 安装指南

## 系统要求

### 操作系统支持
| 操作系统 | 最低版本 | 支持状态 |
|---------|---------|---------|
| **macOS** | 10.15 (Catalina) | ✅ 完全支持 |
| **Linux** | Ubuntu 20.04+, Debian 11+, CentOS 8+ | ✅ 完全支持 |
| **Windows** | Windows 10+ | ✅ 支持 (WSL2 推荐) |

### 软件依赖
- **Python**: 3.9, 3.10, 3.11, 3.12
- **Git**: 2.25+
- **pip**: 21.0+

### 硬件要求
- **CPU**: 2 核心及以上
- **内存**: 4GB 及以上（推荐 8GB）
- **磁盘空间**: 500MB 及以上

---

## 安装方式

### 方式一：PyPI 安装（推荐）

适用于大多数用户，安装简单快捷。

```bash
# 安装最新版本
pip install agently

# 安装特定版本
pip install agently==1.0.0

# 升级到最新版本
pip install --upgrade agently
```

#### 使用虚拟环境（推荐）

```bash
# 创建虚拟环境
python3 -m venv agently-env

# 激活虚拟环境
# macOS/Linux:
source agently-env/bin/activate

# Windows:
agently-env\Scripts\activate

# 安装 Agently
pip install agently
```

### 方式二：Homebrew 安装（macOS）

适用于 macOS 用户，便于统一管理。

```bash
# 添加 Agently 仓库（首次使用）
brew tap yunlongwen/agently

# 安装 Agently
brew install agently

# 升级 Agently
brew upgrade agently

# 卸载 Agently
brew uninstall agently
```

### 方式三：Docker 安装

适用于容器化环境或需要隔离运行的场景。

```bash
# 拉取最新镜像
docker pull yunlongwen/agently:latest

# 运行 Agently
docker run -it --rm \
  -v $(pwd):/workspace \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  yunlongwen/agently:latest

# 使用特定版本
docker pull yunlongwen/agently:1.0.0
```

#### Docker Compose 配置

```yaml
version: '3.8'

services:
  agently:
    image: yunlongwen/agently:latest
    volumes:
      - ./:/workspace
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    stdin_open: true
    tty: true
```

### 方式四：GitHub Releases 安装

适用于需要二进制版本或离线安装的场景。

#### macOS

```bash
# 下载最新版本
curl -L -o agently.tar.gz \
  https://github.com/yunlongwen/agently/releases/latest/download/agently-macos.tar.gz

# 解压
tar -xzf agently.tar.gz

# 移动到系统路径
sudo mv agently /usr/local/bin/

# 验证安装
agently --version
```

#### Linux

```bash
# 下载最新版本
curl -L -o agently.tar.gz \
  https://github.com/yunlongwen/agently/releases/latest/download/agently-linux.tar.gz

# 解压
tar -xzf agently.tar.gz

# 移动到系统路径
sudo mv agently /usr/local/bin/

# 验证安装
agently --version
```

#### Windows

1. 从 [GitHub Releases](https://github.com/yunlongwen/agently/releases) 下载 `agently-windows.zip`
2. 解压到指定目录
3. 将目录添加到系统 PATH
4. 验证安装：`agently --version`

### 方式五：源码安装

适用于开发者或需要自定义安装的场景。

```bash
# 克隆仓库
git clone https://github.com/yunlongwen/agently.git
cd agently

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装开发依赖
pip install -e ".[dev]"

# 验证安装
agently --version
```

---

## 安装验证

### 验证安装成功

```bash
# 检查版本
agently --version

# 查看帮助
agently --help

# 测试基本功能
agently doctor
```

### 配置 API 密钥

```bash
# 方式一：环境变量
export OPENAI_API_KEY="your-api-key-here"

# 方式二：配置文件
agently config set openai.api_key "your-api-key-here"

# 方式三：交互式配置
agently config init
```

---

## 平台特定说明

### macOS

#### 使用 Homebrew 管理 Python

```bash
# 安装 Python 3.11
brew install python@3.11

# 链接到系统路径
echo 'export PATH="/usr/local/opt/python@3.11/bin:$PATH"' >> ~/.zshrc

# 重新加载配置
source ~/.zshrc
```

#### 解决权限问题

如果遇到权限错误：

```bash
# 使用 --user 选项
pip install --user agently

# 或修改目录权限
sudo chown -R $(whoami) $(python3 -c "import site; print(site.USER_BASE)")
```

### Linux

#### Ubuntu/Debian

```bash
# 确保安装了必要的系统依赖
sudo apt update
sudo apt install python3-pip python3-venv git

# 安装 Agently
pip3 install agently
```

#### CentOS/RHEL

```bash
# 安装 Python 3.11
sudo dnf install python3.11 python3.11-pip git

# 安装 Agently
pip3.11 install agently
```

#### 解决权限问题

```bash
# 添加到用户本地 bin 目录
pip3 install --user agently

# 确保 PATH 包含本地 bin
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Windows

#### 使用 WSL2（推荐）

```bash
# 在 WSL2 中安装
wsl

# 然后按照 Linux 安装步骤执行
sudo apt update
sudo apt install python3-pip python3-venv git
pip3 install agently
```

#### 原生 Windows 安装

1. 安装 Python 3.11 从 [python.org](https://www.python.org/downloads/)
2. 安装时勾选 "Add Python to PATH"
3. 打开 PowerShell 或 CMD：

```powershell
# 安装 Agently
pip install agently

# 验证安装
agently --version
```

#### 解决路径问题

如果命令找不到：

```powershell
# 查看 Python 安装路径
python -c "import site; print(site.USER_BASE)"

# 将 Scripts 目录添加到 PATH
# 通常是: %APPDATA%\Python\Python311\Scripts
```

---

## 升级 Agently

### PyPI 升级

```bash
# 查看最新版本
pip index versions agently

# 升级到最新版本
pip install --upgrade agently

# 升级到特定版本
pip install --upgrade agently==1.1.0
```

### Homebrew 升级（macOS）

```bash
brew update
brew upgrade agently
```

### Docker 升级

```bash
# 拉取最新镜像
docker pull yunlongwen/agently:latest

# 清理旧镜像
docker image prune
```

---

## 卸载 Agently

### PyPI 卸载

```bash
pip uninstall agently
```

### Homebrew 卸载（macOS）

```bash
brew uninstall agently
brew untap yunlongwen/agently
```

### Docker 清理

```bash
# 删除容器
docker rm $(docker ps -a -q -f ancestor=yunlongwen/agently)

# 删除镜像
docker rmi yunlongwen/agently
```

### 清理配置文件

```bash
# 删除用户配置
rm -rf ~/.config/agently

# 删除缓存
rm -rf ~/.cache/agently
```

---

## 故障排除

### 常见问题

#### 1. pip 安装失败

**问题**: `pip install agently` 失败

**解决方案**:
```bash
# 升级 pip
pip install --upgrade pip

# 使用国内镜像
pip install agently -i https://pypi.tuna.tsinghua.edu.cn/simple

# 检查 Python 版本
python --version  # 需要 3.9+
```

#### 2. 命令未找到

**问题**: `agently: command not found`

**解决方案**:
```bash
# 检查安装位置
pip show agently

# 添加到 PATH
export PATH="$HOME/.local/bin:$PATH"

# 或重新安装到用户目录
pip install --user --force-reinstall agently
```

#### 3. 权限错误

**问题**: `Permission denied`

**解决方案**:
```bash
# 使用 --user 选项
pip install --user agently

# 或使用虚拟环境
python3 -m venv agently-env
source agently-env/bin/activate
pip install agently
```

#### 4. 依赖冲突

**问题**: 与其他包依赖冲突

**解决方案**:
```bash
# 使用虚拟环境隔离
python3 -m venv agently-env
source agently-env/bin/activate
pip install agently

# 或使用 pipx 安装
pip install pipx
pipx install agently
```

### 获取帮助

如果问题仍未解决：

1. 查看 [FAQ](faq.md)
2. 提交 [GitHub Issue](https://github.com/yunlongwen/agently/issues)
3. 参与 [Discussions](https://github.com/yunlongwen/agently/discussions)

---

## 下一步

安装完成后，请参考：
- [快速入门](quickstart.md) - 了解基本使用方法
- [CLI 使用](cli_usage.md) - 学习命令行操作
- [配置指南](#配置-api-密钥) - 设置 API 密钥
