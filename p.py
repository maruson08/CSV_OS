import pandas as pd
table = [[1, 2222, 30, 500], [4, 55, 6777, 1]]
df = pd.DataFrame(table, columns = ['a', 'b', 'c', 'd'], index=['row_1', 'row_2'])
print(df)