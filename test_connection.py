import gradio as gr
from pymongo import MongoClient
import psycopg2
from redis import Redis


def test_connection(db_type, connection_string):
    try:
        if db_type == "MongoDB":
            client = MongoClient(connection_string)
            # The master command is cheap and does not require auth.
            client.admin.command('ismaster')
            return "MongoDB Connection Successful"
        elif db_type == "PostgresSQL":
            conn = psycopg2.connect(connection_string)
            # Open a cursor to perform database operations
            cur = conn.cursor()
            # Check connection
            cur.execute('SELECT 1')
            return "PostgresSQL Connection Successful"
        elif db_type == "Redis":
            r = Redis.from_url(connection_string)
            # Ping the Redis server
            r.ping()
            return "Redis Connection Successful"
        else:
            return "Unsupported Database Type"
    except Exception as e:
        return f"Connection Failed: {str(e)}"


interface = gr.Interface(fn=test_connection,
                         inputs=[gr.Dropdown(["MongoDB", "PostgresSQL", "Redis"], label="Database Type"),
                                 gr.Textbox(label="Connection String")],
                         outputs="text",
                         title="Database Connection Tester",
                         description="Test connections to MongoDB, PostgresSQL, or Redis databases.")

if __name__ == "__main__":
    interface.launch()
