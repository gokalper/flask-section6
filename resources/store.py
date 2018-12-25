from flask_restful import Resource
from flask_jwt import jwt_required
from models.store import StoreModel
from models.item import ItemModel


class Store(Resource):

    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    @jwt_required()
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': 'A Store with name {} already exists.'.format(name)}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'An error occurred while creating the store.'}, 500

        return store.json(), 201


    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        item = ItemModel.find_by_store_id(store.id)

        if item:
            return {'message': 'Store can not be deleted, there are items in the store.'}, 400

        if store:
            store.delete_from_db()

        return {'message': 'Store Deleted.'}


class StoreList(Resource):
    @jwt_required()
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}