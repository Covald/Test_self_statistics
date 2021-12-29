from django.db import models


class Ticket(models.Model):
    data = models.JSONField()


class Item(models.Model):
    name = models.CharField(max_length=256, help_text="Наименование в чеке.")
    paymentType = models.FloatField()
    price = models.IntegerField(help_text="Цена за единицу.")
    quantity = models.IntegerField(help_text="Колличество.")
    sum = models.FloatField(help_text="Сумма.")
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-id",)