from django.test import TestCase

class AddOrderItemTest(TestCase):
    
    @classmethod
    def setUpClass(cls) -> None:
        return super().setUpClass()
    
    def test__add_order_item(self):
        self.client.post('/cart/add', {
            'product': 1,
            'collection' :1
        })
    