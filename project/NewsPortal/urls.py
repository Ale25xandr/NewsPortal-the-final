from django.conf import settings
from django.urls import path, include

from .views import *

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view()),
    path('create/', PostCreate.as_view(), name='create'),
    path('<int:pk>/update/', PostUpdate.as_view()),
    path('<int:pk>/delete/', PostDelete.as_view()),
    path('<int:pk>/UpdateUser/', UserUpdate.as_view(), name='update_user'),
    path('search/', PostListSearch.as_view(), name='post_search'),
    path('logout/', logout_user, name='logout'),
    path('password_change/', User_password_change.as_view(), name='passchange'),
    path('upgrade/', add_author, name='upgrade'),
    path('category/<int:pk>/', CategoryList.as_view(), name='category_list'),
    path('category/<int:pk>/subscrubers/', add_category, name='add_category'),
    path('confirmed_email/', Ok_Email.as_view(), name='ok'),
    path('create_ok/', no_create, name='no_create'),
    path('create_no/', CreateNo.as_view(), name='create_no'),
]


