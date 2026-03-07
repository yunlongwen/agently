# Agently 文档部署方案

## 文档说明

本文档提供 Agently 项目的文档部署方案，包括文档构建、自动化部署和使用指南。

---

## 部署架构

```mermaid
flowchart LR
    A[文档编写] --> B[本地预览]
    B --> C[推送到 GitHub]
    C --> D[GitHub Actions 构建]
    D --> E[部署到 GitHub Pages]
    E --> F[访问文档网站]
```

---

## 技术选型

| 组件 | 技术 | 版本 | 理由 |
|------|------|------|------|
| 文档构建 | MkDocs | 1.5+ | 轻量级、Markdown原生、主题丰富 |
| 部署平台 | GitHub Pages | - | 免费、自动HTTPS、与GitHub集成 |
| CI/CD | GitHub Actions | - | 原生集成、免费、自动化 |
| 域名 | GitHub Pages 默认域名 | - | 无需额外配置 |

---

## 目录结构

```
agently/
├── docs/                      # 文档源文件
│   ├── index.md              # 文档首页
│   ├── user/                # 用户文档
│   ├── agent_layer/          # 智能体层文档
│   ├── cli_layer/            # CLI层文档
│   ├── orchestrator_layer/   # 协调层文档
│   ├── core_services_layer/  # 核心能力层文档
│   ├── infrastructure_layer/ # 基础设施层文档
│   └── developer_skills/     # 开发者技能文档
├── .github/workflows/       # GitHub Actions 工作流
│   └── docs.yml            # 文档部署工作流
└── mkdocs.yml               # MkDocs 配置文件
```

---

## 快速开始

### 1. 本地开发

```bash
# 安装依赖
pip install mkdocs-material

# 本地预览
mkdocs serve

# 访问 http://127.0.0.1:8000

# 构建文档
mkdocs build
```

### 2. 配置文件 (mkdocs.yml)

```yaml
site_name: Agently
site_url: https://yunlongwen.github.io/agently

docs_dir: docs
site_dir: site

nav:
  - 首页: index.md
  - 用户指南:
    - 安装指南: user/installation.md
    - 快速入门: user/quickstart.md
  - 架构设计:
    - 系统架构: architecture.md
    - 智能体层: agent_layer/agent_architecture.md
  - 技术文档:
    - 技术选型: tech_selection.md

theme:
  name: material
  language: zh
  features:
    - navigation.tabs
    - search.suggest
    - toc.integrate

plugins:
  - search
```

### 3. GitHub Actions 工作流

```yaml
name: Documentation

on:
  push:
    branches:
      - master
    paths:
      - 'docs/**'
      - 'mkdocs.yml'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install mkdocs-material
      - run: mkdocs build
      - name: Deploy
        if: github.event_name == 'push' && github.ref == 'refs/heads/master'
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./site
```

---

## 文档编写规范

### Markdown 规范

- **标题**：使用 `#` 表示标题层级
- **代码**：使用 ``` 包裹代码块，指定语言
- **链接**：`[文本](url)`
- **图片**：`![描述](路径)`
- **表格**：使用 `|` 分隔列
- **提示**：使用 `!!! note` 等提示框

### 文档结构

**用户文档**：
- 简介
- 前置条件
- 使用步骤
- 示例
- 常见问题

**架构文档**：
- 概述
- 核心设计
- 架构图
- 接口定义
- 数据流

---

## 部署流程

1. **编写文档**：在 `docs/` 目录下创建 Markdown 文件
2. **本地测试**：运行 `mkdocs serve` 预览
3. **提交代码**：`git add` 和 `git commit`
4. **推送**：`git push` 到 GitHub
5. **自动部署**：GitHub Actions 自动构建和部署
6. **访问**：打开 `https://yunlongwen.github.io/agently`

---

## 最佳实践

1. **保持简洁**：使用清晰、简洁的语言
2. **示例丰富**：提供充分的代码示例
3. **定期更新**：保持文档与代码同步
4. **链接检查**：确保所有链接有效
5. **版本管理**：使用 Git 标签管理文档版本

---

## 故障排查

### 构建失败
- 检查 Markdown 语法错误
- 检查链接有效性
- 检查图片路径

### 部署失败
- 检查 GitHub Token 权限
- 查看 Actions 日志
- 检查分支保护设置

---

## 扩展功能

- **多语言**：支持中英文文档
- **版本管理**：使用 mike 管理多版本文档
- **搜索优化**：配置中文搜索
- **性能优化**：启用缓存和压缩

---

**文档版本**: v1.0  
**最后更新**: 2026-03-07  
**维护者**: Agently 开发团队
