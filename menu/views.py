from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from .models import *
from .forms import *


def menu_list(request):
    '''View that shows a list of all menus filtered by expiration date'''
    all_menus = Menu.objects.all().prefetch_related('items')
    menus = all_menus.order_by('expiration_date')
    return render(request, 'menu/list_all_current_menus.html', {'menus': menus})


def menu_detail(request, pk):
    '''View that shows a menu's details'''
    storage = messages.get_messages(request)
    menu = get_object_or_404(Menu, pk=pk)
    return render(request, 'menu/menu_detail.html', {'menu': menu, 'message': storage})


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
            form.save_m2m()
            messages.success(request, 'New menu has been saved')
            return redirect('menu_detail', pk=menu.pk)
    else:
        form = MenuForm()
    return render(request, 'menu/menu_edit.html', {'form': form})


def edit_menu(request, pk):
    '''A view to edit an existing form'''
    menu = get_object_or_404(Menu, pk=pk)
    form = MenuForm(instance=menu)
    if request.method == "POST":
        form = MenuForm(request.POST, instance=menu)

        '''Checking if the form is valid'''
        if form.is_valid():
            menu = form.save(commit=False)
            menu.created_date = timezone.now()
            menu.save()
            form.save_m2m()
            messages.success(request, 'The form has been updated')
            return redirect('menu_detail', pk=menu.pk) 
    return render(request, 'menu/menu_edit.html', {'form': form})
