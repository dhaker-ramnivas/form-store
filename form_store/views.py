from django.shortcuts import render

# Create your views here.
import logging
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework import status

from .serializers import FormDataSerializer
from  .models import FormData

from rest_framework.response import Response
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
logger = logging.getLogger(__name__)



class DataStore(APIView):
    """ store and retrive data"""

    serializer_class = FormDataSerializer
    def get(self, request):

        form_data = FormData.objects.all()
        serializer=FormDataSerializer(form_data,many=True)
        return Response(serializer.data)


        #----------OR------------
        # form_list=[]
        # form_data=FormData.objects.all()
        # for form in form_data:
        #     temp={
        #         "name":form.name,
        #         "description":form.description,
        #         "data":form.data
        #     }
        #     form_list.append(temp)
        #
        # return Response({"form data":form_list},status=status.HTTP_200_OK)

    def post(self, request):

        # for field in request.data:
        #     # TODO write specific data
        #     print(field,request.data.get(field))
        #     setattr(FormData,field, request.data.get(field))
        try:
            man_data=["name","description","data"]


            create_form=FormData(name=request.data.get("name"),data=request.data.get("data"),\
                                 description=request.data.get("description"))
            create_form.save()
            if create_form:
                return Response({"data saved successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"Some Internal Error Occur,Try Again"},status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"Some Internal Error Occur,Try Again"}, status=status.HTTP_400_BAD_REQUEST)
