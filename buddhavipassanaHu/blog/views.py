
from django.shortcuts import render, HttpResponse, get_object_or_404,Http404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
from .forms import PostForm, DocumentForm
from django.utils import timezone
from  comments.forms import CommentForm

from comments.models import Comment
from django.contrib.contenttypes.models import ContentType
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
                return HttpResponseRedirect(reverse('blog:list'))
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

def document_create(request):
    # if not request.user.is_staff or not request.user.is_superuser:
    #     raise Http404
    # if not request.user.is_authenticated():
    #     raise Http404

    form = DocumentForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        instance = form.save(commit=False)
        #instance.user = request.user
        print (form.cleaned_data.get('title'))
        instance.save()
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {'form':form}



    return render(request, 'blog/document_form.html', context)

def post_detail(request, slug=None):

    post = get_object_or_404(Post, slug=slug)
    document = post.document_set.all().order_by("-timestamp")


    return render(request, 'blog/post_detail.html', {'post':post,
                                                     'document':document,
                                                     })

def read(request, slug=None, postslug=None):

    document = get_object_or_404(Document, slug=slug)
    post = get_object_or_404(Post, slug=postslug)
    document_list = post.document_set.all().order_by("-timestamp")

    # content_type = ContentType.objects.get_for_model(Document)
    # # this will be like this Post.objects.get(id=instance.id)
    # obj_id = document.id
    # # This gives all the comments related to the id
    # comments = Comment.objects.filter(content_type=content_type, object_id=obj_id)

    #comments = document.comments
    initial_data = {
        "content_type": document.get_content_type,
        'object_id': document.id

    }
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid():
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get("object_id")
        content_data = form.cleaned_data.get('content')
        new_comment, created = Comment.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=obj_id,
            content=content_data,
        )

    comments = Comment.objects.filter_by_instance(document)




    return render(request, 'blog/document_read.html', {'document':document,
                                                       'document_list':document_list,
                                                       'postslug':postslug,
                                                       'comments':comments,
                                                       'form':form})



# def post_detail(request, slug=None):

    #instance = get_object_or_404(Post, slug=slug)
    # if instance.draft or instance.publish > timezone.now().date():
    #     if request.user.is_staff or not request.user.is_superuser:
    #         raise Http404


    # context = {
    #     "title": instance.title,
    #     'instance':instance,
    #
    # }
    # if request.user.is_authenticated():
    #     context = {
    #
    #         "title":"welcome USer"
    #     }
    # else:
    #     context = {
    #         'title':'please login'
    #     }
    #return render(request, 'blog/post_detail.html', context)

def post_list(request):
    # queryset_list = Post.objects.filter(draft=False).filter(publish__lte=timezone.now()) #.order_by("-timestamp")
    # queryset_list = Post.objects.all()  # .order_by("-timestamp") after adding PostManager change to active
    # queryset_list = Post.objects.active() #.order_by("-timestamp")
    # if request.user.is_staff or request.user.is_superuser:
    queryset_list = Post.objects.all().order_by("timestamp")



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


def document_update(request, slug=None):
    instance = get_object_or_404(Document, slug=slug)
    form = DocumentForm(request.POST or None, request.FILES or None, instance=instance)

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


def post_delete(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "Successfuly Deleted")
    return redirect("blog:list")

def document_delete(request, slug=None):
    instance = get_object_or_404(Document, slug=slug)
    instance.delete()
    messages.success(request, "Successfuly Deleted")
    return redirect("blog:list")