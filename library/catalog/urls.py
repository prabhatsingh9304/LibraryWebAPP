from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('genres/', views.GenreListView.as_view(), name='genres'),
    path('genre/<int:pk>', views.GenreDetailView.as_view(), name='genre-detail'),  
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('borrowdbooks/', views.LoanedBooksStaffListView.as_view(), name='borrowed'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('books/create/', views.BookCreate.as_view(), name='books-create'),
    path('books/bookinstance/', views.BookInstanceCreate.as_view(), name='books-inst'),
    path('book/<int:pk>/update_book/', views.BookUpdate.as_view(), name='books-update'),
    path('book/<int:pk>/delete_book/', views.BookDelete.as_view(), name='books-delete'),
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update_author/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete_author/', views.AuthorDelete.as_view(), name='author-delete'),
    path('genre/create/', views.GenreCreate.as_view(), name='genre-create'),
    path('genre/<int:pk>/update_genre/', views.GenreUpdate.as_view(), name='genre-update'),
    path('genre/<int:pk>/delete_genre/', views.GenreDelete.as_view(), name='genre-delete'),
    path('book/<uuid:pk>/borrow/', views.borrow_book, name='borrow_book'),
    path('search/',views.search,name='search')
]