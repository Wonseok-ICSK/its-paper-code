# ITS Traffic Analysis Code

Research scripts for analyzing vehicle trajectories, slow vehicles, truck ratios, headway, speed and delay in highD-style highway recordings.

## Where to start

| Path | Purpose |
| --- | --- |
| `src/cv.py` | Shared traffic-analysis and plotting helpers |
| `src/detectSlowVeh.py`, `src/paperDataExtraction.py` | Slow-vehicle analysis and extraction workflows |
| `src/countVehicle_inFrame.py`, `src/truckRatiobyLane.py` | Vehicle counts and lane-level truck ratios |
| `src/spaceHeadway.py`, `src/timeHeadway.py` | Headway analysis |
| `src/integral.py`, `src/accumulateTotalDelay.py` | Cumulative-count and delay experiments |
| `src/drawTrajectory.py`, `src/sectorSpd.py` | Trajectory and speed plots |
| `src/old code/`, `src/BACKUP.py` | Historical variants retained for review |
| `src/README.md` | Original Korean research notes, preserved unchanged |

## Dependencies and data

```console
python -m pip install -r requirement.txt
```

The baseline dependency list constrains SciPy below 1.14 because the unchanged scripts use `scipy.integrate.trapz`. It is an inferred compatibility constraint, not the exact original environment. Python 3.9-3.12 is a practical baseline environment for this legacy SciPy constraint; the source was syntax-checked separately with Python 3.13.

Datasets and generated figures/CSV files are deliberately not uploaded. Supply your authorized dataset separately. Scripts expect files such as `{recording}_tracks.csv`, `{recording}_tracksMeta.csv` and `{recording}_recordingMeta.csv`. Core columns include `id`, `frame`, `laneId`, `xVelocity`, neighbor IDs and headway fields; per-script requirements differ.

Many scripts execute a batch at module load. Inspect the selected recording list and output paths first. Path conventions are mixed: several scripts use `data/` relative to `src`, while others use `../data/`. Arrange local data and output directories for the script you review; there is no single verified end-to-end command for all experiments.

The original nested `.git` directory is not uploaded. This repository starts a new review history from the current selected working files, including local edits. The previous history remains in the original folder.

## Suggested review focus

Frame/time units (many scripts assume 25 fps), lane/direction conventions, missing neighbor observations, denominators, index alignment, dataset paths and plot/output units. Research thresholds and scientific interpretations are retained; reproducing the paper requires the original data and methodology review.

## Review history

- `phase1-original`: the selected source files were imported byte for byte; only repository documentation, dependency lists and Git housekeeping files were added.
- A subsequent update adds English review comments and narrowly scoped fixes. Compare it with `phase1-original` to review the changes.
- Original directory names and sample variants are retained. Source extracted from top-level ZIP files is under `archived-examples/` when present.
- Build outputs, local IDE state, packet captures, datasets, model weights and generated analysis results are excluded. This is a source review repository, not a complete runtime distribution.

## Validation scope

Python source was syntax-checked with Python 3.13 without executing the scripts. Device communication, network traffic, Vehicle Spy integration, Jetson GPIO and full dataset analyses were not run during import. The dependency list, where supplied, is inferred from imports rather than a recovered environment lockfile.

Existing vendor copyright and license notices are retained. No new project-wide license has been assigned.
