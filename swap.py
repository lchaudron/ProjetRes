import numpy as np
import pandas as pd

url = "https://www.stlouisfed.org/-/media/project/frbstl/stlouisfed/research/fred-md/monthly/"
current_month = pd.Timestamp.now().to_period("M")
print(url + f"{current_month}.csv" )

