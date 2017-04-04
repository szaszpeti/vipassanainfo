
from django.shortcuts import render, HttpResponse, get_object_or_404,Http404, redirect

from django.shortcuts import render
from .forms import UserForm

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from .models import Post, Document
from django.db.models import Q
from django.http import HttpResponseRedirect
from .forms import PostForm
from django.utils import timezone

# Create your views here.


def register(request):

    registered = False

    if request.method == 'POST':

        user_form = UserForm(data=request.POST)

        # Check to see  form is valid
        if user_form.is_valid():

            user = user_form.save()  # Save User Form to Databas
            user.set_password(user.password)  # Hash the password
            user.save()  # Update with Hashed password
            registered = True  # Registration Successful!

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request, 'blog/register.html',
                  {'user_form': user_form,
                   'registered': registered,
                   })




def user_login(request):

    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('blog:welcome'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'blog/login.html', {})


@login_required
def welcome(request):
    username = request.user.username


    return render(request, 'blog/welcome.html', {'username':username})





@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return render(request, 'blog/login.html')

def post_create(request):
    # if not request.user.is_staff or not request.user.is_superuser:
    #     raise Http404
    # if not request.user.is_authenticated():
    #     raise Http404
    form = PostForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        instance = form.save(commit=False)
        #instance.user = request.user
        print (form.cleaned_data.get('title'))
        instance.save()
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {'form':form}



    return render(request, 'blog/post_form.html', context)

def post_detail(request, slug=None):

    post = get_object_or_404(Post, slug=slug)
    document = post.document_set.all()

    return render(request, 'blog/post_detail.html', {'post':post, 'document':document})

def read(request, slug=None):

    selected_document = get_object_or_404(Document, slug=slug)

    return render(request, 'blog/document_read.html', {'doc':selected_document})



# def post_detail(request, slug=None):

    instance = get_object_or_404(Post, slug=slug)
    # if instance.draft or instance.publish > timezone.now().date():
    #     if request.user.is_staff or not request.user.is_superuser:
    #         raise Http404


    context = {
        "title": instance.title,
        'instance':instance,

    }
    # if request.user.is_authenticated():
    #     context = {
    #
    #         "title":"welcome USer"
    #     }
    # else:
    #     context = {
    #         'title':'please login'
    #     }
    return render(request, 'blog/post_detail.html', context)

def post_list(request):
    # queryset_list = Post.objects.filter(draft=False).filter(publish__lte=timezone.now()) #.order_by("-timestamp")
    # queryset_list = Post.objects.all()  # .order_by("-timestamp") after adding PostManager change to active
    # queryset_list = Post.objects.active() #.order_by("-timestamp")
    # if request.user.is_staff or request.user.is_superuser:
    queryset_list = Post.objects.all()



    today = timezone.now().date()
    query = request.GET.get("q")
    if query:
        # queryset_list = queryset_list.filter(title__icontains=query) this is simple
        queryset_list = queryset_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(user__username__icontains=query)



        ).distinct() # so NOOOO DUPLICATES

    paginator = Paginator(queryset_list, 10)  # Show 25 contacts per page
    page_request_var = 'page'

    page = request.GET.get(page_request_var)

    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        'title':'working',
        'object_list':queryset,
        'page_request_var':page_request_var,
        'today':today
    }
    return render(request, 'blog/post_list.html', context)





from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def listing(request):
    contact_list = Contacts.objects.all()


    return render(request, 'blog/list.html', {'contacts': contacts})



def post_update(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)

    if form.is_valid():
        instance = form.save(commit=False)
        print(form.cleaned_data.get('title'))
        instance.save()
        messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Not updated")

    context = {
        "title": instance.title,
        'instance': instance,
        'form':form
    }

    return render(request, 'blog/post_form.html', context)


def post_delete(request, id=None):
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, "Successfuly Deleted")
    return redirect("posts:list")