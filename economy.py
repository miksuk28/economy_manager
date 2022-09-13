from db import DatabaseWrapper
from config import economy_config as config
from categories import Categories
from auth import Authentication
import eco_exceptions as exc


class EconomyManager(DatabaseWrapper):
    def __init__(self):
        DatabaseWrapper.__init__(self)
        self.categories = Categories()
        self._currency = config["currency"]
        self._auth = Authentication()

    def _create_items_list(self, items, receipt_id, username):
        new_list = []
        for item in items:
            temp_list = [
                receipt_id,
                username,
                item["item"],
                item["price"],
                item["quantity"],
                item.get("comment")
            ]
            new_list.append(temp_list)

        return new_list


    def create_receipt(self, username, items, store=None, comment=None, date=None, category=None):
        if category is not None:
            category_id = self.categories.create_category(category)[0]
        else:
            category_id = None

        cur = self.conn.cursor()
        cur.execute(
            '''
            INSERT INTO receipts (user_id,store,comment,timestamp,category)
            VALUES ((SELECT id FROM users WHERE username=?),?,?,?,?)
            ''',
            (username, store, comment, date, category_id)
        )
        receipt_id = cur.lastrowid

        cur.executemany(
            '''
            INSERT INTO receipts_junction (receipt_id,user_id,item,price,quantity,comment)
            VALUES (?,(SELECT id FROM users WHERE username=?),?,?,?,?)
            ''',
            self._create_items_list(items, receipt_id, username)
        )
            
        self.conn.commit()
        return receipt_id


    def delete_receipt(self, username, id):
        cur = self.conn.cursor()
        cur.execute(
            '''
            DELETE FROM receipts
            WHERE id=? AND user_id=(SELECT id FROM users WHERE username=?)
            ''',
            (id, username)
        )
        deleted_items = cur.rowcount
        
        if deleted_items == 0:
            raise exc.ReceiptDoesNotExist(id)
        
        self.conn.commit()
        return deleted_items


    def get_receipt_by_id(self, id, username):
        cur = self.conn.cursor()
        cur.execute(
            '''
            SELECT item, comment, price, quantity, price*quantity AS total
            FROM receipts_junction
            JOIN users ON receipts_junction.user_id=users.id
            WHERE receipt_id=? AND username=?
            ''',
            (id, username)
        )
        items = self._list_and_dictify(cur.fetchall())
        
        cur.execute(
            '''
            SELECT store, comment, timestamp, created
            FROM receipts
            JOIN users ON receipts.user_id=users.id
            WHERE receipts.id=? AND username=?
            ''',
            (id, username)
        )
        receipt_data = self._list_and_dictify(cur.fetchone(), one=True)
        
        if receipt_data is None:
            raise exc.ReceiptDoesNotExist(id)

        result = {
            "id":           id,
            "store":        receipt_data.get("store"),
            "comment":      receipt_data.get("comment"),
            "timestamp":    receipt_data.get("timestamp"),
            "created":      receipt_data.get("created"),
            "items":        items
        }

        return result


    def total_spending(self, username, format=False):
        cur = self.conn.cursor()
        cur.execute(
            '''
            SELECT SUM(quantity*price) AS total FROM receipts_junction
            JOIN users ON receipts_junction.user_id=users.id
            WHERE username=?;
            ''',
            (username,)
        )
        result = cur.fetchone()
        # Round to two decimals
        if format:
            return f"{result['total']:.2f} {self._currency['short']}"
            
        return round(result["total"], 2)


    def _group_by_id(self, id, items):
        '''Groups items together by the receipt_id'''
        new_list = []
        for i, item in enumerate(items):
            if item["receipt_id"] == id:
                new_list.append(items.pop(i))
        print(len(new_list))
        return new_list

    
    def _create_full_old(self, receipts, items):
        '''Creates a full dictionary with the items'''
        for i, receipt in enumerate(receipts):
            new_list = self._group_by_id(receipt["id"], items)
            receipts[i]["products"] = new_list

        return receipts


    def _create_full(self, receipts, items):
        index = {}
        # Build index and add products list
        for i, receipt in enumerate(receipts):
            receipts[i]["products"] = []
            index[receipt["id"]] = i

        # Match items and receipts by their id
        for i, item in enumerate(items):
            receipts[index[item["receipt_id"]]]["products"].append(item)

        return receipts



    def _calc_totals(self, results):
        for i, receipt in enumerate(results):
            total = 0
            for products in receipt["products"]:
                total += products.get("total", 0)

            results[i]["total"] = total

        return results


    def get_all_receipts(self, username):
        cur = self.conn.cursor()
        cur.execute(
            '''
            SELECT receipts.id, store, comment, timestamp, created, categories.id AS category_id, categories.name AS category
            FROM receipts
            LEFT JOIN categories ON receipts.category=categories.id
            LEFT JOIN users ON receipts.user_id=users.id
            WHERE username=?
            ''',
            (username,)
        )
        receipts = self._list_and_dictify(items=cur.fetchall())

        cur.execute(
            '''
            SELECT receipts.id AS receipt_id,
                store, item, price, quantity, price*quantity AS total, categories.name AS category
            FROM receipts_junction

            JOIN receipts ON receipt_id=receipts.id
            LEFT JOIN categories ON receipts.category=categories.id
            JOIN users ON receipts.user_id=users.id
            WHERE username=?
            ''',
            (username,)
        )
        items = self._list_and_dictify(cur.fetchall())
        full_list = self._create_full(receipts, items)
        full_list = self._calc_totals(full_list)

        return full_list