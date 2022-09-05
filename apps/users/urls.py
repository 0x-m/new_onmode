from django.urls import path

from apps.catalogue import views as catalog

from . import views

app_name = "users"
urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("verify/", views.verify_code, name="verify"),
    path("signout/", views.signout, name="signout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/profile/", views.profile, name="profile"),
    path("dashboard/addresses", views.addresses, name="addresses"),
    path("dashboard/comments", views.comments, name="comments"),
    path("dashboard/favourites", views.favourites, name="favourites"),
    path("dashboard/messages", views.messages, name="messages"),
    path(
        "dashboard/messages/delete/<message_id>",
        views.delete_message,
        name="delete-message",
    ),
    path(
        "dashboard/messages/read/<message_id>",
        views.read_message,
        name="read-message",
    ),
    path("dashboard/orders", views.orders, name="orders"),
    path("dashboard/wallet", views.wallet, name="wallet"),
    path(
        "dashboard/wallet/deposit/verify/<amount>",
        views.wallet_deposit_verify,
        name="deposit-verify",
    ),
    path("dashboard/wallet/deposit", views.wallet_deposit, name="deposit"),
    path(
        "dashboard/wallet/checkout",
        views.wallet_checkout,
        name="wallet_checkout",
    ),
    path(
        "dashboard/shop/create-shop",
        catalog.create_shop_request,
        name="create-shop",
    ),
    path("dashboard/shop/edit", catalog.edit_shop, name="edit-shop"),
    path("dashboard/shop/products", catalog.shop_products, name="products"),
    path("dashboard/shop/product", catalog.product, name="add-product"),
    path(
        "dashboard/shop/product/edit/<pid>",
        catalog.product,
        name="edit-product",
    ),
    path(
        "dashboard/shop/product/options/add/<pid>",
        catalog.add_option,
        name="add-option",
    ),
    path(
        "dashboard/shop/product/options/delete/<pid>",
        catalog.add_option,
        name="delete-option",
    ),
    path(
        "dashboard/shop/product/delete/<pid>",
        catalog.delete_product,
        name="delete-product",
    ),
    path(
        "dashboard/shop/product/photo/add/<pid>",
        catalog.add_photo,
        name="add-photo",
    ),
    path(
        "dashboard/shop/product/photo/delete/<pid>",
        catalog.delete_photo,
        name="delete-photo",
    ),
    path(
        "dashboard/shop/product/photo/preview/<pid>",
        catalog.change_preview_photo,
        name="make-as-preview",
    ),
    path("check_email/", views.check_email, name="check_email"),
    path(
        "dashboard/messages/create/", views.create_ticket, name="create-ticket"
    ),
    path("dashboard/messages/all/", views.tickets, name="all-tickets"),
    path(
        "dashboard/messages/message/reply/<ticket_id>/",
        views.reply_ticket,
        name="reply-ticket",
    ),
    path(
        "dashboard/messages/message/<ticket_id>/", views.ticket, name="ticket"
    ),
]
