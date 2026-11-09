#!/usr/bin/env python3
"""Generates the profile's decorative SVGs into assets/ (hero, project cards, demo cards, dividers, stack).
Usage: python3 tools/gen_assets.py   (run from the repo root). Pure stdlib, no network."""
import os, html, textwrap
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'DejaVu Sans Mono',monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
e = html.escape
THEMES = {
 "light": dict(bg="#f6f8fa", win="#ffffff", bar="#eaeef2", line="#d0d7de", fg="#1f2328", dim="#656d76", a="#0969da", b="#8250df", ok="#1a7f37", chip="#ddf4ff"),
 "dark":  dict(bg="#0d1117", win="#0d1117", bar="#161b22", line="#30363d", fg="#e6edf3", dim="#8b949e", a="#58a6ff", b="#bc8cff", ok="#3fb950", chip="#12263f"),
}
def w(name, s):
    open(os.path.join(OUT, name), "w").write(s)

def css():
    """CSS vars with automatic dark mode for standalone (img) SVGs."""
    L, D = THEMES["light"], THEMES["dark"]
    f = lambda t: ";".join(f"--{k}:{v}" for k, v in t.items())
    return f"<style>svg{{{f(L)}}}@media (prefers-color-scheme:dark){{svg{{{f(D)}}}}}</style>"

def hero(theme):
    t = THEMES[theme]; W, H = 960, 300; cw = 10.2; fs = 17
    lines = [  # (y, prompt, text, color, start s, secs)
      (112, "$ whoami", "Jerry Zhu", "name", 0.4, 1.0),
      (156, "$ cat role.txt", "CS + Pure Math @ Waterloo '27 | data, infra, ML systems", "fg", 2.2, 3.6),
      (200, "$ ./now --experiments", "a TPU, a RISC-V CPU, DOOM inside stock Qwen weights", "a", 6.6, 3.6),
      (244, "$ ask readme", "a neural net lives in this README. ask it below.", "dim", 11.2, 3.2),
    ]
    T = 17.0
    defs, body = [], []
    for i, (y, p, txt, col, s, d) in enumerate(lines):
        px = 36; pw = len(p) * cw; tx = px + pw + cw; tw = len(txt) * cw
        if i == 0: fs2 = 30; cw2 = 30 * 0.6; tw = len(txt) * cw2; y = 108
        k0, k1 = s / T, (s + d) / T
        defs.append(f'<clipPath id="c{i}"><rect x="{tx}" y="{y-40}" height="56" width="0"><animate attributeName="width" values="0;0;{tw+4:.1f};{tw+4:.1f}" keyTimes="0;{k0:.4f};{k1:.4f};1" dur="{T}s" repeatCount="indefinite"/></rect></clipPath>')
        # prompt appears instantly at start
        body.append(f'<text x="{px}" y="{y}" font-size="{fs}" fill="{t["dim"]}" textLength="{pw:.1f}"><animate attributeName="opacity" values="0;0;1;1" keyTimes="0;{max(k0-0.01,0):.4f};{k0:.4f};1" dur="{T}s" repeatCount="indefinite"/>{e(p)}</text>')
        if i == 0:
            body.append(f'<text x="{tx}" y="{y}" font-size="30" font-weight="700" fill="url(#g)" clip-path="url(#c{i})" textLength="{tw:.1f}" lengthAdjust="spacing">{e(txt)}</text>')
        else:
            body.append(f'<text x="{tx}" y="{y}" font-size="{fs}" fill="{t[col]}" clip-path="url(#c{i})" textLength="{tw:.1f}" lengthAdjust="spacing">{e(txt)}</text>')
        cur_y = y - 20 if i else y - 28; ch = 24 if i else 34
        xs = [tx, tx, tx + tw, tx + tw]
        body.append(f'<rect y="{cur_y}" width="{cw if i else 16}" height="{ch}" fill="{t["a"]}" opacity="0"><animate attributeName="x" values="{xs[0]:.1f};{xs[1]:.1f};{xs[2]+2:.1f};{xs[3]+2:.1f}" keyTimes="0;{k0:.4f};{k1:.4f};1" dur="{T}s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0;.9;0;0" keyTimes="0;{k0-0.002 if k0>0.002 else 0:.4f};{(k0+k1)/2:.4f};{k1:.4f};1" dur="{T}s" repeatCount="indefinite" calcMode="discrete"/></rect>')
    # blinking final cursor
    ly = 244; lx = 36 + len(lines[3][1]) * cw + cw + len(lines[3][2]) * cw + 2
    body.append(f'<rect x="{lx:.1f}" y="{ly-20}" width="{cw}" height="24" fill="{t["a"]}" opacity="0"><animate attributeName="opacity" values="0;0;1;0;1;0;1;0;1;0;0" keyTimes="0;{(11.2+3.2)/T:.4f};{14.5/T:.4f};{15/T:.4f};{15.4/T:.4f};{15.8/T:.4f};{16.2/T:.4f};{16.6/T:.4f};0.99;0.995;1" dur="{T}s" repeatCount="indefinite" calcMode="discrete"/></rect>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{MONO}" role="img" aria-label="Terminal animation: Jerry Zhu, CS and Pure Math at Waterloo, software engineer on data, infra and ML systems">
<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{t["a"]}"/><stop offset="1" stop-color="{t["b"]}"/></linearGradient>
<linearGradient id="sweep" x1="0" x2="1"><stop offset="0" stop-color="{t["a"]}" stop-opacity="0"/><stop offset=".5" stop-color="{t["a"]}"/><stop offset="1" stop-color="{t["b"]}" stop-opacity="0"/></linearGradient>
<pattern id="dots" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="{t["line"]}" opacity=".7"/></pattern>
{"".join(defs)}</defs>
<rect width="{W}" height="{H}" rx="14" fill="{t["bg"]}"/>
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="14" fill="url(#dots)" opacity=".55"/>
<rect x="12" y="12" width="{W-24}" height="{H-24}" rx="10" fill="{t["win"]}" stroke="{t["line"]}"/>
<path d="M12 22a10 10 0 0 1 10-10h{W-44}a10 10 0 0 1 10 10v22H12z" fill="{t["bar"]}"/>
<circle cx="34" cy="30" r="6" fill="#ff5f57"/><circle cx="56" cy="30" r="6" fill="#febc2e"/><circle cx="78" cy="30" r="6" fill="#28c840"/>
<text x="{W/2}" y="35" font-size="13" fill="{t["dim"]}" text-anchor="middle">bobliuuu: ~/profile</text>
<rect x="12" y="43" width="{W-24}" height="2" fill="url(#sweep)" opacity=".8"><animate attributeName="opacity" values=".15;.9;.15" dur="4s" repeatCount="indefinite"/></rect>
{"".join(body)}
</svg>'''

def wrap(s, n): return textwrap.wrap(s, n)

def card(name, tag, desc, href_text=None, W=440, H=158, wrapn=50):
    ls = wrap(desc, wrapn)[:4]
    txt = "".join(f'<text x="22" y="{84+i*19}" font-size="13.5" fill="var(--fg)" font-family="{SANS}">{e(l)}</text>' for i, l in enumerate(ls))
    foot = href_text or f"github.com/Bobliuuu/{name}"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{e(name)}: {e(desc)}">{css()}
<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="var(--a)"/><stop offset="1" stop-color="var(--b)"/></linearGradient>
<linearGradient id="s" x1="0" x2="1"><stop offset="0" stop-color="var(--a)" stop-opacity="0"/><stop offset=".5" stop-color="var(--a)"/><stop offset="1" stop-color="var(--b)" stop-opacity="0"/></linearGradient>
<clipPath id="r"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="12"/></clipPath></defs>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="12" fill="var(--win)" stroke="var(--line)" stroke-width="1.5"/>
<g clip-path="url(#r)"><rect x="-200" y="1" width="200" height="3" fill="url(#s)"><animateTransform attributeName="transform" type="translate" from="0 0" to="{W+200} 0" dur="5s" repeatCount="indefinite"/></rect></g>
<text x="22" y="38" font-size="18" font-weight="700" font-family="{MONO}" fill="url(#g)">{e(name)}</text>
<rect x="{W-22-len(tag)*7.4-16:.0f}" y="21" width="{len(tag)*7.4+16:.0f}" height="22" rx="11" fill="var(--chip)"/>
<text x="{W-22-len(tag)*7.4/2-8:.0f}" y="36" font-size="11.5" text-anchor="middle" fill="var(--a)" font-family="{MONO}">{e(tag)}</text>
<line x1="22" y1="54" x2="{W-22}" y2="54" stroke="var(--line)"/>
<text x="22" y="68" font-size="0"> </text>{txt}
<text x="22" y="{H-12}" font-size="11" fill="var(--dim)" font-family="{MONO}">{e(foot)}</text>
<circle cx="{W-26}" cy="{H-16}" r="4" fill="var(--ok)"><animate attributeName="opacity" values="1;.25;1" dur="2.4s" repeatCount="indefinite"/></circle>
</svg>'''

def divider(label, W=960, H=44):
    n = len(label) * 12.5 + 40
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{e(label)}">{css()}
<defs><linearGradient id="l" x1="0" x2="1"><stop offset="0" stop-color="var(--a)" stop-opacity="0"/><stop offset=".5" stop-color="var(--a)" stop-opacity=".8"/><stop offset="1" stop-color="var(--b)" stop-opacity="0"/></linearGradient></defs>
<line x1="0" y1="22" x2="{W}" y2="22" stroke="url(#l)" stroke-width="1.5"/>
<rect x="{(W-n)/2:.0f}" y="6" width="{n:.0f}" height="32" rx="16" fill="var(--win)" stroke="var(--line)"/>
<circle cx="{(W-n)/2+18:.0f}" cy="22" r="3.5" fill="var(--a)"><animate attributeName="opacity" values="1;.2;1" dur="2s" repeatCount="indefinite"/></circle>
<text x="{W/2+6}" y="27" font-size="13" letter-spacing="3.5" text-anchor="middle" fill="var(--fg)" font-family="{MONO}" font-weight="700">{e(label.upper())}</text>
</svg>'''

def stack():
    rows = [("languages", ["Python", "Rust", "Go", "C/C++", "CUDA", "TypeScript"]),
            ("infra", ["Kubernetes", "Terraform", "ArgoCD", "AWS", "GCP"]),
            ("data + ml", ["Snowflake", "dbt", "Airflow", "PyTorch"])]
    W, H = 960, 170; out = []
    for r, (lab, items) in enumerate(rows):
        y = 28 + r * 46; x = 150
        out.append(f'<text x="24" y="{y+19}" font-size="13" fill="var(--dim)" font-family="{MONO}">{lab}</text>')
        for i, it in enumerate(items):
            wd = len(it) * 8.6 + 26
            out.append(f'<g><rect x="{x:.0f}" y="{y}" width="{wd:.0f}" height="30" rx="15" fill="var(--chip)" stroke="var(--line)"/><text x="{x+wd/2:.0f}" y="{y+20}" font-size="13" text-anchor="middle" fill="var(--fg)" font-family="{MONO}">{e(it)}<animate attributeName="fill" values="var(--fg);var(--a);var(--fg)" dur="{6+r}s" begin="{i*0.6+r*0.3}s" repeatCount="indefinite"/></text></g>')
            x += wd + 10
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Stack. Languages: Python, Rust, Go, C/C++, CUDA, TypeScript. Infra: Kubernetes, Terraform, ArgoCD, AWS, GCP. Data and ML: Snowflake, dbt, Airflow, PyTorch.">{css()}
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="12" fill="var(--win)" stroke="var(--line)"/>{"".join(out)}</svg>'''

CARDS = [
 ("qwentpu", "qwen / tpu", "A TPU compiled into the weights of a stock Qwen3.5. A language model that does exact matrix multiplication."),
 ("qwen-os", "qwen / os", "A tiny OS that boots, opens a shell, and runs DOOM on a CPU living inside Qwen's weights."),
 ("qwentensor", "qwen / pytorch", "Write a PyTorch net, quantize it, run it inside Qwen3.5. The \"program\" is the prompt."),
 ("qweninqwen", "qwen / qwen", "A real Qwen3-0.6B token computed by the weights and recurrent state of another, stock Qwen."),
 ("ten-percent-challenge", "compression", "Shrinking a 7B model to ~10% of its bf16 size while keeping it useful."),
 ("kvm", "gpu / cuda", "A GPU virtual machine: one kernel runs real Doom, trains a 162M GPT and serves live inference. v2 of open-flapping-airplanes."),
 ("allgit", "rust / vcs", "Next-gen version control in Rust: one global object graph, independent zones, S3-backed remotes."),
 ("bobliu-os", "x86 / os", "From-scratch 32-bit x86 OS: preemptive multitasking, COW fork, VFS, libc, shell, Lua, DOOM."),
 ("open-flapping-airplanes", "cuda", "Reproducing the Flapping Airplanes megakernel (CUDA), in collaboration with Magni."),
 ("readme-lm", "this page", "A tiny transformer stored inside this README. Click a question and a GitHub Action runs it.", "github.com/Bobliuuu/readme-lm"),
]
DEMOS = [
 ("demo-1", "1 / real gpt-2 + qa model", "Real GPT-2 (124M, int8) and the 600K QA model, run by a GitHub Action from Markdown files. Open an issue, get an animated answer."),
 ("demo-2", "2 / pure mediawiki", "A neural net written in pure MediaWiki markup. GitHub's own renderer does the arithmetic."),
 ("demo-3", "3 / svg filters", "A neural net drawn inline as an SVG filter. Coming up."),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for th in THEMES: w(f"hero-{th}.svg", hero(th))
    for c in CARDS: w(f"card-{c[0]}.svg", card(*c))
    for i, (n, tag, d) in enumerate(DEMOS):
        w(f"{n}.svg", card(n.replace("demo-", "demo "), tag, d, "github.com/Bobliuuu/readme-lm"))
    for k, lab in dict(experiments="Experiments", interactive="Interactive", now="Now", background="Background", stack="Stack", menu="No-Action menu").items():
        w(f"hdr-{k}.svg", divider(lab))
    w("stack.svg", stack())
