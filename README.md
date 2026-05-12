# NYC Shooting Incidents: When and Where Does Gun Violence Happen?

🌐 **Website**: [yilan-h.github.io/socialdata2026](https://yilan-h.github.io/socialdata2026/)  
📓 **Explainer Notebook**: [GitHub](https://github.com/yilan-h/socialdata2026/blob/main/NYC_Shootings_Explainer.ipynb)

---

## About

This project analyzes 20 years of NYPD shooting incident data (2006–2025) to uncover when and where gun violence happens in New York City. The story moves from the long-term time trend, to the geographic concentration across boroughs, to the time-of-day and weekday patterns.

**Dataset**: [NYPD Shooting Incident Data (Historic)](https://data.cityofnewyork.us/Public-Safety/NYPD-Shooting-Incident-Data-Historic-/833y-fsy8) — NYC Open Data  
**Records**: 23,988 incidents · 13 variables · 2006–2025

---

## Files

```
├── index.html                    # Main website (Magazine Style)
├── viz_annual.html               # Figure 1: Annual trend (Plotly)
├── viz_map.html                  # Figure 2: Geographic heatmap with year slider
├── viz_heatmap.html              # Figure 3: Hour × Weekday heatmap with borough filter
├── NYC_Shootings_Explainer.ipynb # Explainer notebook (7 sections)
├── build_viz.py                  # Script to regenerate visualizations
└── README.md
```

---

## Reproducing the Visualizations

```bash
python build_viz.py
```

Requires: `pandas` `numpy` `plotly` `folium`
