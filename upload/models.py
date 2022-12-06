from django.db import models

from utils.base_model import BaseModel


# Create your models here.
class pictures(BaseModel):
    cartsid = models.CharField(max_length=200,db_index=True,default='1')
    photo = models.ImageField(upload_to='photos', default='avatar.jpg')
    class Meta:
        db_table='pictures'