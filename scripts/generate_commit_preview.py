#!/usr/bin/env python3
import argparse
import html
import os
import subprocess
import sys
import webbrowser
from datetime import datetime
from pathlib import Path


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


def render_section(title, body, empty="No data."):
    content = esc(body) if body else empty
    return f"""
    <section>
      <h2>{esc(title)}</h2>
      <pre>{content}</pre>
    </section>
    """


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--open", action="store_true")
    parser.add_argument("--require-approval", action="store_true")
    args = parser.parse_args()

    root, err, code = run_git(["rev-parse", "--show-toplevel"])
    if code != 0:
        print(err or "Not a git repository.")
        return 1

    root_path = Path(root)
    git_dir, _, _ = run_git(["rev-parse", "--git-dir"])
    preview_dir = (root_path / git_dir / "commit-preview").resolve()
    preview_dir.mkdir(parents=True, exist_ok=True)
    preview_path = preview_dir / "index.html"

    status, _, _ = run_git(["status", "--short"])
    staged_stat, _, _ = run_git(["diff", "--cached", "--stat"])
    staged_names, _, _ = run_git(["diff", "--cached", "--name-status"])
    staged_diff, _, _ = run_git(["diff", "--cached", "--", "."])
    recent_commits, _, _ = run_git(["log", "--oneline", "--decorate", "-12"])
    branch, _, _ = run_git(["branch", "--show-current"])

    if not staged_names:
        print("No staged changes. Nothing to preview.")
        return 0

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html_doc = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Commit Preview - {esc(branch)}</title>
  <style>
    :root {{
      --bg: #fbf7ef;
      --paper: #fffdf8;
      --ink: #111827;
      --muted: #64748b;
      --line: #d7d0c2;
      --green: #188038;
      --amber: #d97706;
      --red: #dc2626;
    }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font-family: Inter, "Microsoft YaHei", "Segoe UI", Arial, sans-serif;
      line-height: 1.55;
    }}
    main {{
      max-width: 1180px;
      margin: 0 auto;
      padding: 40px 24px 72px;
    }}
    header {{
      border: 2px solid var(--ink);
      border-radius: 18px;
      padding: 26px 30px;
      background: var(--paper);
      box-shadow: 8px 8px 0 rgba(17, 24, 39, .12);
    }}
    h1 {{
      margin: 0 0 10px;
      font-size: 34px;
    }}
    .meta {{
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      color: var(--muted);
      font-size: 14px;
    }}
    .pill {{
      border: 1px solid var(--line);
      border-radius: 999px;
      padding: 5px 12px;
      background: white;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 18px;
      margin-top: 22px;
    }}
    section {{
      background: var(--paper);
      border: 1px solid var(--line);
      border-radius: 14px;
      padding: 18px;
      overflow: auto;
    }}
    section.full {{
      grid-column: 1 / -1;
    }}
    h2 {{
      margin: 0 0 12px;
      font-size: 18px;
    }}
    pre {{
      margin: 0;
      white-space: pre-wrap;
      word-break: break-word;
      font-family: "Cascadia Mono", Consolas, monospace;
      font-size: 13px;
    }}
    .notice {{
      margin-top: 18px;
      padding: 14px 16px;
      border-left: 5px solid var(--amber);
      background: #fff7e6;
      border-radius: 10px;
    }}
  </style>
</head>
<body>
  <main>
    <header>
      <h1>开源提交预览</h1>
      <div class="meta">
        <span class="pill">Repo: {esc(root_path.name)}</span>
        <span class="pill">Branch: {esc(branch or "(detached)")}</span>
        <span class="pill">Generated: {esc(now)}</span>
      </div>
      <div class="notice">
        预览 staged changes。确认无误后回到终端输入 <strong>APPROVE</strong> 继续提交；输入其他内容会取消提交。
      </div>
    </header>
    <div class="grid">
      {render_section("Staged Files", staged_names)}
      {render_section("Staged Stat", staged_stat)}
      {render_section("Working Tree Status", status)}
      {render_section("Recent Commits", recent_commits)}
      <section class="full">
        <h2>Staged Diff</h2>
        <pre>{esc(staged_diff[:80000])}{'\\n\\n[Diff truncated for preview.]' if len(staged_diff) > 80000 else ''}</pre>
      </section>
    </div>
  </main>
</body>
</html>
"""
    preview_path.write_text(html_doc, encoding="utf-8")
    print(f"Commit preview generated: {preview_path}")

    if args.open:
        try:
            if os.name == "nt":
                os.startfile(str(preview_path))  # type: ignore[attr-defined]
            else:
                webbrowser.open(preview_path.as_uri())
        except Exception as exc:
            print(f"Could not open preview automatically: {exc}")

    if args.require_approval:
        if not sys.stdin.isatty():
            print("Non-interactive commit blocked. Review the preview and commit from an interactive terminal, or set SKIP_COMMIT_PREVIEW=1.")
            return 1
        answer = input("Type APPROVE to continue commit: ").strip()
        if answer != "APPROVE":
            print("Commit cancelled by preview hook.")
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
