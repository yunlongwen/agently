# Agently

Agently 是一个专注于编程任务的 AI 驱动的编程助手，旨在帮助开发者提高编程效率，简化软件开发流程。

## ✨ 特性

- **全开发场景覆盖**：覆盖软件开发的完整生命周期（SDLC）
- **智能代码理解**：深度理解代码结构和语义
- **多智能体协作**：专业的 SDLC 智能体系统
- **灵活的交互方式**：命令行界面、交互式对话、菜单式导航

## 🚀 快速开始

### 安装

```bash
pip install agently
```

### 配置

```bash
# 设置 OpenAI API 密钥
export OPENAI_API_KEY="your_openai_api_key"

# 或使用配置文件
agently config set openai.api_key "your_openai_api_key"
```

### 使用

```bash
# 启动交互式对话
agently chat

# 快速提问
agently ask "如何在 Python 中实现单例模式？"

# 使用特定智能体
agently chat --agent code-generator
```

## 📚 文档索引

### 项目概述
- [项目概述](../README.md)

### 架构设计
- [系统架构](architecture.md)
- [智能体层](agent_layer/agent_architecture.md)
- [CLI 层](cli_layer/cli_architecture.md)
- [协调层](orchestrator_layer/orchestrator_architecture.md)
- [核心能力层](core_services_layer/core_services_architecture.md)
- [基础设施层](infrastructure_layer/infrastructure_architecture.md)

### 技术文档
- [需求文档](requirements.md)
- [技术选型](tech_selection.md)
- [开发指南](developer_skills/AGENTIC_CODING_BEST_PRACTICES.md)
- [文档部署](documentation_guide.md)

### 用户文档
- [项目简介](user/introduction.md)
- [安装指南](user/installation.md)
- [快速入门](user/quickstart.md)
- [CLI 使用](user/cli_usage.md)
- [命令参考](user/cli_reference.md)
- [常见问题](user/faq.md)

## 🔗 快速导航

### 开发者
1. 阅读 [项目概述](../README.md)
2. 查看 [需求文档](requirements.md)
3. 深入 [系统架构](architecture.md)
4. 研究 [智能体架构](agent_layer/agent_architecture.md)
5. 了解 [协调层架构](orchestrator_layer/orchestrator_architecture.md)
6. 查看 [核心能力层架构](core_services_layer/core_services_architecture.md)
7. 研究 [基础设施层架构](infrastructure_layer/infrastructure_architecture.md)
8. 了解 [CLI 架构](cli_layer/cli_architecture.md)

### 贡献者
1. 阅读 [开发指南](developer_skills/AGENTIC_CODING_BEST_PRACTICES.md)
2. 查看 [技术选型](tech_selection.md)

### 用户
1. 阅读 [项目简介](user/introduction.md)
2. 查看 [安装指南](user/installation.md)
3. 参考 [快速入门](user/quickstart.md)
4. 查看 [CLI 使用](user/cli_usage.md)
5. 浏览 [命令参考](user/cli_reference.md)
6. 查看 [常见问题](user/faq.md)

## 🤝 贡献

欢迎贡献代码、报告问题或提出建议！

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

感谢所有为 Agently 做出贡献的开发者！

---

**GitHub**: [https://github.com/yunlongwen/agently](https://github.com/yunlongwen/agently)  
**Issues**: [https://github.com/yunlongwen/agently/issues](https://github.com/yunlongwen/agently/issues)  
**Discussions**: [https://github.com/yunlongwen/agently/discussions](https://github.com/yunlongwen/agently/discussions)
