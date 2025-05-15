import osmnx as ox
import networkx as nx
import folium
from geopy.distance import geodesic


class FeatureEngineering:
    """
    A class to perform feature engineering on the NYC Taxi dataset.
    """

    def __init__(self):
        pass

    @staticmethod
    def haversine_distance(u, v, G):
        """
        Calculate the Haversine distance between two nodes in a graph.
        Euclidean distance is not accurate for lat/long coordinates

        Args:
            u: The current node.
            v: The target node.
            G: The graph containing node coordinates.
        """
        u_coord = (G.nodes[u]["y"], G.nodes[u]["x"])
        v_coord = (G.nodes[v]["y"], G.nodes[v]["x"])
        return geodesic(u_coord, v_coord).meters

    @staticmethod
    def plot_route_lat_lon(start_lat, start_lon, end_lat, end_lon, G, plot=True):
        """
        Plots a route for a single ride based on latitude and longitude coordinates.

        Args:
        - start_lat, start_lon: Latitude and longitude of the ride start point.
        - end_lat, end_lon: Latitude and longitude of the ride end point.
        - G: The road network graph (should already be loaded using osmnx).
        - plot (bool): Whether to plot the route on a map (default: True).
        """
        try:
            # Find nearest nodes using latitude and longitude
            start_node = ox.distance.nearest_nodes(G, X=start_lon, Y=start_lat)
            end_node = ox.distance.nearest_nodes(G, X=end_lon, Y=end_lat)

            # Check if a path exists
            if nx.has_path(G, start_node, end_node):

                if plot:
                    path = nx.astar_path(
                        G,
                        start_node,
                        end_node,
                        heuristic=lambda u, v: FeatureEngineering.haversine_distance(
                            u, v, G
                         ),
                        weight="length",
                    )

                    # Get node coordinates
                    path_coords = [
                        (G.nodes[node]["y"], G.nodes[node]["x"]) for node in path
                    ]

                    # Calculate total path length using sum of edge lengths
                    path_length = sum(
                        G.edges[path[i - 1], path[i], 0]["length"]
                        for i in range(1, len(path))
                    )

                    # Create a Folium map centered at the start location
                    route_map = folium.Map(
                        location=(start_lat, start_lon), zoom_start=13
                    )

                    # Plot the path with popup
                    folium.PolyLine(
                        locations=path_coords,
                        color="blue",
                        weight=5,
                        opacity=0.8,
                        popup=f"A* Shortest Path\nLength: {path_length:.2f} meters",
                    ).add_to(route_map)

                    # Add Start, End, and Midpoint Markers
                    folium.Marker(
                        location=(start_lat, start_lon),
                        popup=f"Start Point\nLat: {start_lat:.4f}, Lon: {start_lon:.4f}",
                        icon=folium.Icon(color="green", icon="play"),
                    ).add_to(route_map)

                    folium.Marker(
                        location=(end_lat, end_lon),
                        popup=f"End Point\nLat: {end_lat:.4f}, Lon: {end_lon:.4f}",
                        icon=folium.Icon(color="red", icon="stop"),
                    ).add_to(route_map)

                    midpoint = path_coords[len(path_coords) // 2]
                    folium.Marker(
                        location=midpoint,
                        popup=f"Path Length: {path_length:.2f} meters",
                        icon=folium.Icon(color="blue", icon="info-sign"),
                    ).add_to(route_map)

                    # Save the map
                    route_map.save("ride_route.html")
                    print("🗺️ Map saved as 'ride_route.html'")

                else:
                    path_length = nx.astar_path_length(
                        G,
                        start_node,
                        end_node,
                        # heuristic=lambda u, v: FeatureEngineering.haversine_distance(
                        #     u, v, G
                        # ),
                        weight="length",
                    )

                return path_length
            else:
                print(f"❌ No path exists between the given points.")

        except Exception as e:
            print(f"🚨 Error - {e}")


if __name__ == "__main__":
    # Load the road network graph once
    place = "New York City, New York, USA"
    G = ox.graph_from_place(place, network_type="drive")  # takes a few seconds
    print("🌍 Graph loaded successfully.")

    import sys

    sys.path.append("../")
    from configs.data_configs import PROCESSED_DATA_DIR
    import polars as pl

    # Load the NYC Taxi Zones dataset
    taxi_zones = pl.read_parquet(
        PROCESSED_DATA_DIR / "taxi_zones/taxi_zones_with_centroids.parquet"
    )

    start_lat, start_long = (
        taxi_zones.filter(taxi_zones["LocationID"] == 3)[["lat", "long"]]
        .to_pandas()
        .values[0]
    )
    end_lat, end_long = (
        taxi_zones.filter(taxi_zones["LocationID"] == 4)[["lat", "long"]]
        .to_pandas()
        .values[0]
    )

    # Plot a single route
    FeatureEngineering.plot_route_lat_lon(
        start_lat, start_long, end_lat, end_long, G, plot=True
    )
