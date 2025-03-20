##################
### Librairies ###
##################

import warnings
warnings.filterwarnings('ignore')

# Classics
import pandas as pd
import geopandas as gpd
import numpy as np
from tqdm import tqdm
import requests

# OSMnx
import osmnx as ox
# Turn response caching off
ox.settings.use_cache = False
ox.settings.log_console = False
# Select useful tags
ox.settings.useful_tags_way = ['name', 'highway', 'lanes', 'oneway',  'lanes:backward', 'lanes:forward']

# Pytrack
from pytrack.graph import distance
from pytrack.analytics import visualization
from pytrack.matching import candidate, mpmatching_utils, mpmatching

# Geometry
from shapely.geometry import box, Point, LineString

from pyproj import CRS, Transformer
from shapely.geometry import Point
from shapely.ops import transform

##############
### Points ###
##############

# This is the ranking of highway importance for our algorithm
highway_importance = {
    "motorway": 1,
    "motorway_link": 2,
    "trunk": 3,
    "trunk_link": 4,
    "primary": 5,
    "primary_link": 6,
    "secondary": 7,
    "secondary_link": 8,
    "tertiary": 9,
    "tertiary_link": 10,
    "unclassified": 11,
    "residential": 12,
    "living_street": 13,
    "service": 13,
    "living_street": 14,
    
    # These are not requested:
    # "track": 15,
    # "path": 16,
    # "footway": 17,
    # "cycleway": 18,
    # "bridleway": 19,
    # "other": 20,  
}

def geodesic_point_buffer(lat, lon, m):
    # Azimuthal equidistant projection
    aeqd_proj = CRS.from_proj4(
        f"+proj=aeqd +lat_0={lat} +lon_0={lon} +x_0=0 +y_0=0")
    tfmr = Transformer.from_proj(aeqd_proj, aeqd_proj.geodetic_crs)
    buf = Point(0, 0).buffer(m).simplify(1)  # distance in metres
    # return the simplified geometry bounding polygon
    return transform(tfmr.transform, buf)


def points_matching(gdf, start_radius = 3, increase_radius = 3, threshold_radius = 20):
    """
    gdf: GeoDataFrame with shapely Points geometries to match
    start_radius: float (in meters) to search nodes in OSM networks
    increase_radius: float (meters) to add recursively to the previous search radius
    threshold_radius: float (meters) limit to the searched perimeter
    """
    
    # Intialize results list
    closest_roads, highways, distances, lanes, oneway, osmids = list(), list(), list(), list(), list(), list()
    # Extract bounding box
    xmin, ymin, xmax, ymax = gdf.total_bounds

    # Prepare the request
    url = "http://overpass-api.de/api/interpreter"  # To avoid the natural space at the end
    query = (
        f'[out:json][timeout:120];(way({ymin},{xmin},{ymax},{xmax})[highway~"^(motorway|trunk|primary|secondary|tertiary|residential|unclassified|living_street|service|(motorway|trunk|primary|secondary)_link)$"];);out geom;'
    )  

    # Make request
    response = requests.get(url, params={"data": query})
    
    # Treat response
    if response.status_code == 200:
        # Retrieve elements
        gdf_city = pd.json_normalize(response.json()["elements"])
        # Transform geometries
        gdf_city['geometry'] = gdf_city.geometry.apply(lambda x : LineString([(d['lon'], d['lat']) for d in x]))
        # Create GeoDataFrame and retrieve useful features
        gdf_city = gpd.GeoDataFrame(gdf_city[['tags.highway', 'tags.name', 'tags.lanes', 
                                              'tags.oneway', 'tags.lanes:backward', 'tags.lanes:forward',
                                              'id', 'geometry']],
                    geometry = 'geometry',
                    crs = 'epsg:4326'
                    )
        # Rename columns
        gdf_city.rename(columns = {
                'tags.highway' : 'highway',
                'tags.name' : 'name',
                'tags.lanes':'lanes',
                'tags.oneway':'oneway',
                'tags.lanes:backward':'lanes:backward',
                'tags.lanes:forward':'lanes:forward',
                'id':'osmid'
                    }, inplace = True)
        print('City downloaded')
        
        # Convert lanes to float
        gdf_city.loc[gdf_city.lanes.notna(), 'lanes'] = gdf_city.loc[gdf_city.lanes.notna(), 'lanes'].apply(lambda s : float("".join([ele for ele in s if ele.isdigit()])))
        gdf_city['lanes'] = gdf_city.lanes.astype(float)
        
    elif response.status_code == 504:
            print('Request denied: Status code 504')
        
    else : 
        print('City not found: Statud code', response.status_code)



    for point in tqdm(gdf.geometry) :
        # Initialize empty gdf
        gdf_edges = gpd.GeoDataFrame()
        # Retrieve sensor location
        lon, lat = list(point.coords)[0]
        # Reset the search radius
        radius = start_radius

        # Search nearby roads
        while gdf_edges.shape[0] == 0 :
            # Create a buffer of a given radius
            buff = geodesic_point_buffer(lat, lon, m=radius)
            # Find roads within the buffer
            gdf_edges = gdf_city.clip(buff)

            # We increase the search radius
            radius += increase_radius
            if radius > threshold_radius :
                # Then we failed finding roads within a reasonable perimeter (18m)
                break
        
        # Find best candidate within the matched roads
        if gdf_edges.shape[0] > 0:
            
            # Assign distance metric  
            # (Change the crs to 6933 to get results in meter, otherwise the distance values are likely incorrect)
            gdf_edges["distance"] = gdf_edges.to_crs(epsg=6933).geometry.distance(
                gpd.GeoSeries(point, crs = 'epsg:4326').to_crs(epsg=6933).values[0]
            )

            # Assign importance ranking
            gdf_edges["importance"] = gdf_edges["highway"].apply(lambda x: highway_importance[x])

            # Find the closest edge based on importance and then distance
            closest_edge = gdf_edges.sort_values(by=["importance", "distance"]).iloc[0]
            
            # Save relevant features
            closest_roads.append(closest_edge["name"])
            highways.append(closest_edge["highway"])
            lanes.append(closest_edge["lanes"])
            distances.append(closest_edge["distance"])
            osmids.append(closest_edge["osmid"])
            # Sometimes oneway attribute is absent but there are lanes backward/forward indicating the osmid accounts for both direction
            if closest_edge["oneway"] :
                oneway.append(closest_edge["oneway"])
            else : # It is nan
                if closest_edge["lanes:backward"].notna() & closest_edge["lanes:forward"].notna() :
                    oneway.append(False) # We have likely two flow directions
                else :
                    oneway.append(np.nan)
            # Convert to boolean
            oneway = [True if k=="yes" else False if k=="no" else k for k in oneway]
            
        else : # Found no OSM ways within the requested polygon.
            print('Value Error - No roads found nearby current index')
            closest_roads.append(np.nan)
            highways.append(np.nan)
            lanes.append(np.nan)
            oneway.append(np.nan)
            distances.append(np.nan)
            osmids.append(np.nan)
    
    # Update results in the gdf
    gdf['osm_name'] = closest_roads
    gdf['osm_type'] = highways
    gdf['osm_lanes'] = lanes
    gdf['osm_oneway'] = oneway
    gdf['osm_distance'] = distances
    gdf['osmid'] = osmids
    
    # Show information
    print('We failed to match', gdf.osmid.isna().sum(), 'sensors')
    print('...on a total of', gdf.shape[0], 'sensors')
    
    return gdf


###################
### LineStrings ###
###################
# With LineStrings, we can use more refined map matching techniques such as the ones provided by Pytrack

# Utils
def main_occurence(x):
    m=0
    champ=None
    for k in x :
        if x.count(k) > m:
            champ = k
            m = x.count(k)
    return champ


def lines_matching(gdf, name = None, radius = 30, interp = 5):
    """
    gdf: GeoDataFrame with shapely LineString geometries to match
    name (usually not used): city name to retrieve the OSM graph, example: "Paris, France"
    This function can be changed to use a polygon instead, see OSMnx reference "graph_from_polygon"
    radius:  Radius of the search circle around each linestring coordinate
    interp: Step to interpolate the graph. The smaller the interp_dist, the greater the precision and the longer the computational time.
    """
    if name :
        # We get the graph from the name
    
        # # Load the entire city graph with OSMnx
        P = ox.graph_from_place(name, network_type = 'drive', simplify = False)
        
    else : # get graph from boundaries
            # Load the entire graph bbox with OSMnx
        P = ox.graph_from_bbox(
            gdf.total_bounds,
            # distance.enlarge_bbox(*gdf.total_bounds, dist = 1000),
            network_type = 'drive', 
            simplify = False)
         
    print('Main graph loaded')
    
    # Get the cooresponding GeoDataFrame
    edges = ox.graph_to_gdfs(P, nodes = False)
    
    # Convert lanes to float
    edges['lanes'] = edges.lanes.astype(float)
    edges['lanes:forward'] = edges['lanes:forward'].astype(float)
    edges['lanes:backward'] = edges['lanes:backward'].astype(float)
    
    # Innitialize lists to store results
    osm_match=[]
    names = []
    lanes = []
    oneway = []
    highways = []

    # For each sensor geometry
    for idx in gdf.index:
        #We get the points of the iu_ac
        points = [u[::-1] for u in list(gdf.loc[idx].geometry.coords)]
        # Create BBOX 
        north, east = np.max(np.array([*points]), 0)
        south, west = np.min(np.array([*points]), 0)
        
        # Extract road graph
        north, south, west, east = distance.enlarge_bbox(north, south, west, east, dist = 100)
        # dist is the Distance in meters indicating how much to expand the bounding box.
        bbox = box(west, south, east, north) # Used to clip the edges dataframe
        t = gpd.clip(edges, mask = bbox)
        filtr = t.index.get_level_values(0).to_list()+t.index.get_level_values(1).to_list()
        # This simplifies the matching process
        G = P.subgraph(filtr)
        
        # Necessary
        loc = np.mean(np.array(points), axis=0)
        maps = visualization.Map(location=loc, zoom_start=40)
        
        try :
            maps.add_graph(G)
            # Extract candidates
            G_interp, candidates = candidate.get_candidates(G, points, interp_dist=interp, closest=True, radius=radius)
            # Extract trellis DAG graph
            trellis = mpmatching_utils.create_trellis(candidates)
        except Exception as e :
            print(type(e), e)  
            # No candidates
            osm_match.append(np.nan)
            names.append(np.nan)
            lanes.append(np.nan)
            oneway.append(np.nan)
            highways.append(np.nan)
        else : 
            # Perform the map-matching process
            try : 
                path_prob, predecessor = mpmatching.viterbi_search(G_interp, trellis, "start", "target") 
                #Get path
                path_elab = mpmatching_utils.create_path(G_interp, trellis, predecessor)
                edges_id = []
                #We get edges id
                for k in range(len(path_elab)-1):
                    edges_id.append(G_interp.edges[(path_elab[k], path_elab[k+1], 0)]['osmid'])
                
                # We keep the main occurence
                osmid = main_occurence(list(np.unique(edges_id)))
                
                if osmid is None :
                    # Corresponding link not found (empty list)
                    osm_match.append(np.nan)
                    names.append(np.nan)
                    lanes.append(np.nan)
                    oneway.append(np.nan)
                    highways.append(np.nan)
                else :
                    # Get the name and highway attribute
                    name_val, high_val, lanes_val, oneway_val, laneback_val, lanefor_val = t.loc[t.osmid == osmid][[
                        'name', 'highway', 'lanes', 'oneway', 'lanes:backward', 'lanes:forward',
                    ]].values[0]
                    # Add to lists
                    names.append(name_val)
                    highways.append(high_val)
                    lanes.append(lanes_val)
                    oneway.append(oneway_val if oneway_val else False if not np.isnan(laneback_val) | np.isnan(lanefor_val) else np.nan)
                    osm_match.append(osmid)
                              
                 
            except Exception as e :
                print(type(e), e) 
                # Error when viterbi
                osm_match.append(np.nan)
                names.append(np.nan)
                lanes.append(np.nan)
                oneway.append(np.nan)
                highways.append(np.nan)


    # This is to save all osmids in geographical data ref
    gdf['osm_name'] = names
    gdf['osm_type'] = highways
    gdf['osm_lanes'] = lanes
    gdf['osm_oneway'] = oneway
    gdf['osmid'] = osm_match

    # Show information
    print('Missing match', gdf.osmid.isna().sum())
    print('...on a total of', gdf.shape[0], 'sensors')
    
    # Return result
    return gdf

