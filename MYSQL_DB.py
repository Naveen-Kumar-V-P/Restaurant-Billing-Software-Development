import mysql.connector
from mysql.connector import Error
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def connect_to_mysql():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Vpnk'
        )
        if connection.is_connected():
            logging.info("Connected to MySQL server")
            cursor = connection.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS order_db")
            cursor.execute("USE order_db")
            return connection, cursor
    except Error as e:
        logging.error(f"Connection error: {e}")
        return None, None

def create_orders_table(cursor):
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Orders (
                ID INT AUTO_INCREMENT PRIMARY KEY,
                Customer_Name VARCHAR(100),
                Order_Detials TEXT,
                Total DECIMAL(10, 2),
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB
        """)
        logging.info("Orders table created successfully")
    except Error as e:
        logging.error(f"Error creating Orders table: {e}")

def insert_single_order(cursor, connection, order):
    try:
        query = "INSERT INTO Orders (Customer_Name, Order_Detials, Total) VALUES (%s, %s, %s)"
        cursor.execute(query, (order['Customer_Name'], order['Order_Detials'], order['Total']))
        connection.commit()
        logging.info("Inserted single order")
    except Error as e:
        logging.error(f"Insert error: {e}")

def insert_multiple_orders(cursor, connection, orders):
    try:
        query = "INSERT INTO Orders (Customer_Name, Order_Detials, Total) VALUES (%s, %s, %s)"
        values = [(o['Customer_Name'], o['Order_Detials'], o['Total']) for o in orders]
        cursor.executemany(query, values)
        connection.commit()
        logging.info(f"Inserted {len(orders)} orders")
    except Error as e:
        logging.error(f"Insert error: {e}")

def fetch_all_orders(cursor):
    try:
        cursor.execute("SELECT * FROM Orders ORDER BY timestamp DESC")
        rows = cursor.fetchall()
        logging.info("Fetched all orders")
        return rows
    except Error as e:
        logging.error(f"Select error: {e}")
        return []

def update_order_total(cursor, connection, order_id, new_total):
    try:
        cursor.execute("UPDATE Orders SET Total = %s WHERE ID = %s", (new_total, order_id))
        connection.commit()
        logging.info(f"Updated order ID {order_id}")
    except Error as e:
        logging.error(f"Update error: {e}")

def delete_order(cursor, connection, order_id):
    try:
        cursor.execute("DELETE FROM Orders WHERE ID = %s", (order_id,))
        connection.commit()
        logging.info(f"Deleted order ID {order_id}")
    except Error as e:
        logging.error(f"Delete error: {e}")

def transaction_example(cursor, connection):
    try:
        connection.start_transaction()
        insert_single_order(cursor, connection, {
            'Customer_Name': 'Transaction Test',
            'Order_Detials': 'Sample item',
            'Total': 100.00
        })
    
        connection.commit()
        logging.info("Transaction committed")
    except Exception as e:
        connection.rollback()
        logging.error(f"Transaction failed: {e}")

def main():
    connection, cursor = connect_to_mysql()
    if not connection or not cursor:
        return

    create_orders_table(cursor)

    insert_single_order(cursor, connection, {
        'Customer_Name': 'John Doe',
        'Order_Detials': '2x Pizza, 1x Coke',
        'Total': 450.00
    })

    insert_multiple_orders(cursor, connection, [
        {'Customer_Name': 'Jane Smith', 'Order_Detials': '1x Pasta', 'Total': 220.00},
        {'Customer_Name': 'Mike Tyson', 'Order_Detials': '3x Burger', 'Total': 330.00}
    ])

    for row in fetch_all_orders(cursor):
        logging.info(row)

    update_order_total(cursor, connection, 1, 499.00)
    delete_order(cursor, connection, 2)
    transaction_example(cursor, connection)

    cursor.close()
    connection.close()
    logging.info("Connection closed")

if __name__ == "__main__":
    main()








