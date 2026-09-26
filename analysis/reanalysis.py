"""Reproduce every statistic in the paper from analysis/survey_75.csv.
Columns: exp(구력), score(최근 1년 평균 타수), hcp(핸디캡), ww/sf/em/flow(2문항 평균 지수), lv(실력 그룹)."""
import pandas as pd, statsmodels.api as sm
from scipy import stats
from statsmodels.stats.outliers_influence import variance_inflation_factor as vif

df = pd.read_csv('survey_75.csv')

def alpha(a, b):
    x = df[[a, b]]
    return 2 * (1 - x.var(ddof=1).sum() / x.sum(axis=1).var(ddof=1))

print('Cronbach α', {k: round(alpha(*v), 3) for k, v in
      dict(무위=('ww1', 'ww2'), 유약=('sf1', 'sf2'), 허정=('em1', 'em2'), 플로우=('fl1', 'fl2')).items()})
print(df[['exp', 'score', 'hcp', 'last10', 'ww', 'sf', 'em', 'tao', 'goal', 'fl1', 'fl2']]
      .describe().T[['mean', '50%', 'std', 'min', 'max']].round(2))
print(df.lv.value_counts().sort_index())
for v in ['ww', 'sf', 'em', 'flow']:
    F, p = stats.f_oneway(*[g[v] for _, g in df.groupby('lv')])
    print('ANOVA', v, round(F, 3), round(p, 3), df.groupby('lv')[v].mean().round(2).to_dict())
for v in ['ww', 'sf', 'em']:
    for y in ['score', 'hcp']:
        r, p = stats.pearsonr(df[v], df[y]); print('r', v, y, round(r, 3), round(p, 3))
lo, hi = df[df.em < df.em.median()], df[df.em >= df.em.median()]
print('허정 집단', len(lo), round(lo.score.mean(), 2), round(lo.hcp.mean(), 2), '|', len(hi), round(hi.score.mean(), 2), round(hi.hcp.mean(), 2))
X = sm.add_constant(df[['exp', 'ww', 'sf', 'em']]); m = sm.OLS(df.hcp, X).fit()
z = df[['exp', 'ww', 'sf', 'em', 'hcp']].apply(lambda c: (c - c.mean()) / c.std())
beta = sm.OLS(z.hcp, z[['exp', 'ww', 'sf', 'em']]).fit().params
print(pd.DataFrame({'B': m.params, 'beta': beta, 'p': m.pvalues,
                    'VIF': {c: vif(X.values, i) for i, c in enumerate(X.columns) if c != 'const'}}).round(3))
print('R2', round(m.rsquared, 3), 'adjR2', round(m.rsquared_adj, 3), 'F', round(m.fvalue, 2))
