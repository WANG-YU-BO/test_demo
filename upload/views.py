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
from new_demo.settings import MEDIA_ROOT, shopLimitedDict, DOMAIN_URL
from upload.models import pictures
from utils.compress_image import compress_image
from utils.judgearea import judgearea


class UploadView(APIView):
    def post(self,request):
        tk=request.META.get('X-storeHash')
        if pictures.objects.filter(cartsid=request.data.get('CARTSID')).count()>=shopLimitedDict[judgearea(tk)]:
            return JsonResponse({
                "code":404,
                "message":"more than {} pictures were uploaded".format(shopLimitedDict[judgearea(tk)])
            })
        pic=pictures.objects.create(
            cartsid=request.data.get('CARTSID'),
            photo=request.FILES.get('photo'),
        )
        path=os.path.join(MEDIA_ROOT,str(pic.photo))
        try:
            compress_image(path)
        except:
            os.remove(path)
            pictures.objects.filter(id=pic.id).delete()
            return JsonResponse({
                "code":404,
                "message":"invalid input photo"
            })
        return JsonResponse({
            "code":200,
            "message":"success",
            "data":{
                "pic-id":pic.id,
                "pic-uri":pic.photo.url,
                "pic-url":DOMAIN_URL+pic.photo.url
            }
        })
    def get(self,request):
        return render(request, 'upload.html', locals())

class DeletePhotoView(APIView):
    def post(self,request):
        if not pictures.objects.filter(id=request.data.get('pic_id'),cartsid=request.data.get('CARTSID')).first():
            return JsonResponse({
                "code":404,
                "message":"pic not exist"
            })
        path=str(pictures.objects.filter(id=request.data.get('pic_id'),cartsid=request.data.get("CARTSID")).first().photo)
        os.remove(os.path.join(MEDIA_ROOT,path))
        pictures.objects.filter(id=request.data.get('pic_id')).delete()
        return JsonResponse({
            "code":200,
            "message":"success"
        })