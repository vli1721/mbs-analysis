import pandas as pd
import math

def main():
	########################################################################################################################
	#     													Data Cleaning												   #
	########################################################################################################################
	# Read CSV file, dropping NaN rows to clean data
	data = pd.read_csv("data/metro-bike-share-trip-data.csv").dropna()

	# Some rows in the data have (0.0, 0.0) as the (latitude, longitude) of stations
	# while other rows may have nonzero latitude and longitude for the same station.
	# Therefore, create a dictionary mapping station ID to a nonzero (latitude, longitude) tuple, if it exists.
	# These latitudes and longitudes will be used in later calculations.
	station_location = dict()

	for index, row in data.iterrows():
		# Starting station ID
		ssid = row["Starting Station ID"]
		# Ending station ID
		esid = row["Ending Station ID"]

		# Latitude and Longitude of starting station
		lat1 = row["Starting Station Latitude"]
		lon1 = row["Starting Station Longitude"]
		# Latitude and Longitude of ending station
		lat2 = row["Ending Station Latitude"]
		lon2 = row["Ending Station Longitude"]

		if lat1 != 0 and lon1 != 0 and ssid not in station_location:
			station_location[ssid] = (lat1, lon1)

		if lat2 != 0 and lon2 != 0 and esid not in station_location:
			station_location[esid] = (lat2, lon2)

	# Constants
	# For start times, data collection starts at "2016-07-07T04:17:00" and ends at "2016-12-31T23:26:00"
	# (found by data["Start Time"].min() and data["Start Time"].max() respectively)
	# Therefore, we are looking at 178 days of start time data
	START_NUM_DAYS = 178

	# For end times, data collection starts at "2016-07-07T04:20:00" and ends at "2017-01-01T18:01:00"
	# (found by data["End Time"].min() and data["End Time"].max() respectively)
	# Therefore, we are looking at 179 days of end time data
	END_NUM_DAYS = 179


	# ########################################################################################################################
	# #                              		Question 1 - Display or graph 3 metrics or trends                                  #
	# ########################################################################################################################
	# # Metric 1 - Bike Rentals and Returns Per Hour in a Day (Number of trips per start hour and end hour)
	# # Average number of trips (per day) starting in hour given by index
	# num_trips_by_start_hour = []

	# # Average number of trips (per day) ending in hour given by index
	# num_trips_by_end_hour = []
	# for i in range(24):
	# 	hour = ""
	# 	if i < 10:
	# 		hour = "0" + str(i)
	# 	else:
	# 		hour = str(i)
	# 	num_trips_by_start_hour.append(1.0 / START_NUM_DAYS *
	# 		len(data.loc[data["Start Time"].str.contains(r"{hour}:\d\d:\d\d".format(hour=hour), regex=True)]["Start Time"]))

	# 	num_trips_by_end_hour.append(1.0 / END_NUM_DAYS * 
	# 		len(data.loc[data["End Time"].str.contains(r"{hour}:\d\d:\d\d".format(hour=hour), regex=True)]["End Time"]))

	# hours_list = [i for i in range(24)]

	# # Export dataframe of number of trips by start hour to CSV
	# num_trips_by_start_hour_df = pd.DataFrame.from_dict({"Hour": hours_list, "Number of Trips": num_trips_by_start_hour})
	# num_trips_by_start_hour_df.to_csv("data/num_trips_by_start_hour.csv")

	# # Export dataframe of number of trips by start hour to CSV
	# num_trips_by_end_hour_df = pd.DataFrame.from_dict({"Hour": hours_list, "Number of Trips": num_trips_by_end_hour})
	# num_trips_by_end_hour_df.to_csv("data/num_trips_by_end_hour.csv")


	# # Metric 2 - Average Trip Duration by Passholder Type
	# # List of passholder types
	# pass_types = ["Monthly Pass", "Walk-up", "Flex Pass"]
	# # Compute average duration (converting seconds to minutes) by filtering dataframe by passholder type
	# avg_duration_by_pass = []
	# for pass_type in pass_types:
	# 	avg_duration_by_pass.append(data.loc[data["Passholder Type"] == pass_type]["Duration"].mean() / 60.0)
	# # Export dataframe of average trip duration by passholder type to CSV
	# avg_duration_by_pass_df = pd.DataFrame.from_dict({"Passholder Type": pass_types, "Average Trip Duration": avg_duration_by_pass})
	# avg_duration_by_pass_df.to_csv("data/avg_duration_by_pass.csv")


	# # Metric 3 - Efficiency of Bikes: Total number of trips and total duration by Bike ID
	# # Total number of trips by Bike ID
	# bike_trips_df = data["Bike ID"].value_counts().to_frame("Frequency")
	# bike_trips_df.index.name = "Bike ID"
	# bike_trips_df.to_csv("data/bike_trips.csv")

	# # Total Duration by Bike ID
	# # Dictionary mapping bike ID (key) to total duration that bike is used (value)
	# bike_duration_dict = dict()
	# for index, row in data.iterrows():
	# 	bike_id = row["Bike ID"]
	# 	# Convert duration from seconds to minutes
	# 	duration = 1.0 * row["Duration"] / 60
	# 	if bike_id not in bike_duration_dict:
	# 		bike_duration_dict[bike_id] = duration
	# 	else:
	# 		bike_duration_dict[bike_id] += duration

	# # Convert bike_duration_dict to list of keys and list of values to convert to dataframe and export to CSV
	# bike_duration_keys = []
	# bike_duration_vals = []
	# # Iterate through bike_duration_dict
	# for key, val in bike_duration_dict.items():
	# 	bike_duration_keys.append(key)
	# 	bike_duration_vals.append(val)

	# # Export dataframe of bike total durations to CSV
	# bike_duration_df = pd.DataFrame.from_dict({"Bike ID": bike_duration_keys, "Duration": bike_duration_vals})
	# bike_duration_df.to_csv("data/bike_duration.csv")


	# ########################################################################################################################
	# #                              Question 2 - Which start/stop stations are most popular?                                #
	# ########################################################################################################################
	# # Export dataframe of starting station frequencies sorted in descending order to CSV
	# starting_station_df = data["Starting Station ID"].value_counts().to_frame("Frequency")
	# starting_station_df.index.name = "Starting Station ID"
	# starting_station_df.to_csv("data/starting_station.csv")

	# # Export dataframe of ending station frequencies sorted in descending order to CSV
	# ending_station_df = data["Ending Station ID"].value_counts().to_frame("Frequency")
	# ending_station_df.index.name = "Ending Station ID"
	# ending_station_df.to_csv("data/ending_station.csv")

	# # Export dataframe of overall station frequencies (starting + ending) sorted in descending order to CSV
	# overall_station_df = starting_station_df.add(ending_station_df, fill_value=0).sort_values("Frequency", ascending=False)
	# overall_station_df.index.name = "Station ID"
	# overall_station_df.to_csv("data/overall_station.csv")


	# ########################################################################################################################
	# #     								Question 3 - What is the average distance traveled?							 	   #
	# ########################################################################################################################
	# # Filter data by one way trips (OWT)
	# OWT_df = data.loc[data["Trip Route Category"] == "One Way"]


	# # Dictionary of list of OWT distances (in miles), based on starting station ID as the key
	# OWT_distance_list_dict = dict()

	# # Dictionary of sum of OWT durations (in minutes) for each starting station ID (key)
	# OWT_duration_sum_dict = dict()

	# # Dictionary to track total distance (in miles) for each starting station ID (key)
	# distance_by_ssid_dict = dict()

	# # Dictionary to track total number of trips for each starting station ID (key)
	# num_trips_by_ssid_dict = dict()

	# # Track total distance (in miles) across all trips
	# total_distance = 0

	# # Track total duration (in minutes) across all trips
	# total_duration = 0

	# # Track total number of trips
	# num_trips = 0

	# for index, row in OWT_df.iterrows():
	# 	# Starting station ID
	# 	ssid = row["Starting Station ID"]
	# 	# Ending station ID
	# 	esid = row["Ending Station ID"]

	# 	# Calculate distance between start and end, using latitude and longitude stored in station_location dictionary
	# 	# Note: Pre-checked that each ssid and esid are in station_location dictionary, so there will be no key errors
	# 	lat1 = station_location[ssid][0]
	# 	lon1 = station_location[ssid][1]
	# 	lat2 = station_location[esid][0]
	# 	lon2 = station_location[esid][1]
	# 	distance = dist_from_lat_lon(lat1, lon1, lat2, lon2)
		
	# 	# Add current trip distance to list by starting station ID in dictionary
	# 	if ssid not in OWT_distance_list_dict:
	# 		OWT_distance_list_dict[ssid] = [distance]
	# 	else:
	# 		OWT_distance_list_dict[ssid].append(distance)

	# 	# Add distance to total distance tracker
	# 	total_distance += distance

	# 	# Add distance to distance_by_ssid dict
	# 	if ssid not in distance_by_ssid_dict:
	# 		distance_by_ssid_dict[ssid] = distance
	# 	else:
	# 		distance_by_ssid_dict[ssid] += distance

	# 	# Increment number of trips tracker
	# 	num_trips += 1

	# 	# Increment num_trips_by_ssid_dict
	# 	if ssid not in num_trips_by_ssid_dict:
	# 		num_trips_by_ssid_dict[ssid] = 1
	# 	else:
	# 		num_trips_by_ssid_dict[ssid] += 1

	# 	# Convert duration from seconds to minutes
	# 	duration = 1.0 * row["Duration"] / 60

	# 	# Add current trip duration to sum of durations for specified station ID in dictionary
	# 	if ssid not in OWT_duration_sum_dict:
	# 		OWT_duration_sum_dict[ssid] = duration
	# 	else:
	# 		OWT_duration_sum_dict[ssid] += duration

	# 	# Add duration to total duration tracker
	# 	total_duration += duration

	# # Dictionary to store avg speed of trips starting from station ID (key)
	# OWT_avg_speed_dict = dict()
	# for ssid in OWT_distance_list_dict:
	# 	OWT_avg_speed_dict[ssid] = 1.0 * sum(OWT_distance_list_dict[ssid]) / OWT_duration_sum_dict[ssid]

	# overall_OWT_avg_speed = 1.0 * total_distance / total_duration

	# # Calculate distance for round trips (RT) from a specific station ID by multiplying
	# # trip duration by average speed for OWT originating from the specific station ID
	# RT_df = data.loc[data["Trip Route Category"] == "Round Trip"]
	# for index, row in RT_df.iterrows():
	# 	# Starting station ID (equivalent to ending station ID for round trips)
	# 	ssid = row["Starting Station ID"]
	# 	# Convert duration from seconds to minutes
	# 	duration = 1.0 * row["Duration"] / 60

	# 	# Estimate distance for round trip by multiply duration by average speed for OWT from specified station ID
	# 	# If specified station ID has no average speed for OWT, use overall average speed for OWT
	# 	estimated_distance = 0
	# 	if ssid in OWT_avg_speed_dict:
	# 		estimated_distance = duration * OWT_avg_speed_dict[ssid]
	# 	else:
	# 		estimated_distance = duration * overall_OWT_avg_speed

	# 	# Add distance to total distance tracker
	# 	total_distance += distance

	# 	# Add distance to distance_by_ssid dict
	# 	if ssid not in distance_by_ssid_dict:
	# 		distance_by_ssid_dict[ssid] = estimated_distance
	# 	else:
	# 		distance_by_ssid_dict[ssid] += estimated_distance

	# 	# Increment number of trips tracker
	# 	num_trips += 1

	# 	# Increment num_trips_by_ssid_dict
	# 	if ssid not in num_trips_by_ssid_dict:
	# 		num_trips_by_ssid_dict[ssid] = 1
	# 	else:
	# 		num_trips_by_ssid_dict[ssid] += 1

	# # Convert distance_by_ssid_dict to list of keys and list of values to convert to dataframe and export to CSV
	# ssid_keys = []
	# distance_by_ssid_vals = []
	# # List to store average distance values (list of keys is same as distance_by_ssid keys)
	# avg_distance_by_ssid = []

	# # Iterate through distance_by_ssid_dict
	# for key, val in distance_by_ssid_dict.items():
	# 	ssid_keys.append(key)
	# 	distance_by_ssid_vals.append(val)
	# 	avg_distance_by_ssid.append(1.0 * val / num_trips_by_ssid_dict[key])

	# # Export dataframe of distance by starting station to CSV
	# distance_by_ssid_df = pd.DataFrame.from_dict({"Station ID": ssid_keys, "Total Distance": distance_by_ssid_vals})
	# distance_by_ssid_df.to_csv("data/distance_by_ssid.csv")

	# # Export dataframe of avg distance by starting station to CSV
	# avg_distance_by_ssid_df = pd.DataFrame.from_dict({"Station ID": ssid_keys, "Avg Distance": avg_distance_by_ssid})
	# avg_distance_by_ssid_df.to_csv("data/avg_distance_by_ssid.csv")

	# # Average distance traveled (in miles) per trip
	# total_avg_distance = 1.0 * total_distance / num_trips

	# # Export dataframe of total distance stats to CSV
	# total_distance_df = pd.DataFrame.from_dict({"Stat": ["total_distance", "num_trips", "total_avg_distance"], "Value": [total_distance, num_trips, total_avg_distance]})
	# total_distance_df.to_csv("data/total_distance_stats.csv")


	# ########################################################################################################################
	# # 					Question 4 - How many riders include bike sharing as a regular part of their commute?   		   #
	# ########################################################################################################################
	# passholder_type_df = data["Passholder Type"].value_counts().to_frame("Frequency")
	# passholder_type_df.index.name = "Passholder Type"
	# passholder_type_df.to_csv("data/passholder_type.csv")


	# ########################################################################################################################
	# #                             	 	Bonus 1 - How does ridership change with seasons?                                  #
	# ########################################################################################################################
	# # Average trip duration per starting month
	# # For start times, data collection starts at "2016-07-07T04:17:00" and ends at "2016-12-31T23:26:00"
	# # (found by data["Start Time"].min() and data["Start Time"].max() respectively)
	# # Therefore, we are looking at months 7-12

	# # List of average trip duration for month given by (index + 7)
	# avg_duration_by_start_month = []
	# # List of total trip duration for month given by (index + 7)
	# total_duration_by_start_month = []
	# # List of number of trips for month given by (index + 7)
	# num_trips_by_start_month = []

	# for i in range(7, 13):
	# 	month = ""
	# 	if i < 10:
	# 		month = "0" + str(i)
	# 	else:
	# 		month = str(i)
	# 	filtered_data_by_month = data.loc[data["Start Time"].str.contains(r"\d\d\d\d-{month}-\d\dT".format(month=month), regex=True)]
		
	# 	# Convert durations from seconds to minutes
	# 	avg_duration_by_start_month.append(filtered_data_by_month["Duration"].mean() / 60.0)
	# 	total_duration_by_start_month.append(filtered_data_by_month["Duration"].sum() / 60.0)
	# 	num_trips_by_start_month.append(len(filtered_data_by_month["Duration"]))


	# months_list = [i for i in range(7, 13)]

	# # Export dataframe of number of trips by start hour to CSV
	# duration_by_start_month_df = pd.DataFrame.from_dict({"Month": months_list, "Avg Trip Duration": avg_duration_by_start_month,
	# 	"Total Trip Duration": total_duration_by_start_month, "Number of Trips": num_trips_by_start_month})
	# duration_by_start_month_df.to_csv("data/duration_by_start_month.csv")


	# ########################################################################################################################
	# #                        	Bonus 2 - Is there a net change of bikes over the course of a day?                         #
	# ########################################################################################################################
	# # Calculate hourly supply (returns) and demand (rentals) for each station ID for each hour of the day
	# for i in range(24):
	# 	hour = ""
	# 	if i < 10:
	# 		hour = "0" + str(i)
	# 	else:
	# 		hour = str(i)

	# 	# For each hour, filter data by start hour and write to CSV a dataframe with frequency of bike rental at each station ID
	# 	# (divide frequency by total number of start days)
	# 	filtered_data_by_start_hour = data.loc[data["Start Time"].str.contains(r"{hour}:\d\d:\d\d".format(hour=hour), regex=True)]
	# 	ssid_by_start_hour_df = filtered_data_by_start_hour["Starting Station ID"].value_counts().divide(START_NUM_DAYS).to_frame("Frequency")
	# 	ssid_by_start_hour_df.index.name = "Station ID"
	# 	ssid_by_start_hour_df.to_csv("data/bonus_2/ssid_by_start_hour_{hour}.csv".format(hour=hour))

	# 	# For each hour, filter data by end hour and write to CSV a dataframe with frequency of bike return at each station ID
	# 	# (divide frequency by total number of end days)
	# 	filtered_data_by_end_hour = data.loc[data["End Time"].str.contains(r"{hour}:\d\d:\d\d".format(hour=hour), regex=True)]
	# 	esid_by_end_hour_df = filtered_data_by_end_hour["Ending Station ID"].value_counts().divide(END_NUM_DAYS).to_frame("Frequency")
	# 	esid_by_end_hour_df.index.name = "Station ID"
	# 	esid_by_end_hour_df.to_csv("data/bonus_2/esid_by_end_hour_{hour}.csv".format(hour=hour))


	########################################################################################################################
	#              	Bonus 3 - What is the breakdown of Trip Route Category-Passholder type combinations?                   #
	########################################################################################################################
	# For each of 3 pass types, compute frequency of each route (ssid-esid)
	pass_types = ["Monthly Pass", "Walk-up", "Flex Pass"]
	for pass_type in pass_types:
		# Filter data by pass_type
		filtered_data_by_pass = data.loc[data["Passholder Type"] == pass_type]
		# Dictionary that maps a string of "ssid-esid" representing the route (for example: '5534-5340') to the frequency of this route
		route_dict = dict()
		for index, row in filtered_data_by_pass.iterrows():
			ssid = row["Starting Station ID"]
			esid = row["Ending Station ID"]
			key = str(int(ssid)) + "-" + str(int(esid))
			if key not in route_dict:
				route_dict[key] = 1
			else:
				route_dict[key] += 1

		route_keys = []
		route_vals = []
		for key, val in route_dict.items():
			route_keys.append(key)
			route_vals.append(val)

		# Export dataframe of average trip duration by passholder type to CSV
		route_df = pd.DataFrame.from_dict({"Route": route_keys, "Frequency": route_vals})
		route_df.to_csv("data/bonus_3/route_by_pass_type_{first_letter}.csv".format(first_letter=pass_type[0]))



# Calculate distance between two points, given latitude and longitude
# Adapted from https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula
def dist_from_lat_lon(lat1, lon1, lat2, lon2):
	# Radius of the earth in km
	R = 6371.0
	# Convert degrees to radians for use in sin and cos
	dLat = math.radians(lat2-lat1);
	dLon = math.radians(lon2-lon1); 
	a = 1.0 * math.sin(dLat/2) * math.sin(dLat/2)
	a += 1.0 * math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon/2) * math.sin(dLon/2)
	c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1-a))
	# Return distance in miles
	return R * c / 1.609


if __name__ == "__main__":
	main()