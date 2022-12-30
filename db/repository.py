from utils.singleton import SingletonPattern
from constants import *
import mysql.connector

singleton = SingletonPattern()

@singleton.singleton
class Repository:

    def __init__(self):

        self.db = mysql.connector.connect(
            user='root',
            password='fenske12',
            host='localhost',
            # host='mysql',
            port='3306',
            database='tradingbot'
        )

    def insert(self, table: str, data: dict):
        cursor = self.db.cursor()
        columns = ""
        values = ""
        for key, value in data.items():
            columns += key + ","
            values += "'" + str(value) + "',"
        columns = columns[:-1]
        values = values[:-1]
        query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
        cursor.execute(query)
        self.db.commit()
        return cursor.lastrowid


    def update(self, table: str, data: dict, where: dict):
        cursor = self.db.cursor()
        values = ",".join([f"{key}='{value}'" for key, value in data.items()])
        where = " AND ".join([f"{key}='{value}'" for key, value in where.items()])
        query = f"UPDATE {table} SET {values} WHERE {where}"
        cursor.execute(query)
        self.db.commit()

    def select(self, table: str, columns: list) -> list:

        cursor = self.db.cursor()
        columns = ",".join(columns)
        # where = " AND ".join([f"{key}='{value}'" for key, value in where.items()])
        query = f"SELECT {columns} FROM {table};"
        cursor.execute(query)

        data = cursor.fetchall()


        operations = []


        for i in range (len(data)):

            date = data[i][0]
            market = data[i][1]
            id = data[i][2]
            result = data[i][3]
            ammount_use = float(data[i][4])
            try:
                profit = float(data[i][5])
            except:
                profit = None
            duration_in_min = data[i][6]
            operation_type = data[i][7]
            state = data[i][8]
            message = data[i][9]

            operation = {
                'id': id,
                'date': date,
                'market': market,
                'result': result,
                'ammount_use': ammount_use,
                'profit': profit,
                'duration_in_min': duration_in_min,
                'type': operation_type,
                'state': state,
                'message': message
            }

            operations.append(operation)

        return operations


    def select_pending_operations(self, table: str, columns: list) -> list:

        print('Entra al select del repository')

        cursor = self.db.cursor()
        columns = ",".join(columns)
        # where = " AND ".join([f"{key}='{value}'" for key, value in where.items()])
        query = f"SELECT {columns} FROM {table} WHERE state = 'pending';"
        cursor.execute(query)

        data = cursor.fetchall()

        operations = []

        for i in range (len(data)):

            date = data[i][0]
            market = data[i][1]
            id = data[i][2]
            result = data[i][3]
            ammount_use = float(data[i][4])
            try:
                profit = float(data[i][5])
            except:
                profit = None
            duration_in_min = data[i][6]
            operation_type = data[i][7]
            state = data[i][8]
            message = data[i][9]

            operation = {
                'id': id,
                'date': date,
                'market': market,
                'result': result,
                'ammount_use': ammount_use,
                'profit': profit,
                'duration_in_min': duration_in_min,
                'type': operation_type,
                'state': state,
                'message': message
            }

            operations.append(operation)

        return operations



