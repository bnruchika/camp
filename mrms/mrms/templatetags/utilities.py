from datetime import date
from django import template

register = template.Library()


@register.filter(name='split')
def split(value, key):
    """
        Returns the value turned into a list.
    """
    return value.split(key)


@register.filter(name="age_calculator")
def age_calculator(born):
    """ given a date will calculate the age and return the age

    """
    print(born)
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
