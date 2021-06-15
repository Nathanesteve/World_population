import pandas as pd
import folium
import base64
from folium import IFrame
import branca.colormap as cmp

# probleme taille chine inde
# probleme 0 habitant
Version = '1.1.0'
# import data
countries = pd.read_csv("data/countries.csv")
countries2 = pd.read_csv('data/population_by_country_2020.csv')


def Create_localisation(latitude, longitude, localisation, initiale, radius):
    hab = radius
    n = 1/200  # scaling coef
    if hab > 1000297825:  # China and India problem
        radius = radius/3

    encoded = base64.b64encode(open(f'data/Flags/{initiale}.PNG', 'rb').read())
    html = '<img src="data:image/PNG;base64,{}">'.format
    iframe = IFrame(html(encoded.decode("UTF-8")), width=158, height=148)
    localisaiton = folium.Popup(iframe, max_width=2650)

    if hab > 250000000:
        radius_color = 'fffff'
        marker_color = 'black'
    if 250000000 > hab > 50000000:
        radius_color = 'darkgreen'
        marker_color = 'darkgreen'
    if 50000000 > hab > 5000000:
        radius_color = 'green'
        marker_color = 'green'
    if 5000000 > hab > -1:
        radius_color = 'lightgreen'
        marker_color = 'lightgreen'

    folium.Marker(location=[latitude, longitude],
                  popup=localisaiton,
                  draggable=False,
                  icon=folium.Icon(color=marker_color,
                                   icon='ok-sign'),
                  ).add_to(m)

    folium.Circle(
        radius = radius*n,
        location=[latitude, longitude],
        popup=f'{localisation}, la population est de {hab} habitants',
        color=radius_color,
        fill=True,
    ).add_to(m)


m = folium.Map(titles='LA MAP', location=[43.59666660141285,
               3.878532192712331], zoom_start=3)

# legend
step = cmp.StepColormap(
 ['lightgreen', 'green', 'darkgreen', 'black'],
 vmin=0, vmax=260,
 index=[0, 5, 50, 250],  # for change in the colors, not used fr linear
 caption='Population en millions'  # caption for Color scale or Legend
)
step.add_to(m)

# create list of country
# 244 countries
country_list = []
for i in range(244):
    country_list.append(str(countries.iloc[i, 3]))

# for each country set marker and circle

for i in range(244):
    radius = 0
    for j in range(235):
        if country_list[i] == countries2.iloc[j, 0]:
            radius = countries2.iloc[j, 1]

    Create_localisation(countries.iloc[i, 1],
                        countries.iloc[i, 2],
                        country_list[i],
                        (countries.iloc[i, 0]).lower(),
                        int(radius))
m.save(f'World_population.{Version}.html')


