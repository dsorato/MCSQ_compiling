import matplotlib.pyplot as plt
import pandas as pd
import os
import sys
import numpy as np




def plot_stats_per_language(df):

	CB_color_cycle = ['#377eb8', '#ff7f00', '#4daf4a','#f781bf', '#a65628', '#984ea3','#999999', '#e41a1c', '#dede00']

	print(df)
	x_labels = ['POR','SPA','ENG','GER','RUS','NOR','CAT','CZE','FRE']
	ax = df.plot.bar(color=CB_color_cycle)
	ax.legend(loc='upper left',ncol=3, borderpad=0.3, labelspacing=0.3, frameon=False, bbox_to_anchor=(0, 1.15))
	ax.set_xticklabels(x_labels)
	# plt.xlabel('Number of sentences')
	# plt.ylabel('Number of sentences', fontsize=12)

	plt.show()





def main(filename):
	df = pd.read_csv(filename, delimiter='\t')
	plot_stats_per_language(df)


if __name__ == "__main__":
	filename = str(sys.argv[1])
	main(filename)