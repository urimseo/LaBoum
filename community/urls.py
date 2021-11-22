from django.urls import path, include
from . import views

app_name = 'community'

urlpatterns = [
    # 리뷰작성
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:review_pk>/', views.detail, name='detail'),
    path('<int:review_pk>/update/', views.update_review, name='update_review'),
    path('<int:review_pk>/delete/', views.delete_review, name='delete_review'),

    # 댓글작성
    path('<int:review_pk>/comments/create/', views.create_comment, name='create_comment'),
    path('<int:review_pk>/comments/<int:comment_pk>/delete/', views.delete_comment, name='delete_comment'),
    
    #좋아요 
    path('<int:review_pk>/like/', views.like, name='like'),
    

]
