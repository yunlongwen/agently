# CLI 使用指南

Agently 提供了强大的命令行界面（CLI），支持多种交互方式，满足不同场景的需求。

## 交互模式

### 1. 对话模式

对话模式是最常用的交互方式，适合进行连续的对话和复杂任务。

#### 启动对话模式
```bash
# 启动默认对话模式
agently chat

# 使用特定智能体启动对话
agently chat --agent code-generator

# 使用特定技能启动对话
agently chat --skill test-driven-development
```

#### 对话模式特性
- **上下文记忆**：记住之前的对话内容
- **多轮交互**：支持连续的多轮对话
- **实时反馈**：显示实时的处理进度
- **历史记录**：自动保存对话历史

#### 对话模式示例
```bash
$ agently chat
Agently v1.0.0 - AI 驱动的编程助手
输入 'help' 查看帮助，输入 'exit' 退出

> 我正在开发一个用户管理系统
好的，我了解您正在开发用户管理系统。请问您需要什么帮助？

> 帮我设计用户模块的数据库表结构
[Agently 正在分析需求...]
[Agently 正在设计数据库表结构...]

我为您设计了以下用户模块的数据库表结构：

1. users 表
   - id: 主键
   - username: 用户名
   - email: 邮箱
   - password_hash: 密码哈希
   - created_at: 创建时间
   - updated_at: 更新时间

2. user_profiles 表
   - id: 主键
   - user_id: 外键关联 users 表
   - full_name: 全名
   - avatar: 头像
   - bio: 个人简介

您需要我生成对应的 SQL 语句吗？

> 是的，请生成
[Agently 正在生成 SQL 语句...]

-- 创建 users 表
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建 user_profiles 表
CREATE TABLE user_profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    full_name VARCHAR(100),
    avatar TEXT,
    bio TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

> exit
感谢使用 Agently！
```

### 2. 命令模式

命令模式适合快速执行单个任务，不需要交互。

#### 基本语法
```bash
agently ask "您的问题或请求"
```

#### 命令模式示例
```bash
# 快速提问
agently ask "如何在 Python 中实现单例模式？"

# 生成代码
agently ask "写一个快速排序算法"

# 代码审查
agently ask "审查这段代码的性能问题：[粘贴代码]"

# 解释代码
agently ask "解释这段代码的作用：[粘贴代码]"
```

#### 命令模式选项
```bash
# 使用特定智能体
agently ask --agent code-reviewer "审查这段代码"

# 使用特定技能
agently ask --skill test-driven-development "开发一个计算器类"

# 指定输出文件
agently ask --output result.py "生成一个 Python 脚本"

# 指定输出格式
agently ask --format json "分析这段代码"
```

### 3. 菜单模式

菜单模式提供图形化的菜单界面，适合不熟悉命令行的用户。

#### 启动菜单模式
```bash
agently menu
```

#### 菜单模式特性
- **可视化菜单**：清晰的菜单选项
- **快捷键支持**：支持键盘快捷键
- **分类导航**：按功能分类的菜单
- **状态显示**：显示当前状态和上下文

#### 菜单模式示例
```
┌─────────────────────────────────────────┐
│         Agently v1.0.0 - 主菜单          │
├─────────────────────────────────────────┤
│ 1. 智能体选择                             │
│ 2. 技能选择                               │
│ 3. 工具选择                               │
│ 4. 上下文管理                             │
│ 5. 配置管理                               │
│ 6. 帮助                                   │
│ 0. 退出                                   │
└─────────────────────────────────────────┘

选择 [1-6, 0]: 1

┌─────────────────────────────────────────┐
│         智能体选择                        │
├─────────────────────────────────────────┤
│ 1. Nexus 协调器                          │
│ 2. 代码生成器                            │
│ 3. 代码审查器                            │
│ 4. 测试生成器                            │
│ 5. 文档生成器                            │
│ 0. 返回主菜单                            │
└─────────────────────────────────────────┘

选择 [1-5, 0]: 1

已选择 Nexus 协调器
输入您的问题或需求：
```

## 智能体管理

### 列出可用智能体
```bash
agently agents list
```

输出示例：
```
可用智能体：
1. Nexus 协调器 (nexus)
   - 描述：综合智能体，可以调度其他智能体
   - 适用场景：复杂任务、多步骤任务

2. 代码生成器 (code-generator)
   - 描述：生成各种编程语言的代码
   - 适用场景：代码生成、框架搭建

3. 代码审查器 (code-reviewer)
   - 描述：审查代码质量、性能和安全性
   - 适用场景：代码审查、代码优化

4. 测试生成器 (test-generator)
   - 描述：生成单元测试和集成测试
   - 适用场景：测试编写、测试覆盖

5. 文档生成器 (doc-generator)
   - 描述：生成 API 文档和代码注释
   - 适用场景：文档编写、代码注释
```

### 查看智能体详情
```bash
agently agents info <agent-name>
```

示例：
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

### 使用特定智能体
```bash
# 在对话模式中使用
agently chat --agent <agent-name>

# 在命令模式中使用
agently ask --agent <agent-name> "您的问题"

# 在菜单模式中选择
agently menu
# 然后选择智能体
```

## 技能管理

### 列出可用技能
```bash
agently skills list
```

输出示例：
```
可用技能：
1. 测试驱动开发 (test-driven-development)
   - 描述：使用 TDD 方法开发代码
   - 适用场景：需要严格测试的开发

2. 敏捷开发 (agile-development)
   - 描述：使用敏捷开发方法
   - 适用场景：快速迭代开发

3. 代码重构 (code-refactoring)
   - 描述：重构代码以改善质量
   - 适用场景：代码优化、技术债务清理

4. 安全编码 (secure-coding)
   - 描述：编写安全的代码
   - 适用场景：安全敏感的应用
```

### 查看技能详情
```bash
agently skills info <skill-name>
```

示例：
```bash
agently skills info test-driven-development
```

### 使用特定技能
```bash
# 在对话模式中使用
agently chat --skill <skill-name>

# 在命令模式中使用
agently ask --skill <skill-name> "您的需求"
```

## 工具管理

### 列出可用工具
```bash
agently tools list
```

输出示例：
```
可用工具：
1. 文件系统 (filesystem)
   - 描述：读写文件、创建目录
   - 命令：read, write, create, delete

2. Git (git)
   - 描述：Git 版本控制操作
   - 命令：status, commit, push, pull

3. 测试 (test)
   - 描述：运行测试、生成测试报告
   - 命令：run, report

4. 代码分析 (code-analysis)
   - 描述：分析代码结构、复杂度
   - 命令：analyze, complexity
```

### 查看工具详情
```bash
agently tools info <tool-name>
```

### 使用工具
```bash
# 在对话中请求使用工具
> 使用 git 工具查看当前分支的状态

# 在命令模式中使用
agently ask "使用 filesystem 工具读取文件 src/main.py"
```

## 上下文管理

### 查看当前上下文
```bash
agently context list
```

输出示例：
```
当前上下文：
1. 用户管理系统开发 (active)
   - 创建时间：2026-03-07 10:30:00
   - 消息数：15
   - 最后更新：2026-03-07 10:45:00

2. 代码优化任务 (inactive)
   - 创建时间：2026-03-07 09:00:00
   - 消息数：8
   - 最后更新：2026-03-07 09:15:00
```

### 切换上下文
```bash
agently context switch <context-id>
```

### 创建新上下文
```bash
agently context create "上下文名称"
```

### 删除上下文
```bash
agently context delete <context-id>
```

### 清除上下文
```bash
# 清除当前对话的上下文
> clear context

# 清除所有上下文
agently context clear
```

## 配置管理

### 查看配置
```bash
# 查看所有配置
agently config show

# 查看特定配置
agently config get <key>
```

示例：
```bash
agently config get models.default
```

输出：
```
models.default = openai
```

### 设置配置
```bash
agently config set <key> <value>
```

示例：
```bash
# 设置默认模型
agently config set models.default anthropic

# 设置温度参数
agently config set models.anthropic.temperature 0.5

# 设置最大内存
agently config set performance.max_memory 4096
```

### 重置配置
```bash
# 重置特定配置
agently config reset <key>

# 重置所有配置
agently config reset --all
```

## 高级功能

### 1. 批处理模式

批处理模式允许您从文件中读取多个任务并执行。

```bash
# 从文件读取任务
agently batch tasks.txt
```

tasks.txt 示例：
```
生成一个 Python 类，表示银行账户
为这个类生成单元测试
生成 API 文档
```

### 2. 流式输出

对于长文本输出，可以使用流式输出模式。

```bash
agently ask --stream "生成一个完整的 RESTful API 框架"
```

### 3. 调试模式

调试模式提供详细的日志信息，帮助排查问题。

```bash
agently chat --debug
```

### 4. 静默模式

静默模式只输出最终结果，不显示中间过程。

```bash
agently ask --silent "生成一个快速排序算法"
```

### 5. 输出重定向

将输出重定向到文件。

```bash
agently ask --output result.py "生成一个 Python 脚本"
```

## 快捷键

### 对话模式快捷键
- `Ctrl+C`：中断当前任务
- `Ctrl+D`：退出对话模式
- `Ctrl+L`：清屏
- `↑` / `↓`：浏览历史命令
- `Tab`：自动补全

### 菜单模式快捷键
- `Esc`：返回上一级菜单
- `Enter`：选择当前选项
- `↑` / `↓`：在菜单中导航
- `0`：退出菜单模式

## 环境变量

Agently 支持通过环境变量配置：

```bash
# API 密钥
export OPENAI_API_KEY="your_openai_api_key"
export ANTHROPIC_API_KEY="your_anthropic_api_key"
export GOOGLE_API_KEY="your_google_api_key"

# 模型配置
export AGLY_DEFAULT_MODEL="openai"
export AGLY_TEMPERATURE="0.7"

# 性能配置
export AGLY_MAX_MEMORY="4096"
export AGLY_MAX_CONCURRENT_CONTEXTS="3"
export AGLY_TIMEOUT="120"

# 日志配置
export AGLY_LOG_LEVEL="INFO"
export AGLY_LOG_FILE="/path/to/log/file.log"
```

## 最佳实践

### 1. 选择合适的交互模式
- **对话模式**：适合复杂任务、多轮对话
- **命令模式**：适合快速任务、单次查询
- **菜单模式**：适合不熟悉命令行的用户

### 2. 有效使用上下文
- 为不同的任务创建不同的上下文
- 定期清理不需要的上下文
- 使用有意义的上下文名称

### 3. 合理配置
- 根据任务复杂度调整温度参数
- 根据系统资源调整内存限制
- 根据网络情况调整超时时间

### 4. 使用智能体和技能
- 选择最适合当前任务的智能体
- 使用技能来规范开发流程
- 组合多个智能体和技能完成复杂任务

## 故障排查

### 问题：命令无法识别
**解决方案**：
```bash
# 检查 Agently 是否正确安装
agently --version

# 检查 PATH 环境变量
which agently

# 重新安装
pip install --upgrade agently
```

### 问题：API 调用失败
**解决方案**：
```bash
# 检查 API 密钥
echo $OPENAI_API_KEY

# 检查网络连接
ping api.openai.com

# 使用调试模式查看详细信息
agently chat --debug
```

### 问题：内存不足
**解决方案**：
```bash
# 调整内存限制
agently config set performance.max_memory 4096

# 减少并发上下文
agently config set performance.max_concurrent_contexts 2

# 清理不需要的上下文
agently context clear
```

---

**相关文档**:
- [快速入门](quickstart.md)
- [命令参考](cli_reference.md)
- [常见问题](faq.md)
