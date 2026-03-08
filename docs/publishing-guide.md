# 发布指南

本文档说明如何将 Agently 发布到 PyPI，让普通用户可以通过 `pip install agently` 安装。

## 发布流程

### 方式 1：自动发布（推荐）

通过 GitHub Release 自动发布到 PyPI：

1. **更新版本号**

   编辑 `src/agently/__init__.py`：
   ```python
   __version__ = "0.2.0"  # 更新版本号
   ```

2. **创建 Git Tag**

   ```bash
   git tag v0.2.0
   git push origin v0.2.0
   ```

3. **创建 GitHub Release**

   - 访问 https://github.com/yunlongwen/agently/releases
   - 点击 "Draft a new release"
   - 选择刚推送的 tag `v0.2.0`
   - 填写 Release notes
   - 点击 "Publish release"

4. **自动发布**

   GitHub Actions 会自动：
   - 构建包（wheel 和 sdist）
   - 发布到 PyPI
   - 构建各平台二进制文件
   - 上传到 GitHub Release

### 方式 2：手动发布

如果需要手动发布：

```bash
# 1. 安装发布工具
pip install build twine

# 2. 构建包
python -m build

# 3. 检查包
twine check dist/*

# 4. 发布到 PyPI
twine upload dist/*
```

## PyPI 配置

### 首次配置（一次性）

1. **注册 PyPI 账号**

   访问 https://pypi.org/account/register/

2. **配置 GitHub Actions Trusted Publishing**

   - 访问 https://pypi.org/manage/account/publishing/
   - 点击 "Add a new pending publisher"
   - 填写：
     - PyPI Project Name: `agently`
     - Owner: `yunlongwen`
     - Repository name: `agently`
     - Workflow name: `publish.yml`
   - 点击 "Add"

3. **验证配置**

   GitHub Actions 工作流已配置为使用 Trusted Publishing，无需 API Token。

## 版本管理

### 版本号规则

遵循 [PEP 440](https://peps.python.org/pep-0440/) 版本规范：

```
MAJOR.MINOR.PATCH  # 例如：0.1.0, 0.2.0, 1.0.0
```

- **MAJOR**: 重大变更，不兼容的 API 修改
- **MINOR**: 新功能，向后兼容
- **PATCH**: Bug 修复，向后兼容

### 预发布版本

```python
__version__ = "0.2.0a1"  # Alpha
__version__ = "0.2.0b1"  # Beta
__version__ = "0.2.0rc1" # Release Candidate
```

### 开发版本

```python
__version__ = "0.2.0.dev1"  # 开发版本
```

## 发布检查清单

发布前请确认：

- [ ] 更新 `src/agently/__init__.py` 中的版本号
- [ ] 更新 `CHANGELOG.md` 记录变更
- [ ] 运行测试确保通过：`make test`
- [ ] 运行代码检查：`make lint` 和 `make type-check`
- [ ] 更新文档（如有需要）
- [ ] 创建 Git Tag
- [ ] 推送 Tag 到远程
- [ ] 创建 GitHub Release 并填写 Release notes

## 验证发布

发布后验证：

```bash
# 1. 检查 PyPI 页面
# 访问 https://pypi.org/project/agently/

# 2. 测试安装
pip install agently==0.2.0

# 3. 测试运行
agently --version
```

## 回滚版本

如果发现问题需要回滚：

1. **从 PyPI 删除版本**

   访问 https://pypi.org/manage/project/agently/releases/
   删除对应的版本

2. **删除 GitHub Release**

   - 访问 GitHub Releases 页面
   - 删除对应的 Release

3. **删除 Git Tag**

   ```bash
   git tag -d v0.2.0
   git push origin :refs/tags/v0.2.0
   ```

4. **修复问题后重新发布**

   使用新的版本号重新发布。

## 常见问题

### Q: 发布失败怎么办？

A: 检查 GitHub Actions 日志，常见原因：
- 版本号已存在（需要更新版本号）
- Trusted Publishing 未配置
- 包名冲突（检查 PyPI 上是否已有同名包）

### Q: 如何发布到 TestPyPI？

A: 修改 `.github/workflows/publish.yml`：

```yaml
- name: Publish to TestPyPI
  uses: pypa/gh-action-pypi-publish@release/v1
  with:
    repository-url: https://test.pypi.org/legacy/
```

测试安装：
```bash
pip install --index-url https://test.pypi.org/simple/ agently
```

### Q: 如何更新包描述？

A: 更新 `pyproject.toml` 中的 `readme` 和 `description` 字段，然后重新发布。

## 相关资源

- [PyPI 官方文档](https://pypi.org/help/)
- [PEP 440 版本规范](https://peps.python.org/pep-0440/)
- [GitHub Actions PyPI 发布](https://github.com/pypa/gh-action-pypi-publish)
- [Trusted Publishing](https://docs.pypi.org/trusted-publishers/)
