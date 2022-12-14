## WEATHER APP

I wrote this weather app for a friend. It connects to the ZAMG api and plots the past temperature, rainfall, and wind speed of a chosen time period and a chosen weather station.

The date range is restricted to 2015 to now (for now) and might be changed in the future. I'm still working on the app, hence features might change, or new plots will appear, maybe a slightly nicer layout, etc. (And hopefully I will update the README accordingly)

This app is written in **python** with **dash/plotly**.

The file *station_ids.csv* contains a list with station IDs and station areas as well as the county in which the station is located.

To create a docker container to run the app: *docker build -t weather_app .*

And to run it: *docker run -d --name weather_app -p 8080:80 weather_app*