import gradio as gr
from pymongo import MongoClient
import psycopg2
from redis import Redis
import logging

# Setup logging configuration
logging.basicConfig(filename='db_connection_tester.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def test_connection(db_type, connection_string):
    try:
        if db_type == "MongoDB":
            client = MongoClient(connection_string)
            client.admin.command('ismaster')
            logging.info("MongoDB Connection Successful")
            return "MongoDB Connection Successful"
        elif db_type == "PostgresSQL":
            conn = psycopg2.connect(connection_string)
            cur = conn.cursor()
            cur.execute('SELECT 1')
            logging.info("PostgresSQL Connection Successful")
            return "PostgresSQL Connection Successful"
        elif db_type == "Redis":
            r = Redis.from_url(connection_string)
            r.ping()
            logging.info("Redis Connection Successful")
            return "Redis Connection Successful"
        else:
            logging.error("Unsupported Database Type")
            return "Unsupported Database Type"
    except Exception as e:
        logging.error(f"Connection Failed: {str(e)}")
        return f"Connection Failed: {str(e)}"


interface = gr.Interface(fn=test_connection,
                         inputs=[gr.Dropdown(["MongoDB", "PostgresSQL", "Redis"], label="Database Type"),
                                 gr.Textbox(label="Connection String")],
                         outputs="text",
                         title="Database Connection Tester",
                         description="Test connections to MongoDB, PostgresSQL, or Redis databases.")

if __name__ == "__main__":
    interface.launch()
