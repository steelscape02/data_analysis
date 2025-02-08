# Overview

This project was designed to find the optimal times in your location to be outside. Research has found that the optimal temperature for our bodies is between 68 and 77 degrees F. Using this information and with the assistance of the NCEI NOAA GSOM (Global Summary of the Month) weather API, I created an applet using tkinter and pandas to display the average monthly temperatures in a given area over the past 5 years. I then added shaded regions to the graph, displaying optimal temperatures to be outside as well as extreme temperatures during which precautions should be taken to avoid injury.

[Software Demo Video](https://youtu.be/citohErx5mc)

# Data Analysis Results

Using this analysis, I was able to understand the optimal months to spend additional time outside. Of course, time spent outside is always beneficial, but evidence suggests additional benefits when time outside is spent in optimal temperatures (68 to 77 degrees F).

# Development Environment

For this program, I used Python with the assistance of the Pandas, Matplotlib, and tkinter packages. This program was originally developed in Visual Studio Code, 
which allows for a simple and streamlined Python development experience.

# Useful Websites

* [Optimal and Extreme temperatures to be outside](https://www.healthline.com/health/extreme-temperature-safety)
* [NCEI NOAA GSOM location and station ID's](https://www.ncei.noaa.gov/access/search/data-search/global-summary-of-the-month)

# Future Work

* Add a autocomplete location entry box using a location API (ex: Google Maps Place Autocomplete API)
* Rewrite in C# to build as a WinUI 3 application for simple usability
* Simplify view to either show graph or a text summary with optimal times for outdoor recreation and other activities