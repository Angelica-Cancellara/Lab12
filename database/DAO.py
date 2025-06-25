from oauthlib.uri_validate import query

from database.DB_connect import DBConnect
from model.retailer import Retailer


class DAO():

    @staticmethod
    def getAllNazioni():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary = True)
        query = """select distinct(country)
                    from go_retailers"""
        cursor.execute(query)
        for row in cursor:
            result.append(row["country"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(nazione):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from go_retailers as r 
                    where r.country = %s"""
        cursor.execute(query, (nazione,))
        for row in cursor:
            result.append(Retailer(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllArchi(anno, nazione, idMap):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select r1.Retailer_code as r1, r2.Retailer_code as r2, count(distinct(s1.Product_number)) as n
                    from go_daily_sales as s1, go_daily_sales as s2 ,go_retailers as r1 , go_retailers as r2
                    where s1.Retailer_code = r1.Retailer_code and 
                    s2.Retailer_code = r2.Retailer_code and 
                    Year(s1.Date) = Year(s2.Date) and 
                    Year(s1.Date) = %s and 
                    s1.Product_number = s2.Product_number and 
                    r1.Country = r2.Country and 
                    r1.Country = %s and 
                    r1.Retailer_code < r2.Retailer_code 	 
                    group by r1.Retailer_code, r2.Retailer_code"""
        cursor.execute(query, (anno, nazione))
        for row in cursor:
            result.append((idMap[row["r1"]], idMap[row["r2"]], row["n"]))
        cursor.close()
        conn.close()
        return result

