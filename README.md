# blog_project

## 模板的规划和设计

包括继承，包含

传递参数给模板是通过

```python
return render(request,'index.html',locals())    locals函数
```

### 分页

用到的函数是

```python
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
```

### 归档的显示

通过自定义manager，在models中,目的获取不重复的年份和月份

```python
#自定义文章Model管理器
#1.新加一个数据处理的方法
class ArticleManager(models.Manager):
    def distinct_date(self):
        distinct_date_list=[]
        date_list=self.values('date_publish')
        for date in date_list:
            date=date['date_publish'].strftime('%Y/%m文章存档')
            if date not in distinct_date_list:
                distinct_date_list.append(date)
        return distinct_date_list
```

在文章模型中添加objects

```python
# 文章模型
class Article(models.Model):
    title = models.CharField(max_length=50, verbose_name='文章标题')
    desc = models.CharField(max_length=50, verbose_name='文章描述')
    content = models.TextField(verbose_name='文章内容')
    click_count = models.IntegerField(default=0, verbose_name='点击次数')
    is_recommend = models.BooleanField(default=False, verbose_name='是否推荐')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    user = models.ForeignKey(User, verbose_name='用户')
    category = models.ForeignKey(Category, blank=True, null=True, verbose_name='分类')
    tag = models.ManyToManyField(Tag, verbose_name='标签')

    objects=ArticleManager()
```

views

```python
def index(request):
    try:
        #分类信息获取（导航数据）
        category_list=Category.objects.all()[:3]
        #广告数据
        ad_list=Ad.objects.all()[0:4]
        #最新文章数据
        article_list=Article.objects.all()
        paginator=Paginator(article_list,10)
        try:
            page=int(request.GET.get('page',1))
            article_list=paginator.page(page)
        except (EmptyPage,InvalidPage,PageNotAnInteger):
            article_list = paginator.page(1)
        #文章归档
        #先获取文章中有的年份-月份
        archive_list= Article.objects.distinct_date()
```

### 给各个归档的标题添加链接，传递参数

```html
<div class="tuwen">
      <h3>文章归档</h3>
      <ul>
          {% for archive in archive_list %}
        <li>
          <p><span class="tutime font-size-18">
              <a href='{% url 'archive' %}?year={{ archive | slice:":4" }}&month={{ archive | slice:"5:7" }}'>
                  {{ archive }}</a></span></p>
        </li>
        {% endfor %}
      </ul>
    </div>
```

