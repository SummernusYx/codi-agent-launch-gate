#!/usr/bin/env python3
import argparse
import html
import os
import re
import subprocess
import sys
import webbrowser
from datetime import datetime
from pathlib import Path
from urllib.parse import quote


def run_git(args):
    result = subprocess.run(
        ["git", *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return result.stdout.strip(), result.stderr.strip(), result.returncode


def esc(value):
    return html.escape(value or "")


def file_uri(path):
    return path.resolve().as_uri()


def linkify_inline(text, root_path):
    text = esc(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)

    def image_repl(match):
        alt = esc(match.group(1))
        src = html.unescape(match.group(2))
        if re.match(r"^https?://", src):
            image_src = src
        else:
            image_src = file_uri(root_path / src)
        return f'<img alt="{alt}" src="{image_src}" />'

    def link_repl(match):
        label = esc(match.group(1))
        href = html.unescape(match.group(2))
        if href.startswith("#") or re.match(r"^https?://", href):
            target = href
        else:
            target = quote(href, safe="/#:.")
        return f'<a href="{target}">{label}</a>'

    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", image_repl, text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link_repl, text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    return text


def render_table(lines, root_path):
    rows = []
    for line in lines:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if all(re.match(r"^:?-{3,}:?$", cell) for cell in cells):
            continue
        rows.append(cells)
    if not rows:
        return ""
    head = rows[0]
    body = rows[1:]
    out = ["<table><thead><tr>"]
    out.extend(f"<th>{linkify_inline(cell, root_path)}</th>" for cell in head)
    out.append("</tr></thead><tbody>")
    for row in body:
        out.append("<tr>")
        out.extend(f"<td>{linkify_inline(cell, root_path)}</td>" for cell in row)
        out.append("</tr>")
    out.append("</tbody></table>")
    return "".join(out)


def render_markdown(markdown_text, root_path):
    lines = markdown_text.splitlines()
    html_parts = []
    paragraph = []
    list_items = []
    table_lines = []
    code_lines = []
    in_code = False
    code_lang = ""

    def flush_paragraph():
        nonlocal paragraph
        if paragraph:
            html_parts.append(f"<p>{linkify_inline(' '.join(paragraph), root_path)}</p>")
            paragraph = []

    def flush_list():
        nonlocal list_items
        if list_items:
            html_parts.append("<ul>")
            html_parts.extend(f"<li>{linkify_inline(item, root_path)}</li>" for item in list_items)
            html_parts.append("</ul>")
            list_items = []

    def flush_table():
        nonlocal table_lines
        if table_lines:
            html_parts.append(render_table(table_lines, root_path))
            table_lines = []

    for raw_line in lines:
        line = raw_line.rstrip()
        fence = re.match(r"^```(\w+)?", line)
        if fence:
            flush_paragraph()
            flush_list()
            flush_table()
            if in_code:
                code = esc("\n".join(code_lines))
                lang_class = f' class="language-{esc(code_lang)}"' if code_lang else ""
                html_parts.append(f"<pre><code{lang_class}>{code}</code></pre>")
                code_lines = []
                code_lang = ""
                in_code = False
            else:
                code_lang = fence.group(1) or ""
                in_code = True
            continue

        if in_code:
            code_lines.append(raw_line)
            continue

        if not line.strip():
            flush_paragraph()
            flush_list()
            flush_table()
            continue

        if line.startswith("|") and line.endswith("|"):
            flush_paragraph()
            flush_list()
            table_lines.append(line)
            continue

        flush_table()

        heading = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading:
            flush_paragraph()
            flush_list()
            level = len(heading.group(1))
            title = linkify_inline(heading.group(2), root_path)
            html_parts.append(f"<h{level}>{title}</h{level}>")
            continue

        if line.startswith("> "):
            flush_paragraph()
            flush_list()
            html_parts.append(f"<blockquote><p>{linkify_inline(line[2:], root_path)}</p></blockquote>")
            continue

        item = re.match(r"^-\s+(.+)$", line)
        if item:
            flush_paragraph()
            list_items.append(item.group(1))
            continue

        paragraph.append(line.strip())

    flush_paragraph()
    flush_list()
    flush_table()
    if in_code:
        html_parts.append(f"<pre><code>{esc(chr(10).join(code_lines))}</code></pre>")
    return "\n".join(html_parts)


def render_section(title, body, empty="No data."):
    content = esc(body) if body else empty
    return f"""
    <section>
      <h2>{esc(title)}</h2>
      <pre>{content}</pre>
    </section>
    """


def build_file_tree(root_path):
    ignored_dirs = {".git", "__pycache__", ".pytest_cache", "node_modules"}
    lines = []
    for path in sorted(root_path.rglob("*")):
        rel = path.relative_to(root_path)
        parts = rel.parts
        if any(part in ignored_dirs for part in parts):
            continue
        if len(parts) > 3:
            continue
        indent = "  " * (len(parts) - 1)
        suffix = "/" if path.is_dir() else ""
        lines.append(f"{indent}{parts[-1]}{suffix}")
    return "\n".join(lines[:120])


def write_diff_preview(preview_dir, root_path, branch, now, status, staged_stat, staged_names, staged_diff, recent_commits):
    preview_path = preview_dir / "diff.html"
    html_doc = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Diff Preview - {esc(branch)}</title>
  <style>
    body {{ margin: 0; background: #f6f8fa; color: #24292f; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", Arial, sans-serif; line-height: 1.5; }}
    main {{ max-width: 1180px; margin: 0 auto; padding: 32px 24px 64px; }}
    header, section {{ background: #fff; border: 1px solid #d0d7de; border-radius: 8px; padding: 20px; }}
    header {{ margin-bottom: 18px; }}
    h1 {{ margin: 0 0 8px; font-size: 28px; }}
    h2 {{ margin: 0 0 12px; font-size: 18px; }}
    .grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; }}
    .full {{ grid-column: 1 / -1; }}
    .meta {{ color: #57606a; }}
    pre {{ margin: 0; white-space: pre-wrap; word-break: break-word; font: 13px/1.45 ui-monospace, SFMono-Regular, Consolas, monospace; }}
    a {{ color: #0969da; }}
  </style>
</head>
<body>
  <main>
    <header>
      <h1>提交差异预览</h1>
      <div class="meta">Repo: {esc(root_path.name)} · Branch: {esc(branch or "(detached)")} · Generated: {esc(now)}</div>
      <p><a href="index.html">返回 GitHub 项目页预览</a></p>
    </header>
    <div class="grid">
      {render_section("Staged Files", staged_names)}
      {render_section("Staged Stat", staged_stat)}
      {render_section("Working Tree Status", status)}
      {render_section("Recent Commits", recent_commits)}
      <section class="full">
        <h2>Staged Diff</h2>
        <pre>{esc(staged_diff[:100000])}{'\\n\\n[Diff truncated for preview.]' if len(staged_diff) > 100000 else ''}</pre>
      </section>
    </div>
  </main>
</body>
</html>
"""
    preview_path.write_text(html_doc, encoding="utf-8")
    return preview_path


def write_release_preview(preview_dir, root_path, branch, now, status, staged_stat, recent_commits):
    readme_path = root_path / "README.md"
    readme = readme_path.read_text(encoding="utf-8", errors="replace") if readme_path.exists() else "# Missing README.md"
    readme_html = render_markdown(readme, root_path)
    tree = build_file_tree(root_path)
    preview_path = preview_dir / "index.html"
    html_doc = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>GitHub Release Preview - {esc(root_path.name)}</title>
  <style>
    body {{ margin: 0; background: #f6f8fa; color: #24292f; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", Arial, sans-serif; line-height: 1.5; }}
    a {{ color: #0969da; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .topbar {{ background: #24292f; color: #fff; padding: 14px 24px; }}
    .topbar strong {{ font-weight: 600; }}
    main {{ max-width: 1220px; margin: 0 auto; padding: 24px; }}
    .repo-head {{ display: flex; justify-content: space-between; gap: 16px; align-items: flex-end; margin-bottom: 16px; }}
    .repo-title {{ margin: 0; font-size: 24px; font-weight: 600; }}
    .repo-title span {{ color: #57606a; font-weight: 400; }}
    .meta {{ color: #57606a; font-size: 14px; }}
    .tabs {{ display: flex; gap: 18px; border-bottom: 1px solid #d0d7de; margin-bottom: 20px; }}
    .tab {{ padding: 10px 0 12px; color: #24292f; font-size: 14px; }}
    .tab.active {{ border-bottom: 2px solid #fd8c73; font-weight: 600; }}
    .layout {{ display: grid; grid-template-columns: minmax(0, 1fr) 300px; gap: 24px; align-items: start; }}
    .panel {{ background: #fff; border: 1px solid #d0d7de; border-radius: 6px; overflow: hidden; }}
    .panel-title {{ padding: 12px 16px; border-bottom: 1px solid #d0d7de; background: #f6f8fa; font-weight: 600; }}
    .panel-body {{ padding: 16px; }}
    .notice {{ border: 1px solid #bf8700; background: #fff8c5; border-radius: 6px; padding: 12px 14px; margin-bottom: 16px; color: #3b2300; }}
    .markdown-body {{ padding: 24px 32px; }}
    .markdown-body h1 {{ padding-bottom: .3em; border-bottom: 1px solid #d8dee4; font-size: 2em; }}
    .markdown-body h2 {{ margin-top: 24px; padding-bottom: .3em; border-bottom: 1px solid #d8dee4; font-size: 1.5em; }}
    .markdown-body h3 {{ margin-top: 22px; font-size: 1.25em; }}
    .markdown-body p, .markdown-body ul, .markdown-body table, .markdown-body pre, .markdown-body blockquote {{ margin-top: 0; margin-bottom: 16px; }}
    .markdown-body img {{ max-width: 100%; border-radius: 6px; box-sizing: border-box; }}
    .markdown-body blockquote {{ padding: 0 1em; color: #57606a; border-left: .25em solid #d0d7de; }}
    .markdown-body table {{ display: block; width: 100%; overflow: auto; border-spacing: 0; border-collapse: collapse; }}
    .markdown-body th, .markdown-body td {{ padding: 6px 13px; border: 1px solid #d0d7de; }}
    .markdown-body tr:nth-child(2n) {{ background: #f6f8fa; }}
    .markdown-body pre {{ padding: 16px; overflow: auto; background: #f6f8fa; border-radius: 6px; }}
    .markdown-body code {{ padding: .2em .4em; background: rgba(175,184,193,.2); border-radius: 6px; font: 85% ui-monospace, SFMono-Regular, Consolas, monospace; }}
    .markdown-body pre code {{ padding: 0; background: transparent; border-radius: 0; font-size: 100%; }}
    .side pre {{ white-space: pre-wrap; word-break: break-word; font: 12px/1.45 ui-monospace, SFMono-Regular, Consolas, monospace; margin: 0; }}
    .checklist div {{ margin: 8px 0; }}
    @media (max-width: 900px) {{ .layout {{ grid-template-columns: 1fr; }} .repo-head {{ display: block; }} .markdown-body {{ padding: 18px; }} }}
  </style>
</head>
<body>
  <div class="topbar"><strong>GitHub 本地发布预览</strong> · 这个页面只在本机生成，用来模拟开源仓库首页，不会上传任何内容。</div>
  <main>
    <div class="repo-head">
      <div>
        <h1 class="repo-title"><span>{esc('SummernusYx')} /</span> {esc(root_path.name)}</h1>
        <div class="meta">Branch: {esc(branch or "(detached)")} · Generated: {esc(now)}</div>
      </div>
      <div class="meta"><a href="diff.html">查看提交差异</a></div>
    </div>
    <nav class="tabs">
      <div class="tab active">Code</div>
      <div class="tab">Issues</div>
      <div class="tab">Pull requests</div>
      <div class="tab">Actions</div>
      <div class="tab">Security</div>
    </nav>
    <div class="notice">
      这才是 push 前应该看的页面：重点检查 README 首屏、配图、安装说明、示例、风险边界和中英文结构。技术 diff 放在右上角的“查看提交差异”。
    </div>
    <div class="layout">
      <article class="panel">
        <div class="panel-title">README.md</div>
        <div class="markdown-body">{readme_html}</div>
      </article>
      <aside class="side">
        <section class="panel">
          <div class="panel-title">发布检查</div>
          <div class="panel-body checklist">
            <div>✓ README 会作为 GitHub 仓库首页显示</div>
            <div>✓ 配图使用仓库相对路径</div>
            <div>✓ 中英文分篇，不混排</div>
            <div>✓ hooks 文档在 docs/ 中</div>
            <div>✓ skill 验证仍需在提交前跑一次</div>
          </div>
        </section>
        <section class="panel" style="margin-top:16px;">
          <div class="panel-title">Staged Stat</div>
          <div class="panel-body"><pre>{esc(staged_stat or "No staged changes.")}</pre></div>
        </section>
        <section class="panel" style="margin-top:16px;">
          <div class="panel-title">Working Tree</div>
          <div class="panel-body"><pre>{esc(status or "Clean working tree.")}</pre></div>
        </section>
        <section class="panel" style="margin-top:16px;">
          <div class="panel-title">Recent Commits</div>
          <div class="panel-body"><pre>{esc(recent_commits)}</pre></div>
        </section>
        <section class="panel" style="margin-top:16px;">
          <div class="panel-title">Repo Files</div>
          <div class="panel-body"><pre>{esc(tree)}</pre></div>
        </section>
      </aside>
    </div>
  </main>
</body>
</html>
"""
    preview_path.write_text(html_doc, encoding="utf-8")
    return preview_path


def ask_approval():
    prompt = "Type APPROVE to continue: "
    if sys.stdin.isatty():
        return input(prompt).strip() == "APPROVE"
    tty_path = Path("/dev/tty")
    if tty_path.exists():
        with tty_path.open("r+", encoding="utf-8", errors="replace") as tty:
            tty.write(prompt)
            tty.flush()
            return tty.readline().strip() == "APPROVE"
    if os.name == "nt":
        try:
            with open("CONOUT$", "w", encoding="utf-8", errors="replace") as out:
                out.write(prompt)
                out.flush()
            with open("CONIN$", "r", encoding="utf-8", errors="replace") as conin:
                return conin.readline().strip() == "APPROVE"
        except OSError:
            pass
    print("Interactive approval is unavailable. Re-run from an interactive terminal, or set SKIP_COMMIT_PREVIEW=1 / SKIP_RELEASE_PREVIEW=1.")
    return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--open", action="store_true")
    parser.add_argument("--require-approval", action="store_true")
    parser.add_argument("--preview", choices=["release", "diff", "both"], default="both")
    args = parser.parse_args()

    root, err, code = run_git(["rev-parse", "--show-toplevel"])
    if code != 0:
        print(err or "Not a git repository.")
        return 1

    root_path = Path(root)
    git_dir, _, _ = run_git(["rev-parse", "--git-dir"])
    preview_dir = (root_path / git_dir / "commit-preview").resolve()
    preview_dir.mkdir(parents=True, exist_ok=True)

    status, _, _ = run_git(["status", "--short"])
    staged_stat, _, _ = run_git(["diff", "--cached", "--stat"])
    staged_names, _, _ = run_git(["diff", "--cached", "--name-status"])
    staged_diff, _, _ = run_git(["diff", "--cached", "--", "."])
    recent_commits, _, _ = run_git(["log", "--oneline", "--decorate", "-12"])
    branch, _, _ = run_git(["branch", "--show-current"])
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    release_path = None
    diff_path = None
    if args.preview in {"release", "both"}:
        release_path = write_release_preview(preview_dir, root_path, branch, now, status, staged_stat, recent_commits)
        print(f"GitHub-style release preview generated: {release_path}")
    if args.preview in {"diff", "both"}:
        diff_path = write_diff_preview(preview_dir, root_path, branch, now, status, staged_stat, staged_names, staged_diff, recent_commits)
        print(f"Diff preview generated: {diff_path}")

    open_path = release_path or diff_path
    if args.open and open_path:
        try:
            if os.name == "nt":
                os.startfile(str(open_path))  # type: ignore[attr-defined]
            else:
                webbrowser.open(open_path.as_uri())
        except Exception as exc:
            print(f"Could not open preview automatically: {exc}")

    if args.require_approval:
        print("Review the generated preview in your browser.")
        if not ask_approval():
            print("Git action cancelled by preview hook.")
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
