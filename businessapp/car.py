from dataapp.models import TBook


# 购物车对象
class Car(object):
    # 属性
    def __init__(self):
        # 1. 商品们(书的id和书的数量)
        self.car_items = []
        # 2. 购物车总价
        self.total_price = 0
        # 3. 购物车的总节省金额
        self.save_price = 0

    # 方法
    # 1. 增
    def add_car(self, book_id, num=1):
        # 向car_items里添加一本书的Car_Item对象
        for i in self.car_items:
            if i.book.id == book_id:
                i.num += num
                self.calculator()
                print(i.book.id, '-------的数量更新为------', i.num)
                return
        book = TBook.objects.get(id=book_id)
        car_item = Car_Item(book, num)
        self.car_items.append(car_item)
        self.calculator()
        return

    # 2. 删
    def del_item(self, book_id):
        for i in self.car_items:
            if i.book.id == book_id:
                self.car_items.remove(i)
        self.calculator()

    # 3. 改
    def change_num(self, book_id, num):
        for i in self.car_items:
            if i.book.id == book_id:
                i.num = num
        self.calculator()

    # 4. 算价格
    def calculator(self):
        self.total_price = 0
        self.save_price = 0
        for i in self.car_items:
            self.total_price += i.book.d_price * i.num
            self.save_price += (i.book.price-i.book.d_price)*i.num

    # 5. 得到购物车中所有图书
    def get_items(self):
        return self.car_items

    # 6. 清空购物车
    def clear_items(self):
        self.car_items = []
        self.calculator()

    # 类方法，如果Car对象存在，则不创建新对象
    @classmethod
    def car(cls):
        pass


# 购物车中的书籍对象
class Car_Item():
    def __init__(self, book, num):
        # book为一个model对象
        self.book = book
        self.num = num


