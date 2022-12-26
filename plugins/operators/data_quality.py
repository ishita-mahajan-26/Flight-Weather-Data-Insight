from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import logging
import sys

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 tables=[],
                 quality_checks=[],
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.tables = tables
        self.redshift_conn_id = redshift_conn_id
        self.quality_checks = quality_checks

    def execute(self, context):
        self.log.info('DataQualityOperator has been implemented')
        redshift_hook = PostgresHook(self.redshift_conn_id)
        
        quality_checks_errors_count = 0
        tables_which_failed_quality_checks = []
        
        if 'table_exists_check' in self.quality_checks:
            for table in self.tables:
                sql = "SELECT COUNT(*) FROM " + str(table)
                records = redshift_hook.get_records(sql)
                self.log.info(f"records of {table} - {records[0][0]}")
            
                if len(records) < 1 or len(records[0]) < 1:
                    quality_checks_errors_count += 1
                    tables_which_failed_quality_checks.append(table)
                    
               
            if quality_checks_errors_count > 0:
                raise ValueError(f"Data quality check failed. {tables_which_failed_quality_checks} returned no results")
            
            logging.info(f"Data quality on {self.tables} check passed")    
        
        # resetting values for next quality test    
        quality_checks_errors_count = 0
        tables_which_failed_quality_checks = []
                    
        if 'table_contains_records_check' in self.quality_checks:
            for table in self.tables:
                sql = "SELECT COUNT(*) FROM " + str(table)
                records = redshift_hook.get_records(sql)
                self.log.info(f"records of {table} - {records[0][0]}")

                num_records = records[0][0]
                if num_records < 1:
                    quality_checks_errors_count += 1
                    tables_which_failed_quality_checks.append(table)
                                
            if quality_checks_errors_count > 0:
                raise ValueError(f"Data quality check failed. {tables_which_failed_quality_checks} contained 0 rows")                    
                    
            logging.info(f"Data quality on {self.tables} check passed") 
            
            
        
        
