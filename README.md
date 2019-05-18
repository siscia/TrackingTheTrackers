# Tracking the Trackers

Code and data for the Tracking the Tracker project.

In order to repeat the analysis is enough to run:

```bash
cat top10milliondomains.csv | awk -F "," '{ print substr($2, 2, length($2) - 2)}' | head -n 1000 | xargs -n1 -P6 python3 tracker.py
```
