from django.shortcuts import render
from rango.models import Category, Page
from rango.forms import CategoryForm
from rango.forms import PageForm
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse

def index(request):
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by the number of likes in descending order.
    # Retrieve the top 5 only -- or all if less than 5.
    # Place the list in our context_dict dictionary (with our boldmessage!)
    # that will be passed to the template engine.
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list

    # query database for all pages stored
    # order the pages by number of likes in descending order
    # retrieve top 5
    # place list in context_dict
    page_list = Page.objects.order_by('-views')[:5]
    context_dict['pages'] = page_list
    # Render the response and send it back!
    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    return render(request, 'rango/about.html')


def show_category(request, category_name_slug):

    # create a context dictionary which we can pass to the template rendering engine
    context_dict = {}

    try:
        # can we find a category with the given name?
        # if we cannot, the .get method raises an DoesNotExist exception
        category = Category.objects.get(slug=category_name_slug)

        # retrieve all of the associated pages
        # the filter() will return a list of page objects or an empty list
        pages = Page.objects.filter(category=category)

        # adds our results list to the templates context under name pages
        context_dict['pages'] = pages
        # we also add the category object from the database to the context dictionary
        # we'll use this in the template to verify that the category exists
        context_dict['category'] = category
    except Category.DoesNotExist:
    # we get here if we didn't find the specified category
        # dont' do anything - the template will display a message saying no category
        context_dict['category'] = None
        context_dict['pages'] = None
    # render response and return it to the client
    return render(request, 'rango/category.html', context=context_dict)


def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():

            form.save(commit=True)

            return redirect('/rango/')
        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    # you cannot add a page to a category that does not exist
    if category is None:
        return redirect('/rango/')

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('rango:show_category',
                                        kwargs={'category_name_slug': category_name_slug}))
            else:
                print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)

