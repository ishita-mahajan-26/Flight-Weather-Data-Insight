# Data Dictionary

## weather Table

It is the dimension table in the data model. This table contains information hourly weather information for all date and location.

| Column               | Description                                                                                        |
|----------------------|----------------------------------------------------------------------------------------------------|
| date                 | date for which weather information is kept in the table, in DD-MM-YYYY format                      |
| location             | location for which weather information is kept in the table                                        |
| time                 | time for which weather information is kept in the table                                            |
| mintempC             | for unique date and location; minimum tempreture of that day in Celcius                            |
| maxtempF             | for unique date and location; maximum tempreture of that day in Fahrenheit                         |
| sunHour              | hour with max intensity of the sunlight for that day, unique to a location.                        |
| mintempF             | for unique date and location; miniimum tempreture of that day in Fahrenheit                        |
| maxtempC             | for unique date and location; maximum tempreture of that day in Celcius                            |
| uvIndex              | UV index for that time, for the date and location                                                  |
| tempC                | tempreture value for unique date, time and location                                                |
| windspeedKmph        | wind speed value for unique date, time and location                                                |
| weather_Desc         | describes weather in human understandable value for unique date, time and location                 |
| HeatIndexC           | heat index value for unique date, time and location                                                |
| visibility           | visibility value for unique date, time and location                                                |
| weatherCode          | weather code is for technical use for example in flight information charts                         |
| humidity             | value for unique date, time and location                                                           |

## location Table

It is a dimension table. It contains all metadata information related to a location.

| Column             | Descritpion                                                                        |
|--------------------|------------------------------------------------------------------------------------|
| LocationCode       | A unique ID, contains location/city code                                           |
| LocationName       | full City Name with state                                                          |
| LocationStateCode  | contains state code for the LocationCode                                           |
| LocationStateFips  | State Fips code                                                                    |
| LocationStateName  | contains state name for the StateCode                                              |

## flight Table

It is a dimension table. It contains the code and information about the flight.
| Column              | Descritpion                                                                                                         |
|---------------------|---------------------------------------------------------------------------------------------------------------------|
| Flightid            | unique id to identify all data in the table                                                                         |
| FlightDate          | Date in which the flight was scheduled                                                                              |
| TailNum             | plane tail number                                                                                                   |
| FlightNum           | flight number                                                                                                       |
| Origin              | origin IATA airport code                                                                                            |
| Dest                | destination IATA airport code                                                                                       |
| CRSDepTime          | CRS Elapsed Time of Flight (estimated elapse time), in minutes                                                      |
| CRSArrTime          | scheduled arrival time (local, hhmm)                                                                                |
| ArrTime             | actual arrival time (local, hhmm)                                                                                   |
| ArrDelay            | Difference in minutes between scheduled and actual arrival time. Early arrivals show negative numbers, in minutes   |
| Cancelled           | contains '1' if flight cancelled                                                                                    |
| WeatherDelay        | denotes if there was a delay die to bad weather                                                                     |
| Diverted            | A description of the admission port code indicating information about its location.                                 |

## flight-weather Table

It is a fact table. It is designed for quick analysis of flight data with weather information for that flight.


| Column              | Descritpion                                                                                                         |
|---------------------|---------------------------------------------------------------------------------------------------------------------|
| flight_weather_id   | unique id to identify all data in the table                                                                         |
| flightId            | Flight id given by airline                                                                                          |
| FlightDate          | Date in which the flight was scheduled                                                                              |
| CRSDepTime          | scheduled departure time (local, hhmm)                                                                              |
| Origin              | origin IATA airport code                                                                                            |
| Dest                | destination IATA airport code                                                                                       |
| ArrDelay            | Difference in minutes between scheduled and actual arrival time. Early arrivals show negative numbers, in minutes   |
| Cancelled           | contains '1' if flight cancelled                                                                                    |
| WeatherDelay        | denotes if there was a delay due to bad weather, in minutes                                                         |
| Diverted            | contains '1' if flight was diverted                                                                                 |
| location            | Location code for the flight origin                                                                                 |
| time                | time for the flight departure, rounded off to ceiling hour for weather prediction                                   |
| mintempC            | for unique date and location; minimum tempreture of that day in Celcius                                            |
| maxtempF            | for unique date and location; maximum tempreture of that day in Fahrenheit                                         |
| tempC               | tempreture value for unique date, time and location                                                                |
| weather_Desc        | describes weather in human understandable value for unique date, time and location                                 |
