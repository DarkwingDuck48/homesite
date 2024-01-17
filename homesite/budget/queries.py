""" Запросы которые часто используем во время работы приложения """
from datetime import date, datetime
from unicodedata import category

from django.shortcuts import get_object_or_404
from django.db.models import Sum, F, Value

from .models import Category, Operation, Period


# Периоды
def get_period(period_date: None | date = None) -> Period:
    if not period_date:
        period_date = datetime.now()
    period = get_object_or_404(
        Period, start_date__lte=period_date, end_date__gte=period_date
    )
    return period

def get_period_by_name(period_name:str) -> Period:
    period = get_object_or_404(Period, name=period_name)
    return period

def get_period_by_short_name(period_short_name:str) -> Period:
    period = get_object_or_404(Period, short_name=period_short_name)
    return period

def get_period_by_year_month(year: int, month:int) -> Period:
    period = get_object_or_404(Period, year=year, month=month)
    return period

# Операции

def get_operations_by_period_and_category_sum(period: Period):
    """Получаем операции, просуммированные по категориям и по нужному периоду"""
    operations_credit = (
        get_operations_by_period(period).filter(category__cat_type="Cr")
        .values("category", "category__name", "category__limit", "category__id")
        .annotate(
            rest_by_category=F("category__limit") - Sum("amount"),
            spend_by_category=Sum("amount"),
        )
    )
    operations_debit = (
         get_operations_by_period(period).filter(category__cat_type="Dr")
         .values("category","category__name", "category__limit", "category__id")
         .annotate(
             get_by_category=Sum("amount")
         )
    )
    return operations_credit, operations_debit


def get_operations_by_period(period: Period|None = None):
    if not period:
        period = get_period()
    operations = Operation.objects.all().filter(operation_period=period)
    return operations

# Категории

def get_credit_categories():
    return Category.objects.all().filter(cat_type="Cr")
    

def get_debit_categories():
    return Category.objects.all().filter(cat_type="Dr")