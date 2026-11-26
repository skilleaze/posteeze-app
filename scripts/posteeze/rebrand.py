#!/usr/bin/env python3
"""Posteeze rebrand: run from the repo root after pulling a new upstream release.

    python3 scripts/posteeze/rebrand.py

Idempotent. Replaces user-visible Postiz names, links, logos, favicons and
purple brand colours with the Posteeze (Orbit) brand. Identifiers, package
names, env var names and HTTP headers are left alone so the code keeps working.
"""
import os, re, shutil, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
ASSETS = pathlib.Path(__file__).resolve().parent / "assets"
os.chdir(ROOT)

BRAND = "Posteeze"
SOURCE_URL = "https://github.com/skilleaze/posteeze-app"
SITE = "https://posteeze.com"
LIME, MOSS, NIGHT, PALE, PALE2, DEEP = "#C6F432", "#7BA300", "#121417", "#E4FA9C", "#F3FCD6", "#1E2A0A"

TEXT_DIRS = [
    "apps/frontend/src", "apps/frontend/public", "apps/backend/src", "apps/orchestrator/src",
    "libraries/react-shared-libraries/src", "libraries/nestjs-libraries/src", "libraries/helpers/src",
]
EXTS = (".ts", ".tsx", ".json", ".scss", ".css", ".svg", ".html", ".hbs", ".mjml")

# --- user-visible links -------------------------------------------------------
LINKS = [
    ("https://github.com/gitroomhq/postiz-app", SOURCE_URL),
    ("https://docs.postiz.com", f"{SITE}/docs"),
    ("https://postiz.com/terms", f"{SITE}/terms"),
    ("https://postiz.com/privacy", f"{SITE}/privacy"),
    ("https://platform.postiz.com", "https://app.posteeze.com"),
    ("https://postiz.com", SITE),
    ("nevo@postiz.com", "support@posteeze.com"),
    ("postiz.example.com", "app.posteeze.com"),
    ("MyPostizAgent", "MyPosteezeAgent"),
]

# --- colours: Postiz purples/pinks -> Orbit palette ----------------------------
ACCENT = ["612bd3", "5520cb", "8155dd", "612ad5", "7b3ff2", "8b5cf6", "5023b8", "8c66ff", "622aff",
          "7c3aff", "7236f1", "7950f2", "832ad5", "622ff6", "8a3ffc", "7640e0", "9333ea", "662fda",
          "5720cb", "5826c2", "713ce2", "6730d9", "7c65c1", "3900b2", "9d6eff", "fc69ff", "aa0fa4",
          "ff3ea2", "d6249f", "ec4899", "d82d7e"]
LIGHT = {"ae8afc": PALE, "b69dec": PALE, "a78bfa": PALE, "c4b5fd": PALE, "cebdf2": PALE,
         "dacbfb": PALE2, "e7ddfe": PALE2, "ebe8ff": PALE2}
DARK = {"291259": DEEP, "2d1b57": DEEP}
COLOR_MAP = {**{h: LIME for h in ACCENT}, **LIGHT, **DARK}
COLOR_RE = re.compile(r"#(" + "|".join(COLOR_MAP) + r")\b", re.I)

# "Postiz" as a whole word, not inside an identifier (MyPostizAgent) and not
# the lowercase package / header / env forms.
WORD_RE = re.compile(r"(?<![A-Za-z0-9_])Postiz(?![A-Za-z0-9_])")
GITROOM_TITLE_RE = re.compile(r"'Gitroom'")
# Lime backgrounds need dark text: fix white text in the same class string.
CLASS_RE = re.compile(r"(className=)([\"'`])(.*?)\2", re.S)


def fix_classes(src):
    def repl(m):
        cls = m.group(3)
        if ("bg-btnPrimary" in cls or f"bg-[{LIME}]" in cls) and "text-white" in cls:
            cls = cls.replace("text-white", f"text-[{NIGHT}]")
        return f"{m.group(1)}{m.group(2)}{cls}{m.group(2)}"
    return CLASS_RE.sub(repl, src)


def rewrite_text():
    changed = 0
    for d in TEXT_DIRS:
        for dp, dn, fn in os.walk(d):
            if "node_modules" in dp:
                continue
            for f in fn:
                if not f.endswith(EXTS):
                    continue
                p = pathlib.Path(dp) / f
                try:
                    s = p.read_text()
                except UnicodeDecodeError:
                    continue
                o = s
                for a, b in LINKS:
                    s = s.replace(a, b)
                s = WORD_RE.sub(BRAND, s)
                s = GITROOM_TITLE_RE.sub(f"'{BRAND}'", s)
                s = COLOR_RE.sub(lambda m: COLOR_MAP[m.group(1).lower()], s)
                if f.endswith(".tsx"):
                    s = fix_classes(s)
                if s != o:
                    p.write_text(s)
                    changed += 1
    print(f"text/colour: {changed} files")


def scss_tokens():
    p = pathlib.Path("apps/frontend/src/app/colors.scss")
    s = p.read_text()
    s = re.sub(r"--new-btn-primary:\s*#[0-9a-fA-F]{6};", f"--new-btn-primary: {LIME};", s)
    s = re.sub(r"--new-ai-btn:\s*#[0-9a-fA-F]{6};", f"--new-ai-btn: {LIME};", s)
    # buttons are lime in both themes, so their text is always dark
    s = re.sub(r"--new-btn-text:\s*#[0-9a-fA-F]{6};", f"--new-btn-text: {NIGHT};", s)
    s = s.replace("--new-bgColor: #0e0e0e;", f"--new-bgColor: {NIGHT};")
    p.write_text(s)
    print("colors.scss tokens set")


def assets():
    pub = pathlib.Path("apps/frontend/public")
    icon = (ASSETS / "icon.svg").read_text()
    for name in ["postiz.svg", "logo.svg"]:
        (pub / name).write_text(icon)
    for name in ["postiz-text.svg", "logo-text.svg"]:
        shutil.copy(ASSETS / "logo-text-dark.svg", pub / name)
    shutil.copy(ASSETS / "favicon.ico", pub / "favicon.ico")
    shutil.copy(ASSETS / "icon-512.png", pub / "favicon.png")
    shutil.copy(ASSETS / "icon-512.png", pub / "postiz-fav.png")
    shutil.copy(ASSETS / "icon-180.png", pub / "apple-touch-icon.png")
    print("logo files replaced")


RING = ('<path d="M46 18 A20 20 0 1 0 52 32" fill="none" stroke="{c}" strokeWidth="7" strokeLinecap="round" />'
        '<circle cx="50" cy="20" r="5" fill="{c}" /><circle cx="32" cy="32" r="5" fill="{c}" />')


def components():
    ring = RING.format(c=LIME)
    pathlib.Path("apps/frontend/src/components/new-layout/logo.tsx").write_text(f"""'use client';

export const Logo = () => {{
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="60"
      height="60"
      viewBox="0 0 64 64"
      fill="none"
      role="img"
      aria-label="{BRAND}"
      className="mt-[8px] min-w-[60px] min-h-[60px]"
    >
      <rect width="64" height="64" rx="16" fill="{NIGHT}" />
      {ring}
    </svg>
  );
}};
""")
    W, H, s, wm_y, xmin = map(float, (ASSETS / "dims.txt").read_text().split())
    path = (ASSETS / "wordmark_path.txt").read_text()
    pathlib.Path("apps/frontend/src/components/ui/logo-text.component.tsx").write_text(f"""import React from 'react';

export const LogoTextComponent = () => {{
  return (
    <svg
      width="{W:.0f}"
      height="{H:.0f}"
      viewBox="0 0 {W:.2f} {H:.0f}"
      fill="none"
      role="img"
      aria-label="{BRAND}"
      xmlns="http://www.w3.org/2000/svg"
    >
      <g transform="scale(0.625)">
        {ring}
      </g>
      <path
        transform="translate({50 - xmin * s:.3f} {wm_y:.3f}) scale({s:.6f})"
        d="{path}"
        fill="currentColor"
      />
    </svg>
  );
}};
""")
    print("logo components rewritten")


def auth_layout():
    p = pathlib.Path("apps/frontend/src/app/(app)/auth/layout.tsx")
    s = p.read_text()
    s = re.sub(
        r'<div className="text-\[36px\] flex-1 pt-\[88px\].*?<TestimonialComponent />\s*</div>',
        f'''<div className="flex-1 hidden lg:flex flex-col items-center justify-center rounded-[12px] bg-[#1A1D21] px-[48px]">
          <div className="max-w-[520px] flex flex-col gap-[20px]">
            <div className="text-[44px] leading-[1.1] font-[800]">
              Your socials, on <span className="text-[{LIME}]">autopilot</span>.
            </div>
            <div className="text-[18px] text-[#B8BCC4] leading-[1.5]">
              Plan, write and schedule posts for every channel from one calendar. {BRAND} publishes them on time.
            </div>
          </div>
        </div>''',
        s, flags=re.S)
    s = s.replace("import { TestimonialComponent } from '@gitroom/frontend/components/auth/testimonial.component';\n", "")
    if SOURCE_URL + '" target' not in s:
        s = s.replace(
            "<div className=\"flex\">{children}</div>",
            "<div className=\"flex\">{children}</div>\n"
            f"            <a href=\"{SOURCE_URL}\" target=\"_blank\" rel=\"noreferrer\" className=\"text-[12px] text-[#8A8F98] hover:text-white mt-auto\">Source code</a>")
    s = s.replace("bg-[#0E0E0E]", f"bg-[{NIGHT}]")
    p.write_text(s)
    print("auth layout rebranded")


def extra_ui():
    """Hide upstream-only ecosystem pieces (Postiz CLI, Chrome extension, n8n
    package link) and name MCP servers 'posteeze' in copy-paste snippets."""
    p = pathlib.Path("apps/frontend/src/components/public-api/public.component.tsx")
    s = p.read_text()
    for a, b in [("add postiz", "add posteeze"), ("login postiz", "login posteeze"),
                 ("--name postiz", "--name posteeze"), ("mcp_servers.postiz", "mcp_servers.posteeze"),
                 ("http postiz ", "http posteeze "),
                 ("\\n  postiz:\\n", "\\n  posteeze:\\n"),
                 ("https://www.npmjs.com/package/n8n-nodes-postiz", f"{SITE}/docs/n8n")]:
        s = s.replace(a, b)
    s = re.sub(r"(?<=[{\s])postiz(?=: \{)", "posteeze", s)
    s = s.replace("<CliSection apiKey={user.publicApi} />", "{null /* Posteeze: upstream CLI hidden */}")
    s = re.sub(r"'Install the Posteeze CLI.*?environment variable before using the CLI\.'",
               "'Ask me for my Posteeze API key, then use the Posteeze public API at /public/v1 with it in the Authorization header.'", s, flags=re.S)
    p.write_text(s)
    s = s.replace("const officialConnectors = billingEnabled || isSelfHosted;", "const officialConnectors = false;")
    p.write_text(s)
    p = pathlib.Path("apps/frontend/src/components/onboarding/onboarding.modal.tsx")
    s = p.read_text()
    s = s.replace("const officialConnectors = billingEnabled || isSelfHosted;", "const officialConnectors = false;")
    s = s.replace("                {cliSection}\n", "                {null /* Posteeze: upstream CLI hidden */}\n")
    p.write_text(s)
    p = pathlib.Path("apps/frontend/src/components/new-layout/layout.component.tsx")
    s = p.read_text()
    s = s.replace("<ChromeExtensionComponent />", "{null /* Posteeze: no browser extension */}")
    p.write_text(s)
    print("ecosystem UI hidden")


if __name__ == "__main__":
    rewrite_text()
    scss_tokens()
    assets()
    components()
    auth_layout()
    extra_ui()
    left = os.popen("grep -rIl 'Postiz' apps/frontend/src libraries/react-shared-libraries/src --include=*.tsx --include=*.json | head").read()
    print("files still containing 'Postiz':", left or "none")
