# era5_repack
Repacking ERA5 data without differing scale factors and offsets

# High5_FM_Days

Run repacking for a specific year/var combination (designated by id from 0 to 140)
- This will repack all hourly files into daily aggregations (with no scale factor/offset) for each day in a year for that variable.

# High5_FM_Specific

Run repacking for a specific set of daily files (due to past failures)
- Takes a list of repacked daily files from above to retry packing, due to failures in computation.

# Isitthere

Run this to determine any gaps in the ERA5 repacked dataset directories/files. Will give a set of ids that are missing at the end, that can each be put into High5_FM_Days.