import os
from io import BytesIO

from PIL import ImageFile
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.db import models
# Create your views here.
import json

from rest_framework.views import APIView
from PIL import Image
from new_demo.settings import MEDIA_ROOT
from upload.models import carts,pictures
from utils.compress_image import compress_image


class UploadView(APIView):
    def post(self,request):
        if not pictures.objects.filter(carts=carts.objects.filter(CARTSID=request.data.get('CARTSID')).first()):
            return JsonResponse({
                "code":404,
                "message":"cart do not exist"
            })
        if pictures.objects.filter(carts=carts.objects.filter(CARTSID=request.data.get('CARTSID')).first()).count()>=5:
            return JsonResponse({
                "code":404,
                "message":"more than 5 pictures were uploaded"
            })
        pic=pictures.objects.create(
            carts=carts.objects.filter(CARTSID=request.data.get('CARTSID')).first(),
            photo=request.FILES.get('photo'),
        )
        path=os.path.join(MEDIA_ROOT,str(pic.photo))
        compress_image(path)
        return JsonResponse({
            "code":200,
            "message":"success",
            "data":{
                "pic-id":pic.id,
            }
        })
    def get(self,request):
        return render(request, 'upload.html', locals())

class DeletePhotoView(APIView):
    def post(self,request):
        if not pictures.objects.filter(id=request.data.get('pic_id')).first():
            return JsonResponse({
                "code":404,
                "message":"pic not exist"
            })
        path=str(pictures.objects.filter(id=request.data.get('pic_id')).first().photo)
        os.remove(os.path.join(MEDIA_ROOT,path))
        pictures.objects.filter(id=request.data.get('pic_id')).delete()
        return JsonResponse({
            "code":200,
            "message":"success"
        })