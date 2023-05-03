from django.core.cache import cache
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        postRL = list(Post.objects.filter(author=Author.objects.get(id=self.user_id)).values('rating'))
        L = [postRL[i]['rating'] for i in range(0, len(postRL))]
        rating_post = sum(L) * 3

        commentRL = list(Comment.objects.filter(user=User.objects.get(username=self.user.username)).values('rating'))
        K = [commentRL[i]['rating'] for i in range(0, len(commentRL))]
        rating_comment = sum(K)

        Q = Post.objects.filter(author=Author.objects.get(id=self.user_id)).values('comment')
        Q_1 = [Q[i]['comment'] for i in range(0, len(Q))]
        C = [list(Comment.objects.filter(id=i).values('rating')) for i in Q_1]
        CR = [C[i][0]['rating'] for i in range(0, len(C))]
        rating_comment_post = sum(CR)

        self.rating = rating_post + rating_comment + rating_comment_post
        self.save()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    category = models.CharField(max_length=255, unique=True)
    subscrubers = models.ManyToManyField(User, related_name='category')

    def __str__(self):
        return self.category


class Post(models.Model):
    news = 'Новость'
    POST = 'Статья'
    articl = [(news, 'Новость'), (POST, "Статья")]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    article = models.CharField(max_length=255, choices=articl)
    date_of_creation = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory', blank=False)
    heading = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        text_1 = self.text[0:12:1]
        return text_1 + "..."

    def __str__(self):
        return self.heading

    @staticmethod
    def get_absolute_url():
        return reverse('post_list')

    def name_category(self):
        p = PostCategory.objects.filter(post_id=self.id)
        p_1 = (p[i].category for i in range(0, len(p)))
        p_ci = {}
        for k in p_1:
            p_ci[f'{k.id}'] = k.category
        for c, i in p_ci.items():
            yield c, i

    @staticmethod
    def best_post():
        a = Post.objects.order_by('-rating').values('date_of_creation')[0]
        a_1, a_2 = a['date_of_creation'].time().isoformat(), a['date_of_creation'].strftime("%A %d. %B %Y"),
        b = Post.objects.order_by('-rating')[0].author.user.username
        c = Post.objects.order_by('-rating').values('rating', 'article')[0]
        d = Post.preview(Post.objects.order_by('-rating')[0])
        Value = {'Дата и время добавления': f'{a_1}, {a_2}',
                 'Имя автора': b,
                 'Рейтинг': c['rating'],
                 'Тип': c['article'],
                 'Предварительный просмотр': d}
        for k, v in Value.items():
            print(f"{k} : {v}")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs),
        cache.delete(self.pk)


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date_of_creation = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    @staticmethod
    def comments_best_post():
        a = Comment.objects.filter(post=Post.objects.order_by('-rating')[0])
        for i in a.values():
            print(f"Дата добавления: {i['date_of_creation'].time().isoformat()}",
                  f" {i['date_of_creation'].strftime('%A %d. %B %Y')}")
            print(f"Имя пользователя: {User.objects.get(id=i['user_id']).username}")
            print(f"Рейтинг: {i['rating']}")
            print(i['text'])