import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import random
from matplotlib.patches import Patch

def plot_france(most_represented_per_dpt):
    geojson_path = "departements.geojson"
    gdf = gpd.read_file(geojson_path)

    labels = get_labels(most_represented_per_dpt)
    colors = []
    for i in range(len(gdf)):
        if gdf['dep_code'][i][0] in most_represented_per_dpt:
            colors.append(labels[most_represented_per_dpt[gdf['dep_code'][i][0]]["metier"]])
        else:
            colors.append('lightgrey')

    gdf['color'] = colors

    fig, ax = plt.subplots(figsize=(20, 10))

    gdf.plot(ax=ax, edgecolor='black',color=gdf['color'])

    # Ajouter la légende
    legend_elements = [Patch(facecolor=color, edgecolor='black', label=metier) for metier, color in labels.items()]
    ax.legend(handles=legend_elements, title="Métiers", loc='upper left', bbox_to_anchor=(1, 1))

    plt.title('Carte des métiers les plus demandés par département')

    # Afficher la carte
    plt.show()

def get_labels(most_represented_per_dpt):
    labels = {}
    for dpt, metier in most_represented_per_dpt.items():
        if metier["metier"] not in labels:
            labels[metier['metier']] = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    
    return labels

def load_data():
    df = pd.read_excel("cleaned_file.xlsx")
    return df

def get_total_per_dpt(df):
    total_per_dpt = {}
    for index, row in df.iterrows():
        if row['Dept'] not in total_per_dpt:
            total_per_dpt[row['Dept']] = []
            total_per_dpt[row['Dept']].append({"metier": row["Nom métier BMO"], "total": row["met"]})
        else:
            if row["Nom métier BMO"] in [d["metier"] for d in total_per_dpt[row["Dept"]]]:
                for d in total_per_dpt[row["Dept"]]:
                    if d["metier"] == row["Nom métier BMO"]:
                        d["total"] += row["met"]
            else:
                total_per_dpt[row['Dept']].append({"metier": row["Nom métier BMO"], "total": row["met"]})
    return total_per_dpt

def get_most_represented_per_dpt(total_per_dpt):
    most_represented_per_dpt = {}
    for dpt, metiers in total_per_dpt.items():
        most_represented_per_dpt[dpt] = max(metiers, key=lambda x: x["total"])
    return most_represented_per_dpt

def get_top_ten_france(df):
    top_ten = []
    for index, row in df.iterrows():
        if row["Nom métier BMO"] in [d["metier"] for d in top_ten]:
            for d in top_ten:
                if d["metier"] == row["Nom métier BMO"]:
                    d["total"] += row["met"]
        else:
            top_ten.append({"metier": row["Nom métier BMO"], "total": row["met"]})
    top_ten = sorted(top_ten, key=lambda x: x["total"], reverse=True)[:10]
    return top_ten

def plot_top_ten(top_10_metiers):
    # Extraire les métiers et les totaux
    metiers = [item['metier'] for item in top_10_metiers]
    totals = [item['total'] for item in top_10_metiers]

    # Créer le graphique en barres
    plt.figure(figsize=(12, 8))
    plt.barh(metiers, totals, color='skyblue')
    plt.xlabel('Total')
    plt.ylabel('Métier')
    plt.title('Top 10 des métiers les plus recherchés en France')
    plt.gca().invert_yaxis()  # Inverser l'axe y pour avoir le plus grand en haut
    plt.tight_layout()  # Ajuster l'espacement pour que tout s'affiche correctement
    plt.show()



df = load_data()
top_ten = get_top_ten_france(df)
plot_top_ten(top_ten)
total_per_dpt = get_total_per_dpt(df)
most_represented_per_dpt = get_most_represented_per_dpt(total_per_dpt)
plot_france(most_represented_per_dpt)
