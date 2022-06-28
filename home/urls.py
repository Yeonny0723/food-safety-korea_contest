from django.urls import path
from . import views # 같은 폴더 내의 views.py를 import
from django.conf import settings
from django.conf.urls.static import static

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/',views.logout_view, name='logout'),
    path('signup/',views.signup_view, name='signup'),
    path('recipe/<int:recipeID>/', views.recipe_detail, name='recipe_detail'),
    path('item/<int:itemID>/', views.item_detail, name='item_detail'),
    path('search/', views.search, name='search'),
    path('analyze/', views.analyze, name='analyze'),
    path('analyze/pass_val',views.pass_val, name='pass_val'),
    path('comments/', views.comments, name='comments'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
