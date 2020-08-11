from pymongo import MongoClient,errors
from pymongo import UpdateMany,DeleteMany

class Contacts():

    def __init__(self,host="localhost",port=27017): # mongo's default config
        '''

        :param host: The host where the database server is running. If None, the default host will be "localhost".
        :param port: The port where the host is listening. If None, the default listening port will be 27017.

        '''
        # creates the mongo client
        print("trying to connect to MongoDB...")
        try:
            client = MongoClient(host=host,port=port)
            print("MongoDB connected: " + str(client.address[0]) + ":" + str(client.address[1]))

            self.client = client
        except errors.ServerSelectionTimeoutError:

            print("Database Timeout... restart the module...")

        except:
            print("Unknown error")

    def get_contact(self, name):
        '''

        :param name: The name of the contact we're searching.
        :return: Returns a list dicts of the contacts in the format: {"name":str,
                                                                         "email":str,
                                                                         "fonenumber":str}

        '''
        contacts = self.client.contact_db.contacts

        l = []

        for c in contacts.find({'name':name}):
            l.append(c)


        self.client.close()
        #print(l)
        return l

    def get_all_contacts(self):
        '''

        :return: Returns a list of dicts of the contacts in the format: {"name":str,
                                                                         "email":str,
                                                                         "fonenumber":str}

        '''
        contacts = self.client.contact_db.contacts

        l = []


        for c in contacts.find():
            l.append(c)

        self.client.close()
        #print(l)
        return l

    def insert_contact(self,obj):
        '''

        :param obj: The json of the new contact.
        :return: Returns a dict containing all the data included plus the ID generated in MongoDB

        '''

        data = {'name':obj['name'],
                'email':obj['email'],
                'fonenumber':obj['fonenumber']}

        contacts = self.client.contact_db.contacts
        contact_id = contacts.insert_one(data).inserted_id
        self.client.close()

        data['_id'] = str(contact_id)

        return data

    def delete_contacts(self,name):
        '''

        :param name: The name of the contact we'll search to delete.
        :return: Returns a dict with the status and the number of deleted files

        '''
        contacts = self.client.contact_db.contacts

        # can be used with more than one operation in a list of operations
        operations = [DeleteMany({'name': name})]

        results = contacts.bulk_write(operations)

        print("{} object deleted.".format(results.deleted_count))

        return {"status":"sucess","deleted_count":results.deleted_count}

    def update_contact(self,name_filter,new_obj):
        '''

        :param name_filter: The name of the contact we'll search for update.
        :param new_obj: The new json for this contact.
        :return: Returns a dict with the new data plus the number of modified files.

        '''
        contacts = self.client.contact_db.contacts

        new = {"name":new_obj['name'],
               "email":new_obj['email'],
               "fonenumber":new_obj['fonenumber']}

        operations = [UpdateMany({'name': name_filter},{"$set":new})]

        results = contacts.bulk_write(operations)
        print("{} object modified.".format(results.modified_count))

        new["modified_count"] = results.modified_count

        return new

# connection test
if __name__ == '__main__':

    #client = MongoClient(host="localhost",port=27017)
    #try:
    #    print("Connected - "+str(client.address[0])+":"+str(client.address[1]))
    #except errors.ServerSelectionTimeoutError:
    #    print("Database Timeout")

    db = Contacts()
    print(db.get_all_contacts())