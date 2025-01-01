from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('search_results', views.search, name='search_results'),
    path('my-listings', views.my_listings, name= 'my_listings'),
    path('watchlist/',views.watchlist, name = 'watchlist'),
    path('delete_watchlist_item/<int:id>/', views.delete_watchlist_item, name= 'delete_watchlist_item'),
    path('watchlist/add/<int:id>/', views.add_to_watchlist, name='add_to_watchlist'),  # For adding a listing

    path('listing/<int:id>/', views.listing, name='listing'),
    path('create-listing', views.create_listing, name='create_listing'),
    path('delete-listing/<int:id>/', views.delete_listing, name='delete_listing'),

    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)