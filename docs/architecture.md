# Product
Products are the most important object in Onmode Architecture. A product object holds generl information about a product including, name, price, SKU, tax, photos, options, quantity, ...

# Option
Options (Attributes) describes specific properties of the product (Ex. size, color variant, ...). Each product may have any number of options.

# Category
Each product must belongs to the exactly one category, categories can be nested. Each category can have many products. Each category has its own webpage available in (onmode.ir/categories/<category_id> | <category_slug>). category_slug is optional but must be unique. The Category page is customizable.

# Collection
Same as category, a **Collection** can have any number of products and they have their own webpage. It is possible to define discount for all product of a collection. **Collection can not be nested**.

# Discount
Discount describes the price off for a product or a collection of products. Each product (or collection) has a field named **Discount** that can be filled with an instance of discount object.

# Coupon:
A coupon may be applied to an order to reduced the total price by **A predefined amount** or **A precent of the total price bound by a predefined amount**.

# Gitf cart
Gift cart object is a predefined amount of balance specifically defined for a user of the onmode.
The user whom gift cart is belongs to can use git cart to load his(her) site's wallet.
