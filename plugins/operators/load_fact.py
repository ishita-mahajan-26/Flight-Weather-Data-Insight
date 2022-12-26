from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import logging

class LoadFactOperator(BaseOperator):

    ui_color = '#F98866'
    base_sql = """
        INSERT INTO {}
        {};
        COMMIT;
    """
    base_sql_append = """
        INSERT INTO {}
        {};
        COMMIT;
    """

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 table="",
                 sql="",
                 delete_load= True,
                 *args, **kwargs):
                 

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.table = table
        self.redshift_conn_id = redshift_conn_id
        self.sql=sql
        self.delete_load= delete_load

    def execute(self, context):
        self.log.info('LoadFactOperator implemented')
        redshift_hook = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        if self.delete_load:  
            self.log.info("Clearing data from destination Redshift table")
            redshift_hook.run("DELETE FROM {}".format(self.table))
        
        formatted_sql = LoadFactOperator.base_sql.format(self.table, self.sql)
        self.log.info(formatted_sql)
        redshift_hook.run(formatted_sql)
