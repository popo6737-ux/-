import pandas as pd, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
for f in fm.findSystemFonts():
    if 'NanumGothic.ttf' in f or 'NanumGothic-Regular' in f: fm.fontManager.addfont(f)
plt.rcParams.update({'font.family':'NanumGothic','axes.unicode_minus':False,'font.size':10})
BLUE, INK, MUTED, GRID = '#2a78d6', '#0b0b0b', '#52514e', '#e6e5e1'
df = pd.read_csv('survey_clean.csv')
order = ['1비기너','2중급','3고수','4티칭','5투어']
labels = ['비기너\n(100타 이상)','중급자\n(보기 플레이어, 90대)','고수\n(싱글, 70~80대)','티칭 프로\n(USGTF 등)','투어 프로\n(KPGA/KLPGA 등)']
n = df.lv.value_counts().reindex(order)

def style(ax):
    for s in ('top','right'): ax.spines[s].set_visible(False)
    for s in ('left','bottom'): ax.spines[s].set_color(MUTED)
    ax.tick_params(colors=MUTED, labelcolor=INK)
    ax.yaxis.grid(True, color=GRID, lw=0.8); ax.set_axisbelow(True)

# Figure 1: distribution (bar, counts + %)
fig, ax = plt.subplots(figsize=(7.2, 3.6), dpi=200)
bars = ax.bar(range(5), n.values, width=0.55, color=BLUE)
for i, v in enumerate(n.values):
    ax.text(i, v + 0.8, f'{v}명 ({v/len(df)*100:.0f}%)', ha='center', va='bottom', color=INK, fontsize=9)
ax.set_xticks(range(5), [f'{l}' for l in labels], fontsize=8.5)
ax.set_ylabel('응답자 수(명)', color=MUTED); ax.set_ylim(0, 42)
style(ax); fig.tight_layout(); fig.savefig('fig1.png'); plt.close(fig)

def line(var, fname, ylabel):
    m = df.groupby('lv')[var].mean().reindex(order)
    fig, ax = plt.subplots(figsize=(7.2, 3.6), dpi=200)
    ax.plot(range(5), m.values, color=BLUE, lw=2, marker='o', ms=7, mec='white', mew=1.5)
    for i, v in enumerate(m.values):
        ax.text(i, v + 0.12, f'{v:.2f}', ha='center', va='bottom', color=INK, fontsize=9)
    ax.set_xticks(range(5), [f'{l}\nn={c}' for l, c in zip(labels, n.values)], fontsize=8.5)
    ax.set_ylim(1, 5); ax.set_yticks([1,2,3,4,5]); ax.set_ylabel(ylabel, color=MUTED)
    style(ax); fig.tight_layout(); fig.savefig(fname); plt.close(fig)
    return m.round(2).tolist()

print(line('ww','fig2.png','무위 지수 평균 (1–5점)'))
print(line('em','fig3.png','허정 지수 평균 (1–5점)'))
print(line('flow','fig4.png','플로우 지수 평균 (1–5점)'))
