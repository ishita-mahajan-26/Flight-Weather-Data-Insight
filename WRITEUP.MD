Example Query:

-- find out weather description for all airports in the month of June where the flight was delayed
select 
flightid, 
flightdate,
origin,
weather_desc,
locationcode,
locationname,
locationstatename
from 
flight_weather as f
join 
location as l
on 
l.locationcode = f.origin
where extract(month from flightdate) = 6 and arrdelay = true

[output_of the above_query]:

--
