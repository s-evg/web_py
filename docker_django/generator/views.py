from django.shortcuts import render
from django.http import HttpResponse
import random


def home(request):
    return render(
        request,
        'generator/home.html',
    )


def about(request):
    return render(
        request,
        'generator/about.html',
    )


def password(request):

    length = int(request.GET.get('length', 11))
    amount = int(request.GET.get('amount', 3))

    amount_password = []

    characters = list('abcdefghijklmnopqrstuvwxyz')

    if request.GET.get('uppercase'):
        characters.extend(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))

    if request.GET.get('numbers'):
        characters.extend(list('1234567890'))

    if request.GET.get('special'):
        characters.extend(list('!@#$%^&*()_+|[]{},.?~;:<>'))

    for count in range(amount):
        thepassword = ''
        for x in range(length):
            thepassword += random.choice(characters)
        amount_password.append(thepassword)

    context = {
        'amount_password': amount_password,
    }

    return render(
        request,
        'generator/password.html',
        context
    )
