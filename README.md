# Harmonized Annual Averaged Traffic Data at Street Segment Level for European Cities

This repository provides a framework for standardizing road traffic data from various European cities. Many cities offer road count data on their open data websites, but these datasets often differ in language, format, variables, and geometries. This project aims to harmonize these datasets into a standardized structure for ease of analysis and integration.

## Repository Structure

Each folder in this repository corresponds to a specific city and includes the following components:

- **`raw/`**  
  Contains the raw data downloaded directly from the city's open data website. If the original dataset is too large, a sample is provided to serve as an example.
  
- **`source.txt`**  
  A text file containing the URL of the page where the raw data can be downloaded.
  
- **`{cityname}.ipynb`**  
  A Python Jupyter Notebook that processes the raw data and converts it into standardized traffic data.
  
- **`treated/`**  
  Contains the processed (treated) data in a standardized format.

## Data Naming and Content

Processed data in the `treated/` folder typically consists of GeoJSON files, named using the following format:

**`{cityname}_{variable}_{year}.GeoJSON`** 

A summary of available processed data can be found in `assets/cities_all.csv`. Analysis of this table can be made in `cities_available.ipynb`.

## Required Variables

- **Average Annual Daily Traffic (AADT)**  
  Represents the average daily traffic volume for all days of the year.
  
- **Average Annual Weekday Traffic (AAWT)**  
  Represents the average daily traffic volume for weekdays / working days.

Some datasets may include both variables, depending on what is provided by the city.
The geometries in the final files are expected to be one of the following:

- **Points**: Representing the location of a road section.  
- **Oriented LineStrings**: Representing road sections with directional flow.

## Data Dictionary

### Local Dataset

| Feature Name | Type  | Description |
|-------------|-------|-------------|
| AADT or AAWT | float | Average Annual Daily (Weekday) Traffic (vehicles per day). |
| s85         | float | 85th percentile of observed speed (km/h). |
| savg        | float | Average monitored speed (km/h). |

### Abbreviations

| Abbreviation | Example | Meaning |
|-------------|---------|---------|
| TR          | TR_AADT | Trucks (variables related to trucks/heavy vehicles). |
| 2W          | 2W_savg | 2-Wheels (variables related to 2-wheels). |
| pct         | TR_pct_AAWT | Percentage (value as a percentage of AADT/AAWT). |

### Road Segment Information

| Feature Name  | Type | Description |
|--------------|------|-------------|
| geometry     | Point / LineString | Geographic coordinates of the sensor location (Point) or the corresponding road segment (LineString) in the WGS84 projection. |
| raw_name    | text  | Name of the road segment. |
| raw_oneway  | boolean | Whether or not the sensor monitors flow in one direction only. If this is not provided, one may look at the city-level labeling in `cities_summary.csv`. |
| raw_direction | text | Indication for the direction of the flow. This field can be an angle value or text indication (not translated). `NaN` if `raw_oneway` is `False`. |
| raw_lanes   | float | The number of lanes of the monitored road segment. |
| raw_techno  | text | The counting technique employed when this information is provided at the sensor level (not translated). Otherwise, one may look at the city-level attribute Table 1. |

### OpenStreetMap

| Feature Name  | Type  | Description |
|--------------|-------|-------------|
| osmid       | float | The "road segment ID" that links the provided data to the OSM referential. |
| osm_name    | text  | Name of the matched road segment. |
| osm_type    | text  | The OSM “highway” classification type. |
| osm_lanes   | float | The number of lanes of the matched road segment. Many values could be missing. |
| osm_oneway  | boolean | Whether or not the matched road segment has flow in one direction only. Retrieved from the presence of the `oneway` attribute or `lanes:backward/forward` in OSM. Many values could be missing. |
| osm_maxspeed   | float | The indicated speed limit on the road segment (km/h) retrieved from “maxspeed” in OSM. |
| osm_distance | float | The distance (meters) between the sensor location and the matched road segment (for point geometries only). This can serve as a quality indicator for the matching process. |

## How to Contribute

We welcome contributions to this repository! You can contribute by adding new cities and their corresponding data sources. 

### Installation

To set up the required dependencies, ensure you are using **Python 3.12.8**, then run:
`pip install -r requirements.txt`

### Contribution Guidelines

1. Include a **sample of the raw data** in the `raw/` folder (if the full dataset is too large).  
2. Provide the **source URL** in the `source.txt` file.  
3. Include a **Jupyter Notebook** (`{cityname}.ipynb`) that transforms the raw data into the standardized format.  
4. If the raw data files are too large to upload, include only the URLs, the processing code, and the final processed data.

### Notebook Guidelines

To optimize the repository's size and usability:
- **Avoid excessive figures or interactive maps** in the notebook files to conserve space in the repository.  
- **Provide clear explanations** within the notebooks, including:
  - Translations of variable names or key data terms.
  - Additional documentation when needed (e.g., external references or detailed metadata).
  - Justifications for any assumptions or transformations applied to the data. The files `map_matching_OSM.py` and `temporal_agg.py` can be used.
- The final processed files should be uploaded to the `treated/` folder. 
- Ensure the final data uses one of the accepted geometries (Points or oriented LineStrings).

This ensures transparency and reproducibility for all contributors and users.

## Reference

This work is currently under review in Nature Scientific Data
