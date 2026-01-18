from ibm_watsonx_data_integration.common.auth import IAMAuthenticator
from ibm_watsonx_data_integration import Platform
from ibm_watsonx_data_integration.services.streamsets.api import *
from ibm_watsonx_data_integration.services.datastage import *
from ibm_watsonx_data_integration.services.streamsets import *
from ibm_watsonx_data_integration.codegen import PythonGenerator

import random
import string
import os

from dotenv import load_dotenv

load_dotenv()



# Read API key from .env file
api_key = os.getenv('IBM_WATSONX_API_KEY')

if not api_key:
    raise ValueError("IBM_WATSONX_API_KEY environment variable not found.")

auth = IAMAuthenticator(api_key)


auth = IAMAuthenticator(api_key=api_key)
platform = Platform(auth, base_api_url=os.getenv('WATSONX_BASE_URL', 'https://api.ca-tor.dai.cloud.ibm.com'))

# Get project
project = platform.projects.get(name='Customer Demo Project')




flow_name = "New streaming flow for fraud detection1"


flow = project.create_flow(
    name=flow_name,
    environment=None,
    description=""
)

kafka_multitopic_consumer_1 = flow.add_stage("Kafka Multitopic Consumer")
kafka_multitopic_consumer_1.max_batch_size_in_records = 1
kafka_multitopic_consumer_1.field_path_to_regex_group_mapping = [{'fieldPath': '/', 'group': 1}]
kafka_multitopic_consumer_1.broker_uri = "kafka:9092"
kafka_multitopic_consumer_1.topic_list = ['new_credit_card_transactions']
kafka_multitopic_consumer_1.import_sheets = ['']
kafka_multitopic_consumer_1.data_format = 'JSON'
kafka_multitopic_consumer_1.schema_registry_urls = ['']

jdbc_lookup_1 = flow.add_stage("JDBC Lookup")
jdbc_lookup_1.password = os.getenv('JDBC_PASSWORD', 'your-password')
jdbc_lookup_1.sql_query = """WITH prev AS (
    SELECT location, timestamp
    FROM transactions
    WHERE account_id = ${record:value('/account_id')} AND suspicious = FALSE
    ORDER BY transaction_id DESC
    LIMIT 1
)
SELECT
    GEOGRAPHY_DISTANCE(prev.location, \"${record:value('/location')}\") as delta_x,
    TIMESTAMPDIFF(SECOND, prev.timestamp, \"${record:value('/timestamp')}\") as delta_t
FROM prev;"""
jdbc_lookup_1.username = os.getenv('JDBC_USERNAME', 'your-username')
jdbc_lookup_1.jdbc_connection_string = os.getenv('JDBC_CONNECTION_STRING', 'jdbc:singlestore://host:port/database')

expression_evaluator_1 = flow.add_stage("Expression Evaluator")
expression_evaluator_1.field_attribute_expressions = [{'fieldToSet': '/'}]
expression_evaluator_1.field_expressions = [{'fieldToSet': '/suspicious', 'expression': "${record:exists('/delta_x') and record:exists('/delta_t') and \\n  record:value('/delta_x') / record:value('/delta_t') > 268.224}"}]
expression_evaluator_1.header_attribute_expressions = [{}]

elasticsearch_1 = flow.add_stage("Elasticsearch")
elasticsearch_1.index = "transactions"
elasticsearch_1.http_urls = "http://10.89.0.196:9200"

singlestore_1 = flow.add_stage("SingleStore")
singlestore_1.password = os.getenv('SINGLESTORE_PASSWORD', 'your-password')
singlestore_1.schema_name = "finance"
singlestore_1.data_sqlstate_codes = ['']
singlestore_1.username = os.getenv('SINGLESTORE_USERNAME', 'your-username')
singlestore_1.table_name = "transactions"
singlestore_1.jdbc_connection_string = os.getenv('SINGLESTORE_CONNECTION_STRING', 'jdbc:singlestore://host:port/database')


ibm_db2_1 = flow.add_stage("IBM Db2",type='destination')
ibm_db2_1.port = int(os.getenv('DB2_PORT', '50000'))
ibm_db2_1.use_ssl = True
ibm_db2_1.username = os.getenv('DB2_USERNAME', 'your-username')
ibm_db2_1.host = os.getenv('DB2_HOST', 'your-host')
ibm_db2_1.database = os.getenv('DB2_DATABASE', 'your-database')
ibm_db2_1.password = os.getenv('DB2_PASSWORD', 'your-password')
ibm_db2_1.ssl_certificate = os.getenv('DB2_SSL_CERT', 'your-ssl-cert')



amazon_s3_1 = flow.add_stage("Amazon S3")
amazon_s3_1.encryption_context = [{}]
amazon_s3_1.bucket = os.getenv('S3_BUCKET', 'your-bucket')
amazon_s3_1.region_definition_for_s3 = "SPECIFY_REGION"
amazon_s3_1.access_key_id = os.getenv('AWS_ACCESS_KEY_ID', 'your-access-key')
amazon_s3_1.secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY', 'your-secret-key')




snowflake_1 = flow.add_stage("Snowflake", type='destination')
snowflake_1.encryption_context = [{}]
snowflake_1.role = os.getenv('SNOWFLAKE_ROLE', 'your-role')
snowflake_1.connection_properties = [{}]
snowflake_1.user = os.getenv('SNOWFLAKE_USER', 'your-user')
snowflake_1.account = os.getenv('SNOWFLAKE_ACCOUNT', 'your-account')
snowflake_1.organization = os.getenv('SNOWFLAKE_ORG', 'your-org')
snowflake_1.database = os.getenv('SNOWFLAKE_DATABASE', 'your-database')
snowflake_1.password = os.getenv('SNOWFLAKE_PASSWORD', 'your-password')
snowflake_1.schema = os.getenv('SNOWFLAKE_SCHEMA', 'your-schema')
snowflake_1.warehouse = os.getenv('SNOWFLAKE_WAREHOUSE', 'your-warehouse')
snowflake_1.authentication_method = "CREDENTIALS"
snowflake_1.table = "tbl"


kafka_multitopic_consumer_1.connect_output_to(jdbc_lookup_1)
jdbc_lookup_1.connect_output_to(expression_evaluator_1)
expression_evaluator_1.connect_output_to(elasticsearch_1)
expression_evaluator_1.connect_output_to(singlestore_1)
expression_evaluator_1.connect_output_to(ibm_db2_1)
expression_evaluator_1.connect_output_to(amazon_s3_1)   
expression_evaluator_1.connect_output_to(snowflake_1)

project.update_flow(flow)
print("New streaming data for fraud detection flow has been created")



