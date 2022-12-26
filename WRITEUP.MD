## Example Query:

-- Query to get weather description for all airports with location information in the month of June in cases where the flight was delayed
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

[output_of the above_query]:https://github.com/ishita-mahajan-26/Flight-Weather-Data-Insight/blob/main/210548-1672080909202.csv

-- Flight Dataset loaded in S3: 

[flight_data]:

-- Weather Dataset loaded in S3:

