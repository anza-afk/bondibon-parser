import pandas as pd

read_file = pd.read_csv('games.csv', delimiter=(';'))
read_file.to_excel (r'bondibon_games.xlsx', index = None, header=True)