import itertools
import os
import matplotlib.pyplot as plt
from itertools import cycle

# データフレームの列の組み合わせを作成
column_combinations = list(itertools.permutations(df.columns, 3))  # 列の組み合わせを順列で生成

# 出力先のディレクトリを作成
if not os.path.exists('./scatter_fig'):
    os.makedirs('./scatter_fig')

# 各組み合わせに対して散布図を描画し保存
for combination in column_combinations:
    x_column, y_column, color_column = combination
    unique_values = df[color_column].unique()
    color_cycle = cycle(colors)  # 色のリストをループさせるためにcycleを使用
    color_dict = {}
    for value in unique_values:
        color_dict[value] = next(color_cycle)
    plt.figure(figsize=(10, 8))
    for value, color in color_dict.items():
        subset = df[df[color_column] == value]
        plt.scatter(subset[x_column], subset[y_column], label=f'{color_column}={value}', color=color)
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title(f'Scatter plot of {x_column} vs {y_column}, colored by {color_column}')
    plt.legend(bbox_to_anchor=(1.05, 1))
    plt.tight_layout()
    plt.savefig(f'./scatter_fig/scatter_{x_column}_vs_{y_column}_by{color_column}.png')
    plt.close()
