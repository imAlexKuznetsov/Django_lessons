from django.urls import path
from .views import index, by_rubric, add_and_save, detail,  add,  BdCreateView, BdByRubricView, BdDetailView, BdAddView
from .views import BdEditView, BdDeleteView


app_name = 'bboard'
urlpatterns = [
    # path('item/<int:bb_id>/', detail, name='detail'),
    # path('<int:rubric_id>/', by_rubric, name='by_rubric'),
    # path('add/', add_and_save, name='add'),
    # path('add/save', add_save, name='add_save'),
    # path('add/', BdCreateView.as_view(), name='add'),
    path('delete/<int:pk>', BdDeleteView.as_view(), name='delete'),
    path('edit/<int:pk>', BdEditView.as_view(), name='edit'),
    path('add/', BdAddView.as_view(), name='add'),
    path('<int:rubric_id>/', BdByRubricView.as_view(), name='by_rubric'),
    path('detail/<int:pk>/', BdDetailView.as_view(), name='detail'),
    path('', index, name='index'),
]
