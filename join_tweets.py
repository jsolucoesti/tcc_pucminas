import os
import glob
import pandas as pd
os.chdir('outputs')
# obtain all files to dir with extension .csv
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
# using pandas to concat all files
combine_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
# using pandas for export to csv
os.chdir('union')
combine_csv.to_csv('tweets_btc_2021-01-01_to_2021-12-31.csv', index=False)