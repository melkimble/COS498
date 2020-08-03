'''
Section for generating labeled maps from pdf site predictions
https://stackoverflow.com/questions/35716830/basemap-with-python-3-5-anaconda-on-windows
http://www.datadependence.com/2016/06/creating-map-visualisations-in-python/
'''

import warnings
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# there are some depricated errors that do not affect anything that like to pop up here, so warnings
# are ignored from mpl_toolkits.
warnings.filterwarnings(action='ignore', category=UserWarning, module='mpl_toolkits')

def get_marker_color(sentiment):
    if sentiment == 'Positive':
        # green points
        return ('go')
    elif sentiment == 'Negative':
        # red points
        return ('ro')
    else:
        # yellow points
        return ('yo')

def array2Map(lats, lons, labels, cols):
    print('starting map...')
    # setup mercator prj basemap.
    # set resolution=None to skip processing of boundary datasets.
    map = Basemap(projection='merc', lat_0=43.0, lon_0=-70.0,
                  resolution='h', area_thresh=0.1,
                  llcrnrlon=-71.0, llcrnrlat=43.0,
                  urcrnrlon=-67.0, urcrnrlat=45.0)

    map.drawcoastlines()
    map.drawcountries()
    map.fillcontinents(color='coral')
    map.drawmapboundary()

    # add x,y coordinates to map based on lats/lon array from results.
    # for each coordinate, add a label based on predicted place from results
    # also add color based on predicted sentiment from results
    for label, xpt, ypt, col in zip(labels, lons, lats, cols):
        x, y = map(xpt, ypt)
        plt.text(x + 10000, y + 5000, label)
        marker_string=get_marker_color(col)
        map.plot(x,y,marker_string,markersize=6)

    title_string = "Naive Bayes Predicted Place and Sentiment"
    plt.title(title_string)
    plt.show()