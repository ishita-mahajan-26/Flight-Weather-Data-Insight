# Flight-Weather-Data-Insight

<p>This project simplifies querying of the flight and weather data for major cities in the US for better analysis of Flight-weather relationship that can be useful for planning a journey.</p>

***

## Contents

1. [About the project](https://github.com/ishita-mahajan-26/Flight-Weather-Data-Insight#about-the-project)
2. [ETL flow diagram](https://github.com/ishita-mahajan-26/Flight-Weather-Data-Insight#etl-flow-diagram)
3. [Built with](https://github.com/ishita-mahajan-26/Flight-Weather-Data-Insight#built-with)
4. [Getting started](https://github.com/ishita-mahajan-26/Flight-Weather-Data-Insight#getting-started)
5. [Data Model](https://github.com/ishita-mahajan-26/Flight-Weather-Data-Insight#data-model)
6. [Future requirements](https://github.com/ishita-mahajan-26/Flight-Weather-Data-Insight#future-requirements)

***

## About the project

<p>The data source is stored in two formats:
	- flight information across all major cities in US (in csv format) - month wise datafiles
	- hourly weather information for all the major cities in US (in json format) - location level month wise data-files. 
</p>
 
<p>Since the datset is in 2 different formats, json format is highly nested and the data size is big, hence, it is not ideal for querying and gaining usable information.</p>
    
<p>The pipeline is configured to run once every month for the previous month for location specific weather information and flight information which is month wise</p>
    
<p>The aim is to create a datalake to store flight, city and weather information in a way that data is usable for advanced analytics.</p>

- The datalake could be used for analytics and can answer the following questions:

	1. What weather conditions are to be expected in any given month for the major cities for US?
	2. how many flights got delayed for any source-destination pair cities for each month from 1-2016 to 12-2017
	3. How many flights have been delayed which were caused by a specific weather condition (eg windy, stormy) in any given month
		select count(distinct flight_unique_code) from table1 where weather_condition == 'storm'and and month = '6' and flight_take_off time > flight_scheduled_time
	4. Sort best months to travel by week-month to a destination city based on flight cancellations and weather
	5. Which weather conditions have0 caused most delayed or cancelled flight
	6. Which month should you fly on to avoid extreme weather conditions?
	7. weather-wise flight delays
	8. weather-wise flight cancellations probablity
	9. month-wise flight delays 
</p>

***

## ETL flow diagram

![ETL](https://github.com/ishita-mahajan-26/Flight-Weather-Data-Insight/blob/main/ETL_flow_diagram.png)

***

## Data Sources and their processing

<p>The original data set is taken from Kaggel: https://www.kaggle.com/datasets/preethgunasekaran/flight-delayweather-dataset</p>

<p>As can be seen in the previous image, the pipeline takes the source data from 2 different sources kept in S3, processes the data and makes the data available in AWS Redshift Datawarehouse for analytics. </p>

<p>Data Processing for both source files is as follows:

1. **Weather Data**:
- Raw data is kept in S3 in JSON format on monthly basis.
- Since the file is highly nested, we process it to convert it into a file fit for relational database.
- The processed file is saved in S3 in CSV format. 
- The file goes through ETL process and data is saved in appropriate analytics tables in redshift.
- The correctness of the processed data is checked.
- The airflow pipeline runs every month to process new data.

2. **Flight Data**:
- Raw data is kept in S3 in CSV format on monthly basis.
- The file goes through ETL process and the data is saved in appropriate analytics tables in redshift.
- The correctness of the processed data is checked.
- The airflow pipeline runs every month to process new data.

</p>

***

## Built with

- Python
- SQL
- Airflow
- AWS S3 
- AWS Redshift
- general conceptual knowledge of IAM users and VPC is also needed.

***

## Getting started

<p>In order to run Data pipeline, you need to do the following:

- Create an AWS Redshift cluster and a IAM user with relevant s3 full access policies attached. Please note that the cluster must be in "Available" status. 
- Once Cluster is ready you must create all the tables by running the sql queries present in 'create_tables.sql'
- You will also need to update variables and connection information in your airflow as per the need of the code (create aws redshift connection and aws user connection)
- Start airflow server and start up the dag on the Airflow UI

</p>

***

## Custom built Operators - Airflow

- **StageToRedshiftOperator** - the operator is present in the python script called "stage_redshift.py". This Operator is used for copying data present as json from S3 into a table present on AWS Redshift

- **DataQualityOperator** -  the operator is present in the python script called "data_quality.py". This Operator is used for checking the data quality of a table that was recently loaded into Redshift

- **LoadDimensionOperator** - the operator is present in the python script called "load_dimension.py". This Operator is used for copying  load data present in staging table into a deminsion table present on AWS Redshift

- **LoadFactOperator** - the operator is present in the python script called "load_fact.py". This Operator is used for copying fact data present in staging table into a fact table present on AWS Redshift

***

## Data Model

<p>The data model follows star schema; with the central fact table and related dimentional tables in the side.</p>

![Data Model](https://github.com/ishita-mahajan-26/Flight-Weather-Data-Insight/blob/main/Data_Model.png)

***

## Future requirements

- **The data was increased by 100x.** 

<p>If the data increased by 100 times, We would need to process the dataset using Apache Spark. This will require running the preprocessing and ETL logic using Spark code</p>

- **The pipelines would be run on a daily basis by 7 am every day.**

<p>The pipeline currently uses airflow and is expected to run once every month where new data will be inserted into respective S3 buckets for processing. If we start getting data daily, we can easily modify the Airflow DAG to ensure that pipeline runs everyday at 7 AM</p>

- **The database needed to be accessed by 100+ people.**

<p>Since the data warehouse tool that we are using for the dataset is in redshift, If we need to scale the analytics table for broader audience we need to modify the Redshift cluster so that server handles more requests</p>
