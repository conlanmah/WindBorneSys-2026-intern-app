# WindBorneSys-2026-intern-app
This is my coding challenge for the WindBorne Systems 2026 internship application.

View the live site here: https://windborne-applicaiton-production.up.railway.app/
Although I likely have stopped paying for Railway credits.

[Screenshot showing a world map with colored dots and satellites](/screenshots/Screenshot From 2025-10-27 15-01-20.png?raw=true)

# Explanation

This website creates a global map using leaflet and OpenStreetMap to plot WindBorneSystems Global Sounding Balloons. It then plots NOAA satellites from N2YO's api and calculates the closest satellite for each balloon. Balloons are color coded based on how close they are to a satellite, resulting in a global heat map of satellite access for the WindBorne constellation. This provides availability insights for a constellation that is inherantly hard to access: balloons are spread over massive distances, and contain limited transmission/reception technology resulting in (I presume) spotty availability. While I am not certain about how WindBorne GSBs are communicated with, this technique can be applied to any networking solution due to the fact that geographic distance is a major factor for any form of wireless communication.

# Web Site Break Down

Having a less than extensive background in web development, I vaguely recalled that Django was a widely applicable Python web framework. While I intended to do more server side computing via Python, I ultimately implemented most of the sites features in Javascript--meaning client side--to limit my usage of the free Railway (hosting platform) credits.

I have created a Nix Flake for handling the Python development environment. However for the production build, I could not figure out a way for Railway to deploy the application using Nix. Therefore you see the requirements.txt for buildling this project in a 'traditional' Python environment.
