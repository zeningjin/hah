from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from dataapp.models import TBook, TBookClass
# Create your views here.


# 主页
def index(request):
    all_class_1 = TBookClass.objects.filter(parent_id=0)
    all_class_2 = TBookClass.objects.filter(parent_id__gt=0)
    all_book = TBook.objects.all()[0:8]
    hot_book = TBook.objects.all().order_by('publishing_time', 'sale_count')[0:8]
    dict1 = {'all_class_1': all_class_1, 'all_class_2': all_class_2, 'all_book': all_book, 'hot_book': hot_book}
    return render(request, 'index.html', dict1)


# 图书详情
def book_detail(request):
    book_id = request.GET.get('book_id')
    if not book_id:
        book_id = 1
    # 获取到这本书
    this_book = TBook.objects.filter(id=book_id)[0]
    # 二级分类id
    two_class_id = this_book.book_class_id
    # 二级分类
    two_class = TBookClass.objects.filter(id=two_class_id)[0]
    # 一级分类
    one_class = TBookClass.objects.filter(id=two_class.parent_id)[0]
    dict1 = {'this_book': this_book, 'one_class': one_class, 'two_class': two_class}
    # two_class = TBookClass.objects.filter(id=this_book.)
    return render(request, 'Book details.html', dict1)


# 书籍列表
def book_list(request):
    # 所有一级分类
    all_class_1 = TBookClass.objects.filter(parent_id=0)
    # 所有二级分类
    all_class_2 = TBookClass.objects.filter(parent_id__gt=0)
    # 获取类型id
    type_id = request.GET.get('type_id')
    if not type_id:
        type_id = 2
    # 具体路径的一级和二级分类
    one_class = None
    two_class = None
    # 如果为真，则是一级分类
    if TBookClass.objects.filter(parent_id=0, id=type_id):
        # 获取一级分类
        one_class = TBookClass.objects.filter(id=type_id)[0]
        # 它下的子分类
        sub_class2 = TBookClass.objects.filter(parent_id=type_id)
        # 所有子类的id
        sub_id_list = [i.id for i in sub_class2]
        # 所有书籍,创建一个空的QuerySet对象
        all_book = TBook.objects.none()
        # 所有子类的QuerySet对象
        for class_id in sub_id_list:
            cur_book = TBook.objects.filter(book_class=class_id)
            # 将查到的数据并入到all_book中
            all_book = all_book | cur_book
    # 如果二级标题为真，则是二级分类
    elif TBookClass.objects.filter(parent_id__gt=0, id=type_id):
        # 获取二级分类
        two_class = TBookClass.objects.filter(id=type_id)[0]
        # 获取对应的一级分类
        one_class = TBookClass.objects.filter(id=two_class.parent_id)[0]
        all_book = TBook.objects.filter(book_class=type_id)
        book_type = 2
    else:
        all_book = TBook.objects.none()
        book_type = None

    page_count = request.GET.get('page_count')
    if not page_count:
        page_count = 1
    page_data = Paginator(all_book, per_page=5)
    per_page = page_data.page(page_count)
    dict1 = {'all_class_1': all_class_1,
             'all_class_2': all_class_2,
             'type_id': type_id,
             'one_class': one_class,
             'two_class': two_class,
             'per_page': per_page}
    return render(request, 'booklist.html', dict1)


# 根据类型排序
def book_sort(request):
    # 排序类型
    sort_class = request.POST.get('sort_class')
    # 书籍分类类型
    book_class = request.POST.get('book_class')
    return JsonResponse()


# 测试iframe框架
def iframe_booklist(request):
    # 获取类型id，默认为2，2中有数据
    type_id = request.GET.get('type_id')
    if not type_id:
        type_id = 2
    # 获取排序类型，默认为0，0是数据库默认规则 1:按销量  2：按价格  3：按出版时间
    sort_type = request.GET.get('sort_type')
    if not sort_type:
        sort_type = '0'
    # 获取排序顺序，0：降序，1：默认，升序
    sort_order = request.GET.get('sort_order')
    if not sort_order:
        sort_type = '1'
    # 具体路径的一级和二级分类
    one_class = None
    two_class = None
    # 如果为真，则是一级分类
    if TBookClass.objects.filter(parent_id=0, id=type_id):
        # 获取一级分类
        one_class = TBookClass.objects.filter(id=type_id)[0]
        # 它下的子分类
        sub_class2 = TBookClass.objects.filter(parent_id=type_id)
        # 所有子类的id
        sub_id_list = [i.id for i in sub_class2]
        # 所有书籍,创建一个空的QuerySet对象
        all_book = TBook.objects.none()
        # 所有子类的QuerySet对象
        for class_id in sub_id_list:
            cur_book = TBook.objects.filter(book_class=class_id)
            # 将查到的数据并入到all_book中
            all_book = all_book | cur_book
    # 如果二级标题为真，则是二级分类
    elif TBookClass.objects.filter(parent_id__gt=0, id=type_id):
        # 获取二级分类
        two_class = TBookClass.objects.filter(id=type_id)[0]
        # 获取对应的一级分类
        one_class = TBookClass.objects.filter(id=two_class.parent_id)[0]
        # 所有的书
        all_book = TBook.objects.filter(book_class=type_id)
    else:
        all_book = TBook.objects.none()
    # 页数，默认为第一页
    page_count = request.GET.get('page_count')
    if not page_count:
        page_count = 1
    # 按规则排序，图书列表不为空
    if all_book:
        # 按销售数量排序
        if sort_type == '1':
            if sort_order == '1':
                all_book = all_book.order_by("sale_count")
            elif sort_order == '0':
                all_book = all_book.order_by("-sale_count")
        # 按当当价排序
        elif sort_type == '2':
            if sort_order == '1':
                all_book = all_book.order_by("d_price")
            elif sort_order == '0':
                all_book = all_book.order_by("-d_price")

        # 按出版社时间排序
        elif sort_type == '3':
            if sort_order == '1':
                all_book = all_book.order_by("publishing_time")
            elif sort_order == '0':
                all_book = all_book.order_by("-publishing_time")

    page_data = Paginator(all_book, per_page=5)
    per_page = page_data.page(page_count)
    dict1 = {'type_id': type_id,
             'sort_type': sort_type,
             'sort_order': sort_order,
             'one_class': one_class,
             'two_class': two_class,
             'per_page': per_page}
    return render(request, 'iframe_booklist.html', dict1)


# booklist_test测试视图
def booklist_test(request):
    # 所有一级分类
    all_class_1 = TBookClass.objects.filter(parent_id=0)
    # 所有二级分类
    all_class_2 = TBookClass.objects.filter(parent_id__gt=0)
    # 获取类型id
    type_id = request.GET.get('type_id')
    if not type_id:
        # 默认为2，因为数据都在2中
        type_id = 2
    # 具体路径的一级和二级分类
    one_class = None
    two_class = None
    # 如果为真，则是一级分类
    if TBookClass.objects.filter(parent_id=0, id=type_id):
        # 获取一级分类
        one_class = TBookClass.objects.filter(id=type_id)[0]
    # 如果二级标题为真，则是二级分类
    elif TBookClass.objects.filter(parent_id__gt=0, id=type_id):
        # 获取二级分类
        two_class = TBookClass.objects.filter(id=type_id)[0]
        # 获取对应的一级分类
        one_class = TBookClass.objects.filter(id=two_class.parent_id)[0]


    dict1 = {'all_class_1': all_class_1,
             'all_class_2': all_class_2,
             'type_id': type_id,
             'one_class': one_class,
             'two_class': two_class,
             }
    return render(request, 'booklist_test.html', dict1)