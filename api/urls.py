from django.urls import path
from . import views

#FOR EVERY NEW VIEW API MUST ADD PATH

urlpatterns = [
    path('', views.getRoutes, name="routes"),
    path('users/', views.getUsers, name="users"),
    path('users/<str:pk>', views.getUser, name="user"),
    path('user/<str:pk>',views.getUserByEmail,name='user'),
    path('stocks/', views.getStock, name="stocks"),
    path('postUser/', views.create_user, name='create_user'),
    path('postStock/<str:stock_ticker>', views.create_Stock, name='create_Stock'),
    path('postStockToUser/<str:u_id>/<str:ticker>/<str:shares>', views.addStockToUser, name='create_Stock'),
    path('getUserStocks/<str:u_id>', views.getUserStocks,name='get_stocks'),
    path('updateStockShares/<str:user_id>/<stock_ticker>/<str:shares>', views.UpdateUserStockBuy, name='update_Stock'),
    path('updateStockSharesSell/<str:user_id>/<stock_ticker>/<str:shares>', views.UpdateUserStockSell, name='update_Stock'),
    path('updateMoneySpent/<str:pk>/<str:money>', views.updateUserMoneySpent, name='update_Money'),
    path('deleteUserStock/<str:userstock_id>', views.userStockDelete, name='delete_userStock'),
]