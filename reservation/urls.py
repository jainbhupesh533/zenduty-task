from django.urls import *
from .views import *

urlpatterns = [
	path('books/', BooksApiView.as_view()),
	path('allocate/', IssueBooksApiView.as_view()),
	path('due/', MemberDuesAPiView.as_view()),
	path('return/', ReturnBookApiView.as_view()),
	path('analytics/', AnalyticsView.as_view(), name='analytics'),
]