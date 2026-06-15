# 手动上传到 GitHub

这个文件夹就是**完整的仓库根目录**。上传时把**本文件夹里的所有内容**作为 GitHub 仓库根，不要多包一层。

## 步骤

### 1. 创建空仓库

1. 打开 https://github.com/new
2. 仓库名：`skillforskill`
3. **不要**勾选 "Add a README"（本文件夹已有）
4. Create repository

### 2. 上传文件

**方式 A — 网页拖拽（最简单）**

1. 进入新建的空仓库
2. 点击 **Add file → Upload files**
3. 把本文件夹 `github-upload` 里的**全部文件和文件夹**拖进去  
   （包括 `skill-core/`、`examples/`、`docs/`、`.github/` 等）
4. Commit changes

**方式 B — 打包 zip 上传**

1. 选中本文件夹内所有内容，打成 zip（不要 zip 文件夹本身）
2. GitHub 不支持直接传 zip 解压，仍需解压后按方式 A 上传  
   或使用 Git：

```bash
cd 本文件夹路径
git init
git add .
git commit -m "Initial release: Skill-Core v2.0"
git branch -M main
git remote add origin https://github.com/azhimiao/skillforskill.git
git push -u origin main
```

### 3. 发布前修改

- [x] `README.md` 用户名：`azhimiao`，仓库名：`skillforskill`
- [x] `pyproject.toml` 已更新

### 4. （可选）开启文档站

Settings → Pages → Build from branch → `main` → folder: **`/docs`**

---

## 文件夹说明

| 内容 | 说明 |
|------|------|
| `skill-core/` | CLI + 编译器 + meta skill |
| `examples/` | 3 个官方示例 skill |
| `docs/` | 文档站（index.html） |
| `registry.json` | skill 索引 |
| `skill` / `skill.cmd` | 命令行入口 |
| `README.md` | 仓库首页 |

## 用户克隆后怎么用

```bash
pip install -r requirements.txt
python skill-core/skill.py init my-skill
python skill-core/skill.py compile my-skill
python skill-core/skill.py test my-skill
```

Windows: `skill init my-skill`
