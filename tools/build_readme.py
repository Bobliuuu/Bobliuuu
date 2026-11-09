#!/usr/bin/env python3
"""Rebuilds the top of README.md (everything before the pure-Markdown QA menu) from a template.
The QA menu and the weights block are copied through untouched. Usage: python3 tools/build_readme.py ORIG.md > README.md"""
import sys, urllib.parse as U
orig = open(sys.argv[1]).read()
tail = orig[orig.index("<!--LM-WEIGHTS-START-->"):]   # only the model's weights block stays in the README (the Action reads it)
BODY = "&body=Just+hit+Submit.+A+GitHub+Action+runs+the+model+stored+in+the+profile+README+and+replies+with+the+answer."
def ask(q): return f"[**{q}**](https://github.com/Bobliuuu/Bobliuuu/issues/new?title=ask%3A+{U.quote_plus(q)}{BODY})"
def ask_html(q): return f'<a href="https://github.com/Bobliuuu/Bobliuuu/issues/new?title=ask%3A+{U.quote_plus(q)}{BODY.replace("&","&amp;")}"><b><code>ask:</code> {q}</b></a>'
def rl(tpl, pre, text): return f"https://github.com/Bobliuuu/readme-lm/issues/new?template={tpl}.md&title={pre}%3A+{U.quote_plus(text)}"
cards = [("qwentpu",), ("qwen-os",), ("qwentensor",), ("qweninqwen",), ("ten-percent-challenge",), ("kvm",), ("allgit",), ("bobliu-os",), ("open-flapping-airplanes",), ("readme-lm",)]
rows = []
for i in range(0, len(cards), 2):
    tds = "".join(f'<td width="50%"><a href="https://github.com/Bobliuuu/{n}"><img src="assets/card-{n}.svg" alt="{n}" width="100%"></a></td>' for (n,) in cards[i:i+2])
    rows.append(f"<tr>{tds}</tr>")
cards_html = "<table>\n" + "\n".join(rows) + "\n</table>"
head = f'''<div align="center">

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/hero-dark.svg"><img src="assets/hero-light.svg" alt="Terminal animation: Jerry Zhu, CS and Pure Math at Waterloo, data infrastructure at Shopify, inference and kernel engineering" width="100%"></picture>

**CS + Pure Math @ University of Waterloo ('27** · Varsity Ultimate (Open B) · Data infrastructure @ Shopify · inference and kernel engineering

[Website](https://jerryzhu.org) · [LinkedIn](https://www.linkedin.com/in/jerryzhu2/) · [Resume](https://jerryzhu.org/ZhuJerryResume.pdf)

</div>

<img src="assets/hdr-now.svg" alt="Now" width="100%">

- **Data Infrastructure @ Shopify**
- **Inference and kernel engineering**: persistent GPU kernels, speculative decoding, KV-cache compression, and the 10% Challenge (a capable LLM in a tenth of its fp16 size)
- **Embedded compute inside LLMs**: a TPU, a RISC-V CPU and DOOM running inside stock Qwen3.5 weights, no training
- **UTMIST** (sparse attention research) · **WAT.ai** (PianoFi) · **CSC** (sysadmin)

<img src="assets/hdr-experiments.svg" alt="Experiments" width="100%">

<div align="center">

{cards_html}

</div>

<img src="assets/hdr-interactive.svg" alt="Interactive" width="100%">

<div align="center">
<img src="assets/readme-lm.svg?v=337291d3" alt="Terminal animation of a tiny transformer answering a question about Jerry's GitHub" width="640">
</div>

**README-LM: neural networks you can talk to from a README.** Three demos. Open an issue and a GitHub Action runs the network and replies. The profile bot's weights are in this very file, in the collapsed block at the bottom.

<table>
<tr>
<td width="33%" valign="top"><img src="assets/demo-1.svg" alt="Demo 1" width="100%"><br>
<a href="https://github.com/Bobliuuu/readme-lm/issues/new?template=gpt2.md&title=gpt2%3A+The+meaning+of+life+is"><b><code>gpt2:</code> ask real GPT-2</b></a><br>
<a href="https://github.com/Bobliuuu/readme-lm/issues/new?template=qa.md&title=qa%3A+what+is+qwentpu"><b><code>qa:</code> ask the GitHub model</b></a><br>
{ask_html("what is qwentpu")}</td>
<td width="33%" valign="top"><img src="assets/demo-2.svg" alt="Demo 2" width="100%"><br>
<a href="https://github.com/Bobliuuu/readme-lm/blob/main/demos/mediawiki/README.mediawiki"><b>open the MediaWiki net</b></a><br>
<a href="{rl("mediawiki", "mediawiki", "hello")}"><b><code>mediawiki:</code> run it on your text</b></a></td>
<td width="33%" valign="top"><img src="assets/demo-3.svg" alt="Demo 3" width="100%"><br>
<b>Coming up:</b> <code>svg: &lt;text&gt;</code> issues will answer with an SVG-filter network drawn inline.</td>
</tr>
</table>

**Or ask the profile bot directly**, then hit Submit: {ask("what is qwentpu")} · {ask("which repo runs doom inside qwen")} · {ask("what is the ten percent challenge")} · {ask("what language is allgit written in")} · {ask("where does jerry study")} · {ask("what is qweninqwen")}

Or write your own: open an issue titled `ask: <your question>`. The Action loads a **600K-parameter character-level transformer** (3 layers, 4-bit weights, base64) straight out of this README, runs it in numpy, replies and updates the animation above. It only knows Jerry's public GitHub; anything else gets a polite refusal. It is tiny, so expect short answers; it is the only model that physically fits in one README (GitHub renders 500 KiB at most).

<details><summary><b>Demo 1 in motion: real GPT-2, token by token</b></summary>

<img src="assets/gpt2-generation.gif" alt="Real GPT-2 generating text token by token" width="100%">

Real GPT-2 (OpenAI's pretrained 124M weights, int8) is stored as Markdown files in [**readme-lm**](https://github.com/Bobliuuu/readme-lm). [**Click through its real predictions with no Action**](https://github.com/Bobliuuu/readme-lm/blob/main/graph/gpt2/README.md): precomputed link graphs of GPT-2's top next tokens, plus [the QA model as a click-through graph](https://github.com/Bobliuuu/readme-lm/blob/main/graph/qa/README.md). GitHub's renderer cannot compute a GPT-2 forward pass live; those pages are navigation of precomputed predictions. Details and measurements are in the repo.

</details>

<img src="assets/hdr-background.svg" alt="Background" width="100%">

- **Industry**: Shopify (data infra), StackAdapt, Super.com (data eng), Aview, OPENLANE (SRE), Aviato (founding ML), Sysconverge
- **Community**: AWS Cloud Club captain (Canada's first), Waterloo Data Science Club VP, CS Club, TEDxUW tech lead
- **Competitions**: USACO Gold · Codingame Master (top 0.5%) · Kaggle Competition Expert · Hack the North finalist · picoCTF top 5 in Canada
- **Writing**: two IEEE papers (text-to-SQL, imbalanced classification) and a [Rootly study of DeepSeek R1 on error-log classification](https://rootly.com/blog/classifying-error-logs-with-ai-can-deepseek-r1-outperform-gpt-4o-and-llama-3)

<img src="assets/hdr-stack.svg" alt="Stack" width="100%">

<img src="assets/stack.svg" alt="Stack. Languages: Python, Rust, Go, C/C++, CUDA, TypeScript. Infra: Kubernetes, Terraform, ArgoCD, AWS, GCP. Data and ML: Snowflake, dbt, Airflow, PyTorch." width="100%">

<div align="center"><sub>Off the clock: varsity ultimate frisbee 🥏 · a cappella · dance · gardening</sub></div>

'''
sys.stdout.write(head + tail)
