
import mysql.connector
from mysql.connector import Error


# Connect to the FLEETOS database
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR_MYSQL_PASSWORD",
        database="fleetos"
    )


# Create a new mission
def create_mission(data):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO missions
            (mission_type, priority, deadline, location,
             required_capabilities, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            data["mission_type"],
            data["priority"],
            data.get("deadline"),
            data["location"],
            data.get("required_capabilities", ""),
            "Pending"
        )

        cursor.execute(query, values)
        connection.commit()

        return {
            "mission_id": cursor.lastrowid,
            "message": "Mission created successfully"
        }

    except Error:
        if connection and connection.is_connected():
            connection.rollback()
        raise

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


# Get all missions
def get_all_missions():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT *
            FROM missions
            ORDER BY mission_id DESC
        """

        cursor.execute(query)
        missions = cursor.fetchall()

        return missions

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


# Get a mission using its ID
def get_mission_by_id(mission_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT *
            FROM missions
            WHERE mission_id = %s
        """

        cursor.execute(query, (mission_id,))
        mission = cursor.fetchone()

        return mission

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


# Update the status of a mission
def update_mission_status(mission_id, new_status):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            UPDATE missions
            SET status = %s
            WHERE mission_id = %s
        """

        cursor.execute(query, (new_status, mission_id))
        connection.commit()

        return cursor.rowcount > 0

    except Error:
        if connection and connection.is_connected():
            connection.rollback()
        raise

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()