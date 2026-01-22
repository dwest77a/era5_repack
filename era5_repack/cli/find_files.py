# Convert files to ecmwf-era5X_oper_an_sfc_200001011000.10u.nc

import glob

def main():
    """
    Assemble the filesets for 2007-2020 Era5 data for specific variables.
    """
    VARS = "10u 10v 2d 2t msl tcc tcwv".split()

    for yr in range(2007,2021):
        for var in VARS:
            dir = f'/badc/ecmwf-era5/data/oper/an_sfc/{yr}/*/*/ecmwf-era5_oper_an_sfc_{yr}*.{var}.nc'
            files = glob.glob(dir, recursive=True)
            with open(f'dfiles/{yr}_{var}.txt','w') as f:
                f.write('\n'.join(files))

if __name__ == '__main__':
    main()