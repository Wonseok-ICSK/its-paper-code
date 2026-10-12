# Second-pass Review Notes

Baseline: [`phase1-original`](https://github.com/Wonseok-ICSK/its-paper-code/tree/phase1-original). The updated source is tagged `phase2-reviewed`.

## Scope

English explanations were added to 30 application/example files. Existing Korean comments, user-facing strings, directory names and historical variants were retained. No large refactor or new runtime feature was introduced.

## Corrections

- `src/cv.py`: Use the equivalent supported SciPy trapezoidal integration API without changing spacing or research parameters.
- `src/integral.py`: Use the equivalent supported SciPy trapezoidal integration API without changing spacing or research parameters.
- `src/accumulateTotalDelay.py`: Use the equivalent supported SciPy trapezoidal integration API without changing spacing or research parameters.
- `src/cv.py`: Check the current vehicle's preceding-speed samples before averaging, rather than the outer list.
- `src/cv.py`: Skip undefined speed ratios when the preceding vehicle's mean speed is zero.
- `src/countVehicle_inFrame.py`: Compute the maximum final frame across all metadata rows instead of taking the last row.

## Validation

Five unittest methods passed using synthetic data: known trapezoidal area, stationary preceding vehicle, absent preceding observation, moving-vehicle classification and unsorted metadata end frames.

```console
python -m unittest discover -s tests -v
```

Test environment: Python 3.13, NumPy 2.3.5, pandas 2.3.3, SciPy 1.16.3 and Matplotlib 3.10.8. These versions describe the host checks; they do not recover or lock the original research environment.

## Remaining review items

Datasets and published results were not reproduced. Mixed data paths, empty-observation conventions, units and thresholds remain research-review topics. In particular, detectSlowVehPandas still mixes the original vehicle-speed and converted neighbor-speed units; changing that scientific behavior is beyond this limited pass. The unused alternative detectSlowVehs has index-alignment questions, and avgTT remains a placeholder. No methods or thresholds were redesigned.

The integration API replacement follows the [SciPy 1.14 release notes](https://docs.scipy.org/doc/scipy/release/1.14.0-notes.html).

## Commented files

- `src/accumulateTotalDelay.py`
- `src/averageVehicleNumPerLane.py`
- `src/BACKUP.py`
- `src/chartmod.py`
- `src/colorbar.py`
- `src/comparewTruck.py`
- `src/countVehicle_inFrame.py`
- `src/cv.py`
- `src/data extract.py`
- `src/detectSlowVeh.py`
- `src/drawTrajectory.py`
- `src/dump_conti.py`
- `src/flow graph.py`
- `src/integral.py`
- `src/manipulate_csv.py`
- `src/ncurve.py`
- `src/NewSTD.py`
- `src/paperDataExtraction.py`
- `src/read recording meta.py`
- `src/SectionalState.py`
- `src/sectorSpd.py`
- `src/smoothing N.py`
- `src/spaceHeadway.py`
- `src/speedHisto.py`
- `src/timeHeadway.py`
- `src/truckPoint Trajectory.py`
- `src/truckRatiobyLane.py`
- `src/old code/colourmap.py`
- `src/old code/maint.py`
- `src/old code/new cont colour.py`
