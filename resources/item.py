from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="Este campo no puede estar vacío"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Cada Item necesita tener una Tienda asignada."
    )

    @jwt_required()
    def get(self, name):
        #for item in items:
        #    if item['name'] == name:
        #        return item
        #return {'item': None}, 404 #codigo para indicar que no fue encontrado
        #lo anterior es igual a:
        #item = next(filter(lambda x: x['name'] == name, items), None)
        #return {'item': item}, 200 if item else 404
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404



    def post(self,name):
        #if next(filter(lambda x: x['name'] == name, items),None):
            #return {'message': "Ya existe un Item con el nombre '{}'".format(name)},400 #codigo para indicar que hay  un error
        #data = request.get_json()
        #if self.find_by_name(name):
        if ItemModel.find_by_name(name):
            return {'message': "Ya existe un Item con el nombre '{}'".format(name)},400 #codigo para indicar que hay  un error
        data = Item.parser.parse_args()
        #item = {'name':name, 'price': data['price']}
        #item = ItemModel(name, data['price'], data['store_id'])
        item = ItemModel(name, **data)
        #items.append(item)
        try:
            item.save_to_db()
            #ItemModel.insert(item)
        except:
            return {"message": "An error occurred inserting the item."}, 500 #Internal Server Error

        return item.json(), 201 #codigo para indicar que registro fue creado
        #202 codigo para indicar que se esta creando




    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        ##if next(filter(lambda x: x['name'] == name, items),None):
        ##    global items
        ##    items = list(filter(lambda x: x['name']!=name, items))
        ##    return{'message': 'Item deleted'}
        #connection =sqlite3.connect('data.db')
        #cursor = connection.cursor()
        #query = "DELETE FROM items where name=?"
        #cursor.execute(query,(name,))
        #connection.commit()
        #connection.close()
        return{'message': 'Item deleted'}

        #return{'message': "Item '{}' no existe".format(name)},400

    def put(self,name):
        ##data = request.get_json() no controla los argumentos
        data = Item.parser.parse_args()  #aqui viene el precio dado por el json
        ##item = next(filter(lambda x: x['name'] == name, items), None)
        item = ItemModel.find_by_name(name) #en item quedan los datos del registro actual
        if item is None:
            #item = ItemModel(name, data['price'], data['store_id'])
            item = ItemModel(name, **data)
        else:
            item.price= data['price']
        item.save_to_db()
        return item.json()
        ##if item is None:
        ##    item = {'name':name, 'price': data['price']}
        ##    items.append(item)
        ##else:
        ##    item.update(data)
        ##return item
        ##updated_item = {'name':name, 'price': data['price']}  #el nuevo item
        #updated_item = ItemModel(name, data['price'])
        #if item is None: #si no existe
        #    try:
        #        updated_item.insert()
        #        ##ItemModel.insert(updated_item)
        #    except:
        #        return {"message": "Ocurrió un error insertando el item."},500
        #else:
        #    try:
        #        updated_item.update()
        #        ##ItemModel.update(updated_item)
        #    except:
        #        return {"message": "Ocurrió un error actualizando el item."},500
        #return updated_item.json()




class ItemList(Resource):
    def get(self):
        #return {'items':[item.json() for item in ItenModel.query.all()]}
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
    #    return {'items': items}
        #connection =sqlite3.connect('data.db')
        #cursor = connection.cursor()
        #query = "SELECT * FROM items"
        #result=cursor.execute(query)
        #items = []
        #for row in result:
        #    items.append({'name': row[0],'price':row[1]})

        #connection.close()
        #return {'items': items}
