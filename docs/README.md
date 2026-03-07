# Agently 文档中心

欢迎来到 Agently 文档中心！这里包含了 Agently 项目的所有技术文档和设计文档。

## 文档索引

### 📋 项目概述

| 文档 | 描述 | 状态 |
|------|------|------|
| [../README.md](../README.md) | 项目概述、愿景、核心特性 | ✅ 已完成 |

### 📐 架构设计

| 文档 | 描述 | 状态 |
|------|------|------|
| [architecture.md](./architecture.md) | 系统整体技术架构设计 | ✅ 已完成 |
| [agent_architecture.md](./agent_layer/agent_architecture.md) | 智能体架构设计（Nexus + 专业智能体） | ✅ 已完成 |
| [cli_architecture.md](./cli_layer/cli_architecture.md) | CLI 界面架构设计 | ✅ 已完成 |
| [orchestrator_architecture.md](./orchestrator_layer/orchestrator_architecture.md) | 协调层架构设计（智能体协调和工作流编排） | ✅ 已完成 |
| [core_services_architecture.md](./core_services_layer/core_services_architecture.md) | 核心能力层架构设计（代码理解、模型集成等） | ✅ 已完成 |
| [infrastructure_architecture.md](./infrastructure_layer/infrastructure_architecture.md) | 基础设施层架构设计（文件系统、Git、测试等） | ✅ 已完成 |

### 📋 需求分析

| 文档 | 描述 | 状态 |
|------|------|------|
| [requirements.md](./requirements.md) | 功能性和非功能性需求 | ✅ 已完成 |

### 🔧 技术选型（待完成）

| 文档 | 描述 | 状态 |
|------|------|------|
| tech_selection.md | 各组件技术选型分析 | 📝 待创建 |
| database_design.md | 数据库/存储设计 | 📝 待创建 |
| api_design.md | API 接口设计 | 📝 待创建 |

### 📖 开发指南（待完成）

| 文档 | 描述 | 状态 |
|------|------|------|
| development_guide.md | 开发环境搭建和贡献指南 | 📝 待创建 |
| coding_standards.md | 代码规范和最佳实践 | 📝 待创建 |
| testing_guide.md | 测试策略和指南 | 📝 待创建 |

### 📚 用户文档（待完成）

| 文档 | 描述 | 状态 |
|------|------|------|
| user_guide.md | 用户使用指南 | 📝 待创建 |
| cli_reference.md | CLI 命令参考手册 | 📝 待创建 |
| faq.md | 常见问题解答 | 📝 待创建 |

---

## 快速导航

### 如果你是开发者

1. 先阅读 [项目概述](../README.md) 了解 Agently 是什么
2. 查看 [需求文档](./requirements.md) 了解功能需求
3. 深入 [架构设计](./architecture.md) 理解系统架构
4. 研究 [智能体架构](./agent_layer/agent_architecture.md) 了解多智能体设计
5. 查看 [协调层架构](./orchestrator_layer/orchestrator_architecture.md) 了解智能体协调
6. 了解 [核心能力层架构](./core_services_layer/core_services_architecture.md) 了解核心服务
7. 查看 [基础设施层架构](./infrastructure_layer/infrastructure_architecture.md) 了解底层服务
8. 研究 [CLI 架构](./cli_layer/cli_architecture.md) 了解界面设计

### 如果你想贡献代码

1. 阅读 [开发指南](./development_guide.md)（待创建）
2. 了解 [代码规范](./coding_standards.md)（待创建）
3. 查看 [测试指南](./testing_guide.md)（待创建）

### 如果你是用户

1. 阅读 [用户指南](./user_guide.md)（待创建）
2. 查看 [CLI 命令参考](./cli_reference.md)（待创建）
3. 浏览 [FAQ](./faq.md)（待创建）

---

## 文档维护

### 文档规范

- 所有文档使用 Markdown 格式
- 架构图使用 Mermaid 语法
- 代码示例使用语法高亮
- 保持文档间的链接有效性

### 更新记录

| 日期 | 更新内容 | 作者 |
|------|----------|------|
| 2026-03-07 | 创建文档索引 | Agently Team |
| 2026-03-07 | 完成架构设计文档 | Agently Team |
| 2026-03-07 | 完成智能体架构文档 | Agently Team |
| 2026-03-07 | 完成 CLI 架构文档 | Agently Team |
| 2026-03-07 | 完成协调层架构文档 | Agently Team |
| 2026-03-07 | 完成核心能力层架构文档 | Agently Team |
| 2026-03-07 | 完成基础设施层架构文档 | Agently Team |
| 2026-03-07 | 完成需求文档 | Agently Team |

---

## 贡献文档

欢迎为 Agently 文档做出贡献！请遵循以下步骤：

1. Fork 项目仓库
2. 创建文档分支
3. 编写或更新文档
4. 提交 Pull Request

### 文档编写规范

1. **清晰性**：使用简洁明了的语言
2. **完整性**：覆盖所有必要的信息
3. **一致性**：保持术语和格式的一致性
4. **可维护性**：使用相对路径，避免硬编码

---

**文档版本**: v1.0  
**最后更新**: 2026-03-07  
**维护者**: Agently 开发团队