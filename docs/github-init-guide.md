# GitHub Init Guide

这份指南教你把 `E:\codex\agent-launch-gate` 复制到一个干净的新 GitHub repo `codi-agent-launch-gate`，再初始化、提交、推送。

This guide shows how to copy `E:\codex\agent-launch-gate` into a clean GitHub repo `codi-agent-launch-gate`, initialize it, commit it, and push it.

## 0. 先理解当前问题

现在这个项目放在 `E:\codex` 下面，而 `E:\codex\.gitignore` 默认忽略几乎所有文件。也就是说，`agent-launch-gate` 适合作为工作目录，但不适合直接在父仓库里发布。

Current issue: the project lives under `E:\codex`, whose parent `.gitignore` ignores almost everything. So `agent-launch-gate` is fine as a working folder, but not ideal as the publishing repo.

更稳的做法是：新建一个干净目录，把整个项目复制过去，在那个目录里重新 `git init`。

The safer path: create a clean folder, copy the project there, and run `git init` in that new folder.

## 1. 准备一个干净目录

建议放在：

Recommended location:

```powershell
E:\github\codi-agent-launch-gate
```

如果 `E:\github` 不存在，先创建：

If `E:\github` does not exist:

```powershell
New-Item -ItemType Directory -Force -Path 'E:\github'
```

## 2. 复制项目

如果目标目录已经存在，先确认里面没有重要文件。下面这条命令会创建或覆盖同名文件，但不会删除目标目录里额外存在的文件。

If the target folder already exists, make sure it does not contain important files. This command creates or overwrites matching files, but does not delete extra files already in the target.

```powershell
New-Item -ItemType Directory -Force -Path 'E:\github\codi-agent-launch-gate'
Copy-Item -Recurse -Force -LiteralPath 'E:\codex\agent-launch-gate\*' -Destination 'E:\github\codi-agent-launch-gate'
```

复制后检查：

Check the result:

```powershell
Get-ChildItem -LiteralPath 'E:\github\codi-agent-launch-gate'
```

你应该看到：

You should see:

```text
SKILL.md
README.md
README_EN.md
LICENSE
SECURITY.md
.gitignore
install.ps1
install.sh
agents
assets
docs
examples
references
```

## 3. 进入新目录

```powershell
Set-Location 'E:\github\codi-agent-launch-gate'
```

确认当前位置：

Confirm location:

```powershell
Get-Location
```

## 4. 初始化 Git

```powershell
git init
```

检查状态：

```powershell
git status --short
```

这时应该能看到 README、SKILL、references、assets、examples 等文件都作为未跟踪文件出现。

You should now see README, SKILL, references, assets, and examples as untracked files.

## 5. 本地校验 skill

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

## 6. 检查是否有不该提交的文件

```powershell
git status --short --untracked-files=all
```

再做一次敏感词搜索：

Run a basic secret keyword search:

```powershell
rg --no-ignore -n "(?i)(api[_-]?key|secret|token|password|private[_-]?key|BEGIN RSA|BEGIN OPENSSH|cookie|authorization)"
```

如果搜到真实密钥、cookie、token，不要提交。

If it finds real secrets, cookies, or tokens, do not commit.

## 7. 第一次提交

```powershell
git add .
git commit -m "Initial release of Agent Launch Gate"
```

如果 Git 提示没有设置用户名邮箱：

If Git asks for name/email:

```powershell
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"
```

然后重新提交。

Then run the commit again.

## 8. 在 GitHub 新建空仓库

在 GitHub 网页上：

On GitHub:

1. 点右上角 `+`
2. 选择 `New repository`
3. Repository name 填 `codi-agent-launch-gate`
4. Visibility 先选 `Private` 更稳，确认无误后再改 Public
5. 不要勾选 `Add a README file`
6. 不要勾选 `.gitignore`
7. 不要勾选 `LICENSE`
8. 创建仓库

为什么不要勾选这些？因为本地已经有 README、.gitignore 和 LICENSE。GitHub 再生成一份会造成首次推送冲突。

Why leave those unchecked? This repo already has README, `.gitignore`, and LICENSE. Letting GitHub generate them can create first-push conflicts.

## 9. 连接远程仓库

GitHub 创建仓库后，会给你一个地址。形如：

After creating the repo, GitHub shows a URL like:

```text
https://github.com/YOUR_NAME/codi-agent-launch-gate.git
```

在本地运行：

Run locally:

```powershell
git remote add origin https://github.com/YOUR_NAME/codi-agent-launch-gate.git
git branch -M main
git push -u origin main
```

把 `YOUR_NAME` 换成你的 GitHub 用户名或组织名。

Replace `YOUR_NAME` with your GitHub username or organization.

## 10. 推送后检查

打开 GitHub 仓库页面，检查：

Open the GitHub repo page and check:

- README 能正常显示
- `SKILL.md` 在根目录
- `references/`、`assets/`、`examples/`、`docs/` 都存在
- README 里的 example 链接能点开
- 没有提交本机私密路径、token、cookie、API key

## 11. 什么时候改成 Public

建议先保持 Private，完成这些检查后再 Public：

Keep it Private first. Make it Public after:

- README 看起来顺
- LICENSE 确认就是你想要的
- SECURITY.md 没有暴露私人联系方式
- examples 没有私人路径或项目名
- 本地跑过 `quick_validate.py`
- 至少做过一次真实项目中杯试跑

## 12. 如果你想用 GitHub CLI

如果安装并登录了 `gh`，可以不用网页创建仓库：

If `gh` is installed and logged in:

```powershell
gh repo create codi-agent-launch-gate --private --source . --remote origin --push
```

之后如果要改成公开：

To make it public later:

```powershell
gh repo edit codi-agent-launch-gate --visibility public
```

这一步会把信息发到 GitHub。执行前确认仓库里没有敏感内容。

This sends data to GitHub. Confirm there are no secrets before running it.
