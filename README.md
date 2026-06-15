# Skill-Core

> **GitHub 上传包** — 本目录即仓库根目录，见 [UPLOAD.md](UPLOAD.md)

**Agent Skills 工具链** — 用 IR 设计 skill，一键编译、测试、安装到任意兼容宿主。

基于 [Agent Skills 开放标准](https://agentskills.io)，不绑定 Cursor / Claude / 任何单一 IDE。

```
edit references/ir.md  →  skill compile  →  skill test  →  skill install
```

---

## 这个仓库是什么？

**整个仓库就是一个产品**，不需要拆开发。推 GitHub 时上传根目录全部内容（见下方结构）。

| 目录 | 作用 | 是否必需 |
|------|------|----------|
| `skill-core/` | CLI + 编译器 + meta skill | 核心 |
| `examples/` | 3 个官方示例 skill | 推荐 |
| `docs/` | 静态文档站（可开 GitHub Pages） | 推荐 |
| `registry.json` | skill 目录索引 | 推荐 |
| `.github/` | CI 流水线 | 推荐 |

---

## 快速开始

### 方式 A：克隆即用（推荐）

```bash
git clone https://github.com/azhimiao/skillforskill.git
cd skillforskill

pip install -r requirements.txt
# 或: pip install -e .

python skill-core/skill.py init my-skill
# 编辑 my-skill/references/ir.md
python skill-core/skill.py compile my-skill
python skill-core/skill.py test my-skill
python skill-core/skill.py install my-skill --host cursor --scope global
```

Windows：

```cmd
skill init my-skill
skill compile my-skill
skill test my-skill
```

### 方式 B：pip 安装 CLI

```bash
pip install git+https://github.com/azhimiao/skillforskill.git
skill init my-skill
```

---

## CLI 命令

| 命令 | 说明 |
|------|------|
| `skill init <name>` | 创建 skill 脚手架 |
| `skill compile <path>` | IR → SKILL.md |
| `skill diff <path>` | 检查 IR 是否漂移 |
| `skill validate <path>` | 校验 SKILL.md |
| `skill test <path>` | L0/L1 自动化测试 |
| `skill install <name>` | 安装到 cursor / claude / agents |
| `skill list` | 浏览 registry |
| `skill registry build` | 重建 registry.json |
| `skill migrate <file> --name x` | 迁移旧 rule/command |
| `skill migrate-scan` | 批量迁移项目规则 |
| `skill docs` | 文档站地址 |

完整说明：[QUICKSTART.md](QUICKSTART.md) · [docs/index.html](docs/index.html)

---

## 仓库结构

```
skill-core/                 # 工具链 + meta skill
├── skill.py                # CLI 入口
├── lib/                    # 编译器、测试、安装、迁移
├── schema/ir.schema.json   # IR JSON Schema
└── references/             # 模板、协议参考

examples/                   # 官方示例（simple / medium / complex）
docs/                       # 文档站
registry.json               # skill 索引
skill / skill.cmd           # CLI 快捷入口
pyproject.toml              # pip 安装
.github/workflows/skills.yml
```

---

## 安装目标

```bash
skill install medium-commit-message --host cursor --scope global
skill install ./my-skill --host agents --scope project --project /path/to/repo
```

| Host | 全局 | 项目 |
|------|------|------|
| `agents` | `~/.agents/skills/` | `.agents/skills/` |
| `cursor` | `~/.cursor/skills/` | `.cursor/skills/` |
| `claude` | `~/.claude/skills/` | `.claude/skills/` |

---

## 推送到 GitHub

1. 在 GitHub 新建仓库（建议名：`skillforskill`）
2. 在本目录执行：

```bash
git init
git add .
git commit -m "Initial release: Skill-Core toolchain v2.0"
git branch -M main
git remote add origin https://github.com/azhimiao/skillforskill.git
git push -u origin main
```

3. （可选）Settings → Pages → 选 `main` 分支 `/docs` 文件夹发布文档站

**不要上传的内容** 已在 `.gitignore` 中排除：`__pycache__`、生成的 `ir.json`、本地测试 skill 等。

---

## 开发自己的 skill 放哪？

两种方式：

| 场景 | 做法 |
|------|------|
| 贡献给本仓库 | 在 `examples/` 下新建目录，PR 进来 |
| 私人/团队 skill | `skill init my-skill --dir ~/my-skills`，独立仓库或本地目录 |
| 安装到 IDE | `skill install ./my-skill --host cursor` |

本仓库是 **工具链 + 官方示例**，不是你的 skill 生产目录。批量开发 skill 建议另建仓库，把 `skillforskill` 当依赖或 submodule。

---

## License

MIT — 见 [LICENSE](LICENSE)
