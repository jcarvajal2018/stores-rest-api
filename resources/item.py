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
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404



    def post(self,name):
        if ItemModel.find_by_name(name):
            return {'message': "Ya existe un Item con el nombre '{}'".format(name)},400 #codigo para indicar que hay  un error
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500 #Internal Server Error

        return item.json(), 201 #codigo para indicar que registro fue creado





    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return{'message': 'Item deleted'}



    def put(self,name):
        data = Item.parser.parse_args()  #aqui viene el precio dado por el json
            item = ItemModel.find_by_name(name) #en item quedan los datos del registro actual
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price= data['price']
        item.save_to_db()
        return item.json()





class ItemList(Resource):
    def get(self):
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
