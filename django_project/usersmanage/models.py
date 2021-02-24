from django.db import models


class TimeBasedModels(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class User(TimeBasedModels):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    id = models.AutoField(primary_key=True)
    user_id = models.BigIntegerField(unique=True, default=1, verbose_name="ID пользователя Telegram")
    name = models.CharField(max_length=100, verbose_name="Имя пользователя")
    username = models.CharField(max_length=100, verbose_name="Username Telegram")
    email = models.CharField(max_length=100, verbose_name='Email', null=True, blank=True)

    def __str__(self):
        return f"№{self.id} {self.user_id} - {self.name}"


class Photo(TimeBasedModels):
    class Meta:
        verbose_name = "Фотография"
        verbose_name_plural = "Фотографии"

    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Название", max_length=50)
    file_id = models.CharField(verbose_name="Фото file_id", max_length=200)

    def __str__(self):
        return f"№{self.id} - {self.name}"


class Item(TimeBasedModels):
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Название Товара", max_length=50)
    photo = models.ForeignKey(Photo, verbose_name="Фото", on_delete=models.CASCADE, null=True)
    price = models.DecimalField(verbose_name="Цена", decimal_places=2, max_digits=8)
    description = models.TextField(verbose_name="Описание", max_length=3000, null=True)
    file = models.FileField(verbose_name="Файл (название должно быть на английском)", upload_to="documents")

    def __str__(self):
        return f"№{self.id} - {self.name}"


class Purchase(TimeBasedModels):
    class Meta:
        verbose_name = "Покупка"
        verbose_name_plural = "Покупки"

    id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(User, verbose_name="Покупатель", on_delete=models.SET(0))
    item_id = models.ForeignKey(Item, verbose_name="Идентификатор товара", on_delete=models.CASCADE)
    amount = models.DecimalField(verbose_name="Стоимость", decimal_places=2, max_digits=8)
    purchase_time = models.DateTimeField(verbose_name="Время Покупки", auto_now_add=True)
    email = models.CharField(verbose_name="Email", max_length=100, null=True)
    receiver = models.CharField(verbose_name="Имя Получателя", max_length=100, null=True)

    def __str__(self):
        return f"№{self.id} - {self.item_id}"



