import pandas as pd
import numpy as np
read = pd.read_excel("C:\\users\\jva12\\Documents\\CFB Poll\\Offense.xlsx", sheet_name=None, index_col=0)
df = pd.DataFrame(0, index=list(read.keys()), columns=read["Auburn"].index)
for team in read.keys():
    df.loc[team] = read[team].sum(axis=1)

df["Rush S%"] = df["Rush Successes"] / df["Rushes"]
df["Pass S%"] = df["Pass Successes"] / df["Passes"]
df["1st S%"] = df["1st Successes"] / df["1st Downs"]
df["2nd S%"] = df["2nd Successes"] / df["2nd Downs"]
df["3rd S%"] = df["3rd Successes"] / df["3rd Downs"]
df.loc["National Average"] = df.mean(axis=0)
df.loc["National Stdv"] = df.std(axis=0)
df["Standard Rush"] = (df["Rush S%"] - df["Rush S%"].mean()) / df["Rush S%"].std()
df["Standard Pass"] = (df["Pass S%"] - df["Pass S%"].mean()) / df["Pass S%"].std()
df["Total Offense"] = np.cbrt((df["Standard Rush"] ** 3 + df["Standard Pass"] ** 3))
print(df)
df.to_excel("C:\\users\\jva12\\Documents\\CFB Poll\\Offense-Processed.xlsx")
