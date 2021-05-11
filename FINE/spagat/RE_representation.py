'''
Functions to represent RE time series 
'''

import numpy as np
import xarray as xr
import geopandas as gpd 
from sklearn.cluster import AgglomerativeClustering
from dask.distributed import Client, progress

import FINE.spagat.utils as spu
import FINE.spagat.RE_representation_utils as RE_rep_utils

@spu.timer
def represent_RE_technology(gridded_RE_ds, 
                            CRS_attr,
                            shp_file,
                            n_timeSeries_perRegion=1,  
                            capacity_var_name='capacity',
                            capfac_var_name='capacity factor',
                            longitude='x', 
                            latitude='y',
                            time='time',
                            index_col='region_ids', 
                            geometry_col='geometry',
                            linkage='average'):

    """Represents RE time series and their corresponding capacities, within each region.
    
    Parameters
    ----------
    gridded_RE_ds : str/xr.Dataset 
        Either the path to the dataset or the read-in xr.Dataset
        - Dimensions in this data - `latitude`, `longitude`, and `time` 
        - Variables - `capacity_var_name` and `capfac_var_name` 
    CRS_attr : str
        The attribute in `gridded_RE_ds` that holds its 
        Coordinate Reference System (CRS) information 
    shp_file : str/Shapefile
        Either the path to the shapefile or the read-in shapefile 
        that should be added to `gridded_RE_ds`
    n_timeSeries_perRegion : strictly positive int, optional (default=1)
        The number of time series to which the original set should be aggregated,
        within each region. 
        - If set to 1, performs simple aggregation
            - Within every region, calculates the weighted mean of RE 
              time series (capacities being weights), and sums the capacities.
        - If set to a value more than 1, time series clustering is employed
            - Clustering method: agglomerative hierarchical clustering
            - Distance measure: Euclidean distance
            - Aggregation within each resulting cluster is the same as simple 
              aggregation
    capacity_var_name : str, optional (default='capacity')
        The name of the data variable in `gridded_RE_ds` that corresponds 
        to capacity 
    capfac_var_name : str, optional (default='capacity factor')
        The name of the data variable in `gridded_RE_ds` that corresponds 
        to capacity factor time series  
    longitude : str, optional (default='x')
        The dimension name in `gridded_RE_ds` that corresponds to longitude 
    latitude : str, optional (default='y')
        The dimension name in `gridded_RE_ds` that corresponds to latitude
    time : str, optional (default='time')
        The dimension name in `gridded_RE_ds` that corresponds to time
    index_col : str, optional (default='region_ids')
        The column in `shp_file` that needs to be taken as location-index in `gridded_RE_ds`
    geometry_col : str, optional (default='geometry')
        The column in `shp_file` that holds geometries 
    linkage : str, optional (default='average') 
        - Relevant only if `n_timeSeries_perRegion` is more than 1. 
        - The linkage criterion to be used with agglomerative hierarchical clustering. 
          Can be 'complete', 'single', etc. Refer to Sklearn's documentation for more info.

    Returns
    -------
    represented_RE_ds : xr.Dataset 
    - Dimensions in this data - `time`, 'region_ids'
        - The dimension 'region_ids' has its coordinates corresponding to `index_col` 
    If `n_timeSeries_perRegion` is more than 1, additional dimension - 'TS_ids' is present
        -  Within each region, different time seires are indicated by this 'TS_ids'   
    """

    def _simply_aggregate_RE_technology(region):
    
        #STEP 1. Create resultant xarray dataset 
        time_steps = rasterized_RE_ds[time].values  
        n_timeSteps = len(time_steps)

        ## time series 
        data = np.zeros((n_timeSteps, 1))

        represented_timeSeries = xr.DataArray(data, [(time, time_steps),
                                                    ('region_ids', [region])])

        #capacities
        represented_capacities = xr.DataArray(0, [('region_ids', [region])])

        #STEP 2. Representation
        regional_ds = rasterized_RE_ds.sel(region_ids = region)
    
        regional_capfac_da = regional_ds[capfac_var_name].where(regional_ds.rasters == 1)
        regional_capacity_da = regional_ds[capacity_var_name].where(regional_ds.rasters == 1)

        #STEP 2b. Preprocess regional capfac and capacity dataArrays 

        #STEP 2b (i). Restructure data
        regional_capfac_da = regional_capfac_da.stack(x_y = [longitude, latitude]) 
        regional_capfac_da = regional_capfac_da.transpose(transpose_coords= True) 

        regional_capacity_da = regional_capacity_da.stack(x_y = [longitude, latitude])
        regional_capacity_da = regional_capacity_da.transpose(transpose_coords= True)

        #STEP 2b (ii). Remove all time series with 0 values 
        regional_capfac_da = regional_capfac_da.where(regional_capacity_da > 0)
        regional_capacity_da = regional_capacity_da.where(regional_capacity_da > 0)

        #STEP 2b (iii). Drop NAs 
        regional_capfac_da = regional_capfac_da.dropna(dim='x_y')
        regional_capacity_da = regional_capacity_da.dropna(dim='x_y')

        #Print out number of time series in the region 
        n_ts = len(regional_capfac_da['x_y'].values)
        print(f'Number of time series in {region}: {n_ts}')

        #STEP 2c. Get power curves from capacity factor time series and capacities 
        regional_power_da = regional_capacity_da * regional_capfac_da

        #STEP 2d. Aggregation
        ## capacity
        capacity_total = regional_capacity_da.sum(dim = 'x_y').values
        represented_capacities.loc[region] = capacity_total
        
        ## capacity factor 
        power_total = regional_power_da.sum(dim = 'x_y').values
        capfac_total = power_total/capacity_total
        
        represented_timeSeries.loc[:,region] = capfac_total

        #STEP 3. Create resulting dataset 
        regional_represented_RE_ds = xr.Dataset({capacity_var_name: represented_capacities,
                                        capfac_var_name: represented_timeSeries}) 

    
        return regional_represented_RE_ds 


    def _cluster_RE_technology(region):
    
        #STEP 1. Create resultant xarray dataset 
        time_steps = rasterized_RE_ds[time].values  
        n_timeSteps = len(time_steps)

        TS_ids = [f'TS_{i}' for i in range(n_timeSeries_perRegion)] 

        ## time series 
        data = np.zeros((n_timeSteps, 1, n_timeSeries_perRegion))

        represented_timeSeries = xr.DataArray(data, [(time, time_steps),
                                                    ('region_ids', [region]),
                                                    ('TS_ids', TS_ids)])

        data = np.zeros((1, n_timeSeries_perRegion))

        #capacities
        represented_capacities = xr.DataArray(data, [('region_ids', [region]),
                                                    ('TS_ids', TS_ids)])

        #STEP 2. Representation
        regional_ds = rasterized_RE_ds.sel(region_ids = region)
    
        regional_capfac_da = regional_ds[capfac_var_name].where(regional_ds.rasters == 1)
        regional_capacity_da = regional_ds[capacity_var_name].where(regional_ds.rasters == 1)

        #STEP 2b. Preprocess regional capfac and capacity dataArrays 

        #STEP 2b (i). Restructure data
        regional_capfac_da = regional_capfac_da.stack(x_y = [longitude, latitude]) 
        regional_capfac_da = regional_capfac_da.transpose(transpose_coords= True) 

        regional_capacity_da = regional_capacity_da.stack(x_y = [longitude, latitude])
        regional_capacity_da = regional_capacity_da.transpose(transpose_coords= True)

        #STEP 2b (ii). Remove all time series with 0 values 
        regional_capfac_da = regional_capfac_da.where(regional_capacity_da > 0)
        regional_capacity_da = regional_capacity_da.where(regional_capacity_da > 0)

        #STEP 2b (iii). Drop NAs 
        regional_capfac_da = regional_capfac_da.dropna(dim='x_y')
        regional_capacity_da = regional_capacity_da.dropna(dim='x_y')

        #Print out number of time series in the region 
        n_ts = len(regional_capfac_da['x_y'].values)
        print(f'Number of time series in {region}: {n_ts}')

        #STEP 2c. Get power curves from capacity factor time series and capacities 
        regional_power_da = regional_capacity_da * regional_capfac_da

        #STEP 2d. Clustering  
        agg_cluster = AgglomerativeClustering(n_clusters=n_timeSeries_perRegion, 
                                              affinity="euclidean",  
                                              linkage=linkage)
        agglomerative_model = agg_cluster.fit(regional_capfac_da)

        #STEP 2e. Aggregation
        for i in range(np.unique(agglomerative_model.labels_).shape[0]):
            ## Aggregate capacities 
            cluster_capacity = regional_capacity_da[agglomerative_model.labels_ == i]
            cluster_capacity_total = cluster_capacity.sum(dim = 'x_y').values

            represented_capacities.loc[region, TS_ids[i]] = cluster_capacity_total

            #aggregate capacity factor 
            cluster_power = regional_power_da[agglomerative_model.labels_ == i]
            cluster_power_total = cluster_power.sum(dim = 'x_y').values
            cluster_capfac_total = cluster_power_total/cluster_capacity_total

            represented_timeSeries.loc[:,region, TS_ids[i]] = cluster_capfac_total
            
        #STEP 3. Create resulting dataset 
        regional_represented_RE_ds = xr.Dataset({capacity_var_name: represented_capacities,
                                        capfac_var_name: represented_timeSeries})  

        return regional_represented_RE_ds 


    #STEP 1. Rasterize the gridded dataset
    rasterized_RE_ds = RE_rep_utils.rasterize_xr_ds(gridded_RE_ds, 
                                                    CRS_attr,
                                                    shp_file, 
                                                    index_col, 
                                                    geometry_col,
                                                    longitude, 
                                                    latitude)


    region_ids = rasterized_RE_ds['region_ids'].values 

    results = []

    client = Client(threads_per_worker=4, n_workers=len(region_ids))

    futures = []
    if n_timeSeries_perRegion==1:
        for region in region_ids:
            future = client.submit(_simply_aggregate_RE_technology, region)
            futures.append(future)

    else:
        for region in region_ids:
            future = client.submit(_cluster_RE_technology, region)
            futures.append(future)

    results = client.gather(futures)  
    represented_RE_ds =  xr.merge(results)

    
    #TODO: the below code is using concurrent.futures. Delete this later
    #import concurrent.futures
    # if n_timeSeries_perRegion==1:
    #     with concurrent.futures.ThreadPoolExecutor() as executor:
    #         for region in region_ids:
    #             results.append(executor.submit(_simply_aggregate_RE_technology, region))
    
    # else:
    #     with concurrent.futures.ThreadPoolExecutor() as executor:
    #         for region in region_ids:
    #             results.append(executor.submit(_cluster_RE_technology, region))

    # represented_RE_ds = xr.Dataset()
    # for r in results: 
    #     represented_RE_ds = xr.merge([represented_RE_ds, r.result()])
   
    return represented_RE_ds 
