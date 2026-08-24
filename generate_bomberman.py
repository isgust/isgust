import re
import urllib.request
import json
import os

url = "https://github.com/users/isgust/contributions"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
except Exception as e:
    with open(r'C:\Users\User\.gemini\antigravity-ide\brain\3190b259-3917-411b-8170-c739f29a93b7\.system_generated\steps\95\content.md', 'r', encoding='utf-8') as f:
        html = f.read()

# Extract total contributions
count_match = re.search(r'([0-9,]+)\s+contributions\s+in the last year', html)
total_contributions = count_match.group(1) if count_match else "253"

# Extract cells
# In github contribution graph: each week is a column or tr/td
# Let's extract all cells with data-date and data-level
cells = re.findall(r'data-date="([^"]+)"[^>]*data-level="([^"]+)"', html)
if not cells:
    cells = re.findall(r'data-level="([^"]+)"[^>]*data-date="([^"]+)"', html)
    cells = [(d, l) for l, d in cells]

print(f"Total contributions: {total_contributions}, extracted days: {len(cells)}")

# Color scheme for GitHub dark mode / shadcn
colors = {
    "0": "#161b22", # dark empty cell
    "1": "#0e4429", # level 1 green
    "2": "#006d32", # level 2
    "3": "#26a641", # level 3
    "4": "#39d353"  # level 4 bright green
}

# The grid is 53 weeks x 7 days
# Cell size: 10px, gap: 3px
cell_size = 10
gap = 3
start_x = 48
start_y = 65

# Generate SVG
rects = []
for i, (date, level) in enumerate(cells):
    week_idx = i // 7
    day_idx = i % 7
    x = start_x + week_idx * (cell_size + gap)
    y = start_y + day_idx * (cell_size + gap)
    fill = colors.get(str(level), "#161b22")
    # Add id for target block animation if active
    rects.append(f'<rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" rx="2" fill="{fill}" data-date="{date}" data-level="{level}" />')

# Let's determine where Bomberman will plant the bomb: on a recent high-level cluster around week 38 (May) or week 50 (Aug)
# Let's pick week 40, day 3: x = 48 + 40*13 = 568, y = 65 + 3*13 = 104
bomb_target_x = start_x + 40 * (cell_size + gap)
bomb_target_y = start_y + 3 * (cell_size + gap)

svg_content = f'''<svg width="100%" height="auto" viewBox="0 0 820 220" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Background Gradient -->
    <linearGradient id="grid-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#09090b" />
      <stop offset="50%" stop-color="#101014" />
      <stop offset="100%" stop-color="#09090b" />
    </linearGradient>

    <!-- Border Gradient -->
    <linearGradient id="grid-border" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#27272a" />
      <stop offset="50%" stop-color="#22c55e" stop-opacity="0.6" />
      <stop offset="100%" stop-color="#27272a" />
    </linearGradient>

    <!-- Glow for Explosion -->
    <radialGradient id="boom-glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#fef08a" stop-opacity="1" />
      <stop offset="35%" stop-color="#f59e0b" stop-opacity="0.9" />
      <stop offset="70%" stop-color="#ef4444" stop-opacity="0.7" />
      <stop offset="100%" stop-color="#ef4444" stop-opacity="0" />
    </radialGradient>

    <style><![CDATA[
      .gh-text {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
        font-size: 10px;
        fill: #71717a;
      }}
      .gh-header {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
        font-size: 13px;
        font-weight: 600;
        fill: #e4e4e7;
      }}
      .arcade-font {{
        font-family: "JetBrains Mono", monospace;
        font-size: 11px;
        font-weight: 700;
      }}

      /* ====== BOMBERMAN ANIMATION ON REAL HEATMAP ====== */

      /* Movement across the actual calendar matrix */
      @keyframes bombermanRun {{
        0% {{ transform: translate(60px, 100px); }}
        20% {{ transform: translate(280px, 75px); }}
        35% {{ transform: translate({bomb_target_x}px, {bomb_target_y}px); }} /* Places bomb */
        42% {{ transform: translate({bomb_target_x}px, {bomb_target_y}px); }} 
        55% {{ transform: translate({bomb_target_x + 90}px, 60px); }} /* Runs up/right */
        68% {{ transform: translate({bomb_target_x + 90}px, 60px) scaleX(-1); }} /* Turns to look */
        78% {{ transform: translate({bomb_target_x + 90}px, 50px) scaleX(-1); }} /* Victory Jump */
        86% {{ transform: translate({bomb_target_x + 90}px, 60px) scaleX(-1); }}
        100% {{ transform: translate(60px, 100px); }}
      }}

      /* Bomb spawn, swell and explosion */
      @keyframes bombDrop {{
        0%, 34% {{ opacity: 0; transform: translate({bomb_target_x + 5}px, {bomb_target_y + 5}px) scale(0); }}
        37% {{ opacity: 1; transform: translate({bomb_target_x + 5}px, {bomb_target_y + 5}px) scale(1); }}
        48% {{ transform: translate({bomb_target_x + 5}px, {bomb_target_y + 5}px) scale(1.15); filter: drop-shadow(0 0 6px #ef4444); }}
        58% {{ opacity: 1; transform: translate({bomb_target_x + 5}px, {bomb_target_y + 5}px) scale(1.4); }}
        60%, 100% {{ opacity: 0; transform: translate({bomb_target_x + 5}px, {bomb_target_y + 5}px) scale(0); }}
      }}

      /* Fuse Spark */
      @keyframes fuseLight {{
        0%, 36% {{ opacity: 0; }}
        37%, 59% {{ opacity: 1; fill: #facc15; }}
        60%, 100% {{ opacity: 0; }}
      }}

      /* Heatmap Crossfire Blast */
      @keyframes blastCross {{
        0%, 59% {{ opacity: 0; transform: translate({bomb_target_x + 5}px, {bomb_target_y + 5}px) scale(0); }}
        61% {{ opacity: 1; transform: translate({bomb_target_x + 5}px, {bomb_target_y + 5}px) scale(1); }}
        68% {{ opacity: 0.95; transform: translate({bomb_target_x + 5}px, {bomb_target_y + 5}px) scale(1.3); }}
        76% {{ opacity: 0; transform: translate({bomb_target_x + 5}px, {bomb_target_y + 5}px) scale(1.6); }}
        100% {{ opacity: 0; transform: translate({bomb_target_x + 5}px, {bomb_target_y + 5}px) scale(0); }}
      }}

      /* Blast illuminate surrounding real commit tiles */
      @keyframes tileGlow {{
        0%, 59% {{ opacity: 0; }}
        61% {{ opacity: 0.9; fill: #facc15; }}
        70% {{ opacity: 0.5; fill: #22c55e; }}
        80%, 100% {{ opacity: 0; }}
      }}

      .bomber-actor {{ animation: bombermanRun 6.5s ease-in-out infinite; }}
      .bomb-actor {{ animation: bombDrop 6.5s ease-in-out infinite; }}
      .spark-actor {{ animation: fuseLight 6.5s ease-in-out infinite; }}
      .blast-actor {{ animation: blastCross 6.5s cubic-bezier(0.1, 0.9, 0.2, 1) infinite; }}
      .blast-light {{ animation: tileGlow 6.5s ease-in-out infinite; }}
    ]]></style>
  </defs>

  <!-- Container Box -->
  <rect x="2" y="2" width="816" height="216" rx="14" fill="url(#grid-bg)" stroke="url(#grid-border)" stroke-width="1.5" />

  <!-- Header: Real Contributions Count + Arcade HUD -->
  <g transform="translate(24, 24)">
    <!-- Actual Count -->
    <text x="0" y="0" class="gh-header">{total_contributions} contributions in the last year</text>
    
    <!-- HUD Items -->
    <text x="560" y="0" fill="#22c55e" class="arcade-font">BOMBERMAN MODE: ACTIVE</text>
    <text x="730" y="0" fill="#f59e0b" class="arcade-font">💣 ∞</text>
  </g>

  <!-- Months Header -->
  <g transform="translate(48, 52)">
    <text x="0" y="0" class="gh-text">Aug</text>
    <text x="60" y="0" class="gh-text">Sep</text>
    <text x="120" y="0" class="gh-text">Oct</text>
    <text x="180" y="0" class="gh-text">Nov</text>
    <text x="240" y="0" class="gh-text">Dec</text>
    <text x="300" y="0" class="gh-text">Jan</text>
    <text x="360" y="0" class="gh-text">Feb</text>
    <text x="420" y="0" class="gh-text">Mar</text>
    <text x="480" y="0" class="gh-text">Apr</text>
    <text x="540" y="0" class="gh-text">May</text>
    <text x="600" y="0" class="gh-text">Jun</text>
    <text x="660" y="0" class="gh-text">Jul</text>
    <text x="720" y="0" class="gh-text">Aug</text>
  </g>

  <!-- Day Labels (Mon, Wed, Fri) -->
  <g transform="translate(18, 65)">
    <text x="0" y="20" class="gh-text">Mon</text>
    <text x="0" y="46" class="gh-text">Wed</text>
    <text x="0" y="72" class="gh-text">Fri</text>
  </g>

  <!-- Real Heatmap Tiles -->
  <g id="heatmap-cells">
    {"".join(rects)}
  </g>

  <!-- Highlight Overlay for Exploded Blocks -->
  <g class="blast-light">
    <rect x="{bomb_target_x - 13}" y="{bomb_target_y}" width="{cell_size}" height="{cell_size}" rx="2" />
    <rect x="{bomb_target_x + 13}" y="{bomb_target_y}" width="{cell_size}" height="{cell_size}" rx="2" />
    <rect x="{bomb_target_x}" y="{bomb_target_y - 13}" width="{cell_size}" height="{cell_size}" rx="2" />
    <rect x="{bomb_target_x}" y="{bomb_target_y + 13}" width="{cell_size}" height="{cell_size}" rx="2" />
    <rect x="{bomb_target_x}" y="{bomb_target_y}" width="{cell_size}" height="{cell_size}" rx="2" />
  </g>

  <!-- Bomb Actor -->
  <g class="bomb-actor">
    <circle cx="0" cy="0" r="10" fill="#09090b" stroke="#3f3f46" stroke-width="1.5" />
    <ellipse cx="-3" cy="-3" rx="2.5" ry="1.5" fill="#52525b" transform="rotate(-30 -3 -3)" />
    <rect x="-2.5" y="-12" width="5" height="2.5" rx="1" fill="#71717a" />
    <path d="M 0 -12 Q 5 -16 8 -14" fill="none" stroke="#d4d4d8" stroke-width="1.5" />
    <circle cx="8" cy="-14" r="2.5" class="spark-actor" />
  </g>

  <!-- Cross Explosion Wave -->
  <g class="blast-actor">
    <circle cx="0" cy="0" r="24" fill="url(#boom-glow)" />
    <rect x="-55" y="-7" width="110" height="14" rx="4" fill="#f59e0b" />
    <rect x="-45" y="-3.5" width="90" height="7" rx="2" fill="#fef08a" />
    <rect x="-7" y="-55" width="14" height="110" rx="4" fill="#f59e0b" />
    <rect x="-3.5" y="-45" width="7" height="90" rx="2" fill="#fef08a" />
    <polygon points="0,-22 5,-7 20,-7 8,2 12,18 0,9 -12,18 -8,2 -20,-7 -5,-7" fill="#ffffff" />
  </g>

  <!-- Bomberman Actor -->
  <g class="bomber-actor">
    <!-- Shadow -->
    <ellipse cx="0" cy="14" rx="10" ry="3.5" fill="#000000" opacity="0.5" />

    <!-- Suit & Belt -->
    <rect x="-7" y="0" width="14" height="11" rx="3" fill="#3b82f6" stroke="#1d4ed8" stroke-width="1" />
    <rect x="-7" y="6" width="14" height="2.5" fill="#18181b" />
    <rect x="-2" y="5.5" width="4" height="3.5" rx="1" fill="#ec4899" />

    <!-- Boots -->
    <ellipse cx="-4" cy="12" rx="3.5" ry="2.5" fill="#ec4899" stroke="#be185d" stroke-width="0.8" />
    <ellipse cx="4" cy="12" rx="3.5" ry="2.5" fill="#ec4899" stroke="#be185d" stroke-width="0.8" />

    <!-- Head -->
    <rect x="-10" y="-16" width="20" height="17" rx="5" fill="#ffffff" stroke="#e4e4e7" stroke-width="1" />
    <line x1="0" y1="-16" x2="0" y2="-21" stroke="#18181b" stroke-width="1.5" />
    <circle cx="0" cy="-22" r="3.2" fill="#ec4899" stroke="#be185d" stroke-width="0.8" />

    <!-- Face Visor -->
    <rect x="-6.5" y="-12.5" width="13" height="10" rx="3" fill="#fed7aa" stroke="#f97316" stroke-width="0.8" />
    <rect x="-3.5" y="-10.5" width="1.8" height="4.5" rx="0.8" fill="#18181b" />
    <rect x="1.8" y="-10.5" width="1.8" height="4.5" rx="0.8" fill="#18181b" />

    <!-- Gloves -->
    <circle cx="-9" cy="4" r="3" fill="#ec4899" stroke="#be185d" stroke-width="0.8" />
    <circle cx="9" cy="4" r="3" fill="#ec4899" stroke="#be185d" stroke-width="0.8" />
  </g>

  <!-- Legend & Bottom Footer -->
  <g transform="translate(48, 185)">
    <text x="0" y="10" class="gh-text">Learn how we count contributions</text>
    
    <g transform="translate(640, 2)">
      <text x="-30" y="8" class="gh-text">Less</text>
      <rect x="0" y="0" width="10" height="10" rx="2" fill="#161b22" />
      <rect x="14" y="0" width="10" height="10" rx="2" fill="#0e4429" />
      <rect x="28" y="0" width="10" height="10" rx="2" fill="#006d32" />
      <rect x="42" y="0" width="10" height="10" rx="2" fill="#26a641" />
      <rect x="56" y="0" width="10" height="10" rx="2" fill="#39d353" />
      <text x="74" y="8" class="gh-text">More</text>
    </g>
  </g>
</svg>
'''

output_path = r'c:\Users\User\Music\readme profissional\assets\bomberman.svg'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(svg_content)

print(f"Successfully generated {output_path} with REAL contribution graph!")
