import xarray as xr
import numpy as np
import sys
from netCDF4 import Dataset
from datetime import datetime
import os
import math

def assemble_file(outdir: str, file_subset: list, var: str):
    """
    Pull data from the original file and repack without compression to a new file
    """

    file0 = file_subset[0]
    ymd = ''.join(file0.split('/')[6:9])
    outfile = os.path.join(outdir, *file0.split('/')[6:9]) + f'/ecmwf-era5X_oper_an_sfc_{ymd}_{var}_repack.nc'

    if os.path.isfile(outfile):
        return

    outdir = os.path.join(outdir, *file0.split('/')[6:9])
    if not os.path.isdir(outdir):
        os.makedirs(outdir)

    # Create new netcdf file using NetCDF4 library
    out_ds = Dataset(outfile, 'w', format = 'NETCDF4')

    agg_vars = {}
    agg_time = []

    corruptions = []
    for hr, file in enumerate(file_subset):

        # Open xarray representation of source dataset
        ds = xr.open_dataset(file, decode_times=False)

        # Assemble list of non-dimension variables
        vars = list(set(ds.variables) - set(ds.dims))

        if hr == 0:

            # Extract global attributes
            global_attrs = ds.attrs

            new_dims, dim_vars = [],[]
            for d in ds.dims:

                if d == 'time':
                    new_dims.append(out_ds.createDimension(str(d), len(ds[d])*len(file_subset)))
                else:

                    # Create new labelled dimension
                    new_dims.append(out_ds.createDimension(str(d), len(ds[d])))
                
                # Create variable array for dimension
                # (If coordinate dimensions are present, will have to skip this)
                dim_vars.append(out_ds.createVariable(str(d), ds[d].dtype, (str(d),), compression='zlib'))

                # Copy over attributes
                for attr, val in ds[d].attrs.items():
                    setattr(dim_vars[-1], attr, val)

                if d != 'time':
                    # Copy data with standard dtype
                    dim_vars[-1][:] = ds[d].compute()

        agg_time.append(np.array(ds['time'].compute()))

        for attr, val in ds.attrs.items():
            if not global_attrs.get(attr, False):
                global_attrs[attr] = 'See hourly source files for details.'
            if global_attrs[attr] != val:
                global_attrs[attr] = 'See hourly source files for details.'

        for v in vars:
            if v not in agg_vars:
                agg_vars[v] = [np.array(ds[v].compute())]
            else:
                try:
                    agg_vars[v].append(np.array(ds[v].compute()))
                except:
                    # Data corruption - track
                    agg_vars[v].append(agg_vars[v][-1])
                    corruptions.append(file)

    # dim = 'time'
    time = np.concatenate(agg_time, axis=0)
    dim_vars[list(ds.dims).index('time')][:] = time

    new_vars = []
    for v in vars:
        # Create variable array
        # Dtype is now transformed to match scale_factor - will not be compressed back to int16
        new_vars.append(out_ds.createVariable(str(v), np.dtype(np.float32), ds[v].dims, compression='zlib'))

        # Copy attributes
        for attr, val in ds[v].attrs.items():
            setattr(new_vars[-1], attr, val)

        # Transfer data (expect time,lat,lon)
        arr = np.concatenate(agg_vars[v], axis=list(ds[v].dims).index('time'))
        print(arr.shape)
        new_vars[-1][:,:,:] = arr

    # Copy global attributes
    for attr, val in global_attrs.items():
        setattr(out_ds, attr, val)

    # Update history (custom)
    setattr(out_ds,'history',getattr(out_ds, 'history') + ',\n' + \
        datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' GMT ' + \
        'Repacked for FRAME-FM AI Project Applications (https://github.com/dwest77a/era5_repack)'
    )

    print(f'{file} -> {outfile}')
    out_ds.close()

    return corruptions