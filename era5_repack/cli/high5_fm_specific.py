import sys
import os
import glob

from era5_repack.repack_daily import assemble_file

def main():

    refills = sys.argv[-1]
    with open(refills) as f:
        files = [r.strip() for r in f.readlines()]
    corruptions = []
    for file in files:
        print(file)
        # /gws/ssde/j25b/eds_ai/public/era5_repack/daily_reprocess/2010/12/07/ecmwf-era5X_oper_an_sfc_20101207_tcwv_repack.nc
        yr, mth, day = file.split('/')[8:11]

        var = file.split('_')[-2]

        era5x = 'era5'
        if int(yr) >= 2000 and int(yr) < 2007:
            era5x = 'era51'

        print(f'/badc/ecmwf-{era5x}/data/oper/an_sfc/{yr}/{mth}/{day}/ecmwf-{era5x}_oper_an_sfc_{yr}{mth}{day}*.{var}.nc')

        filesubset = glob.glob(f'/badc/ecmwf-{era5x}/data/oper/an_sfc/{yr}/{mth}/{day}/ecmwf-{era5x}_oper_an_sfc_{yr}{mth}{day}*.{var}.nc')

        os.system(f'rm {file}')

        try:
            corruptions += assemble_file('/gws/ssde/j25b/eds_ai/public/era5_repack/daily_reprocess',filesubset, var)
        except Exception as err:
            raise err
            print(f'Failed for {var} {yr} {mth} {day}')

    with open('corruption_files.txt','w') as f:
        f.write('\n'.join(corruptions))

if __name__ == '__main__':
    main()