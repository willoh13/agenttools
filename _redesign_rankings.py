#!/usr/bin/env python3
"""Redesign all 4 ranking pages with Visit Site + Get Config buttons."""

import re
from pathlib import Path

RANKINGS_DIR = Path(r"C:\Users\info\agenttools-site\rankings")

# New CSS to inject (before the @media query)
NEW_CSS = """
        /* Action buttons row */
        .rank-item .rank-body {
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
        .btn-affiliate {
            border-color: #3b2f6e; color: #a78bfa;
        }
        .btn-affiliate:hover { border-color: #7c3aed; background: #1e1b2e; }
        .prod-link { display: block; color: #71717a; font-size: 0.75rem; text-align: center; }
"""

# Tool data: (name, site_url, has_affiliate, product_id, product_label)
PAGES = {
    "best-ai-coding-agents.html": [
        ("Claude Code", "https://claude.ai/code", False, "xinbbm", "Dev Agent Toolkit $19"),
        ("Cursor", "https://cursor.com", True, "xinbbm", "Dev Agent Toolkit $19"),
        ("Codex CLI", "https://github.com/openai/codex-cli", False, "xinbbm", "Dev Agent Toolkit $19"),
        ("Continue", "https://continue.dev", True, "cvpkp", "AI Agent Workflow Playbook $27"),
        ("Windsurf", "https://codeium.com/windsurf", False, "xinbbm", "Dev Agent Toolkit $19"),
        ("GitHub Copilot", "https://github.com/features/copilot", False, "cvpkp", "AI Agent Workflow Playbook $27"),
        ("Tabnine", "https://www.tabnine.com", False, "cvpkp", "AI Agent Workflow Playbook $27"),
        ("Sourcegraph Cody", "https://sourcegraph.com/cody", False, "xinbbm", "Dev Agent Toolkit $19"),
    ],
    "best-ai-writing-tools.html": [
        ("Claude", "https://claude.ai", False, "ddwnyg", "Content Creator AI Stack $15"),
        ("ChatGPT", "https://chatgpt.com", False, "ddwnyg", "Content Creator AI Stack $15"),
        ("Gemini", "https://gemini.google.com", False, "ddwnyg", "Content Creator AI Stack $15"),
        ("Jasper", "https://www.jasper.ai", True, "ddwnyg", "Content Creator AI Stack $15"),
        ("Copy.ai", "https://www.copy.ai", True, "ddwnyg", "Content Creator AI Stack $15"),
        ("Writer", "https://writer.com", True, "cvpkp", "AI Agent Workflow Playbook $27"),
    ],
    "best-agentic-frameworks.html": [
        ("Hermes Agent", "https://github.com/nousresearch/hermes-agent", False, "cvpkp", "AI Agent Workflow Playbook $27"),
        ("CrewAI", "https://www.crewai.com", False, "cvpkp", "AI Agent Workflow Playbook $27"),
        ("LangChain", "https://www.langchain.com", False, "cvpkp", "AI Agent Workflow Playbook $27"),
        ("AutoGen", "https://microsoft.github.io/autogen", False, "xinbbm", "Dev Agent Toolkit $19"),
        ("Dify", "https://dify.ai", False, "cvpkp", "AI Agent Workflow Playbook $27"),
        ("MetaGPT", "https://github.com/geekan/metagpt", False, "xinbbm", "Dev Agent Toolkit $19"),
    ],
    "best-open-source-models.html": [
        ("DeepSeek V4 Flash", "https://chat.deepseek.com", False, "cvpkp", "AI Agent Workflow Playbook $27"),
        ("Llama 4", "https://www.llama.com", False, "xinbbm", "Dev Agent Toolkit $19"),
        ("Qwen 3.5", "https://github.com/QwenLM/Qwen", False, "cvpkp", "AI Agent Workflow Playbook $27"),
        ("Gemma 4", "https://ai.google.dev/gemma", False, "cvpkp", "AI Agent Workflow Playbook $27"),
        ("Mistral Large 3", "https://mistral.ai", False, "xinbbm", "Dev Agent Toolkit $19"),
        ("Phi-4", "https://azure.microsoft.com/products/phi", False, "xinbbm", "Dev Agent Toolkit $19"),
        ("Yi-Lightning", "https://www.lingyiwanwu.com", False, "cvpkp", "AI Agent Workflow Playbook $27"),
        ("DeepSeek R1", "https://chat.deepseek.com", False, "cvpkp", "AI Agent Workflow Playbook $27"),
    ],
}

# Affiliate disclosure footer
AFFILIATE_FOOTER = """
    <div class="container" style="margin-top:-20px;margin-bottom:20px;">
        <p style="color:#52525b;font-size:0.7rem;text-align:center;border:1px solid #18181b;border-radius:8px;padding:12px;background:#0d0d10;">
            🔗 Some links on this page are affiliate links. We may earn a commission if you purchase through them — at no extra cost to you.
        </p>
    </div>
"""


def inject_css(html: str) -> str:
    """Insert new CSS rules before the @media query."""
    return html.replace(
        "@media (max-width: 768px)",
        NEW_CSS + "\n        @media (max-width: 768px)"
    )


def build_new_cta(site_url: str, has_affiliate: bool, product_id: str, product_label: str) -> str:
    btn_class = "btn-visit btn-affiliate" if has_affiliate else "btn-visit"
    # Add a small star indicator for affiliate links
    link_text = "Visit Site ★" if has_affiliate else "Visit Site →"
    return f"""                    <div class="rank-cta">
                        <a href="{site_url}" class="{btn_class}" target="_blank" rel="noopener">{link_text}</a>
                        <a href="https://wiseai.gumroad.com/l/{product_id}" class="btn-micro">Get Config →</a>
                        <span class="prod-link">{product_label}</span>
                    </div>"""


def replace_ctas(html: str, tools: list) -> str:
    """Replace each rank-item's cta div with the new two-button version."""
    # Find all rank-items and their ctas
    items = list(re.finditer(
        r'(<div class="rank-item">.*?<div class="rank-cta">)(.*?)(</div>\s*</div>\s*</div>)',
        html, re.DOTALL
    ))
    
    if len(items) != len(tools):
        print(f"  WARNING: Found {len(items)} rank items but {len(tools)} tools in data")
        # Fall back: process sequentially by position
        result = html
        for i, (name, site_url, has_aff, prod_id, prod_label) in enumerate(tools):
            # Find the i-th rank-cta
            pattern = r'(<div class="rank-cta">)(.*?)(</div>\s*</div>\s*</div>)'
            matches = list(re.finditer(pattern, result, re.DOTALL))
            if i < len(matches):
                new_cta = build_new_cta(site_url, has_aff, prod_id, prod_label)
                full_match = matches[i].group(0)
                result = result.replace(full_match, new_cta, 1)
        return result
    
    # Build replacement mapping
    result = html
    for i, (name, site_url, has_aff, prod_id, prod_label) in enumerate(tools):
        if i < len(items):
            new_cta = build_new_cta(site_url, has_aff, prod_id, prod_label)
            result = result.replace(items[i].group(0), new_cta, 1)
    
    return result


def add_affiliate_disclosure(html: str, has_affiliates: bool) -> str:
    """Add affiliate disclosure if page has affiliate links."""
    if not has_affiliates:
        return html
    # Insert before the footer
    return html.replace("<footer>", AFFILIATE_FOOTER + "\n    <footer>")


def update_rank_body_grid(html: str) -> str:
    """Remove old rank-body grid-template-columns rule, new one is in NEW_CSS."""
    # The old rule is:
    # .rank-item .rank-body {
    #     display: grid; grid-template-columns: 1fr 160px; gap: 20px;
    # }
    old_rule = """.rank-item .rank-body {
            display: grid; grid-template-columns: 1fr 160px; gap: 20px;
        }"""
    # We replace it with nothing — the new rule in NEW_CSS (200px) takes over
    return html.replace(old_rule, "")


def process_page(filename: str, tools: list, has_affiliates: bool):
    path = RANKINGS_DIR / filename
    html = path.read_text(encoding="utf-8")
    
    html = update_rank_body_grid(html)
    html = inject_css(html)
    html = replace_ctas(html, tools)
    html = add_affiliate_disclosure(html, has_affiliates)
    
    path.write_text(html, encoding="utf-8")
    print(f"  ✅ {filename} updated ({len(tools)} tools)")


def main():
    has_affiliate_pages = {"best-ai-coding-agents.html": True, "best-ai-writing-tools.html": True}
    
    for filename, tools in PAGES.items():
        has_aff = has_affiliate_pages.get(filename, False)
        process_page(filename, tools, has_aff)
    
    print("\nDone! All ranking pages updated.")


if __name__ == "__main__":
    main()
