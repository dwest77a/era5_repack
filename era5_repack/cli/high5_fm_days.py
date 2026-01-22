import sys
import math

from era5_repack.repac_daily import assemble_file

def main():

    VARS = "10u 10v 2d 2t msl tcc tcwv".split()

    id  = sys.argv[-1]
    var = VARS[int(id)%len(VARS)]
    yr  = 2000 + math.floor(int(id)/len(VARS))

    with open(f'dfiles/{yr}_{var}.txt') as f:
        files = [r.strip() for r in f.readlines()]
    for fid in range(int(len(files)/24)):
        filesubset = files[fid*24:(fid+1)*24]
        try:
            _ = assemble_file('/gws/ssde/j25b/eds_ai/public/era5_repack/daily_reprocess',filesubset, var)
        except:
            print(f'Failed for {var} {yr} {fid}')

if __name__ == '__main__':
    main()