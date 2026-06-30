# GitHub Publishing Guide

这份文档是给维护者看的：如果你 fork 了这个项目，或想把自己的 Codex skill 打包成类似的开源仓库，可以按下面的流程发布。

This guide is for maintainers: use it when you fork this project or package another Codex skill as an open-source repository.

## 1. 准备一个干净仓库目录

不要直接从一个很大的工作区里发布。更稳的做法是新建一个干净目录，只放最终要开源的文件。

Do not publish directly from a broad workspace. Create a clean directory that contains only the files intended for release.

```powershell
New-Item -ItemType Directory -Force -Path '<your-clean-repo-path>'
Copy-Item -Recurse -Force -LiteralPath '<your-skill-source>\*' -Destination '<your-clean-repo-path>'
Set-Location '<your-clean-repo-path>'
```

## 2. 检查应该包含的文件

至少确认这些文件和目录存在：

Make sure these files and folders exist:

```text
SKILL.md
README.md
README_EN.md
LICENSE
SECURITY.md
.gitignore
install.ps1
install.sh
agents/
assets/
docs/
examples/
references/
```

## 3. 验证 skill

如果你的系统里有 Codex 的 `quick_validate.py`：

If your system has Codex's `quick_validate.py`:

```powershell
python -X utf8 "$env:USERPROFILE\.codex\skills\.system\skill-creator\scripts\quick_validate.py" .
```

预期结果：

Expected:

```text
Skill is valid!
```

## 4. 检查敏感内容

提交前至少做一次关键词搜索：

Run a basic secret keyword search before committing:

```powershell
rg --no-ignore -n "(?i)(api[_-]?key|secret|token|password|private[_-]?key|BEGIN RSA|BEGIN OPENSSH|cookie|authorization)"
```

如果搜到真实密钥、cookie、token、私有路径或客户数据，不要提交。

If it finds real secrets, cookies, tokens, private paths, or customer data, do not commit.

## 5. 初始化并提交

```powershell
git init
git add .
git commit -m "Initial release"
```

如果 Git 提示没有设置用户名和邮箱，可以只在当前仓库里设置：

If Git asks for name/email, set them for this repository only:

```powershell
git config user.name "YOUR_NAME"
git config user.email "YOUR_EMAIL"
```

## 6. 在 GitHub 新建空仓库

On GitHub:

1. Click `New repository`
2. Enter the repository name
3. Choose `Private` first if you want one more review pass, or `Public` if you are ready to publish
4. Do not add a README
5. Do not add `.gitignore`
6. Do not add a license
7. Create the repository

这些文件已经在本地仓库里。让 GitHub 再生成一份，容易造成首次推送冲突。

Those files already exist locally. Letting GitHub generate them can create first-push conflicts.

## 7. 连接远端并推送

GitHub 创建仓库后，会给你一个地址，形如：

After creating the repo, GitHub shows a URL like:

```text
https://github.com/YOUR_NAME/YOUR_REPO.git
```

然后运行：

Then run:

```powershell
git remote add origin https://github.com/YOUR_NAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

## 8. 推送后检查

打开 GitHub 仓库页面，检查：

Open the GitHub repo page and check:

- README 能正常显示
- README images render correctly
- `SKILL.md` is in the repository root
- `references/`, `assets/`, `examples/`, and `docs/` exist
- README links open without 404s
- Examples do not contain private paths, tokens, cookies, API keys, or customer data

## 9. 什么时候公开

建议先保持 Private，完成这些检查后再 Public：

Keep it Private first. Make it Public after:

- README 首屏看起来清楚
- LICENSE 是你想要的许可证
- SECURITY.md 没有暴露私人联系方式
- examples 没有私人路径或项目名
- 本地跑过 skill 验证
- 至少用一个真实项目试跑过核心模式

## 10. 如果你想用 GitHub CLI

如果安装并登录了 `gh`，可以不用网页创建仓库：

If `gh` is installed and logged in:

```powershell
gh repo create YOUR_REPO --private --source . --remote origin --push
```

之后如果要改成公开：

To make it public later:

```powershell
gh repo edit YOUR_REPO --visibility public
```

这一步会把信息发到 GitHub。执行前确认仓库里没有敏感内容。

This sends data to GitHub. Confirm there are no secrets before running it.
