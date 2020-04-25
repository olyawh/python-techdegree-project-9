from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from .models import *
from .forms import *


def menu_list(request):
    '''View that shows a list of all menus filtered by expiration date'''
    all_menus = Menu.objects.all().prefetch_related('items')
    menus = all_menus.order_by('expiration_date')
    print(menus)
   # for menu in all_menus:
    #    if menu.expiration_date >= timezone.now():
     #       menus.append(menu)

    #menus = sorted(menus, key=attrgetter('expiration_date'))
    return render(request, 'menu/list_all_current_menus.html', {'menus': menus})


def menu_detail(request, pk):
    '''View that shows a menu's details'''
    menu = get_object_or_404(Menu, pk=pk)
    return render(request, 'menu/menu_detail.html', {'menu': menu})


def item_detail(request, pk):
    '''View that displays a menu's item details'''
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'menu/detail_item.html', {'item': item})


def create_new_menu(request):
    '''A view to create and save new menu'''
    if request.method == "POST":
        form = MenuForm(request.POST)

        '''Checking if the form is valid'''
        if form.is_valid():
            menu = form.save(commit=False)
            menu.created_date = timezone.now()
            menu.save()
            menu.save_m2m()
            return redirect('menu_detail', pk=menu.pk)
    else:
        form = MenuForm()
    return render(request, 'menu/menu_edit.html', {'form': form})


def edit_menu(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    items = Item.objects.all()
    if request.method == "POST":
        menu.season = request.POST.get('season', '')
        menu.expiration_date = datetime.strptime(request.POST.get('expiration_date', ''), '%m/%d/%Y')
        menu.items = request.POST.get('items', '')
        menu.save()

    return render(request, 'menu/change_menu.html', {
        'menu': menu,
        'items': items,
        })