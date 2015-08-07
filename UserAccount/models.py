from django.db import models

class UserModel(models.Model):
	model_username = models.TextField()
	model_password = models.TextField()	
        model_activation_key=models.IntegerField() 
	def __unicode__(self):
 		return self.model_username
	class Meta:
        	db_table = 'usermodel'
        	verbose_name = 'UserModel'
       	 	verbose_name_plural = 'UserModels'


