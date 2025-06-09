import pandas as pd

# Читаем CSV в DataFrame
df = pd.read_csv('123.csv')

# Получаем строку с id=2 в виде словаря
row = df[df['id'] == 3].iloc[0].to_dict()
print(row)

