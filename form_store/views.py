from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
# Create your views here.
import logging
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework import status
from bson.objectid import ObjectId

from .serializers import FormDataSerializer
from  .models import FormData
import coreapi

from rest_framework.decorators import api_view,renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.schemas import AutoSchema

from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
logger = logging.getLogger(__name__)
import json


from pymongo import MongoClient
from rest_framework.response import Response

url="mongodb://dbuser:dbpass123@localhost:27017/"
import json

class MongoConnection(object):

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client['form_Store_test']

    def get_collection(self, name):
        self.collection = self.db[name]


class MyCollection(MongoConnection):

    def __init__(self,collection_name):
       super(MyCollection, self).__init__()
       self.get_collection(collection_name)

    def insert_form(self,obj):
        insertID = self.collection.insert_one(obj).inserted_id
        logger.info("Insert Form with data:"+str(obj)+"\n Insertion ID: "+str(insertID))
        return insertID

    # def update_and_save_form(self, obj):
    #    # if self.collection.find({"_id":obj["_id"]}).count():
    #    #     logger.info("update and save form function called with data:"+str(obj))
    #    #     updateID=self.collection.update({"_id":obj["_id"]},obj)
    #    # else:
    #    #      insertID=self.collection.insert_one(obj).inserted_id
    #    #      return insertID
    #
    #     updateID=self.collection.update_one({"_id":obj["_id"]},obj,upsert=True)
    #     return updateID

    def remove(self, obj):
        if self.collection.find({"name":obj["name"]}).count():
           self.collection.delete_one({ "id": 1})

    def get_forms(self,form_id=None):
        print("id",str(form_id))
        if not form_id:
            cursor = self.collection.find({})
            list=[]
            for document in cursor:
                list.append(document)
            return  list
        elif form_id:
            cursor = self.collection.find({"_id":ObjectId(form_id)})
            print("result data count",cursor.count())
            list = []
            for document in cursor:
                list.append(document)
            return  list


    def get_form_by_name(self, form_name=None):
        print("id", str(form_name))
        if not form_name:
            cursor = self.collection.find({})
            list = []
            for document in cursor:
                list.append(document)
            return list
        else:
            cursor = self.collection.find({"name":form_name})
            print("result data count", cursor.count())
            list = []
            for document in cursor:
                list.append(document)
            return list


col_obj = MyCollection('user')




@csrf_exempt
@api_view(('POST',))
@renderer_classes((JSONRenderer,))
def insertForm(request):
    try:
        try:
          json_data = json.loads(request.body.decode("utf-8"))
        except KeyError:
         return Response({"Malformed data!"},status=status.HTTP_400_BAD_REQUEST)

        insertId=col_obj.insert_form(json_data)

        if insertId:
            return Response({"Message": "good do it now","id":str(insertId)},status=status.HTTP_200_OK)
        else:
            return Response({"Message:Error"},status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"Message:Error"+str(e)}, status=status.HTTP_400_BAD_REQUEST)



@csrf_exempt
@api_view(('POST',))
@renderer_classes((JSONRenderer,))
def updateForm(request):
    try:
        try:
          json_data = json.loads(request.body.decode("utf-8"))
        except KeyError:
         return Response({"Malformed data!"},status=status.HTTP_400_BAD_REQUEST)

        updateID=col_obj.update_and_save_form(json_data)

        if updateID:
            return Response({"Message": "data updated","id":str(updateID)},status=status.HTTP_200_OK)
        else:
            return Response({"Message:Error"},status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"Message:Error"+str(e)}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(('GET',))
@renderer_classes((JSONRenderer,))
def getList(request):
    print("Request received")
    try:
        forms=col_obj.get_forms()

        if forms:
            return Response({"data":str(forms)},status=status.HTTP_200_OK)
        else:
            return Response({"Message:Data Not Found"},status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"Message:Error"+str(e)}, status=status.HTTP_400_BAD_REQUEST)




@csrf_exempt
@api_view(('GET',))
@renderer_classes((JSONRenderer,))
def getFormById(request,form_id):
    print("Request received",form_id)
    try:
        forms=col_obj.get_forms(form_id)

        if forms:
            return Response({"data":str(forms)},status=status.HTTP_200_OK)
        else:
            return Response({"Message:Data Not Found"},status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"Message:Error"+str(e)}, status=status.HTTP_400_BAD_REQUEST)




@csrf_exempt
@api_view(('GET',))
@renderer_classes((JSONRenderer,))
def getFormByName(request,form_name):
    print("Request received",form_name)
    try:
        forms=col_obj.get_form_by_name(form_name)

        if forms:
            return Response({"data":str(forms)},status=status.HTTP_200_OK)
        else:
            return Response({"Message:Data Not Found"},status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"Message:Error"+str(e)}, status=status.HTTP_400_BAD_REQUEST)