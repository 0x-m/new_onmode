"""

author: hamze ghaedi (github: 0x-m)

"""


from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import (
    Http404,
    HttpRequest,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotAllowed,
    HttpResponseNotFound,
    JsonResponse,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from apps.index.models import CreateShopGuide

from .forms import CommentForm, CreateShopForm, ProductForm, ShopForm
from .models import (
    Category,
    Collection,
    Comment,
    CreateShopRequest,
    Favourite,
    Option,
    Photo,
    Product,
    ProductFilter,
    ProductOptionValue,
    Shop,
)

# TODO: move to the shop custom manager!


@login_required
def product(request: HttpRequest, pid=None):
    """
    Add or edit a product
    add a new product if pid is not specified
    edit the product with id=pid if it is exist otherwise return 404
    """

    # Does user have any active shop ?
    user = request.user
    shop = get_object_or_404(Shop, owner=user, active=True)

    product = None
    if pid:  # product exists if not return 404
        product = get_object_or_404(Product, pk=pid, deleted=False)
    else:
        # request to add a new product
        if not shop.has_capacity():
            return HttpResponseForbidden(
                "you reached max allowed number of products"
            )  # TODO

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if not form.is_valid():
            return render(
                request,
                "shop/add_product.html/",
                {"errors": form.errors, "product": product},
            )

        print(form.cleaned_data["sales_price"])
        # NOTE: any better way?
        created = False
        if not product:
            # create a new product
            try:
                shop.inc_product_count()
                product = form.save(commit=False)
                product.shop = shop
                product.save()
                created = True
            except Exception as e:
                return HttpResponseBadRequest(
                    f"max allowed product restriction...!\n{e}"
                )  # TODO: needs a conceptual exception...
        else:
            form.save()  # update the product

        return render(
            request,
            "shop/add_product.html/",
            {"status": "created" if created else "edited", "product": product},
        )

    return render(request, "shop/add_product.html", {"product": product})


@login_required
def delete_product(request: HttpRequest, pid):
    """
    Mark a product as deleted if the product with id=pid
    exists otherwise return http 404
    """
    if not request.user.shop:
        return Http404()

    product = get_object_or_404(
        Product,
        pk=pid,
        shop=request.user.shop,
        shop__active=True,
        deleted=False,
    )
    if request.method == "POST":
        product.deleted = True
        product.shop.dec_product_count()
        product.save()
        return render(
            request, "shop/delete_product_consent.html", {"status": "success"}
        )  # TODO

    return render(
        request, "shop/delete_product_consent.html", {"product": product}
    )


@login_required
def add_related_product(request: HttpRequest, product_id):
    print("-------------------------")
    product = get_object_or_404(
        Product, pk=product_id, shop__owner=request.user, deleted=False
    )
    prod_code = request.GET.get("prod_code", None)
    related = get_object_or_404(Product, prod_code=prod_code, deleted=False)

    if product.relateds.count() > 5:
        return HttpResponseForbidden("not allowed")
    product.relateds.add(related)
    return redirect("users:add-option", pid=product.id)


@login_required
def delete_related_product(request: HttpRequest, product_id):
    product = get_object_or_404(
        Product, pk=product_id, shop__owner=request.user, deleted=False
    )
    prod_code = request.GET.get("prod_code", None)
    related_product = get_object_or_404(Product, prod_code=prod_code)
    if product == related_product:
        return HttpResponseForbidden()

    product.relateds.remove(related_product)
    return redirect("users:add-option", pid=product.id)


def filter(request: HttpRequest, shop_name):
    shop = get_object_or_404(Shop, name=shop_name, active=True)
    form = ProductFilter(
        data=request.GET,
        queryset=Product.objects.filter(
            deleted=False, shop__name=shop_name
        ).all(),
        request=request,
    )

    paginator = Paginator(form.qs, 20)
    pg = request.GET.get("page")
    page = None
    try:
        page = paginator.get_page(pg)
    except PageNotAnInteger:
        page = paginator.get_page(1)
    except EmptyPage:
        page = paginator.get_page(paginator.num_pages)

    return render(request, "shop/shop.html", {"page": page, "shop": shop})


@login_required
def add_option(request: HttpRequest, pid):
    if not request.user.has_shop:
        return Http404()

    product = get_object_or_404(
        Product, shop=request.user.shops.first(), pk=pid, deleted=False
    )

    if request.method == "POST":
        data = request.POST
        option_name = data.get("name", None)
        option_value = data.get("value", None)
        if not (option_name and option_value):
            return HttpResponseBadRequest("empty fields")

        option = get_object_or_404(Option, name=option_name)
        optval, created = ProductOptionValue.objects.get_or_create(
            product=product, option=option
        )
        if option.type in [Option.TYPES.Choices, Option.TYPES.MultiChoices]:
            option_value = (
                ",".join(data.getlist("value")) + ","
            )  # needed for filtering

        print(option_value, created)
        optval.value = option_value
        optval.save()
        return redirect("users:add-option", pid=pid)

        # return render(request, 'shop/product_options.html', {
        #     'product': product,
        #     'add_status': 'added' if created else 'edited',
        #     'option_name': option_name
        # })
    return render(request, "shop/product_options.html", {"product": product})


@login_required
def delete_option(request: HttpRequest, pid):
    if not request.user.has_shop:
        return Http404()

    product = get_object_or_404(
        Product, pk=pid, shop=request.user.shops.first(), deleted=False
    )

    if request.method == "POST":
        option_name = request.POST.get("name", None)
        if not option_name:
            return HttpResponseBadRequest()

        option = product.options.all().filter(name=option_name).first()
        if option:
            option.delete()
            return redirect("users:add-option", pid=pid)
        else:
            return Http404()

    return HttpResponseNotAllowed(["POST"])


@login_required
def add_photo(request: HttpRequest, pid):

    if request.method == "POST":
        user = request.user
        shop = get_object_or_404(Shop, owner=user, active=True)
        product = get_object_or_404(Product, pk=pid, shop=shop, deleted=False)

        photo = request.FILES.get("photo", None)
        url = request.POST.get("url")
        alt_text = request.POST.get("alt")

        if not (photo or url):
            return HttpResponseBadRequest(
                "empty fields" + "url:" + str(url) + "img:" + str(photo)
            )

        # in MBytes
        if photo:
            photo_size = photo.size  # in bytes
            if user.storage_has_capacity(photo_size):
                product_photo = Photo(product=product, img=photo, alt=alt_text)
                product_photo.save()
                user.consume_storage(photo_size)  # IMPORTANT....
                return redirect("users:add-option", pid=pid)

            else:
                return HttpResponseBadRequest(
                    "Run out of storage."
                )  # make decent error page

        if url:
            product_photo = Photo(product=product, url=url)
            product.photo.save()
            return redirect("users:add-option", pid=pid)

    return HttpResponseNotAllowed(["POST"])


@login_required
def change_preview_photo(request: HttpRequest, pid):
    if request.method == "POST":
        user = request.user
        shop = get_object_or_404(Shop, owner=user, active=True)
        product = get_object_or_404(Product, shop=shop, pk=pid, deleted=False)

        photo_id = request.POST.get("photo_id")
        if not photo_id:
            return HttpResponseBadRequest("photo_id is not provided")

        the_photo = product.photos.get(pk=photo_id)
        if the_photo:
            product.preview = the_photo
            product.save()
            return redirect("users:add-option", pid=pid)

    return HttpResponseNotAllowed(["POST"])


@login_required
def delete_photo(request: HttpRequest, pid):
    if request.method == "POST":
        user = request.user
        shop = get_object_or_404(Shop, owner=user, active=True)
        product = get_object_or_404(Product, pk=pid, shop=shop, deleted=False)
        photo_id = request.POST.get("photo_id")
        if not photo_id:
            return HttpResponseBadRequest("photo id is not entered")
        try:
            the_photo = product.photos.get(pk=photo_id)
            user.free_storage(
                the_photo.img.size
            )  # TODO: move to the photo post delete!
            the_photo.img.delete()  ##
            the_photo.delete()
            return redirect("users:add-option", pid=pid)
        except Photo.DoesNotExist:
            return HttpResponseNotFound("photo with  give id is not found")

    return HttpResponseNotAllowed(["POST"])


@login_required
def edit_shop(requeset: HttpRequest):

    # Does the user have any active shop if not return http404
    user = requeset.user
    shop = get_object_or_404(Shop, owner=user, active=True)

    if requeset.method == "POST":
        shop_form = ShopForm(requeset.POST, instance=shop)
        if not shop_form.is_valid():
            return render(
                requeset, "shop/about.html", {"status": "invalid", "shop": shop}
            )

        shop = shop_form.save(commit=False)
        logo = requeset.FILES.get("logo", None)
        banner = requeset.FILES.get("banner", None)
        if logo:
            if shop.logo:
                shop.logo.delete()
            shop.logo = logo
        if banner:
            if shop.banner:
                shop.banner.delete()
            shop.banner = banner
        shop.save()
        return render(
            requeset, "shop/about.html", {"status": "success", "shop": shop}
        )

    return render(requeset, "shop/about.html", {"shop": shop})


@login_required
def create_shop_request(request: HttpRequest):
    # Does the user have any shop...?
    # if so, it is not allowed to have more than one shop!
    if request.user.has_shop:
        return Http404()

    # Does the user have any request for creating a shop ?
    shop_req = None
    try:
        shop_req = CreateShopRequest.objects.get(user=request.user)
    except CreateShopRequest.DoesNotExist:
        pass

    guide = CreateShopGuide.objects.first()
    if request.method == "POST":
        form = None
        if shop_req:
            form = CreateShopForm(request.POST, instance=shop_req)
            # create shop request registered and not yet processed by admin
            # so it can not be edited.
            if not shop_req.rejected:
                return Http404()

            # admin rejected the request so, user must modify it.
            if form.is_valid():
                shop_req.rejected = False  # so admin must revisit it.
                shop_req = form.save()
                return render(
                    request,
                    "shop/create_shop.html",
                    {"status": "edited", "shop_req": shop_req, "guide": guide},
                )
            else:
                return render(
                    request,
                    "shop/create_shop.html",
                    {
                        "status": "invalid name",
                        "shop_req": shop_req,
                        "guide": guide,
                    },
                )

        else:
            # Create shop request does not exist so, create one...
            form = CreateShopForm(request.POST)
            if form.is_valid():
                shop_req = form.save(commit=False)
                shop_req.user = request.user
                shop_req.save()
                return render(
                    request,
                    "shop/create_shop.html",
                    {"status": "created", "shop_req": shop_req, "guide": guide},
                )

    # Handle Get request.
    return render(
        request,
        "shop/create_shop.html",
        {"status": "", "shop_req": shop_req, "guide": guide},
    )


def collection(request: HttpRequest, slug):

    collection = get_object_or_404(Collection, en_slug=slug)

    paginator = Paginator(collection.products.all(), 20)
    pg = request.GET.get("page")
    page = None
    try:
        page = paginator.get_page(pg)
    except PageNotAnInteger:
        page = paginator.get_page(1)
    except EmptyPage:
        page = paginator.get_page(paginator.num_pages)

    return render(
        request,
        "shop/collection.html",
        {"collection": collection, "page": page},
    )


# Collection refactored-------------------------------------------
class CollectionProductListView(ListView):
    paginate_by: int = 20
    template_name: str = "shop/collection.html"

    def get_queryset(self):
        collection_slug = self.kwargs.get("slug", None)
        try:
            collection = Collection.objects.get(en_slug=collection_slug)
            return collection.products.filter(published=True, deleted=False)
        except Collection.DoesNotExist:
            return Http404("Collection does not exist.")


# -----------------------------------------------------------------


@login_required
def comment(request: HttpRequest):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            user = request.user
            product = form.cleaned_data["product"]

            comment, created = Comment.objects.update_or_create(
                user=user, product=product, defaults=form.cleaned_data
            )
            if not created:
                comment.published = False
                comment.save()
            else:
                product.stats.inc_comments()

            return redirect(
                "catalogue:product_detail", product_code=product.prod_code
            )

        else:
            return HttpResponseBadRequest("bad request...")

    return HttpResponseNotAllowed(["POST"])


@login_required
def like(request: HttpRequest, product_id):
    print("liek product...")
    user = request.user
    product = get_object_or_404(Product, pk=product_id, deleted=False)
    fav, created = Favourite.objects.get_or_create(user=user, product=product)

    if not created:
        fav.delete()
        product.stats.dec_likes()  # TODO: use F object
    else:
        product.stats.inc_likes()

    return JsonResponse({"status": "liked" if created else "unliked"})


def product_detail(request: HttpRequest, product_code):
    product = get_object_or_404(Product, prod_code=product_code)
    liked = product.likes.filter(user=request.user).exists()
    can_comment = request.use.orders.filter(
        items__product=product, paid=True
    ).exists()
    comment = None
    try:
        comment = request.user.comments.get(product=product)
    except Comment.DoesNotExist:
        pass

    return render(
        request,
        "shop/product.html",
        {
            "product": product,
            "comment": comment,
            "liked": liked,
            "can_comment": can_comment,
        },
    )


def search(request: HttpRequest):
    keywords = request.GET.get("keywords", None)
    if not keywords:
        return render(request, "search.html", {"page": None})
    # products = Product.objects.filter(name__search=keywords) full text-search...
    # MYSQL has limitted support....

    # needs cache...!
    products = Product.objects.filter(
        Q(name__icontains=keywords)
        | Q(meta_keywords__icontains=keywords)
        | Q(meta_description__icontains=keywords)
    )

    paginator = Paginator(products, 20)
    pg = request.GET.get("page")

    page = None
    try:
        page = paginator.get_page(pg)
    except PageNotAnInteger:
        page = paginator.get_page(1)
    except EmptyPage:
        page = paginator.get_page(paginator.num_pages)

    return render(request, "search.html", {"page": page, "keywords": keywords})


# obsolete in favor of CBV version..........................................
def shop(request: HttpRequest, shop_name):
    shop = get_object_or_404(Shop, name=shop_name, active=True)
    paginator = Paginator(
        shop.products.filter(deleted=False, published=True).all(), 20
    )
    pg = request.GET.get("page")

    page = None
    try:
        page = paginator.get_page(pg)
    except PageNotAnInteger:
        page = paginator.get_page(1)
    except EmptyPage:
        page = paginator.get_page(paginator.num_pages)

    return render(request, "shop/shop.html", {"shop": shop, "page": page})


# ..........................................................................

# WARNING: USE MPTT instead of naive preoder tree traverse!
def category(request: HttpRequest, id):
    category = get_object_or_404(Category, id=id)

    # tree traverse..............
    categories = {category.id}
    stack = [category]
    while len(stack):
        curr = stack.pop()
        if not curr.childs:
            continue
        for c in curr.childs.all():
            categories.add(c.id)
            stack.append(c)
    # ...........................

    products = Product.objects.filter(id__in=list(categories))

    paginator = Paginator(products, 20)
    pg = request.GET.get("page")

    page = None
    try:
        page = paginator.get_page(pg)
    except PageNotAnInteger:
        page = paginator.get_page(1)
    except EmptyPage:
        page = paginator.get_page(paginator.num_pages)

    return render(request, "shop/category.html", {"page": page})


def shop_products(request: HttpRequest):

    if not request.user.shop:
        return Http404()

    paginator = Paginator(request.user.shop.products.filter(deleted=False), 20)
    pg = request.GET.get("page")

    page = None
    try:
        page = paginator.get_page(pg)
    except PageNotAnInteger:
        page = paginator.get_page(1)
    except EmptyPage:
        page = paginator.get_page(paginator.num_pages)

    return render(request, "shop/products.html", {"page": page})


# ------------------------------------------------------------------
def check_shop_name(request: HttpRequest, shop_name):
    """Checks wether the shop with give (shop_name) is already exists or not.

    Args:
        request (HttpRequest): ...
        shop_name (_type_): name of the shop to be checked

    Returns:
        bool: Returns True if shop_name is available and False otherwise.
    """
    exists = Shop.objects.filter(name=shop_name).exists()
    return JsonResponse({"status": "unavailable" if exists else "available"})


# --------------------------------------------------------------------

# ------------------------------------------------------
# CBV version of category view. (REFACTORED)
class CategorProductList(ListView):
    queryset = Product.publisheds
    paginate_by: int = 40
    template_name: str = "shop/category.html"

    def get_queryset(self):
        try:
            category_id = self.kwargs.get("id", None)
            category = Category.objects.get(id=category_id)
            return super().get_queryset().filter(category=category)
        except Category.DoesNotExist:
            return Http404("Category does not exist.")


# ------------------------------------------------------


# -------------------------------------------------------
# CBV versio of shop view. (REFACTORED)
class ShopProductsListView(ListView):
    model = Product
    paginate_by: int = 30
    template_name: str = "shop/shop.html"

    def get_queryset(self):
        shop_name = self.kwargs.get("shop_name", None)
        try:
            shop = Shop.objects.get(shop_name=shop_name)
        except Shop.DoesNotExist:
            return Http404()

        return super().get_queryset().filter(shop=shop)


# --------------------------------------------------------


# ---------------------------------------------------------
# User comments view moved from apps.users.view to here and refactored to CBV
@method_decorator(login_required, name="dispatch")
class UserCommentsListVie(ListView):
    model = Comment
    paginate_by: int = 20
    template_name: str = "user/dashboard/comments.html"

    def get_queryset(self):
        state = self.kwargs.get("state", "published")
        return (
            super().get_queryset().filter(user=self.request.user, state=state)
        )


# --------------------------------------------------------


# ---------------------------------------------------------
# User favourites view has moved from apps.users.views to here and refactored to CBV
@method_decorator(login_required, name="dispatch")
class UserFavoriteListview(ListView):
    model = Favourite
    paginate_by: int = 20
    template_name: str = "user/dashboard/favourites.html"

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


# -----------------------------------------------------------
