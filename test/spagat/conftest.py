import pathlib
import numpy as np
import pytest
import xarray as xr 

import FINE.spagat.dataset as spd
import FINE.spagat.representation as spr


@pytest.fixture(scope="package")
def sds():
    sds_folder_path_in = pathlib.Path("test/spagat/data/input")
    sds = spd.SpagatDataset()
    sds.read_dataset(sds_folder_path_in)
    spr.add_region_centroids(sds)

    return sds

@pytest.fixture()
def test_dataset1():    #TODO: rename this fixture to something more descriptive #NOTE: this dataset is not used anywhere in tests!
    """
    Create a simple Test Xarray Dataset containing three variables (without component): opFix(time series var), 1d_cap, 2d_dist
    """
    space = ['01_reg','02_reg','03_reg']
    timestep = ['T0','T1']
    space_2 = space.copy()

    opFix = xr.DataArray(np.array([[1,1],
                                    [0.9,1],
                                    [2,2]]), coords=[space, timestep], dims=['space', 'TimeStep'])
    cap_1d = xr.DataArray(np.array([0.9,
                                       1,
                                       0.9]), coords=[space], dims=['space'])
    dist_2d = xr.DataArray(np.array([[0,1,2],
                                      [1,0,10],
                                      [2,10,0]]), coords=[space,space_2], dims=['space','space_2'])

    ds = xr.Dataset({'operationFixRate': opFix,'1d_capacity': cap_1d,'2d_distance': dist_2d})

    sds = spd.SpagatDataset()
    sds.xr_dataset = ds
    return sds


@pytest.fixture()
def test_dataset2():   #TODO: rename this fixture to something more descriptive 
    """
    Create a Test Xarray Dataset: each variable has several components
    """
    space = ['01_reg','02_reg','03_reg']
    TimeStep = ['T0','T1']
    space_2 = space.copy()
    component = ['c1','c2','c3','c4']
    Period = [0]

    demand = np.stack([[[[np.nan,np.nan, np.nan] for i in range(2)]],
                        [[[1, 0.9,  2],
                          [1, 0,  0.9]]],
                        [[[np.nan,np.nan, np.nan] for i in range(2)]],
                        [[[0,   1, 1],
                          [0.3, 2, 1]]]])
    demand = xr.DataArray(demand, coords=[component, Period, TimeStep, space], dims=['component', 'Period', 'TimeStep','space'])
    cap_1d = np.stack([[0.9,  1,  0.9],
                        [0,    0,  0],
                        [0.9,  1,  0.9],
                        [np.nan] *3])
    cap_1d = xr.DataArray(cap_1d, coords=[component,space], dims=['component','space'])
    dist_2d = np.stack([[[0,1,2],[1,0,10],[2,10,0]],
                         [[0,0.1,0.2],[0.1,0,1],[0.2,1,0]],
                         [[np.nan] * 3 for i in range(3)],
                         [[np.nan] * 3 for i in range(3)]])
    dist_2d = xr.DataArray(dist_2d, coords=[component,space,space_2], dims=['component','space','space_2'])

    ds = xr.Dataset({'operationFixRate': demand, '1d_capacity': cap_1d, '2d_distance': dist_2d})

    sds = spd.SpagatDataset()
    sds.xr_dataset = ds
    return sds


  






