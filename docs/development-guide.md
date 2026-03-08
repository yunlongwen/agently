# 开发指南

本文档说明如何确保代码质量，在 git push 前通过所有检查。

## 代码质量检查

### 自动检查（Pre-commit Hooks）

每次提交代码时，pre-commit hooks 会自动运行以下检查：

1. **Ruff Linting** - 代码风格检查
   ```bash
   ruff check .
   ```

2. **Ruff Formatting** - 代码格式化
   ```bash
   ruff format .
   ```

3. **Pytest** - 单元测试
   ```bash
   pytest tests/unit/ -v --tb=short
   ```

4. **MyPy** - 类型检查
   ```bash
   mypy src/
   ```

### 手动运行检查

如果需要手动运行检查：

```bash
# 运行所有检查
make check

# 或分别运行
make test          # 运行测试
make lint          # 代码检查
make type-check    # 类型检查
make format        # 格式化代码
```

## 安装 Pre-commit Hooks

### 首次安装

```bash
# 安装 pre-commit
pip install pre-commit

# 安装 hooks
make pre-commit-install

# 或直接运行
pre-commit install
```

### 更新 Hooks

```bash
# 更新到最新版本
pre-commit autoupdate

# 重新安装
pre-commit install --force
```

## 跳过 Hooks（不推荐）

如果需要临时跳过检查：

```bash
# 跳过所有 hooks
git commit --no-verify -m "commit message"

# 跳过特定 hook
SKIP=pytest,ruff git commit -m "commit message"
```

⚠️ **注意**: 跳过检查可能导致代码质量问题，仅在紧急情况下使用。

## 检查失败处理

### 测试失败

如果测试失败：

1. 查看错误信息
2. 修复失败的测试
3. 重新运行测试验证修复
4. 提交修复

```bash
# 运行失败的测试
pytest tests/unit/cli/test_logo.py -v

# 运行所有测试
make test
```

### Lint 失败

如果 lint 失败：

1. 查看错误信息
2. 修复 lint 错误
3. 重新运行 lint
4. 提交修复

```bash
# 自动修复
make lint-fix

# 或手动修复后检查
make lint
```

### 类型检查失败

如果类型检查失败：

1. 查看类型错误
2. 添加类型注解
3. 重新运行类型检查
4. 提交修复

```bash
# 运行类型检查
make type-check
```

## GitHub Actions CI/CD

推送代码后，GitHub Actions 会自动运行：

### 工作流

1. **CI** - 持续集成
   - 运行所有测试
   - 代码检查
   - 类型检查
   - 生成覆盖率报告

2. **Publish** - 发布到 PyPI
   - 构建包
   - 发布到 PyPI
   - 构建二进制文件

3. **Build Binaries** - 构建多平台二进制
   - Windows x64
   - macOS x64/ARM64
   - Linux x64/ARM64

### 查看状态

访问 https://github.com/yunlongwen/agently/actions 查看所有工作流状态。

## 最佳实践

### 提交前

```bash
# 1. 运行所有检查
make check

# 2. 如果所有通过，提交代码
git add .
git commit -m "feat: add new feature"

# 3. 如果某个检查失败，修复后重新提交
make test
make lint
make type-check
```

### 推送前

```bash
# 1. 确保本地所有测试通过
make test

# 2. 确保代码检查通过
make lint
make type-check

# 3. 推送到远程
git push origin master
```

### 分支策略

```bash
# 创建功能分支
git checkout -b feature/new-feature

# 开发并提交
# pre-commit hooks 会自动运行检查

# 合并到主分支
git checkout master
git merge feature/new-feature

# 推送
git push origin master
```

## 常见问题

### Q: Pre-commit hooks 运行太慢？

A: 可以调整配置：

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/mirrors-pytest
    hooks:
      - id: pytest
        # 只在修改测试文件时运行
        files: ^tests/
```

### Q: 如何禁用特定 hook？

A: 在 `.pre-commit-config.yaml` 中注释掉：

```yaml
# 暂时禁用 pytest
# - repo: https://github.com/pre-commit/mirrors-pytest
#   hooks:
#     - id: pytest
```

### Q: Hooks 更新后如何重新安装？

A: 运行：

```bash
pre-commit uninstall
pre-commit install
```

## 相关资源

- [Pre-commit 官方文档](https://pre-commit.com/)
- [Ruff 文档](https://docs.astral.sh/ruff/)
- [MyPy 文档](https://mypy.readthedocs.io/)
- [Pytest 文档](https://docs.pytest.org/)
