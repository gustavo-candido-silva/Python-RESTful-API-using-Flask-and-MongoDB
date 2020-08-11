from flask import Flask, request
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth
from utils import Contacts

app = Flask(__name__)
api = Api(app)

class Contact(Resource):

    def get(self,name):

        # opens connection in the database and get the contacts filtered by name
        contact = Contacts().get_contact(name)
        try:

            # prepares the list of dicts for returning in the api
            response = [{"name":c['name'],"email":c['email'],"fonenumber":c['fonenumber']} for c in contact]

        except AttributeError:
            response = {"status":"error","msg":"No contacts found"}
        except:
            response = {"status":"error","msg":"Unknown error"}

        return response

    def put(self,name):

        # opens connection in the database
        contact = Contacts()

        # process the body received in the request
        data = request.json

        try:
            # update the contacts filtering by name with the received data
            response = contact.update_contact(name_filter=name,new_obj=data)
        except:
            response = {"status":"error","msg":"Unknown error"}

        return response

    def delete(self,name):
        # opens connection in the database
        contact = Contacts()

        try:
            # deletes all the contacts with the given name
            response = contact.delete_contacts(name=name)
        except:
            response = {"status":"error","msg":"Unknown error"}

        return response


class ListContacts(Resource):

    def get(self):
        # opens connection with the database and gets all the existing contacts
        contacts = Contacts().get_all_contacts()

        try:
            # prepares the list of dicts for returning in the api
            response = [{"name": c['name'],"email": c['email'],"fonenumber": c['fonenumber']} for c in contacts]

        except AttributeError:
            response = {"status": "error", "msg": "No contacts found"}
        except:
            response = {"status": "error", "msg": "Unknown error"}

        return response

    def post(self):

        # opens connection with database
        contact = Contacts()

        # process the body received in the request
        data = request.json

        try:
            # inserts the new contact in the received data
            response = contact.insert_contact(obj=data)
        except:
            response = {"status":"error","msg":"Unknown error"}

        return response


api.add_resource(Contact,'/contact/<string:name>/')
api.add_resource(ListContacts,'/contact/')

if __name__ == '__main__':
    app.run(debug=True)