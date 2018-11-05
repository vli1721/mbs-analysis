import dash
from dash.dependencies import Input, Output, State, Event
import dash_core_components as dcc
import dash_html_components as html
import plotly
import flask
import pandas as pd
import numpy as np


########################################################################################################################
#                        							Helper Functions                         						   #
########################################################################################################################
# Function to Generate Bike Rentals and Returns Graphs for Bonus 2
def generate_bonus_2_graph(df_list, graph_type):
    return dcc.Graph(
        id='{graph_type}-by-ssid-by-hour-graph'.format(graph_type=graph_type),
        figure={
            'data': [
                {'x': list(df_list[i].loc[df_list[i]["Station ID"] < 3100]["Station ID"]),
                	'y': list(df_list[i].loc[df_list[i]["Station ID"] < 3100]["Frequency"]),
                		'type': 'bar', 'name': 'Hour {hour}'.format(hour=i)} for i in range(len(df_list))
            ],
            'layout': {
            	'xaxis': {'title': 'Station ID', 'range': [3000, 3085]},
                'yaxis': {'title': 'Value'},
                'font': {
                	'size': 15,
                    'color': colors['text'],
                }
            }
        }
    )


########################################################################################################################
#                        					Metadata and Analyzed CSV Files                   						   #
########################################################################################################################
app = dash.Dash()
# Set Web App Title
app.title = 'Metro Bike Share Data Analysis'


# Boostrap CSS
app.css.append_css({'external_url':
	'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})

# Read CSV Files with Data Analyzed using "analysis.py"
# Question 1a
num_trips_by_start_hour = pd.read_csv("data/num_trips_by_start_hour.csv")
num_trips_by_end_hour = pd.read_csv("data/num_trips_by_end_hour.csv")

# Question 1b
avg_duration_by_pass = pd.read_csv("data/avg_duration_by_pass.csv")

# Question 1c
bike_trips = pd.read_csv("data/bike_trips.csv")
bike_duration = pd.read_csv("data/bike_duration.csv")

# Question 2
starting_station = pd.read_csv("data/starting_station.csv")
ending_station = pd.read_csv("data/ending_station.csv")
overall_station = pd.read_csv("data/overall_station.csv")

# Question 3
distance_by_ssid = pd.read_csv("data/distance_by_ssid.csv")
avg_distance_by_ssid = pd.read_csv("data/avg_distance_by_ssid.csv")
# Extract total distance, total number of trips, and total average distance from CSV file converted to dictionary
total_distance_stats_dict = pd.read_csv("data/total_distance_stats.csv").to_dict()
total_distance = "{0:.3f}".format(total_distance_stats_dict['Value'][0])
total_num_trips = str(int(total_distance_stats_dict['Value'][1]))
total_avg_distance = "{0:.3f}".format(total_distance_stats_dict['Value'][2])

# Question 4
passholder_type = pd.read_csv("data/passholder_type.csv")

# Bonus 1
duration_by_start_month = pd.read_csv("data/duration_by_start_month.csv")

# Bonus 2
ssid_by_start_hour_list = []
esid_by_end_hour_list = []
for i in range(24):
	hour = ""
	if i < 10:
		hour = "0" + str(i)
	else:
		hour = str(i)
	ssid_by_start_hour_list.append(pd.read_csv("data/bonus_2/ssid_by_start_hour_{hour}.csv".format(hour=hour)))
	esid_by_end_hour_list.append(pd.read_csv("data/bonus_2/esid_by_end_hour_{hour}.csv".format(hour=hour)))


# Colors
colors = {
    'background': '#FFFFFF',
    'text': '#000000'
}

# Text style
text_style = {
    'textAlign': 'left',
    'color': colors['text'],
    'fontSize': 20,
    'marginLeft': 80,
    'marginRight': 80,
    'marginTop': 20,
    'marginBottom': 20,
}

# Title style
title_style = {
	'marginTop': 40,
    'textAlign': 'center',
    'color': colors['text'],
}

# Notice style
notice_style = {
    'textAlign': 'center',
    'color': colors['text'],
    'fontSize': 15,
    'marginLeft': 80,
    'marginRight': 80,
    'marginTop': 20,
}

########################################################################################################################
#                        						  	  Begin App Layout                  			     			   #
########################################################################################################################
app.layout = html.Div(style={'backgroundColor': colors['background'], 'margin': '80px'}, children=[
	html.H1(
        children='Metro Bike Share - Bike Sharing in Los Angeles, CA',
        style={
        	'marginTop': '50px',
        	'marginBottom': '80px',
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
	html.Hr(),

    # Question 1a: Display Metric 1
    # (Average Bike Rentals and Returns Per Hour in a Day = Average Number of Trips by Start Hour and End Hour in a Day)
    html.H2(children='Net Change of Bikes in a Day: Average Bike Rentals and Returns Per Hour', style=title_style),
    dcc.Graph(
        id='trips-hour-graph',
        figure={
            'data': [
                {'x': list(num_trips_by_start_hour["Hour"]),
                	'y': list(num_trips_by_start_hour["Number of Trips"]),
                		'type': 'bar', 'name': 'Rentals'},
                {'x': list(num_trips_by_end_hour["Hour"]),
                	'y': list(num_trips_by_end_hour["Number of Trips"]),
                		'type': 'bar', 'name': 'Returns'},
            ],
            'layout': {
            	'xaxis': {'title': 'Hour', 'range': [-1, 24]},
                'yaxis': {'title': 'Frequency'},
                'font': {
                	'size': 15,
                    'color': colors['text'],
                }
            }
        }
    ),
    html.Div(children='Click on "Rentals" (number of trips that start in specified hour) or '
    	+ '"Returns" (number of trips that end in specified hour) to toggle the bar graph.',
    	style=notice_style),

    html.Div(children='Most popular rental hours: Hour 17 (48.309 rentals), '
    	+ 'Hour 18 (43.382 rentals), Hour 12 (41.746 rentals). '
    	+ 'These hours are busy because they are around dinner time / '
    	+ 'leaving from work (5pm-7pm) and lunch time (12pm-1pm).',
        style=text_style),
    html.Div(children='Most popular return hours: Hour 17 (46.877 returns), '
    	+ 'Hour 18 (45.251 returns), Hour 13 (41.034 returns). '
    	+ 'These hours are busy because they are also around dinner time / '
    	+ 'leaving from work (5pm-7pm) and lunch time (1pm-2pm).',
    	style=text_style),
    html.Div(children='There are more rentals than returns from 12pm-1pm because '
    	+ 'people rent bikes to get to lunch. However, there are more returns than '
    	+ 'rentals from 1pm-2pm because people return bikes after getting back to work '
    	+ 'from lunch. Likewise, there are more rentals than returns from 5pm-6pm because '
    	+ 'people rent bikes to get back home from work or go to eat dinner. There are '
    	+ 'more returns than rentals from 6pm-7pm because people return bikes after they '
    	+ 'have arrived home or at dinner.',
    	style=text_style),
	html.Hr(),


    # Question 1b: Display average trip duration by passholder type
    html.H2(children='Average Trip Duration by Passholder Type', style=title_style),
    dcc.Graph(
        id='avg-duration-by-pass-graph',
        figure={
            'data': [
                {'x': list(avg_duration_by_pass["Passholder Type"]),
                'y': list(avg_duration_by_pass["Average Trip Duration"]),'type': 'bar'},
            ],
            'layout': {
            	'xaxis': {'title': 'Passholder Type'},
                'yaxis': {'title': 'Average Trip Duration (in minutes)'},
                'font': {
                	'size': 15,
                    'color': colors['text'],
                }
            }
        }
    ),
    html.Div(children='Interestingly, the walk-up passholders used their bikes the longest on average (42.613 minutes per trip). '
    	+ 'This may be because the walk-up price is generally higher than the monthly or flex prices, so walk-up passholders '
    	+ 'may wish to use their bikes for longer to get more "bang for their buck". The monthly passholders used their bikes '
    	+ 'the shortest on average (13.107 minutes per trip), while the flex passholders were in the middle (18.466 minutes per trip. '
    	+ 'This may be because the monthly passholders bought the most frequent pass, so their average price per trip is lower '
    	+ 'than the other two passholders (assuming a steady number of trips throughout the month). Flex passholders represent '
    	+ 'a balance between price per trip and duration of trip.',
    	style=text_style),
	html.Hr(),


	# Question 1c: Bike Effiency - Display number of trips and total duration by bike ID
    html.H2(children='Bike Efficiency - Number of Trips and Total Trip Duration by Bike ID', style=title_style),
    dcc.Graph(
        id='bike-graph',
        figure={
            'data': [
                {'x': list(bike_trips.loc[bike_trips["Bike ID"] > 5000]["Bike ID"]),
                	'y': list(bike_trips.loc[bike_trips["Bike ID"] > 5000]["Frequency"]),
                	'type': 'bar', 'name': 'Number of Trips'},
                {'x': list(bike_duration.loc[bike_duration["Bike ID"] > 5000]["Bike ID"]),
                	'y': list(bike_duration.loc[bike_duration["Bike ID"] > 5000]["Duration"]),
                	'type': 'bar', 'name': 'Total Duration (in minutes)'},
            ],
            'layout': {
            	'xaxis': {'title': 'Bike ID'},
                'yaxis': {'title': 'Value'},
                'font': {
                	'size': 15,
                    'color': colors['text'],
                }
            }
        }
    ),
    html.Div(children='Click on "Number of Trips" or "Total Duration (in minutes)" to toggle the bar graph.',
    	style=notice_style),

    html.Div(children='Note that Bike #4727 and Bike #4728 are not displayed in the graph. '
    	+ 'Bike #4727 has 104 trips and total duration of 5815 minutes. '
    	+ 'Bike #4728 has 220 trips (most used bike in terms of number of trips) and total duration of 2031 minutes.',
    	style=text_style),

    html.Div(children='Most used bikes (number of trips): Bike #4727 (220 trips), '
    	+ 'Bike #6608 (215 trips), Bike #5839 (208 trips)',
    	style=text_style),
    html.Div(children='Least used bikes (number of trips): Bike #5906 (1 trip), '
    	+ 'Bike #6342 (6 trips), Bike #6013 (17 trips)',
    	style=text_style),
    html.Div(children='Most used bikes (total duration): Bike #5929 (7616 minutes), '
    	+ 'Bike #5924 (6801 minutes), Bike #5890 (6561 minutes)',
    	style=text_style),
    html.Div(children='Least used bikes (total duration): Bike #5906 (4 minutes), '
    	+ 'Bike #6342 (115 minutes), Bike #6562 (225 minutes)',
    	style=text_style),
    html.Div(children='The most used bikes could be efficiently placed at stations, suggesting that Metro '
    	+ 'Bike Share could potentially analyze the routes of these bikes to determine efficient placement '
    	+ 'for other bikes. On another note, these bikes may be getting old or worn, so they should be '
    	+ 'checked for repairs or replacement.',
    	style=text_style),
    html.Div(children='The least used bikes could have been old bikes or broken ones that '
    	+ 'were soon replaced by newer ones. Alternatively, their placement at stations could be inefficient.',
    	style=text_style),
	html.Hr(),


    # Question 2: Display most popular stations graph
    html.H2(children='Most Popular Stations', style=title_style),
    dcc.Graph(
        id='popular-station-graph',
        figure={
            'data': [
                {'x': list(starting_station.loc[starting_station["Starting Station ID"] < 3100]["Starting Station ID"]),
                	'y': list(starting_station.loc[starting_station["Starting Station ID"] < 3100]["Frequency"]),
                		'type': 'bar', 'name': 'Start Freq'},
                {'x': list(ending_station.loc[ending_station["Ending Station ID"] < 3100]["Ending Station ID"]),
                	'y': list(ending_station.loc[ending_station["Ending Station ID"] < 3100]["Frequency"]),
                		'type': 'bar', 'name': 'End Freq'},
                {'x': list(overall_station.loc[overall_station["Station ID"] < 3100]["Station ID"]),
                	'y': list(overall_station.loc[overall_station["Station ID"] < 3100]["Frequency"]),
                		'type': 'bar', 'name': 'Overall Freq'},
            ],
            'layout': {
            	'xaxis': {'title': 'Station ID', 'range': [3000, 3085]},
                'yaxis': {'title': 'Frequency'},
                'font': {
                	'size': 15,
                    'color': colors['text'],
                }
            }
        }
    ),
    html.Div(children='Click on "Start Freq" (frequency as starting station), "End Freq" (frequency as ending station), '
    	+ 'or "Overall Freq" (combined frequency as starting or ending station) to toggle the bar graph.',
    	style=notice_style),

    html.Div(children='Most popular starting stations: Station #3030 (freq: 3787), '
    	+ 'Station #3069 (freq: 3715), Station #3005 (freq: 3609)',
        style=text_style),
    html.Div(children='Most popular ending stations: Station #3005 (freq: 4621), '
    	+ 'Station #3031 (freq: 4175), Station #3014 (freq: 4091)',
    	style=text_style),
    html.Div(children='Note that Station #4108 is not displayed in the graph. '
    	+ 'Station #4108 has frequency of 34 as Starting Station and frequency of 50 as Ending Station.',
    	style=text_style),
	html.Hr(),


    # Question 3: Display distance/duration by starting station graph
    html.H2(children='Total Distance and Avg Distance Per Trip By Starting Station ID', style=title_style),
    dcc.Graph(
        id='distance-by-ssid-graph',
        figure={
            'data': [
                {'x': list(distance_by_ssid.loc[distance_by_ssid["Station ID"] < 3100]["Station ID"]),
                	'y': list(distance_by_ssid.loc[distance_by_ssid["Station ID"] < 3100]["Total Distance"]),
                		'type': 'bar', 'name': 'Total Distance (in miles)'},
                {'x': list(avg_distance_by_ssid.loc[overall_station["Station ID"] < 3100]["Station ID"]),
                	'y': list(avg_distance_by_ssid.loc[overall_station["Station ID"] < 3100]["Avg Distance"]),
                		'type': 'bar', 'name': 'Avg Distance (in miles per trip)'},
            ],
            'layout': {
            	'xaxis': {'title': 'Starting Station ID', 'range': [3000, 3085]},
                'yaxis': {'title': 'Value'},
                'font': {
                	'size': 15,
                    'color': colors['text'],
                }
            }
        }
    ),
    html.Div(children='Click on "Total Distance (in miles)" or '
    	+ '"Avg Distance (in miles per trip)" to toggle the bar graph.',
    	style=notice_style),
    html.Div(children='The overall average distance across all trips was ' + total_avg_distance
    	+ ' miles (' + total_distance + ' miles in ' + total_num_trips + ' trips).',
        style=text_style),
    html.Div(children='Starting Stations with Highest Total Distance: Station #3014 (3368.913 miles), '
    	+ 'Station #3048 (3002.530 miles), Station #3069 (2943.367 miles)',
        style=text_style),
    html.Div(children='Starting Stations with Highest Total Distance: Station #3014 (3368.913 miles), '
    	+ 'Station #3048 (3002.530 miles), Station #3069 (2943.367 miles)',
        style=text_style),
    html.Div(children='Starting Stations with Highest Avg Distance Per Trip: Station #3020 (2.013 miles), '
    	+ 'Station #3066 (1.675 miles), Station #3078 (1.518 miles)',
        style=text_style),
    html.Div(children='Note that Station #4108 is not displayed in the graph. '
    	+ 'Station #4108 has Total Distance of 101.137 miles and 2.975 miles per trip on average.',
    	style=text_style),
	html.Hr(),


    # Question 4: Display passholder type graph
    html.H2(children='Passholder Types and Number of Regular Users', style=title_style),
    dcc.Graph(
        id='passholder-type-graph',
        figure={
            'data': [
                {'x': list(passholder_type["Passholder Type"]), 'y': list(passholder_type["Frequency"]), 'type': 'bar'},
            ],
            'layout': {
            	'xaxis': {'title': 'Passholder Type'},
                'yaxis': {'title': 'Frequency'},
                'font': {
                	'size': 15,
                    'color': colors['text'],
                }
            }
        }
    ),
    html.Div(children='Metro Bike Share has 67293 regular users (60093 Monthly Pass holders and 7200 Flex Pass holders).',
    	style=text_style),
	html.Hr(),


	# Bonus 1: Seasonal Variations in Ridership: Display avg duration, total duration, and number of trips by start month
    html.H2(children='Seasonal Variations in Ridership: Duration and Number of Trips Per Month', style=title_style),
    dcc.Graph(
        id='duration-by-month-graph',
        figure={
            'data': [
                {'x': list(duration_by_start_month["Month"]), 'y': list(duration_by_start_month["Avg Trip Duration"]),
                	'type': 'bar', 'name': 'Avg Trip Duration (in minutes)'},
                {'x': list(duration_by_start_month["Month"]), 'y': list(duration_by_start_month["Total Trip Duration"]),
                	'type': 'bar', 'name': 'Total Trip Duration (in minutes)'},
                {'x': list(duration_by_start_month["Month"]), 'y': list(duration_by_start_month["Number of Trips"]),
                	'type': 'bar', 'name': 'Number of Trips'},
            ],
            'layout': {
            	'xaxis': {'title': 'Month'},
                'yaxis': {'title': 'Value'},
                'font': {
                	'size': 15,
                    'color': colors['text'],
                }
            }
        }
    ),
    html.Div(children='Click on "Avg Trip Duration (in minutes)", "Total Trip Duration (in minutes)", or '
    	+ '"Number of Trips" to toggle the bar graph.',
    	style=notice_style),
    html.Div(children='August has the highest ridership (avg trip duration, total trip duration, and number of trips). '
    	+ 'All three measurements decline from August to December, probably due to the change from summer to fall to winter. '
    	+ 'This suggests that the cold weather reduces ridership, so ridership is highest at the end of summer and '
    	+ 'declines through fall and winter. July has the lowest ridership, which may be due to summer vacation. '
    	+ 'Ridership may be higher in August than in July because people are usually '
    	+ 'on vacation in July and return to work in August. Additionally, school starts in August.',
    	style=text_style),
	html.Hr(),

	# Bonus 2: Net change of bikes over the course of a day, based on station ID
	html.H2(children='Net Change of Bikes in a Day: Average Hourly Bike Rentals and Returns Per Station ID', style=title_style),

	html.H3(children='Demand: Average Hourly Bike Rentals Per Station ID', style=title_style),
	generate_bonus_2_graph(ssid_by_start_hour_list, "rental"),
	html.Div(children='Click on each Hour to toggle the bar graph.', style=notice_style),
	html.Div(children='Stations with high demand (high avg hourly bike rentals) include Station #3030 '
    	+ '(2.92 rentals in Hour 16, 2.81 rentals in Hour 17, 2.23 rentals in Hour 12), Station #3014 '
    	+ '(2.80 rentals in Hour 7, 2.35 rentals in Hour 8), Station #3005 (2.34 rentals in Hour 18, '
    	+ '2.16 rentals in Hour 19), and Station #3069 (2.41 rentals in Hour 13, 2.04 rentals in Hour 14).',
    	style=text_style),

	html.H3(children='Supply: Average Hourly Bike Returns Per Station ID', style=title_style),
	generate_bonus_2_graph(esid_by_end_hour_list, "return"),
	html.Div(children='Click on each Hour to toggle the bar graph.', style=notice_style),
	html.Div(children='Stations with high supply (high avg hourly bike returns) include Station #3014 '
    	+ '(4.46 returns in Hour 17, 3.61 returns in Hour 16, 2.26 returns in Hour 16), Station #3042 '
    	+ '(3.80 returns in Hour 17, 2.61 returns in Hour 18, 2.39 returns in Hour 16), Station #3005 '
    	+ '(3.09 returns in Hour 8, 2.65 returns in Hour 9), Station #3031 (2.51 returns in Hour 18), '
    	+ 'Station #3069 (2.44 in Hour 12), and Station #3030 (2.23 in Hour 13).',
    	style=text_style),

	html.Div(children='Bikes should be transferred from stations with high supply and low demand to '
		+ 'stations with high demand and low supplyBased on this analysis, Metro Bike Share should '
		+ 'transfer bikes from Station #3042 and Station #3014 to Station #3030 around Hours 16-17 '
		+ 'and Station #3005 around Hours 17-19. Metro Bike Share should also transfer bikes from '
		+ 'Station #3005 to Station #3014 around Hours 7-8.',
    	style=text_style),
	html.Hr(),



    # List Assumptions made
    html.H3(children='Assumptions', style=title_style),
    html.Div(children='I assumed that each trip designates a unique rider and that '
    	+ '"regular user" indicates a user who bought a plan (Monthly Pass or Flex Pass). '
    	+ 'Additionally, I initially cleaned the dataset before analysis, removing rows with any NaN values. '
    	+ 'Furthermore, to calculate distance traveled by round trips, I assumed the round trip average speed '
    	+ 'could be estimated by the average speed of all one-way trips originating from the given station.' 
    	+ 'If the given station did not have an average speed from one-way trips, I used the average speed of '
    	+ 'all one-way trips from any station.',
        style=text_style),
])


if __name__ == '__main__':
    app.run_server(debug=True)