import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Chargement et préparation des masques
file = 'Data/cleaned_data_no_na.csv'
capsoc = pd.read_csv(file)

masks = {
    "Rural": capsoc['living_place'] == 0,
    "Small Town": (capsoc['living_place'] >= 1) & (capsoc['living_place'] <= 3),
    "Mid Town": capsoc['living_place'] >= 4 & (capsoc['living_place'] <= 6),
    "Metropolis": capsoc['living_place'] >= 7
}

# Liste des variables à analyser
vars_to_plot = ['close_fam', 'close_friends', 'close_neighbors', 'close_colleagues']
labels_network = ['Family', 'Friends', 'Neighbours', 'Colleagues']
colors = ['r', 'g', 'b', 'y']
# L'index cible (Catégories de 1 à 7)
full_index = np.arange(1, 8) 

# 2. Fonction pour traiter un subset et retourner les données prêtes pour le plot
def get_plot_data(subset):
    data_list = []
    for var in vars_to_plot:
        # Calcul pondéré + Réindexation automatique de 1 à 7
        weighted_counts = subset.groupby(var)['weight'].sum().reindex(full_index, fill_value=0)
        data_list.append(weighted_counts)
    return data_list

# 3. Boucle de génération des graphiques
for title, mask in masks.items():
    subset = capsoc[mask]
    if subset.empty:
        continue
        
    # Extraction des données pondérées
    fam, fri, nei, col = get_plot_data(subset)
    
    # Configuration du graphique
    barWidth = 0.20
    fig, ax = plt.subplots(figsize=(12, 6))
    
    br1 = np.arange(len(fam))
    br2 = [x + barWidth for x in br1]
    br3 = [x + barWidth for x in br2]
    br4 = [x + barWidth for x in br3]
    
    # Création des barres
    ax.bar(br1, fam, color='r', width=barWidth, edgecolor='grey', label='Family')
    ax.bar(br2, fri, color='g', width=barWidth, edgecolor='grey', label='Friends')
    ax.bar(br3, nei, color='b', width=barWidth, edgecolor='grey', label='Neighbours')
    ax.bar(br4, col, color='y', width=barWidth, edgecolor='grey', label='Colleagues')
    
    # Mise en forme
    ax.set_xlabel(f'Close network ({title})', fontweight='bold', fontsize=12)
    ax.set_ylabel('Total Weight (Population Estimate)', fontweight='bold')
    ax.set_xticks([r + 1.5 * barWidth for r in range(len(fam))])
    ax.set_xticklabels(['None', '1', '2-5', '6-10', '11-20', '21-50', '50+'])
    
    ax.set_title(f'Social Capital Distribution: {title}', fontsize=15)
    ax.legend()
    
    plt.tight_layout()
    #plt.show()

    plt.savefig(f'outputs/histograms_close/social_capital_{title.lower().replace(" ", "_")}.png')
    