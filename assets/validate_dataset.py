##################
### Librairies ###
##################

import pandas as pd
import numpy as np

def validate_dataset(gdf):
    min_val, max_val = 2, 2e5
    
    # Ensure there are no NaN values
    var = 'AADT' if 'AADT' in gdf.columns else 'AAWT'
    print(f'Number of NaN values for {var}: {gdf[var].isna().sum()}')
    gdf.dropna(subset = var, inplace=True)
    
    print(f'Number of NaN values for geometry: {gdf['geometry'].isna().sum()}')
    gdf.dropna(subset = 'geometry', inplace=True)
    
    # Remove outliers
    print(f'Number of <=1 values for {var}: {gdf[gdf[var] < min_val].shape[0]}')
    gdf = gdf[gdf[var] >= min_val]
    
    print(f'Number of >1e5 values for {var}: {gdf[gdf[var] > max_val].shape[0]}')
    gdf = gdf[gdf[var] <= max_val]
    
    return gdf
    