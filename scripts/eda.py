# authors: Andres Pitta, Braden Tam, Serhiy Pokrovskyy
# date: 2020-01-24

'''This script will generate exploratory data analysis visualizations. It takes as arguments the file were the root 
file is, the path where the visualizations will be saved.

Usage: eda.py [--DATA_FILE_PATH=<DATA_FILE_PATH>] [--EDA_FILE_PATH=<EDA_FILE_PATH>]

Options:
--DATA_FILE_PATH=<DATA_FILE_PATH>  Path (including filename) to gather the csv file. [default: data/vehicles_train.csv]
--EDA_FILE_PATH=<EDA_FILE_PATH>  Path to output EDA files. [default: results/figures/  ]
'''

from docopt import docopt
import pandas as pd
import altair as alt
import plotly.graph_objects as go
from selenium import webdriver
browser = webdriver.Chrome('C:\webdrivers\chromedriver.exe')


opt = docopt(__doc__)

def main(data_file_path, eda_file_path):
    data = pd.read_csv(data_file_path)

    make_correlation(data, eda_file_path)
    make_map_count(data, eda_file_path)
    make_map_price(data, eda_file_path)
    make_bars(data, eda_file_path)

def make_correlation(data, eda_file_path):
    """
    Creates a pearson's correlation plot of the continuous variables.

    Parameters:
    data -- (dataframe) The training data
    eda_file_path -- (str) The path to specify where the plot is saved
    """
    data_corr = (data.drop(columns = ["id", "long", "lat"]) 
                 .corr()
                 .reset_index()
                 .rename(columns = {'index':'Variable 1'})
                 .melt(id_vars = ['Variable 1'],
                       value_name = 'Correlation',
                       var_name = 'Variable 2')
                )

    base = alt.Chart(data_corr).encode(
        alt.Y('Variable 1:N'),
        alt.X('Variable 2:N')
    ) 

    heatmap = base.mark_rect().encode(
        alt.Color('Correlation:Q',
                    scale=alt.Scale(scheme='viridis'))
    )

    text = base.mark_text(baseline='middle').encode(
        text=alt.Text('Correlation:Q', format='.2'),
        color=alt.condition(
            alt.datum.Correlation >= 0.95,
            alt.value('black'),
            alt.value('white')
        )
    )

    plot = (heatmap + text).properties(
        width = 400,
        height = 400,
        title = "Pearson's correlation"
    )

    plot.save(f"{eda_file_path}corrplot.png")
    print(f"corrplot.png saved to {eda_file_path}")

def make_map_count(data, eda_file_path):
    """
    Creates a chloropleth map of the number of vehicles in each state.

    Parameters:
    data -- (dataframe) The training data
    eda_file_path -- (str) The path to specify where the plot is saved
    """
    
    df = data[['price', 'state']].groupby(by = 'state').count().reset_index()

    fig = go.Figure(data=go.Choropleth(
        locations=df['state'], 
        z = df['price'].astype(float), 
        locationmode = 'USA-states', 
        colorscale = 'reds',
        colorbar_title = "Number of Cars",
    ))

    fig.update_layout(
        title_text = 'Total Amount of Market Cars per State',
        geo_scope='usa', 
    )

    fig.write_image(f"{eda_file_path}map_count.png")
    print(f"map_count.png saved to {eda_file_path}")

def make_map_price(data, eda_file_path):
    """
    Creates a chloropleth map of the average price of vehicles in each state.

    Parameters:
    data -- (dataframe) The training data
    eda_file_path -- (str) The path to specify where the plot is saved
    """

    df = data[['price', 'state']].groupby(by = 'state').mean().reset_index()

    fig = go.Figure(data=go.Choropleth(
        locations=df['state'], 
        z = df['price'].astype(float), 
        locationmode = 'USA-states', 
        colorscale = 'greens',
        colorbar_title = "Market Price (USD)",
    ))

    fig.update_layout(
        title_text = 'Average Market Price per State',
        geo_scope='usa', 
    )

    fig.write_image(f"{eda_file_path}map_price.png")
    print(f"map_price.png saved to {eda_file_path}")

def make_bars(data, eda_file_path):
    """
    Creates bar plots of average price of cars vs. all the categorical features.

    Parameters:
    data -- (dataframe) The training data
    eda_file_path -- (str) The path to specify where the plot is saved
    """

    categorical_features = ['manufacturer', 'condition', 'cylinders', 'fuel',
                        'title_status', 'transmission', 'size', 'type', 'paint_color', 'state']

    categorical_encodings = ['manufacturer', 'condition', 'cylinders', 'fuel',
                        'title_status', 'transmission', 'size', 'type', 'paint_color', 'state']


    for i in range(len(categorical_features)):
        vehicles_graph = data[['price', categorical_features[i]]].groupby(by = categorical_features[i])\
                                                                        .mean()\
                                                                        .reset_index()

        chart = alt.Chart(vehicles_graph).mark_bar().encode(
            alt.X('price:Q', title = "Price (USD)"),
            alt.Y(categorical_encodings[i], 
                                    sort = alt.EncodingSortField(field = "price", order = "descending"))
        ).properties(width=700, 
                    height=500, 
                    title = f'Mean market price by {categorical_features[i]}'
                    ).configure_axis(labelFontSize=15, 
                                    titleFontSize=18
                                    ).configure_title(fontSize=20)
        
        chart.save(f'{eda_file_path}{categorical_features[i]}.png')
        print(f"{categorical_features[i]}.png saved to {eda_file_path}")

if __name__ == "__main__":
    main(opt["--DATA_FILE_PATH"], opt["--EDA_FILE_PATH"])

