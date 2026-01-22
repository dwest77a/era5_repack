#!/bin/bash
#SBATCH --partition=standard
#SBATCH --account=cedaproc
#SBATCH --qos=standard
#SBATCH --job-name=ERA5_Repack_EDS_AI
#SBATCH --time=60:00
#SBATCH --mem=2G
#SBATCH -o /home/users/dwest77/cedadev/AI/era5_repack/outs/%A_%a.out
#SBATCH -e /home/users/dwest77/cedadev/AI/era5_repack/errs/%A_%a.err
source /home/users/dwest77/cedadev/AI/era5_repack/.venv/bin/activate
python /home/users/dwest77/cedadev/AI/era5_repack/repacker.py $SLURM_ARRAY_TASK_ID