from django.urls import path
from craigslist.views import home, new_search

app_name = 'craigslist'

urlpatterns = [
    path('', home, name='home'),
    path('new_search/', new_search, name='new_search'),
]
