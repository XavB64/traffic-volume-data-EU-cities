##################
### Librairies ###
##################

import warnings
warnings.filterwarnings('ignore')

# Classics 
import pandas as pd

# Weighted average function
def weighted_avg(group, weights, values):
    return (group[weights] * group[values]).sum() / group[weights].sum()


def daily_to_aadt(df, sensor_id_name, time_name, column_names):
    """
    df: A pandas DataFrame with two index: sensor_id_name and time_name
    time must be a Datetime index with frequency of one day and it should be date-like
    The dataframe should represent a year of data
    sensor_id_name : name of index for sensors
    time_name: name of index for time (date like)
    column_names: a list of attributes to aggregate (average), first element should be related to counting
    """
    
    # Average these values over the number of days
    # for this part, we consider that the variance is the flow is not too great so we can do a simple average for the speeds values
    
    # Data capture rate 
    nb_of_records = df.dropna(subset = column_names[0]).shape[0]
    # The theoretical number of record is NB sensors X timestamps
    nb_of_theoretical_records = df.index.levels[0].unique().size * df.index.levels[1].unique().size
    capture_rate = 100 * nb_of_records / nb_of_theoretical_records
    print(f'Daily capture rate is {round(capture_rate, 1)} %')
    
    # This is to get AADT (over all days)
    AADT = df.groupby(sensor_id_name).apply(
        lambda group: pd.Series(
            # Direct average for every column
            dict((key, group[key].mean()) for key in column_names
            )
        )
    )
    
    # Get weekday information from time index
    df['weekday'] = df.reset_index(level=1)[time_name].apply(lambda x : x.weekday()).values
    
    # Excluding weekends (AAWT)
    AAWT = df[df.weekday <= 4].groupby(sensor_id_name).apply(
        lambda group: pd.Series(
            # Direct average for every column
            dict((key, group[key].mean()) for key in column_names
            )
        )
    )
    # Here the columns will have the same name, so we have to change that
    AAWT.columns = [x + '_AAWT' for x in AAWT.columns]
    
    # Concat both into a new df
    df = pd.concat([AADT, AAWT], axis = 1)

    return df, capture_rate


def hourly_to_aadt(df, sensor_id_name, time_name, counts_name, speeds_name = {}, limit_hours = 4, minimum_hours = 24):
    """
    - df: A pandas DataFrame with two index: sensor_id_name and time_name
    time must be a Datetime index with frequency of one hour
    The dataframe should represent a year of data
    - sensor_id_name : name of index for sensors
    - time_name: name of index for time (hourly)
    - counts_name: a list of count-like attributes to aggregate (sum and average)
    - speeds_name: a dictionnary of count-like attributes to aggregate (weighted average). % of flow should be treated as speeds
    Keys are the column names and values the column name of the weights
    Can be an empty dict if there is no speed values
    - limit_hours: maximum number of consecutive NaNs to fill values with linear interpolation
    - minimum_hours: minimum hours to have a valid day to use within the aggregates
    """
    
    # Step 1: Create a complete hourly index
    # Create a DataFrame of all possible sensor_id + time combinations
    min_time, max_time = df.index.levels[1].min(), df.index.levels[1].max()
    all_times = pd.date_range(min_time, max_time, freq='h')  # All possible hourly timestamps
    unique_sensors = df.index.get_level_values(sensor_id_name).unique()
    complete_index = pd.MultiIndex.from_product(
        [unique_sensors, all_times], names=[sensor_id_name, time_name]
    )
    
    # Data capture rate 
    nb_of_records = df.dropna(subset = counts_name[0]).shape[0]
    # The theoretical number of record is NB sensors X timestamps
    hourly_capture_rate = 100 * nb_of_records / complete_index.size
    print(f'Hourly capture rate is {round(hourly_capture_rate, 1)} %')
    
    # Reindex the DataFrame to include missing rows with NaN values
    df = df.reindex(complete_index)
    
    # Step 2: Fill missing hourly values with linear interpolation
    for col in counts_name + list(speeds_name.keys()):
        #df[col] = df.groupby(sensor_id_name)[col].ffill().bfill()  # Forward then backward fill per sensor
        df[col] = df.groupby(sensor_id_name, group_keys=False)[col].apply(
    lambda group: group.interpolate(method='linear', limit = limit_hours)
)
        
    # Step 3: Filter out days with insufficient records    
    df['date'] = df.reset_index(level=1)[time_name].apply(lambda x : x.date()).values
    
    # Calculate the number of hourly records per day
    # If at least one value is not nan then we have a record - otherwise we don't and it's a "False"
    # Only on counts
    df['hour_present'] = df[counts_name].notna().any(axis=1)
    daily_record_counts = df.groupby([sensor_id_name, 'date'])['hour_present'].sum()
    
    # Keep only days with all 24 hours of data (otherwise it has 4 consecutive missing records or more)
    valid_days = daily_record_counts[daily_record_counts == minimum_hours].index
    # Create a mask for valid days
    valid_mask = df.reset_index().set_index([sensor_id_name, 'date']).index.isin(valid_days)
    
    # Filter the DataFrame to include only rows corresponding to valid days
    # This last step is done AFTER interpolation to keep most information during it
    df = df[valid_mask]
    
    # Step 4: Aggregate data by date
    df = df.groupby([sensor_id_name, 'date']).apply(
        lambda group: pd.Series(
            # Direct sum for flow-like values
            dict([(key, group[key].sum()) for key in counts_name] +
            # (if exist) Weighted averages for speed like values (weighted by flow)
                 [(key, weighted_avg(group, speeds_name[key], key)) for key in speeds_name.keys()]
            )
        )
    )
    
    # Average these values over the number of days
    df, daily_capture_rate = daily_to_aadt(df, 
                       sensor_id_name = sensor_id_name, 
                       time_name = 'date', 
                       column_names = counts_name + list(speeds_name.keys())
                       )

    return df, daily_capture_rate, hourly_capture_rate