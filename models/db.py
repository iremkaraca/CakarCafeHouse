db = DAL("sqlite://storage.sqlite")
# -*- coding: utf-8 -*-

from gluon.contrib.appconfig import AppConfig
myconf = AppConfig(reload=True)

response.generic_patterns = ['*'] if request.is_local else []

response.formstyle = myconf.take('forms.formstyle')
response.form_label_separator = myconf.take('forms.separator')

from gluon.tools import Auth, Service, PluginManager, prettydate
from gluon.tools import Crud

crud = Crud(db)
auth = Auth(db)
service = Service()
plugins = PluginManager()
request.env.http_host = 'www.cakarcafehouse.com'
## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.take('smtp.server')
mail.settings.sender = myconf.take('smtp.sender')
mail.settings.login = myconf.take('smtp.login')

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

db.define_table('categories',
   Field('category_name', 'string', unique=True),
   format = '%(category_name)s'
)
   
"""db.categories.truncate()"""

db.define_table('foods',
   Field('category_id', 'reference categories'),
   Field('food_name', 'string', unique=True),
   Field('price', 'double'),
   Field('description' , 'text'),
   Field('image', 'upload'),
   Field('hikaye', 'text')
)
  
db.define_table('gallery',
   Field('dosya', 'upload'),
   format = '%(dosya)s'
)

"""db.auth_user._format = '%(first_name)s'"""

db.define_table('yorumlar',
   Field('gallery_id', 'reference gallery'),
   Field('icerik', 'text'),
   auth.signature
)

db.define_table('iletisim',
                Field('ad_soyad', 'string'),
                Field('email'),
                Field('telefon', 'float'),
                Field('mesaj', 'text'),
)


db.define_table('rezervasyon',
                Field('ad_soyad', 'string'),
                Field('email'),
                Field('telefon', 'float'),
				Field('tarih', 'date'),
				Field('kisi_sayisi', 'string'),
                Field('ek_mesaj', 'text')
)

############################################ Table Requires###############

#categories tablosu
db.categories.category_name.requires = IS_NOT_EMPTY(error_message='Please enter the category name!')
db.categories.category_name.requires = IS_NOT_IN_DB(db, db.categories.category_name)

#foods tablosu
db.foods.food_name.requires = IS_NOT_IN_DB(db, db.foods.food_name)
db.foods.food_name.requires = IS_NOT_EMPTY(error_message='Please enter the food name!')
db.foods.price.requires = IS_NOT_EMPTY(error_message='Please enter the food price!')
db.foods.image.requires = IS_EMPTY_OR(IS_IMAGE(error_message='Please enter the valid image format!(BMP, GIF, JPEG, PNG)'))

#GALLERY TABLOSU
db.gallery.dosya.requires = IS_NOT_EMPTY()
db.gallery.dosya.requires = IS_IMAGE(error_message='Please enter the valid image format!(BMP, GIF, JPEG, PNG)')

#yorumlar tablosu
db.yorumlar.icerik.requires = IS_NOT_EMPTY(error_message="Please enter your comment!")
db.yorumlar.gallery_id.writable = db.yorumlar.gallery_id.readable = False

#iletisim tablosu
db.iletisim.ad_soyad.requires = IS_NOT_EMPTY(error_message="Please enter your name and surname!")
db.iletisim.email.requires = (IS_EMAIL("Please check your e-mail address!"),
                              IS_NOT_EMPTY("Please enter your e-mail!"))
db.iletisim.telefon.requires = IS_LENGTH(minsize=11, 
                             error_message="Please enter the valid number!(Exp: '05XX XXX XX XX')")
db.iletisim.mesaj.requires = IS_NOT_EMPTY('Please enter your message!')

#rezervasyon tablosu
db.rezervasyon.ad_soyad.requires = IS_NOT_EMPTY(error_message="Please enter your name and surname!")
db.rezervasyon.email.requires = (IS_EMAIL("Please check your e-mail address!"),
                              IS_NOT_EMPTY("Please enter your e-mail!"))
db.rezervasyon.telefon.requires = IS_LENGTH(minsize=11, 
                             error_message="Please enter the valid number!(Exp: '05XX XXX XX XX')")
db.rezervasyon.tarih.requires = IS_DATE(format=T('%Y-%m-%d'), error_message='must be YYYY-MM-DD!')
db.rezervasyon.kisi_sayisi.requires = IS_NOT_EMPTY('Please enter the number')

""""db.yorumlar.truncate()"""