from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
import datetime
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from catalog.forms import RenewBookForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from catalog.models import Book
from django.urls import reverse
from django.views.generic import TemplateView






# Create your views here.
# Book Content View
class BookListView(generic.ListView):
    model = Book
    paginate_by = 10

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10

class AuthorDetailView(generic.DetailView):
    model = Author

    def author_detail_view(request, primary_key):
        try:
            author = Author.objects.get(pk=primary_key)
        except author.DoesNotExist:
            raise Http404('Author does not exist')
        return render(request, 'catalog/author_detail.html', context={'author': author})
class GenreListView(generic.ListView):
    model = Genre
    paginate_by = 10
class GenreDetailView(generic.DetailView):
    model = Genre

    def genre_detail_view(request, primary_key):
        try:
            genre = Genre.objects.get(pk=primary_key)
        except author.DoesNotExist:
            raise Http404('Genre does not exist')
        return render(request, 'catalog/genre_detail.html', context={'genre': genre})



class BookDetailView(generic.DetailView):
    model = Book

    def book_detail_view(request, primary_key):
        try:
            book = Book.objects.get(pk=primary_key)
        except Book.DoesNotExist:
            raise Http404('Book does not exist')
        return render(request, 'catalog/book_detail.html', context={'book': book})




def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')



class LoanedBooksStaffListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_staff.html'
    paginate_by = 10   
    def my_view(request):
        model = BookInstance
        template_name ='catalog/bookinstance_list_borrowed_staff.html'
        paginate_by = 10
        return BookInstance.objects.all().filter(status__exact='o').order_by('due_back')





def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('books') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)

class BookCreate(CreateView):
    model = Book
    fields = '__all__'
    def get_absoulut_url(self):
        return reverse('index',kwargs={'pk':self.pk})

class BookInstanceCreate(CreateView):
    model = BookInstance
    fields = '__all__'
    template_name ='catalog/bookinst_form.html'
    success_url = reverse_lazy('books')    
class BookUpdate(UpdateView):
    model = Book
    fields = '__all__' # Not recommended (potential security issue if more fields added)

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    

class AuthorCreate(CreateView):
    model = Author
    fields = ['first_name', 'last_name']
    

class AuthorUpdate(UpdateView):
    model = Author
    fields = '__all__' # Not recommended (potential security issue if more fields added)
    

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    

class GenreCreate(CreateView):
    model = Genre
    fields = '__all__'
    
    def get_absoulut_url(self):
        return reverse('books',kwargs={'pk':self.pk})

class GenreUpdate(UpdateView):
    model = Genre
    fields = '__all__' # Not recommended (potential security issue if more fields added)
    
class GenreDelete(DeleteView):
    model = Genre
    success_url = reverse_lazy('genres')

def borrow_book(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        if request.user.is_authenticated:
            book_instance.borrower=request.user
            book_instance.due_back=datetime.date.today() + datetime.timedelta(weeks=3)
            book_instance.status= 'o'
            book_instance.save()
            return HttpResponseRedirect(reverse('books'))
        context = {
            'book_instance': book_instance,
        }
    return render(request, 'catalog/book_detail.html', context)

def search(request):
    books=Book.objects.all()
    context= {'book': book}
    return render(request,'catalog/search.html',context)