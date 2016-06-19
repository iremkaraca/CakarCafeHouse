# -*- coding: utf-8 -*-

def Menu():
    categories = db().select(db.categories.ALL)
    return dict(page_title="Menü", categories=categories)
def food():
	categories = db.categories(request.args(0,cast=int))
	if not categories:
		session.flash='page not found'
		redirect(URL('index'))
	foods = db(db.foods.category_id==categories.id).select()
	return dict(page_title="Yiyecek ve İçecekler", categories=categories, foods=foods)
def index():
	random = db().select(db.gallery.ALL, orderby='<random>', limitby=(0,1))
	return dict(page_title="Çakar Cafe&House", random=random)

def Hakkinda():
	return dict(page_title="Hakkında")

def Mekan():
	image_per_page=6 #bir sayfadaki gösterilecek image sayısı
	page = request.args(1, cast=int, default=0)
	start_limit = page * image_per_page
	stop_limit = start_limit + image_per_page
	gallery = db().select(db.gallery.ALL, limitby=(start_limit,stop_limit))
	return dict(page_title="Mekan", gallery=gallery, page=page)

def Spesiyaller():
	spesiyaller = db((db.foods.hikaye != None) & (db.foods.hikaye != "")).select(orderby='<random>')
	print(spesiyaller)
	return dict(page_title="Spesiyaller", spesiyaller=spesiyaller)	

def yorumlarim():
	kullanici_comments = db(db.yorumlar.created_by==auth.user_id).select()
	print(kullanici_comments)
	return dict(page_title="Yorumlarım", kullanici_comments=kullanici_comments)

"""
@auth.requires_login()
def update_yorumlar():
	update_form = crud.update(db.yorumlar, request.args(0))
	return dict(page_title="Yorum Güncelle", update_form=form)

def delete_yorumlar():
	delete_form = crud.delete(db.yorumlar, request.args(0))
	return dict(page_title="Yorum Sil", delete_form=delete_form)

def search_yorumlar():
	search_form = crud.search(db.yorumlar, request.args(0))
	return dict(page_title="Yorum Ara", search_form=search_form)
"""
#######user crud operations#####
def give_create_permission(form):
    group_id = auth.id_group('user_%s' % auth.user.id)
    auth.add_permission(group_id, 'read', db.yorumlar)
    auth.add_permission(group_id, 'create', db.yorumlar)
    auth.add_permission(group_id, 'select', db.yorumlar)

def give_update_permission(form):
	yorumlar_id = form.vars.id 
	group_id = auth.id_group('user_%s' % auth.user.id) # auth.id_group('user_3')
	auth.add_permission(group_id, 'update', db.yorumlar, yorumlar_id)
	auth.add_permission(group_id, 'delete', db.yorumlar, yorumlar_id)

auth.settings.register_onaccept = give_create_permission # kayıt olduğunda create yetkisi veriyoruz.
crud.settings.auth = auth #permissionların geçerli olmasını sağlıyor.

@auth.requires_login()
def update_yorumlar():
	updates = db.yorumlar(request.args(0,cast=int))
	if not updates:
		session.flash='page not found'
		redirect(URL('index'))
	form = crud.update(db.yorumlar, updates)
	return dict(page_title="Yorum Güncelle", form = form)

def yorum():
	resim = db.gallery(request.args(0,cast=int))
	if not resim:
		session.flash='page not found'
		redirect(URL('index'))
	db.yorumlar.gallery_id.default = resim.id
	if auth.user != None:
		form = crud.create(db.yorumlar, onaccept=give_update_permission)
	else:
		form = None
	comments = db(db.yorumlar.gallery_id == resim.id).select()
	print(comments) # yess
	return dict(page_title="Yorumlar", resim=resim, form=form, comments=comments)

# iletisim formları
def iletisim():
	return dict(page_title="İletişim")

def soru_iletisim():
	form = SQLFORM(db.iletisim)
	return dict(page_title="Görüş ve Öneri Formu", form=form)

@auth.requires_login()
def rezervasyon_iletisim():
	form = SQLFORM(db.rezervasyon)
	return dict(page_title="Rezervasyon Formu", form=form)

#admin tablo işlemleri
@auth.requires_membership('admin')
def edit_kategori_table():
    Kategori_Tablosu = SQLFORM.grid(db.categories)
    page_title="Edit Kategori"
    return locals()

@auth.requires_membership('admin')
def edit_foods_table():
    Foods_Tablosu = SQLFORM.grid(db.foods)
    page_title="Edit Foods"
    return locals()

@auth.requires_membership('admin')
def edit_gallery_table():
	Gallery_Tablosu = SQLFORM.grid(db.gallery)
	page_title="Edit Gallery"
	return locals()

@auth.requires_membership('admin')
def edit_yorumlar_table():
	Yorumlar_Tablosu = SQLFORM.grid(db.yorumlar)
	page_title="Edit Yorumlar"
	return locals()

def report():
	return dict(page_title="Report")
def user():
    return dict(page_title="login", form=auth())
@cache.action()
def download():
    return response.download(request, db)

def call():
    return service()
