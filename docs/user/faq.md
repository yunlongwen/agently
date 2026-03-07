# 常见问题

本文档收集了 Agently 使用过程中的常见问题和解决方案。

## 安装和配置

### Q1: 如何安装 Agently？

**A**: 请参考 [安装指南](installation.md) 获取详细的安装步骤。

简要步骤：
1. 安装 Python 3.9+
2. 安装 Git
3. 运行 `pip install agently`
4. 配置 API 密钥

### Q2: 支持哪些操作系统？

**A**: Agently 支持：
- macOS 10.15+
- Linux (Ubuntu 20.04+, Debian 11+, CentOS 8+)
- Windows 10+ (WSL2 推荐)

### Q3: 支持哪些 Python 版本？

**A**: Agently 支持 Python 3.9 及以上版本。推荐使用 Python 3.11。

### Q4: 如何配置 API 密钥？

**A**: Agently 支持三种配置方式：

1. **环境变量**（推荐）：
```bash
export OPENAI_API_KEY="your_openai_api_key"
export ANTHROPIC_API_KEY="your_anthropic_api_key"
export GOOGLE_API_KEY="your_google_api_key"
```

2. **配置文件**：
```bash
agently config set openai.api_key "your_openai_api_key"
```

3. **命令行参数**：
```bash
agently chat --api-key "your_api_key"
```

### Q5: 支持哪些 AI 模型？

**A**: Agently 支持以下云端模型：
- **OpenAI**: GPT-4, GPT-3.5-turbo
- **Anthropic**: Claude 3 Opus, Claude 3 Sonnet, Claude 3 Haiku
- **Google Gemini**: Gemini Pro, Gemini Ultra

### Q6: 为什么不支持本地模型？

**A**: Agently 专注于云端模型，原因如下：
- 云端模型性能更强，更适合复杂编程任务
- 减少用户配置复杂度
- 确保模型更新和功能的一致性
- 降低硬件要求

如果您需要使用本地模型，可以考虑其他工具如 Ollama。

## 使用问题

### Q7: 如何开始使用 Agently？

**A**: 请参考 [快速入门指南](quickstart.md)。

基本步骤：
1. 启动对话模式：`agently chat`
2. 输入您的问题或需求
3. Agently 会分析并生成响应

### Q8: 对话模式和命令模式有什么区别？

**A**: 
- **对话模式** (`agently chat`)：支持多轮对话，记住上下文，适合复杂任务
- **命令模式** (`agently ask`)：单次查询，不记住上下文，适合快速任务

### Q9: 如何选择合适的智能体？

**A**: Agently 提供多个专用智能体：

| 智能体 | 适用场景 |
|--------|----------|
| Nexus 协调器 | 复杂任务、多步骤任务 |
| 代码生成器 | 代码生成、框架搭建 |
| 代码审查器 | 代码审查、代码优化 |
| 测试生成器 | 测试编写、测试覆盖 |
| 文档生成器 | 文档编写、代码注释 |

使用 `agently agents list` 查看所有可用智能体。

### Q10: 如何使用技能？

**A**: 技能是 Agently 的扩展功能，用于规范开发流程。

查看可用技能：
```bash
agently skills list
```

使用特定技能：
```bash
agently chat --skill test-driven-development
```

### Q11: Agently 能理解我的项目代码吗？

**A**: 是的，Agently 可以：
- 读取和分析项目文件
- 理解代码结构和依赖关系
- 识别代码问题和改进建议
- 生成符合项目风格的代码

使用示例：
```bash
# 分析项目结构
agently ask "分析当前项目的代码结构"

# 理解特定文件
agently ask "解释文件 src/main.py 的作用"
```

### Q12: 如何让 Agently 生成特定语言的代码？

**A**: 在请求中明确指定编程语言：

```bash
agently ask "用 Python 写一个快速排序算法"
agently ask "用 JavaScript 创建一个 RESTful API"
agently ask "用 Go 实现一个并发服务器"
```

### Q13: Agently 生成的代码可以直接使用吗？

**A**: Agently 生成的代码质量很高，但建议：
1. 理解生成的代码逻辑
2. 根据项目需求进行调整
3. 编写测试验证功能
4. 进行代码审查

### Q14: 如何提高代码生成的质量？

**A**: 提供更详细和明确的请求：
- 描述具体的功能需求
- 指定编程语言和框架
- 提供代码示例或模板
- 说明性能和安全要求
- 指定代码风格和规范

示例：
```bash
# 好的请求
agently ask "使用 FastAPI 创建一个用户注册 API，包含以下功能：
1. 邮箱验证
2. 密码加密
3. 错误处理
4. 输入验证
使用 Pydantic 进行数据验证，返回 JSON 格式响应"

# 不好的请求
agently ask "创建一个用户注册 API"
```

## 性能问题

### Q15: Agently 响应很慢怎么办？

**A**: 可能的原因和解决方案：

1. **网络问题**：
   - 检查网络连接
   - 使用代理或 VPN
   - 尝试不同的 API 端点

2. **任务复杂**：
   - 简化任务描述
   - 分步骤执行
   - 增加超时时间：`agently config set performance.timeout 180`

3. **模型选择**：
   - 使用更快的模型（如 GPT-3.5-turbo）
   - 减少最大 token 数

### Q16: Agently 占用多少内存？

**A**: 默认配置下，Agently 的内存占用限制为 4GB。

调整内存限制：
```bash
agently config set performance.max_memory 4096  # MB
```

### Q17: 可以同时运行多个对话吗？

**A**: 可以，默认支持 3-5 个并发上下文。

调整并发数：
```bash
agently config set performance.max_concurrent_contexts 5
```

### Q18: 如何减少 API 调用成本？

**A**: 
1. 使用更便宜的模型（如 GPT-3.5-turbo）
2. 减少对话长度
3. 清理不需要的上下文
4. 使用缓存功能

## 错误和故障

### Q19: 遇到 "Invalid API key" 错误怎么办？

**A**: 检查 API 密钥配置：
```bash
# 检查环境变量
echo $OPENAI_API_KEY

# 检查配置文件
agently config show

# 重新设置 API 密钥
agently config set openai.api_key "your_correct_api_key"
```

### Q20: 遇到 "Rate limit exceeded" 错误怎么办？

**A**: API 调用频率超限，解决方案：
1. 等待一段时间后重试
2. 升级 API 计划
3. 减少并发请求
4. 使用不同的 API 密钥

### Q21: 遇到 "MemoryError" 怎么办？

**A**: 内存不足，解决方案：
1. 增加内存限制：
```bash
agently config set performance.max_memory 4096
```

2. 减少并发上下文：
```bash
agently config set performance.max_concurrent_contexts 2
```

3. 清理不需要的上下文：
```bash
agently context clear
```

### Q22: 遇到 "Timeout" 错误怎么办？

**A**: 任务超时，解决方案：
1. 增加超时时间：
```bash
agently config set performance.timeout 180
```

2. 简化任务描述
3. 分步骤执行复杂任务

### Q23: Agently 崩溃了怎么办？

**A**: 
1. 查看日志：
```bash
agently logs --tail 50
```

2. 启用调试模式：
```bash
agently chat --debug
```

3. 检查系统资源：
```bash
# 检查内存
free -h  # Linux
vm_stat  # macOS

# 检查磁盘空间
df -h
```

4. 重新安装 Agently：
```bash
pip uninstall agently
pip install agently
```

## 高级问题

### Q24: 如何自定义智能体？

**A**: Agently 支持自定义智能体，请参考 [开发指南](../developer_skills/AGENTIC_CODING_BEST_PRACTICES.md)。

### Q25: 如何扩展 Agently 的功能？

**A**: Agently 支持通过技能和工具扩展功能：
- **技能**：定义开发流程和最佳实践
- **工具**：添加新的功能能力

### Q26: 如何集成到 CI/CD 流程？

**A**: 可以在 CI/CD 脚本中使用 Agently：

```bash
# 示例：在 GitHub Actions 中使用
- name: Generate documentation
  run: |
    agently ask --output docs/api.md "为 API 生成文档"

- name: Run code review
  run: |
    agently ask --agent code-reviewer "审查 src/ 目录下的代码"
```

### Q27: 如何备份和恢复配置？

**A**: 
导出配置：
```bash
agently export config config_backup.yaml
```

导入配置：
```bash
agently import config config_backup.yaml
```

### Q28: 如何查看 Agently 的日志？

**A**: 
查看日志：
```bash
# 查看最后 50 行
agently logs --tail 50

# 实时跟踪日志
agently logs --follow

# 只显示错误日志
agently logs --level ERROR
```

日志文件位置：
- **Linux/macOS**: `~/.agently/logs/agently.log`
- **Windows**: `%USERPROFILE%\.agently\logs\agently.log`

## 安全和隐私

### Q29: Agently 会收集我的数据吗？

**A**: Agently 不会主动收集用户数据。但请注意：
- 您的对话内容会发送到 API 提供商（OpenAI、Anthropic、Google）
- 请参考各 API 提供商的隐私政策
- 不要在对话中包含敏感信息

### Q30: 如何保护我的 API 密钥？

**A**: 
1. 不要将 API 密钥提交到版本控制系统
2. 使用环境变量或配置文件存储密钥
3. 定期轮换 API 密钥
4. 限制 API 密钥的权限和使用范围

### Q31: Agently 生成的代码安全吗？

**A**: Agently 生成的代码质量很高，但建议：
1. 理解生成的代码逻辑
2. 进行安全审查
3. 编写测试验证功能
4. 不要盲目信任生成的代码

## 社区和支持

### Q32: 如何获取帮助？

**A**: 
1. 查阅文档
2. 搜索 [GitHub Issues](https://github.com/yunlongwen/agently/issues)
3. 在 [GitHub Discussions](https://github.com/yunlongwen/agently/discussions) 提问
4. 加入社区讨论

### Q33: 如何报告 Bug？

**A**: 
1. 在 [GitHub Issues](https://github.com/yunlongwen/agently/issues) 创建新 Issue
2. 提供详细的错误信息
3. 包含复现步骤
4. 附上日志和配置信息

### Q34: 如何贡献代码？

**A**: 
1. Fork 仓库
2. 创建功能分支
3. 提交更改
4. 创建 Pull Request

详细贡献指南请参考 [开发指南](../developer_skills/AGENTIC_CODING_BEST_PRACTICES.md)。

### Q35: 如何联系开发团队？

**A**: 
- GitHub: https://github.com/yunlongwen/agently
- Issues: https://github.com/yunlongwen/agently/issues
- Discussions: https://github.com/yunlongwen/agently/discussions

## 其他问题

### Q36: Agently 是开源的吗？

**A**: 是的，Agently 采用 MIT 开源协议。

### Q37: Agently 的未来计划是什么？

**A**: 请关注 [GitHub Discussions](https://github.com/yunlongwen/agently/discussions) 和 [项目路线图](https://github.com/yunlongwen/agently/milestones)。

### Q38: 如何获取最新版本？

**A**: 
```bash
pip install --upgrade agently
```

或查看 [GitHub Releases](https://github.com/yunlongwen/agently/releases)。

### Q39: Agently 有商业支持吗？

**A**: 目前 Agently 是开源项目，不提供商业支持。欢迎社区贡献和反馈。

### Q40: 如何支持 Agently 项目？

**A**: 
1. 使用并反馈问题
2. 贡献代码和文档
3. 在社交媒体上分享
4. 给项目加 Star ⭐

---

**相关文档**:
- [安装指南](installation.md)
- [快速入门](quickstart.md)
- [CLI 使用](cli_usage.md)
- [命令参考](cli_reference.md)
