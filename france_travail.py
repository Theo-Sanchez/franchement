import pandas as pd
from matplotlib import pyplot as plt
from functools import reduce
import numpy as np

filename = 'data/age_sample.csv'
less_25 = "Moins de 25 ans"
tot = "Ensemble"

INCOHERANT_INCREASE_TRIGGER = 0.5

def clean_dataset(data: list) -> list:
    
    def is_incoherent(after, before) -> bool:
        try:
            return any((
                after / before > 1 + INCOHERANT_INCREASE_TRIGGER,
                after / before < 1 - INCOHERANT_INCREASE_TRIGGER,
                after == 0
            ))
        except ZeroDivisionError:
            return True

    return [index for index in range(0, len(data) -1) if is_incoherent(data[index+1], data[index])]


def get_date_from_range(dates: list) -> int:
    """ 
    dates : list[`YYYYTX`]
    """
    print(dates)
    if len(dates) != 4 or any(dates[0][0:4] != date[0:4] for date in dates):
        raise Exception("Dates not in the good format")
    return int(dates[0][0:4])

def clean_dates(dataframe) -> list:
    """
    check that we have 4 trimester and if not, add index of rows to be removed
    """

    dates = df['Période'].apply(lambda x: x[0:4])
    value_counts = dates.value_counts()

    values_to_keep = value_counts[value_counts >= 4].index
    
    indices_to_remove = dataframe[~dates.isin(values_to_keep)].index
    return indices_to_remove

data = pd.read_csv(filename)
df = pd.DataFrame(data)



indexes_to_delete = clean_dates(df)
for index in indexes_to_delete:
    df = df.drop(axis='index', index=index)

def medium_per_year(tri_list: list) -> int:
    return reduce(lambda a, b: a + b, tri_list) / 4

X = df['Période'].to_list() # periode
X = [get_date_from_range(X[i: i+4]) for i in range(0, len(X), 4)]

# Femme de Moins de 25 ans
Y1 = [int(y.replace("\u202f","")) for y in df[f"f_{less_25}"].to_list()]
Y1 = [medium_per_year(Y1[i: i + 4]) for i in range(0, len(Y1), 4)]

# Homme de Moins de 25 ans
Y2 = [int(y.replace("\u202f","")) for y in df[f"h_{less_25}"].to_list()]
Y2 = [medium_per_year(Y2[i: i + 4]) for i in range(0, len(Y2), 4)]

# Total Hommes
Y3 = [int(y.replace("\u202f","")) for y in df[f"h_{tot}"].to_list()]
Y3 = [medium_per_year(Y3[i: i + 4]) for i in range(0, len(Y3), 4)]

# Total Femmes
Y4 = [int(y.replace("\u202f","")) for y in df[f"f_{tot}"].to_list()]
Y4 = [medium_per_year(Y4[i: i + 4]) for i in range(0, len(Y4), 4)]


if any(clean_dataset(data) for data in [Y1, Y2, Y3, Y4]):
    # clean
    pass

# Part des moins de 25 ans parmi les femmes
YF = [Y2[i] * 100 / Y3[i] for i in range(0, len(Y3))]

# Part des moins de 25 ans parmi les hommes
YH = [Y1[i] * 100 / Y4[i] for i in range(0, len(Y3))]


X_axis = np.arange(len(X)) 
plt.bar(X_axis - 0.2, YF, 0.2, label = 'Femmes') 
plt.bar(X_axis, YH, 0.2, label = 'Hommes')

plt.xticks(X_axis, X)

plt.xlabel("Année") 
plt.ylabel("Part des inscrits de moins de 25 ans") 
plt.title("Evolution des inscrits de moins de 25 ans") 

# Show the plot 
plt.show()