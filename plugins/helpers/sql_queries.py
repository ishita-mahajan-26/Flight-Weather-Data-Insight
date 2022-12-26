class SqlQueries:
    flight_weather_table_insert = ("""
        SELECT 
        md5( f.flightId || w.time ) flight_weather_id ,
        f.flightId, 
        f.FlightDate, 
        CAST(f.CRSDepTime AS int4), 
        f.Origin, 
        f.Dest, 
        CASE WHEN f.ArrDelay is not null OR f.ArrDelay != 0.0 THEN True ELSE False end,
        CASE  f.Cancelled WHEN 1.00 THEN True ELSE False END,
        CASE f.WeatherDelay
            WHEN '0.00' THEN False 
            WHEN ' ' THEN False 
            WHEN '' THEN False
            ELSE True 
            END,
        CASE f.Diverted WHEN 0.00 THEN False ELSE True END,
        w.location , w.time , w.maxtempC , w.mintempC , w.tempC , w.weather_Desc 
        from 
        flight as f 
        JOIN
        weather as w 
        ON f.FlightDate = w.date AND SUBSTRING(f.CRSDepTime, 1, 2) = SUBSTRING(w.time, 1, 2)
    """)

    weather_table_insert = ("""
        SELECT distinct 
        "date", 
        location,
        CASE len("time") 
        WHEN 3 THEN concat('0', "time")
        WHEN 1 THEN CONCAT('000', "time")
        ELSE "time" END,
        cast (mintempC as int4), 
        cast (maxtempF as int4), 
        sunHour, 
        cast (mintempF as int4), 
        cast (maxtempC as int4),
        cast (uvIndex as int4), 
        cast (tempC as int4), 
        cast (windspeedKmph as int4), 
        weather_Desc, 
        cast (HeatIndexC as int4), 
        cast (visibility as int4), 
        cast (weatherCode as int4), 
        cast (humidity as int4)
        FROM staging_weather
    """)

    location_table_insert = ("""
        SELECT DISTINCT * from
        (SELECT distinct 
            Origin, 
            OriginCityName, 
            OriginState, 
            OriginStateFips, 
            OriginStateName
        FROM staging_flights
        union
        SELECT distinct 
            Dest, 
            DestCityName, 
            DestState, 
            DestStateFips, 
            DestStateName
        FROM staging_flights)
    """)

    flight_table_insert = ("""
           SELECT DISTINCT  
           md5( TailNum|| CRSArrTime) flightId, FlightDate, TailNum, FlightNum, Origin, Dest, CRSDepTime, CRSArrTime, ArrTime, ArrDelay, Cancelled, WeatherDelay, Diverted 
            FROM
            staging_flights
    """)
    
    songplay_table_insert = ("""
        SELECT
                md5(events.sessionid || events.start_time) songplay_id,
                events.start_time, 
                events.userid, 
                events.level, 
                songs.song_id, 
                songs.artist_id, 
                events.sessionid, 
                events.location, 
                events.useragent
                FROM (SELECT TIMESTAMP 'epoch' + ts/1000 * interval '1 second' AS start_time, *
            FROM staging_events
            WHERE page='NextSong') events
            LEFT JOIN staging_songs songs
            ON events.song = songs.title
                AND events.artist = songs.artist_name
                AND events.length = songs.duration
    """)

    user_table_insert = ("""
        SELECT distinct userid, firstname, lastname, gender, level
        FROM staging_events
        WHERE page='NextSong'
    """)

    song_table_insert = ("""
        SELECT distinct song_id, title, artist_id, year, duration
        FROM staging_songs
    """)

    artist_table_insert = ("""
        SELECT distinct artist_id, artist_name, artist_location, artist_latitude, artist_longitude
        FROM staging_songs
    """)

    time_table_insert = ("""
        SELECT start_time, extract(hour from start_time), extract(day from start_time), extract(week from start_time), 
               extract(month from start_time), extract(year from start_time), extract(dayofweek from start_time)
        FROM songplays
    """)