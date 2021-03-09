import matplotlib.pyplot as plt
import pandas as pd
import os
import sys
import numpy as np




def plot_stats_per_language(df):
	print(df)
	x_labels = ['POR','SPA','ENG','GER','RUS','NOR','CAT','CZE','FRE']

	ax = df.plot.bar()
	ax.set_xticklabels(x_labels)

	plt.show()





def main(filename):
	df = pd.read_csv(filename, delimiter='\t')
	plot_stats_per_language(df)


if __name__ == "__main__":
	filename = str(sys.argv[1])
	main(filename)