from django.urls import path
from .views import index, by_rubric, add_and_save, add #, add_save, BdCreateView,


app_name = 'bboard'
urlpatterns = [
    path('<int:rubric_id>/', by_rubric, name='by_rubric'),
    path('add/', add_and_save, name='add'),
    # path('add/save', add_save, name='add_save'),
    # path('add/', BdCreateView.as_view(), name='add'),
    path('', index, name='index'),
]
