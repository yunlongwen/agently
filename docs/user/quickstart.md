# 快速入门

本指南将帮助您快速上手 Agently，体验其核心功能。

## 第一次使用

### 1. 启动 Agently

```bash
# 启动交互式对话模式
agently chat

# 或使用命令模式
agently ask "如何优化这段代码？"
```

### 2. 基本对话

在交互式对话模式中，您可以：

```bash
# 询问编程问题
> 如何在 Python 中实现单例模式？

# 请求代码生成
> 帮我写一个快速排序算法

# 请求代码审查
> 审查这段代码的性能问题
```

### 3. 使用智能体

Agently 提供多个专用智能体，您可以选择适合的智能体：

```bash
# 查看可用智能体
agently agents list

# 使用特定智能体
agently agents use code-generator
> 帮我生成一个 RESTful API 的代码框架

# 使用 Nexus 协调器（综合智能体）
agently agents use nexus
> 我需要开发一个用户管理系统，请帮我设计架构并生成代码
```

## 常用场景

### 场景 1：代码生成

#### 生成函数
```bash
agently ask "写一个 Python 函数，计算斐波那契数列的第 n 项"
```

#### 生成类
```bash
agently ask "创建一个 Python 类，表示银行账户，包含存款、取款和查询余额的方法"
```

#### 生成 API 端点
```bash
agently ask "使用 FastAPI 创建一个用户注册的 API 端点"
```

### 场景 2：代码理解

#### 解释代码
```bash
agently ask "解释这段代码的作用：[粘贴代码]"
```

#### 分析代码结构
```bash
agently ask "分析当前项目的代码结构，找出主要的模块和依赖关系"
```

#### 识别技术债务
```bash
agently ask "检查当前项目，识别潜在的技术债务和代码异味"
```

### 场景 3：代码重构

#### 优化性能
```bash
agently ask "优化这段代码的性能：[粘贴代码]"
```

#### 改进代码质量
```bash
agently ask "重构这段代码，使其更符合 Python 最佳实践：[粘贴代码]"
```

#### 添加类型注解
```bash
agently ask "为这段代码添加类型注解：[粘贴代码]"
```

### 场景 4：测试生成

#### 生成单元测试
```bash
agently ask "为这个函数生成单元测试：[粘贴函数代码]"
```

#### 生成集成测试
```bash
agently ask "为这个 API 端点生成集成测试：[粘贴 API 代码]"
```

### 场景 5：文档生成

#### 生成 API 文档
```bash
agently ask "为这个 API 生成文档：[粘贴 API 代码]"
```

#### 生成代码注释
```bash
agently ask "为这段代码添加详细的注释：[粘贴代码]"
```

## 进阶使用

### 1. 使用上下文

Agently 支持上下文管理，可以记住之前的对话：

```bash
# 启动对话
agently chat

# 第一次提问
> 我正在开发一个电商系统

# 第二次提问（会记住之前的上下文）
> 帮我设计用户模块的数据库表结构

# 第三次提问（继续使用上下文）
> 生成用户注册的 API 端点
```

### 2. 使用技能

Agently 支持技能系统，可以扩展功能：

```bash
# 查看可用技能
agently skills list

# 使用特定技能
agently skills use test-driven-development
> 使用 TDD 方法开发一个计算器类
```

### 3. 使用工具

Agently 支持工具调用，可以执行实际操作：

```bash
# 查看可用工具
agently tools list

# 使用工具
agently ask "使用 git 工具查看当前分支的状态"
```

### 4. 文件操作

Agently 可以直接操作文件：

```bash
# 读取文件
agently ask "读取文件 src/main.py 的内容"

# 写入文件
agently ask "将生成的代码写入文件 src/utils.py"

# 创建文件
agently ask "创建一个新的配置文件 config.yaml"
```

## 实战示例

### 示例 1：开发一个简单的 Web API

```bash
# 1. 使用 Nexus 协调器
agently agents use nexus

# 2. 描述需求
> 我需要开发一个简单的待办事项 API，包含以下功能：
> - 创建待办事项
> - 获取待办事项列表
> - 更新待办事项
> - 删除待办事项

# 3. Agently 会自动：
# - 设计 API 架构
# - 生成代码框架
# - 实现各个端点
# - 生成测试代码
# - 生成文档
```

### 示例 2：代码审查和优化

```bash
# 1. 使用代码审查智能体
agently agents use code-reviewer

# 2. 提供代码
> 请审查这段代码的性能和安全性：
> [粘贴代码]

# 3. Agently 会：
# - 分析代码质量
# - 识别潜在问题
# - 提供优化建议
# - 生成优化后的代码
```

### 示例 3：学习新技术

```bash
# 1. 询问技术概念
> 解释什么是 React Hooks？

# 2. 请求代码示例
> 给我一个使用 useState 的示例

# 3. 请求最佳实践
> 使用 Hooks 时有哪些最佳实践？

# 4. 请求完整示例
> 帮我创建一个使用 Hooks 的计数器组件
```

## 命令参考

### 基本命令

```bash
# 查看帮助
agently --help

# 查看版本
agently --version

# 健康检查
agently doctor

# 查看配置
agently config show

# 设置配置
agently config set <key> <value>
```

### 智能体命令

```bash
# 列出可用智能体
agently agents list

# 使用特定智能体
agently agents use <agent-name>

# 查看智能体详情
agently agents info <agent-name>
```

### 技能命令

```bash
# 列出可用技能
agently skills list

# 使用特定技能
agently skills use <skill-name>

# 查看技能详情
agently skills info <skill-name>
```

### 工具命令

```bash
# 列出可用工具
agently tools list

# 查看工具详情
agently tools info <tool-name>
```

## 最佳实践

### 1. 明确需求
- 清晰地描述您的需求
- 提供足够的上下文信息
- 指定期望的输出格式

### 2. 迭代开发
- 从简单开始，逐步增加复杂度
- 使用上下文保持对话连贯性
- 及时反馈和调整

### 3. 代码审查
- 不要盲目接受生成的代码
- 理解生成的代码逻辑
- 根据需要进行调整

### 4. 测试验证
- 为生成的代码编写测试
- 验证代码的正确性
- 检查边界情况和错误处理

## 下一步

完成快速入门后，您可以：

1. 阅读 [CLI 使用指南](cli_usage.md) 了解更多命令
2. 阅读 [命令参考](cli_reference.md) 查看完整的命令列表
3. 查看 [常见问题](faq.md) 解决使用中的问题
4. 阅读 [架构设计文档](../architecture.md) 了解 Agently 的内部实现

## 获取帮助

如果您在使用过程中遇到问题：

1. 查看 [常见问题](faq.md)
2. 在 [GitHub Issues](https://github.com/yunlongwen/agently/issues) 搜索或提问
3. 在 [GitHub Discussions](https://github.com/yunlongwen/agently/discussions) 参与讨论

---

**相关文档**:
- [安装指南](installation.md)
- [CLI 使用](cli_usage.md)
- [命令参考](cli_reference.md)
- [常见问题](faq.md)
