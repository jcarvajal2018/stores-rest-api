from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self,name):
        self.name = name

    def json(self):
        return {'id': self.id,'name': self.name, 'items': [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        return StoreModel.query.filter_by(name=name).first() #SELECT * FROM items WHERE name=name
        #connection = sqlite3.connect('data.db')
        #cursor = connection.cursor()

        #query = "SELECT * FROM items WHERE name=?"
        #result = cursor.execute(query, (name,))
        #row = result.fetchone()
        #connection.close()
        #if row:
            ##return {'item': {'name':row[0], 'price':row[1]}}
            ##return cls(row[o],row[1])
            #return cls(*row)

    def save_to_db(self):  #antes llamado insert
        db.session.add(self)
        db.session.commit()
        #connection =sqlite3.connect('data.db')
        #cursor = connection.cursor()
        #query = "INSERT INTO items VALUES (?,?)"
        #cursor.execute(query,(self.name, self.price))
        #connection.commit()
        #connection.close()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    #def update(self):  #ya no hace falta por que el save_to_db hace todo automatico
    #    connection =sqlite3.connect('data.db')
    #    cursor = connection.cursor()
    #    query = "UPDATE items SET price=? where name=?"
    #    cursor.execute(query,(self.price,self.name))
    #    connection.commit()
    #    connection.close()
    #    return{'message': 'Item deleted'}
