import os  # cho phép truy cập vào các đường dẫn trên hệ thống

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

from flask_sqlalchemy import SQLAlchemy

import uuid

project_dir = os.path.dirname(os.path.abspath(__file__))  # tìm ra vị trí đường dẫn của dự án
database_file = "sqlite:///{}".format(os.path.join(project_dir, "product_database_1.db"))  # thiết lập một tệp csdl

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file  # cho biết ứng  dụng web biết nới cơ sở dũ liệu được lưu trữ

db = SQLAlchemy(app)  # khởi tạo kết nối tới csdl

# chạy python shell để tạo db và table
# import sqlite3
# connection_obj = sqlite3.connect('product_database_1.db')
# cursor_obj = connection_obj.cursor()
# table = """ CREATE TABLE product (
#             id INTEGER NOT NULL PRIMARY KEY,
#             name NVARCHAR(80) NOT NULL,
#             description NVARCHAR(255),
#             price INT NOT NULL
#         ); """
#
# cursor_obj.execute(table)
# connection_obj.close()

class Product(db.Model):  # tạo một lớp mới kế thừa từ mô hình csdl cơ bản do SQLAlchemy cung cấp
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(255))
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Product(name='{}', description='{}', price='{}')>".format(self.title, self.description,
                                                                                  self.price, self.price)

@app.route("/", methods=["GET"])
def get_list():
    # print(uuid.uuid4())
    products = Product.query.all()
    return render_template("list.html", products=products)


@app.route("/create", methods=["GET", "POST"])
def create():
    if request.form:
        try:
            print(request.form.get("title"))
            name = request.form["name"]
            description = request.form["description"]
            price = request.form["price"]

            product = Product(name=name, description=description, price=price)
            db.session.add(product)  # thêm sản phẩm vào csdl
            db.session.commit()  # cam kết các thay đổi ??
        except Exception as e:
            print(f"Error: {str(e)}")
        return redirect("/")

    return render_template("create.html")


@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    product = Product.query.get(id)
    if request.form:
        try:
            print(request.form.get("title"))
            name = request.form["name"]
            description = request.form["description"]
            price = request.form["price"]

            product.name = name
            product.description = description
            product.price = price
            db.session.commit()  # cam kết các thay đổi ??
        except Exception as e:
            print(f"Error: {str(e)}")
        return redirect("/")

    return render_template("update.html", product=product)


@app.route("/delete/<int:id>", methods=["GET", "POST"])
def delete(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return redirect("/")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
