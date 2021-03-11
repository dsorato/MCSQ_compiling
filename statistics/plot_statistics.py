import matplotlib.pyplot as plt
import pandas as pd
import os
import sys
import numpy as np




def plot_stats_per_language(df):
	print(df)
	x_labels = ['POR','SPA','ENG','GER','RUS','NOR','CAT','CZE','FRE']
	ax = df.plot.bar()
	ax.legend(loc='upper left',ncol=3, borderpad=0.3, labelspacing=0.3, frameon=False, bbox_to_anchor=(0, 1.15))
	ax.set_xticklabels(x_labels)

	plt.show()





def main(filename):
	df = pd.read_csv(filename, delimiter='\t')
	plot_stats_per_language(df)


if __name__ == "__main__":
	filename = str(sys.argv[1])
	main(filename)