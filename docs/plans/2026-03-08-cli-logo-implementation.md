# CLI Logo 实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为 Agently CLI 添加清晰显示 AGENTLY 字符的 Logo，仅在运行 `agently` 命令（不带子命令）时显示

**架构:** 在 CLI 主入口添加 Logo 常量，修改 cli() 函数，仅在运行 `agently` 命令（不带子命令）时显示 Logo

**技术栈:** Python, Click

---

## 前置条件

- 已选择方案一（大方块风格 Logo，显示 AGENTLY，字符间距一致）
- 设计文档已保存至 `docs/plans/2026-03-08-cli-logo-design.md`
- 指令保持为 `agently`，不需要修改

---

## Task 1: 在 main.py 中添加 Logo 常量

**Files:**
- Modify: `src/agently/cli/main.py:1-15`

**Step 1: 在文件顶部添加 Logo 常量**

在 imports 之后，`@click.group()` 之前添加：

```python
LOGO = """
    ▄▀█ █▀▀ █▀▀ █▄░█ ▀█▀ █░░ █▄█
    █▀█ █▄█ ██▄ █░▀█ ░█░ █▄▄ ░█░

    🤖 Agently v0.1.0 | AI-Driven Programming Assistant
    ────────────────────────────────────────────────────
    Tips: Run 'agently --help' to see available commands
"""
```

**Step 2: Commit**

```bash
git add src/agently/cli/main.py
git commit -m "feat: add ASCII logo constant to CLI main module"
```

---

## Task 2: 修改 cli() 函数添加 Logo 显示逻辑

**Files:**
- Modify: `src/agently/cli/main.py:29-47` (cli 函数)

**Step 1: 修改 cli() 函数**

将 `@click.group()` 改为 `@click.group(invoke_without_command=True)`，并添加 Logo 显示逻辑：

```python
@click.group(invoke_without_command=True)
@click.version_option(version="0.1.0")
@click.pass_context
def cli(ctx: click.Context) -> None:
    """Agently - AI-driven programming assistant"""
    ctx.ensure_object(dict)
    
    # 只在不带子命令时显示 logo
    if ctx.invoked_subcommand is None:
        click.echo(LOGO)
        click.echo(ctx.get_help())
```

**Step 2: Commit**

```bash
git add src/agently/cli/main.py
git commit -m "feat: display logo only when running 'agently' without subcommand"
```

---

## Task 3: 本地测试验证

**Step 1: 重新安装包**

```bash
pip install -e .
```

**Step 2: 测试 Logo 显示**

```bash
agently
```

**Expected Output:**
- 显示 Logo
- 然后显示帮助信息

**Step 3: 测试其他命令不显示 Logo**

```bash
agently --help
agently version
agently agent list
```

**Expected:** 这些命令不显示 Logo

**Step 4: Commit（如有测试文件修改）**

```bash
git add .
git commit -m "test: verify CLI logo display behavior"
```

---

## Task 4: 运行测试套件

**Step 1: 运行单元测试**

```bash
make test
```

或

```bash
pytest tests/unit/cli/ -v
```

**Expected:** 所有测试通过

**Step 2: 运行代码检查**

```bash
make lint
make type-check
```

**Step 3: Commit**

```bash
git add .
git commit -m "chore: pass all tests and lint checks"
```

---

## 验收标准

- [ ] 运行 `agently` 时显示 Logo
- [ ] 运行 `agently --help` 时不显示 Logo
- [ ] 运行 `agently version` 时不显示 Logo
- [ ] 运行 `agently chat` 时不显示 Logo
- [ ] Logo 字符清晰，无乱码
- [ ] 所有单元测试通过
- [ ] 代码通过 lint 检查

---

## 注意事项

1. Logo 使用 Unicode 字符，确保终端支持 UTF-8
2. 如果终端宽度不足，Logo 可能会换行显示
3. 后续可考虑添加 `--no-logo` 选项来禁用 Logo 显示
