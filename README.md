# mbs-analysis
Web app for analyzing bike share data for the 2018 Capital One SWE Summit Challenge  

Deployed App on Heroku: https://mbs-analysis.herokuapp.com/  

## Screenshots
![Screenshot 1](https://github.com/vli1721/capital-one-challenge-2018/blob/master/screenshots/mbs-analysis-screenshot1.png)

![Screenshot 5](https://github.com/vli1721/capital-one-challenge-2018/blob/master/screenshots/mbs-analysis-screenshot5.png)

![Screenshot 3](https://github.com/vli1721/capital-one-challenge-2018/blob/master/screenshots/mbs-analysis-screenshot3.png)


## Goals
1. Data Visuals: Display or graph 3 metrics or trends from the data set that are interesting to you.
	1. Metric 1: Average Bike Rentals and Returns Per Hour in a Day *(See Graph 1)*
	2. Metric 2: Average Trip Duration by Passholder Type *(See Graph 2)*
	3. Metric 3: Bike Efficiency - Number of Trips and Total Trip Duration by Bike ID *(See Graph 3)*
2. Which start/stop stations are most popular? *(See Graph 4)*
3. What is the average distance traveled? *(See Graph 5)*
4. How many riders include bike sharing as a regular part of their commute? *(See Graph 6)*
5. (Bonus 1) How does ridership change with seasons? *(See Graph 7)*
6. (Bonus 2) Is there a net change of bikes over the course of a day? If so, when and where should bikes be transported in order to make sure bikes match travel patterns? *(See Graph 8a, 8b)*
7. (Bonus 3) What is the breakdown of Trip Route Category-Passholder type combinations? What might make a particular combination more popular? *(See Graph 9)*


## Design
1. `analysis.py`: Data Analysis using `pandas`
	1. Clean raw CSV
	2. Analyze using dataframes and dictionaries
	3. Write analysis results to CSV files stored in the `/data` folder (these CSV files are rendered in `app.py`)
	4. Note: Executing `python analysis.py` will generate all the CSV files needed to display the results in `app.py`
2. `app.py`: Web App created using Dash (Python framework built on Flask, React.js, and Plotly.js)
	1. Render CSV files from `analysis.py` as graphs
	2. Graphs have toggle option to show/hide bars
	3. Hover over bars to reveal their numerical values
	4. Analysis of each graph is located below the graph

## Assumptions
* I assumed that each trip designates a unique rider and that "regular user" indicates a user who bought a plan (Monthly Pass or Flex Pass).
* Additionally, I initially cleaned the dataset before analysis, removing rows with any NaN values.
* Furthermore, to calculate distance traveled by round trips, I assumed the round trip average speed could be estimated by the average speed of all one-way trips originating from the given station. If the given station did not have an average speed from one-way trips, I used the average speed of all one-way trips from any station.
