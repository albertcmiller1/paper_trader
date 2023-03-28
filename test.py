from datetime import datetime as dt
from matplotlib import pyplot as plt, dates as mdates
import pandas as pd 


plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

dates = ["01/02/2020", "01/03/2020", "01/04/2020"]
x_values = [dt.strptime(d, "%m/%d/%Y").date() for d in dates]
y_values = [1, 2, 3]


df = pd.DataFrame({'dates': x_values, "y_vals": y_values})

print(df.head())

ax = plt.gca()

formatter = mdates.DateFormatter("%Y-%m-%d")
ax.xaxis.set_major_formatter(formatter)
locator = mdates.DayLocator()
ax.xaxis.set_major_locator(locator)
plt.plot(df['dates'], df['y_vals'])
# plt.plot(x_values, y_values)

plt.show()