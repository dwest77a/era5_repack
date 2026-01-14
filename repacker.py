import xarray as xr
import numpy as np
import sys
from netCDF4 import Dataset
from datetime import datetime
import glob

def assemble_file(outdir: str, filepath: str):
    """
    Pull data from the original file and repack without compression to a new file
    """

    file    = filepath.split('/')[-1]
    outfile = outdir + file.replace(file.split('.')[-1], 'repack.' + file.split('.')[-1])

    # Open xarray representation of source dataset
    ds = xr.open_dataset(filepath, decode_times=False)

    # Create new netcdf file using NetCDF4 library
    out_ds = Dataset(outfile, 'w', format = 'NETCDF4')

    # Assemble list of non-dimension variables
    vars = list(set(ds.variables) - set(ds.dims))

    # Extract global attributes
    global_attrs = ds.attrs

    new_dims, dim_vars = [],[]
    for d in ds.dims:
        # Create new labelled dimension
        new_dims.append(out_ds.createDimension(str(d), len(ds[d])))
        
        # Create variable array for dimension
        # (If coordinate dimensions are present, will have to skip this)
        dim_vars.append(out_ds.createVariable(str(d), ds[d].dtype, (str(d),) ))

        # Copy over attributes
        for attr, val in ds[d].attrs.items():
            setattr(dim_vars[-1], attr, val)

        # Copy data with standard dtype
        dim_vars[-1][:] = ds[d].compute()

    new_vars = []
    for v in vars:
        # Create variable array
        # Dtype is now transformed to match scale_factor - will not be compressed back to int16
        new_vars.append(out_ds.createVariable(str(v), np.dtype(ds[v].encoding['scale_factor']), ds[v].dims))

        # Copy attributes
        for attr, val in ds[v].attrs.items():
            setattr(new_vars[-1], attr, val)

        # Transfer data (expect time,lat,lon)
        new_vars[-1][:,:,:] = ds[v].compute()

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

def main():

    directory = sys.argv[-1]
    files = glob.glob(f'{directory}/*')
    for f in files:
        assemble_file('example_data/', f)

if __name__ == '__main__':
    main()