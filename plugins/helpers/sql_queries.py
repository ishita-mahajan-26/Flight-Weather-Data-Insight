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
        w.time , 
        w.maxtempC , 
        w.mintempC , 
        w.tempC , 
        w.weather_Desc 
        from 
        flight as f 
        JOIN
        weather as w 
        ON f.FlightDate = w.date 
        AND SUBSTRING(f.CRSDepTime, 1, 2) = SUBSTRING(w.time, 1, 2)
        and w.location = f.Origin
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
           md5( TailNum|| CRSArrTime) flightId, 
           FlightDate, 
           TailNum, 
           FlightNum, 
           Origin, 
           Dest, 
           CRSDepTime, 
           CRSArrTime, 
           ArrTime, 
           ArrDelay, 
           Cancelled, 
           WeatherDelay, 
           Diverted 
           FROM staging_flights
    """)
