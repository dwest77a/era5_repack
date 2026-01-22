import glob
import netCDF4

def main():
    """
    Check/find missing files in the rescan, 
    prints the IDs of the year/var combos that need to be repeated.
    """

    VARS = "10u 10v 2d 2t msl tcc tcwv".split()

    redo = []
    skip = True
    for yr in glob.glob('/gws/ssde/j25b/eds_ai/public/era5_repack/daily_reprocess/*'):

        if yr.split('/')[-1] == '2010':
            skip = False

        if skip:
            continue

        year = yr.split('/')[-1]
        if 'zarr' in yr:
            continue
        completes = {v: True for v in VARS}
        for mth in glob.glob(yr + '/*'):
            for day in glob.glob(mth + '/*'):
                varfiles = glob.glob(day + '/*.nc')

                nvars = [v.split('_')[-2] for v in varfiles]
                missing = [v for v in VARS if v not in nvars]

                for v in varfiles:
                    try:
                        ds = netCDF4.Dataset(v)
                        if len(ds.dimensions) != 3 or len(set(ds.variables) - set(ds.dimensions)) != 1:
                            missing.append(v.split('_')[-2])
                            print(v)
                    except:
                        missing.append(v.split('_')[-2])

                for m in missing:
                    completes[m] = False

        for c, done in completes.items():
            if not done:
                x = VARS.index(c)
                redo.append((int(year)-2000)*7 + x)
    print(','.join([str(i) for i in sorted(redo)]))
            
if __name__ == '__main__':
    main()