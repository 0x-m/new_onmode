# Introduction
Onmode is a **multi-vendor E-commerce platform** targeting fashion retailers.
Onmode is a multi-vendor E-commerce platform targeting fashion retailers. Onmode aimed to empower retailers by providing them with basic online shopping capabilities including customer management, sales management, product management, and order management, and especially, undertakes the process of shipping parcels, tracking them, and handling related issues. Furthermore, All User activities related to products, shops, and orders,... may be accessed via REST API endpoints, which facilitates the development of custom apps, robots, and analyzers.

## How Onmode works:

1. Customers may pick any number of products from different shops and add them to their cart, in the cart page, the added products are grouped by the shop and a new order is created per each of these groups.

2. Customer may pick an order up (let it belongs to the ABC shop!), check it out, and after completing some forms, and paying the order off (directly or via the wallet), the ABC shopkeeper receives an SMS containing information about the new order also, the shopkeeper can see the new registered order in the site's dashboard. The shopkeeper may confirm or cancel the order, Also the corresponding customer can cancel the order before the shopkeeper confirms it.

3. After the order confirmation, a new form below the order is appeared (for the shopkeeper) that asks for the Order tracking code, the shopkeeper must prepare and send the order to the customer, then fill the tracking code form.

4. After that the shopkeeper registered the tracking code, The Admin user must check the code and verify its validity. If the admin verifies the code then the order goes to the Sent state and the user can see the I have received the order button! pressing this button means the process is successfully terminated. If the code was invalid, the admin can leave a message for the shopkeeper and reject the code, in this case, the shopkeeper will be asked again to provide a valid tracking code.


## SMS Notification
SMS notification is another onmode feature, the user will be touched after making an order or their orders got accepted (Rejected|canceled|prepared or sent) by the corresponding shopkeeper. Also, shopkeepers receive SMS when new orders arrived at their shops, users cancel their orders, or after users

## Extensibility
**Onmode** extensible architecture provides for the definition of fully customizable products with custom-defined options and attributes, in which each attribute has a Type and Default value(s), and each product may have any number of options. (Currently, only the admin can define custom product options). In addition, products may be categorized or gathered into collections. (Currently, only the admin can define category and collection)
