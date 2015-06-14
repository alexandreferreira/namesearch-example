from core.models import Entry

__author__ = 'alexandreferreira'
import requests
import random

def get_names(amount=1000):
    """
    Get many names
    :param amount: Number os names, default is 1000
    :type amount: int
    :return: A list of names
    :rtype: list of unicode
    """
    params = {'country': 'brazil', 'amount': amount}
    req = requests.get("http://api.uinames.com/", params=params)
    if req.status_code == requests.codes.ok:
        info = req.json()
        return ["%s %s" % (name.get('name'), name.get("surname")) for name in info]
    else:
        return []

def get_random_number():
    while True:
        number = random.randint(0, 2147483647)
        if not Entry.objects.filter(number=number).exists():
            return number


def import_random_names():
    names = get_names()
    [Entry.objects.create(get_random_number(), names[i]) for i in xrange(len(names))]
    return len(names)
