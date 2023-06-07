import geopandas as gpd
import matplotlib.pyplot as plt

# Getting countries borders data from Natural Earth with high resolution
world = gpd.read_file("maps/ne_10m_admin_0_countries.shp")

def list_of_all_countries():
    return sorted(world['ADMIN'].tolist())

def plot_country_border(country_name, win_or_loose_str):
    # Filtering country by name
    country = world[world['ADMIN'] == country_name]

    # Getting neighbours
    country_geometry = country.geometry.iloc[0]
    neighbors = world[world.geometry.touches(country_geometry)]

    # Making plot
    fig, ax = plt.subplots(figsize=(10, 10))

    # Display country borders and neighboring countries
    country.plot(ax=ax, color='lightblue', edgecolor='black', linewidth=1)
    try:
        neighbors.plot(ax=ax, color='gray', edgecolor='black', linewidth=0.5)
    except :
        pass

    # Adding the signature of the choosen country
    for x, y, label in zip(country.geometry.centroid.x, country.geometry.centroid.y, country['ADMIN']):
        ax.annotate(label, xy=(x, y), xytext=(3, 3), textcoords="offset points", fontsize=8, color='black')

    # Placing the names of neighboring countries on the border of a given country
    boundary = country.boundary.iloc[0]
    for neighbor in neighbors.itertuples():
        neighbor_boundary = neighbor.geometry.boundary
        intersection = boundary.intersection(neighbor_boundary)
        if not intersection.is_empty:
            mid_point = intersection.interpolate(0.5, normalized=True)
            ax.annotate(neighbor.ADMIN, xy=(mid_point.x, mid_point.y), xytext=(3, 3),
                        textcoords="offset points", fontsize=8, color='black')

    # Display settings

    ax.set_xlim(country.total_bounds[0], country.total_bounds[2])
    ax.set_ylim(country.total_bounds[1], country.total_bounds[3])
    ax.set_frame_on(False)

    # Deleting coordinate axes
    ax.set_xticks([])
    ax.set_yticks([])

    plt.tight_layout(pad=0)

    fig = plt.get_current_fig_manager()
    fig.canvas.manager.set_window_title(f"You {win_or_loose_str}. Borders of {country_name} and neighbours ")
    fig.window.state('zoomed')
    plt.show()

def get_neighboring_countries(country_name):
    # Filtering country by name
    selected_country = world[world['ADMIN'] == country_name]

    # Getting neighbours
    country_geometry = selected_country.geometry.iloc[0]
    neighbors = world[world.geometry.touches(country_geometry)]

    # Return a list of neighboring country names
    return list(neighbors['ADMIN'])

