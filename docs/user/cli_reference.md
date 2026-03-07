# 命令参考

本文档提供 Agently CLI 的完整命令参考。

## 基本命令

### `agently --help`
显示帮助信息。

```bash
agently --help
```

### `agently --version`
显示 Agently 版本信息。

```bash
agently --version
```

输出示例：
```
Agently v1.0.0
Python 3.11.0
```

### `agently doctor`
运行健康检查，诊断系统状态。

```bash
agently doctor
```

输出示例：
```
Agently 健康检查
================

✓ Python 版本: 3.11.0
✓ pip 版本: 23.2.0
✓ Agently 版本: 1.0.0
✓ API 密钥: 已配置
✓ 配置文件: 存在
✓ 日志目录: 可写

所有检查通过！
```

## 交互命令

### `agently chat`
启动交互式对话模式。

```bash
agently chat [选项]
```

#### 选项
- `--agent, -a <name>`：指定使用的智能体
- `--skill, -s <name>`：指定使用的技能
- `--context, -c <id>`：指定上下文 ID
- `--debug`：启用调试模式
- `--verbose, -v`：显示详细输出

#### 示例
```bash
# 启动默认对话
agently chat

# 使用特定智能体
agently chat --agent code-generator

# 使用特定技能
agently chat --skill test-driven-development

# 启用调试模式
agently chat --debug
```

### `agently ask`
在命令模式中执行单个任务。

```bash
agently ask [选项] "问题或请求"
```

#### 选项
- `--agent, -a <name>`：指定使用的智能体
- `--skill, -s <name>`：指定使用的技能
- `--output, -o <file>`：指定输出文件
- `--format, -f <format>`：指定输出格式（json, yaml, markdown）
- `--stream`：启用流式输出
- `--silent`：静默模式，只输出结果
- `--timeout, -t <seconds>`：设置超时时间

#### 示例
```bash
# 基本用法
agently ask "如何在 Python 中实现单例模式？"

# 使用特定智能体
agently ask --agent code-reviewer "审查这段代码"

# 输出到文件
agently ask --output result.py "生成一个 Python 脚本"

# 指定输出格式
agently ask --format json "分析这段代码"

# 启用流式输出
agently ask --stream "生成一个完整的 API 框架"

# 静默模式
agently ask --silent "生成一个快速排序算法"

# 设置超时
agently ask --timeout 60 "优化这段代码"
```

### `agently menu`
启动菜单模式。

```bash
agently menu
```

## 智能体命令

### `agently agents list`
列出所有可用的智能体。

```bash
agently agents list
```

输出示例：
```
可用智能体：
1. Nexus 协调器 (nexus)
2. 代码生成器 (code-generator)
3. 代码审查器 (code-reviewer)
4. 测试生成器 (test-generator)
5. 文档生成器 (doc-generator)
```

### `agently agents info`
显示智能体的详细信息。

```bash
agently agents info <agent-name>
```

#### 示例
```bash
agently agents info nexus
```

输出示例：
```
智能体：Nexus 协调器
版本：1.0.0
描述：综合智能体，可以调度其他智能体完成任务

能力：
- 任务规划和分解
- 智能体协调和调度
- 上下文管理
- 进度跟踪

适用场景：
- 复杂的多步骤任务
- 需要多个智能体协作的任务
- 需要上下文管理的任务

配置：
- 默认模型：gpt-4
- 最大上下文数：5
- 超时时间：120秒
```

### `agently agents use`
在对话模式中使用特定智能体。

```bash
agently agents use <agent-name>
```

#### 示例
```bash
agently agents use code-generator
```

## 技能命令

### `agently skills list`
列出所有可用的技能。

```bash
agently skills list
```

### `agently skills info`
显示技能的详细信息。

```bash
agently skills info <skill-name>
```

#### 示例
```bash
agently skills info test-driven-development
```

### `agently skills use`
在对话模式中使用特定技能。

```bash
agently skills use <skill-name>
```

#### 示例
```bash
agently skills use test-driven-development
```

## 工具命令

### `agently tools list`
列出所有可用的工具。

```bash
agently tools list
```

### `agently tools info`
显示工具的详细信息。

```bash
agently tools info <tool-name>
```

#### 示例
```bash
agently tools info filesystem
```

## 上下文命令

### `agently context list`
列出所有上下文。

```bash
agently context list
```

输出示例：
```
当前上下文：
1. 用户管理系统开发 (active)
   - ID: ctx_1234567890
   - 创建时间：2026-03-07 10:30:00
   - 消息数：15
   - 最后更新：2026-03-07 10:45:00

2. 代码优化任务 (inactive)
   - ID: ctx_0987654321
   - 创建时间：2026-03-07 09:00:00
   - 消息数：8
   - 最后更新：2026-03-07 09:15:00
```

### `agently context create`
创建新的上下文。

```bash
agently context create "上下文名称"
```

#### 示例
```bash
agently context create "电商系统开发"
```

### `agently context switch`
切换到指定上下文。

```bash
agently context switch <context-id>
```

#### 示例
```bash
agently context switch ctx_1234567890
```

### `agently context delete`
删除指定上下文。

```bash
agently context delete <context-id>
```

#### 示例
```bash
agently context delete ctx_0987654321
```

### `agently context clear`
清除所有上下文。

```bash
agently context clear
```

## 配置命令

### `agently config show`
显示所有配置。

```bash
agently config show
```

输出示例：
```yaml
models:
  default: openai
  openai:
    api_key: "sk-..."
    model: "gpt-4"
    temperature: 0.7
  anthropic:
    api_key: "sk-ant-..."
    model: "claude-3-opus-20240229"
    temperature: 0.7
  google:
    api_key: "AI..."
    model: "gemini-pro"
    temperature: 0.7

performance:
  max_memory: 4096
  max_concurrent_contexts: 3
  timeout: 120

logging:
  level: INFO
  file: ~/.agently/logs/agently.log
```

### `agently config get`
获取特定配置值。

```bash
agently config get <key>
```

#### 示例
```bash
agently config get models.default
agently config get models.openai.model
agently config get performance.max_memory
```

### `agently config set`
设置配置值。

```bash
agently config set <key> <value>
```

#### 示例
```bash
# 设置默认模型
agently config set models.default anthropic

# 设置模型参数
agently config set models.anthropic.temperature 0.5

# 设置性能参数
agently config set performance.max_memory 4096
agently config set performance.max_concurrent_contexts 3

# 设置日志级别
agently config set logging.level DEBUG
```

### `agently config reset`
重置配置。

```bash
# 重置特定配置
agently config reset <key>

# 重置所有配置
agently config reset --all
```

#### 示例
```bash
agently config reset models.anthropic.temperature
agently config reset --all
```

## 批处理命令

### `agently batch`
从文件中读取并执行多个任务。

```bash
agently batch [选项] <file>
```

#### 选项
- `--agent, -a <name>`：指定使用的智能体
- `--skill, -s <name>`：指定使用的技能
- `--output-dir, -o <dir>`：指定输出目录
- `--parallel, -p`：并行执行任务
- `--continue-on-error`：遇到错误时继续执行

#### 示例
```bash
# 基本用法
agently batch tasks.txt

# 使用特定智能体
agently batch --agent code-generator tasks.txt

# 并行执行
agently batch --parallel tasks.txt

# 遇到错误继续执行
agently batch --continue-on-error tasks.txt
```

#### tasks.txt 格式
```
# 注释行以 # 开头
生成一个 Python 类，表示银行账户
为这个类生成单元测试
生成 API 文档
```

## 高级命令

### `agently export`
导出上下文或配置。

```bash
# 导出上下文
agently export context <context-id> <output-file>

# 导出配置
agently export config <output-file>
```

#### 示例
```bash
agently export context ctx_1234567890 context_backup.json
agently export config config_backup.yaml
```

### `agently import`
导入上下文或配置。

```bash
# 导入上下文
agently import context <input-file>

# 导入配置
agently import config <input-file>
```

#### 示例
```bash
agently import context context_backup.json
agently import config config_backup.yaml
```

### `agently logs`
查看日志。

```bash
agently logs [选项]
```

#### 选项
- `--tail, -n <lines>`：显示最后 N 行
- `--follow, -f`：实时跟踪日志
- `--level <level>`：按级别过滤（DEBUG, INFO, WARNING, ERROR）

#### 示例
```bash
# 查看最后 50 行
agently logs --tail 50

# 实时跟踪日志
agently logs --follow

# 只显示错误日志
agently logs --level ERROR
```

### `agently update`
更新 Agently 到最新版本。

```bash
agently update
```

### `agently uninstall`
卸载 Agently。

```bash
agently uninstall
```

## 全局选项

以下选项适用于所有命令：

- `--help, -h`：显示帮助信息
- `--version, -V`：显示版本信息
- `--verbose, -v`：显示详细输出
- `--quiet, -q`：静默模式
- `--config, -C <file>`：指定配置文件
- `--no-color`：禁用彩色输出

#### 示例
```bash
# 显示详细输出
agently ask --verbose "生成代码"

# 使用指定配置文件
agently chat --config /path/to/config.yaml

# 禁用彩色输出
agently ask --no-color "解释这段代码"
```

## 环境变量

Agently 支持通过环境变量配置：

### API 密钥
```bash
export OPENAI_API_KEY="your_openai_api_key"
export ANTHROPIC_API_KEY="your_anthropic_api_key"
export GOOGLE_API_KEY="your_google_api_key"
```

### 模型配置
```bash
export AGLY_DEFAULT_MODEL="openai"
export AGLY_TEMPERATURE="0.7"
export AGLY_MAX_TOKENS="4096"
```

### 性能配置
```bash
export AGLY_MAX_MEMORY="4096"
export AGLY_MAX_CONCURRENT_CONTEXTS="3"
export AGLY_TIMEOUT="120"
```

### 日志配置
```bash
export AGLY_LOG_LEVEL="INFO"
export AGLY_LOG_FILE="/path/to/log/file.log"
export AGLY_LOG_FORMAT="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

### 其他配置
```bash
export AGLY_CONFIG_FILE="/path/to/config.yaml"
export AGLY_DATA_DIR="/path/to/data/dir"
export AGLY_CACHE_DIR="/path/to/cache/dir"
```

## 退出代码

Agently 命令返回以下退出代码：

- `0`：成功
- `1`：一般错误
- `2`：命令使用错误
- `3`：网络错误
- `4`：API 错误
- `5`：配置错误
- `6`：权限错误
- `7`：超时错误

#### 示例
```bash
# 检查命令是否成功
agently ask "生成代码"
if [ $? -eq 0 ]; then
    echo "命令执行成功"
else
    echo "命令执行失败"
fi
```

## 配置文件

### 配置文件位置

- **Linux/macOS**: `~/.agently/config.yaml`
- **Windows**: `%USERPROFILE%\.agently\config.yaml`

### 配置文件示例

```yaml
# 模型配置
models:
  default: openai
  openai:
    api_key: "your_openai_api_key"
    model: "gpt-4"
    temperature: 0.7
    max_tokens: 4096
  anthropic:
    api_key: "your_anthropic_api_key"
    model: "claude-3-opus-20240229"
    temperature: 0.7
    max_tokens: 4096
  google:
    api_key: "your_google_api_key"
    model: "gemini-pro"
    temperature: 0.7
    max_tokens: 4096

# 性能配置
performance:
  max_memory: 4096
  max_concurrent_contexts: 3
  timeout: 120

# 日志配置
logging:
  level: INFO
  file: ~/.agently/logs/agently.log
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  max_size: 10485760  # 10MB
  backup_count: 5

# 缓存配置
cache:
  enabled: true
  dir: ~/.agently/cache
  max_size: 1073741824  # 1GB
  ttl: 86400  # 24小时

# 上下文配置
context:
  max_messages: 100
  max_age: 604800  # 7天
  auto_save: true
```

---

**相关文档**:
- [CLI 使用](cli_usage.md)
- [快速入门](quickstart.md)
- [常见问题](faq.md)
