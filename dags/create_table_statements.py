CREATE_ARTISTS_TABLE_SQL = """
CREATE TABLE public.artists (
	artistid varchar(256) NOT NULL,
	name varchar(256),
	location varchar(256),
	lattitude numeric(18,0),
	longitude numeric(18,0)
);
"""
CREATE_ARTISTS_SONGPLAYS_SQL = """
CREATE TABLE public.songplays (
	playid varchar(32) NOT NULL,
	start_time timestamp NOT NULL,
	userid int4 NOT NULL,
	"level" varchar(256),
	songid varchar(256),
	artistid varchar(256),
	sessionid int4,
	location varchar(256),
	user_agent varchar(256),
	CONSTRAINT songplays_pkey PRIMARY KEY (playid)
);
"""

CREATE_SONGS_TABLE_SQL = """
CREATE TABLE public.songs (
	songid varchar(256) NOT NULL,
	title varchar(256),
	artistid varchar(256),
	"year" int4,
	duration numeric(18,0),
	CONSTRAINT songs_pkey PRIMARY KEY (songid)
);
"""
CREATE_STAGING_EVENTS_TABLE_SQL = """
CREATE TABLE public.staging_events (
	artist varchar(256),
	auth varchar(256),
	firstname varchar(256),
	gender varchar(256),
	iteminsession int4,
	lastname varchar(256),
	length numeric(18,0),
	"level" varchar(256),
	location varchar(256),
	"method" varchar(256),
	page varchar(256),
	registration numeric(18,0),
	sessionid int4,
	song varchar(256),
	status int4,
	ts int8,
	useragent varchar(256),
	userid int4
);
"""

CREATE_STAGING_SONGS_TABLE_SQL = """
CREATE TABLE public.staging_songs (
	num_songs int4,
	artist_id varchar(256),
	artist_name varchar(256),
	artist_latitude numeric(18,0),
	artist_longitude numeric(18,0),
	artist_location varchar(256),
	song_id varchar(256),
	title varchar(256),
	duration numeric(18,0),
	"year" int4
);
"""

CREATE_TIME_TABLE_SQL = """
CREATE TABLE public."time" (
	start_time timestamp NOT NULL,
	"hour" int4,
	"day" int4,
	week int4,
	"month" varchar(256),
	"year" int4,
	weekday varchar(256),
	CONSTRAINT time_pkey PRIMARY KEY (start_time)
);
"""

CREATE_USERS_TABLE_SQL = """
CREATE TABLE public.users (
	userid int4 NOT NULL,
	first_name varchar(256),
	last_name varchar(256),
	gender varchar(256),
	"level" varchar(256),
	CONSTRAINT users_pkey PRIMARY KEY (userid)
);
"""

# COPY_SQL = """
# COPY {}
# FROM '{}'
# ACCESS_KEY_ID '{{}}'
# SECRET_ACCESS_KEY '{{}}'
# IGNOREHEADER 1
# DELIMITER ','
# """

# COPY_MONTHLY_TRIPS_SQL = COPY_SQL.format(
#     "trips",
#     "s3://udacity-dend/data-pipelines/divvy/partitioned/{year}/{month}/divvy_trips.csv"
# )

# COPY_ALL_TRIPS_SQL = COPY_SQL.format(
#     "trips",
#     "s3://udacity-dend/data-pipelines/divvy/unpartitioned/divvy_trips_2018.csv"
# )

# COPY_STATIONS_SQL = COPY_SQL.format(
#     "stations",
#     "s3://udacity-dend/data-pipelines/divvy/unpartitioned/divvy_stations_2017.csv"
# )

# LOCATION_TRAFFIC_SQL = """
# BEGIN;
# DROP TABLE IF EXISTS station_traffic;
# CREATE TABLE station_traffic AS
# SELECT
#     DISTINCT(t.from_station_id) AS station_id,
#     t.from_station_name AS station_name,
#     num_departures,
#     num_arrivals
# FROM trips t
# JOIN (
#     SELECT
#         from_station_id,
#         COUNT(from_station_id) AS num_departures
#     FROM trips
#     GROUP BY from_station_id
# ) AS fs ON t.from_station_id = fs.from_station_id
# JOIN (
#     SELECT
#         to_station_id,
#         COUNT(to_station_id) AS num_arrivals
#     FROM trips
#     GROUP BY to_station_id
# ) AS ts ON t.from_station_id = ts.to_station_id
# """
