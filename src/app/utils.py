import matplotlib.pyplot as plt
import seaborn as sn
from sklearn import cluster

def make_scatter(data, cluster=False, size=False):

    config = {
        "data":data, 
        "x":"txGenFeminino", 
        "y":"txCorRacaPreta",
        "size":'totalCandidatos',
        "sizes":(5,300),
        "hue":'clusterBr',
        "palette":'viridis',
        "alpha":0.6,
    }

    # tira o cluster caso não exista
    if(not cluster):
        del config["hue"]
        del config["palette"]

    if(not size):
        del config["size"]
        del config["sizes"]

    fig = plt.figure(dpi=150)
    
    # passa config como kwargs
    sn.scatterplot(**config)
        
    # adicionando anotações com o nome dos partidos
    for i in data['SG_PARTIDO']:
        # cordenadas
        data_tmp = data[data['SG_PARTIDO']==i]
        x = float(data_tmp['txGenFeminino'].iloc[0])
        y = float(data_tmp['txCorRacaPreta'].iloc[0])
        plt.annotate(i, (x, y), ha="right", va="bottom")

    plt.grid(True)
    
    # superior title
    plt.suptitle("Cor vs Genero - Eleições 2024")

    # title
    if(size):
        plt.title("Maior a bolha, maior a quantidade de candidaturas", fontdict={"size": 9})

    plt.xlabel("Taxa de mulheres")
    plt.ylabel("Taxa de pessoas pretas")

    txCorRacaPreta = data['totalCorRacaPreta'].sum() / data['totalCandidatos'].sum()
    txGenFeminino = data['totalGenFeminino'].sum() / data['totalCandidatos'].sum()

    # desenho das linhas (média de pessoas pretas)
    plt.hlines(y=txCorRacaPreta, xmin = data['txGenFeminino'].min(), xmax=data['txGenFeminino'].max(), colors='black', alpha=0.6, linestyles="--", label="Taxa Pretos")
    plt.vlines(x=txGenFeminino, ymin = data['txCorRacaPreta'].min(), ymax=data['txCorRacaPreta'].max(), colors='tomato', alpha=0.6, linestyles="--", label="Taxa Mulheres")

    # legenda do gráfico
    handles, labels = plt.gca().get_legend_handles_labels()
    handles = handles[-2:]
    labels = labels[-2:]

    plt.legend(handles=handles, labels=labels, loc='lower right')
    plt.show()

    return fig


def make_clusters(data, n=6):
    model = cluster.KMeans(n_clusters=n, random_state=42)
    model.fit(data[['txGenFeminino', 'txCorRacaPreta']])
    data["clusterBr"] = model.labels_
    return data

