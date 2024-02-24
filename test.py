import unittest
from flask import Flask
from flask_testing import TestCase
from app import app, db, Product

class TestApp(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"  # Sử dụng cơ sở dữ liệu trong bộ nhớ cho kiểm thử
        return app

    # chuẩn bị môi trường kiểm thử
    def setUp(self):
        db.create_all()

    # dọn dẹp môi trường sau khi test xong
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_list_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_create_route(self):
        response = self.client.post('/create', data=dict(
            name='Test Product',
            description='Test Description',
            price=50
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        product = Product.query.filter_by(name='Test Product').first()
        self.assertIsNotNone(product)

    def test_update_route(self):
        # Create a product first
        product = Product(name='Test Product', description='Test Description', price=50)
        db.session.add(product)
        db.session.commit()

        # Update the created product
        response = self.client.post(f'/update/{product.id}', data=dict(
            name='Updated Product',
            description='Updated Description',
            price=75
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check if the product has been updated in the database
        updated_product = Product.query.get(product.id)
        self.assertEqual(updated_product.name, 'Updated Product')
        self.assertEqual(updated_product.description, 'Updated Description')
        self.assertEqual(updated_product.price, 75)

    def test_delete_route(self):
        # Create a product first
        product = Product(name='Test Product', description='Test Description', price=50)
        db.session.add(product)
        db.session.commit()

        # Delete the created product
        response = self.client.post(f'/delete/{product.id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check if the product has been deleted from the database
        deleted_product = Product.query.get(product.id)
        self.assertIsNone(deleted_product)

if __name__ == '__main__':
    unittest.main()
