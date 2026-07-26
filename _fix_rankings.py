#!/usr/bin/env python3
"""Replace rank-cta blocks in all 4 ranking pages. Uses split/join — no regex."""

from pathlib import Path

RANKINGS_DIR = Path(r"C:\Users\info\agenttools-site\rankings")

NEW_CSS = """        .rank-item .rank-body {
            display: grid; grid-template-columns: 1fr 200px; gap: 16px;
        }
        .rank-cta {
            display: flex; flex-direction: column; gap: 8px; align-items: stretch;
        }
        .rank-cta a { text-align: center; }
        .btn-visit {
            display: block; padding: 8px 16px; border-radius: 8px;
            background: transparent; color: #a1a1aa; text-decoration: none; font-weight: 500;
            font-size: 0.8rem; border: 1px solid #27272a; transition: all 0.2s;
        }
        .btn-visit:hover { border-color: #a78bfa; color: #fff; }
        .prod-link { display: block; color: #71717a; font-size: 0.75rem; text-align: center; margin-top: 0px; }
"""

PAGES = {
    "best-ai-coding-agents.html": [
        ("https://claude.ai/code", "xinbbm", "Dev Agent Toolkit $19"),
        ("https://cursor.com", "xinbbm", "Dev Agent Toolkit $19"),
        ("https://github.com/openai/codex-cli", "xinbbm", "Dev Agent Toolkit $19"),
        ("https://continue.dev", "cvpkp", "AI Agent Workflow Playbook $27"),
        ("https://codeium.com/windsurf", "xinbbm", "Dev Agent Toolkit $19"),
        ("https://github.com/features/copilot", "cvpkp", "AI Agent Workflow Playbook $27"),
        ("https://www.tabnine.com", "cvpkp", "AI Agent Workflow Playbook $27"),
        ("https://sourcegraph.com/cody", "xinbbm", "Dev Agent Toolkit $19"),
    ],
    "best-ai-writing-tools.html": [
        ("https://claude.ai", "ddwnyg", "Content Creator AI Stack $15"),
        ("https://chatgpt.com", "ddwnyg", "Content Creator AI Stack $15"),
        ("https://gemini.google.com", "ddwnyg", "Content Creator AI Stack $15"),
        ("https://www.jasper.ai", "ddwnyg", "Content Creator AI Stack $15"),
        ("https://www.copy.ai", "ddwnyg", "Content Creator AI Stack $15"),
        ("https://writer.com", "cvpkp", "AI Agent Workflow Playbook $27"),
    ],
    "best-agentic-frameworks.html": [
        ("https://github.com/nousresearch/hermes-agent", "cvpkp", "AI Agent Workflow Playbook $27"),
        ("https://www.crewai.com", "cvpkp", "AI Agent Workflow Playbook $27"),
        ("https://www.langchain.com", "cvpkp", "AI Agent Workflow Playbook $27"),
        ("https://microsoft.github.io/autogen", "xinbbm", "Dev Agent Toolkit $19"),
        ("https://dify.ai", "cvpkp", "AI Agent Workflow Playbook $27"),
        ("https://github.com/geekan/metagpt", "xinbbm", "Dev Agent Toolkit $19"),
    ],
    "best-open-source-models.html": [
        ("https://chat.deepseek.com", "cvpkp", "AI Agent Workflow Playbook $27"),
        ("https://www.llama.com", "xinbbm", "Dev Agent Toolkit $19"),
        ("https://github.com/QwenLM/Qwen", "cvpkp", "AI Agent Workflow Playbook $27"),
        ("https://ai.google.dev/gemma", "cvpkp", "AI Agent Workflow Playbook $27"),
        ("https://mistral.ai", "xinbbm", "Dev Agent Toolkit $19"),
        ("https://azure.microsoft.com/products/phi", "xinbbm", "Dev Agent Toolkit $19"),
        ("https://www.lingyiwanwu.com", "cvpkp", "AI Agent Workflow Playbook $27"),
        ("https://chat.deepseek.com", "cvpkp", "AI Agent Workflow Playbook $27"),
    ],
}


def make_new_cta(site_url, prod_id, prod_label):
    return f'''                    <div class="rank-cta">
                        <a href="{site_url}" class="btn-visit" target="_blank" rel="noopener">Visit Site →</a>
                        <a href="https://wiseai.gumroad.com/l/{prod_id}" class="btn-micro">Get Config →</a>
                        <span class="prod-link">{prod_label}</span>
                    </div>'''


def inject_css(html):
    if ".btn-visit" in html:
        return html
    # Replace the @media rule with new CSS before it
    return html.replace(
        '@media (max-width: 768px) {',
        NEW_CSS + '\n        @media (max-width: 768px) {'
    )


def replace_ctas_v2(html, tools):
    """Split on rank-cta boundaries and replace each one."""
    marker = '<div class="rank-cta">'
    parts = html.split(marker)
    
    # First part is everything before the first rank-cta — keep it
    result = parts[0]
    
    for i, part in enumerate(parts[1:], 1):
        # Each 'part' starts with the content between <div class="rank-cta"> and the next marker
        # Find the closing </div> of the rank-cta div
        close_pos = part.index('</div>')
        # Everything from 0 to close_pos+6 is the old rank-cta content + closing tag
        # Everything after is the rest of the document
        rest = part[close_pos+6:]
        
        if i <= len(tools):
            site_url, prod_id, prod_label = tools[i-1]
            new_cta = make_new_cta(site_url, prod_id, prod_label)
            result += new_cta + rest
        else:
            # Shouldn't happen, but preserve original
            result += marker + part
    
    return result


def main():
    for filename, tools in PAGES.items():
        path = RANKINGS_DIR / filename
        html = path.read_text(encoding="utf-8")
        html = inject_css(html)
        html = replace_ctas_v2(html, tools)
        # Also remove old text-align:right on rank-cta
        html = html.replace(
            '.rank-item .rank-cta { text-align: right; }\n',
            ''
        )
        path.write_text(html, encoding="utf-8")
        print(f"✅ {filename} ({len(tools)} tools)")

    print("\nDone!")

if __name__ == "__main__":
    main()
