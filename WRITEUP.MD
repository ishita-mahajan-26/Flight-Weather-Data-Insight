## Example Query:

-- Query to get weather description for all airports with location information in the month of June in cases where the flight was delayed
<p>select 
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
</p>

[output_of the above_query](https://github.com/ishita-mahajan-26/Flight-Weather-Data-Insight/blob/main/210548-1672080909202.csv)

### Flight Dataset loaded in S3: 

![flight_s3](https://github.com/ishita-mahajan-26/Flight-Weather-Data-Insight/blob/main/snapshots/flight_s3.png)

### Weather Dataset loaded in S3:

![ETL](https://github.com/ishita-mahajan-26/Flight-Weather-Data-Insight/blob/main/snapshots/weather_s3.png)
![ETL](https://github.com/ishita-mahajan-26/Flight-Weather-Data-Insight/blob/main/snapshots/weather_json_s3.png)

### Details about tables in redshift

![ETL](https://github.com/ishita-mahajan-26/Flight-Weather-Data-Insight/blob/main/snapshots/table_counts.png)
![ETL](https://github.com/ishita-mahajan-26/Flight-Weather-Data-Insight/blob/main/snapshots/tables_in_redshift.png)
