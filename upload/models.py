from django.db import models

from utils.base_model import BaseModel


# Create your models here.

class carts(BaseModel):
    CARTSID = models.CharField(max_length=200,db_index=True)
    class Meta:
        db_table='carts'
class pictures(BaseModel):
    carts = models.ForeignKey(carts,related_name="carts_pictures",on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photos', default='avatar.jpg')
    class Meta:
        db_table='pictures'