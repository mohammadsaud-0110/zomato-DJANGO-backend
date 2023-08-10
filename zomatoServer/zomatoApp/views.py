from django.shortcuts import render,redirect
import json
from django.http import Http404


def menu_list(request):
    with open('menu.json') as menu_file:
        menu_data = json.load(menu_file)
    
    return render(request, 'menu_list.html', {'menu_data': menu_data})


def add_dish(request):
    if request.method == "POST":
        dishId = request.POST['dishId']
        dishName = request.POST['dishName']
        dishPrice = request.POST['dishPrice']
        dishAvailability = request.POST['dishAvailability']

        dishAvailability = dishAvailability.lower()

        if dishAvailability in ["y", "yes"]:
            dishAvailability = "yes"
        else:
            dishAvailability = "no"

        newDish = {
            'dishId':dishId,
            'dishName': dishName,
            'dishPrice':float(dishPrice),
            'dishAvailability':dishAvailability
        }

        with open('menu.json') as menu_file:
         menu_data = json.load(menu_file)

        menu_data.append(newDish)
        with open('menu.json', 'w') as menu_file:
         json.dump(menu_data, menu_file, indent=4)

        return redirect('menu_list')

    return render(request, 'add.html')


def remove_dish(request, dishId):
    with open('menu.json') as menu_file:
        menu_data = json.load(menu_file)
    
    # Find the dish with the specified dishId
    removed_dish = None
    for dish in menu_data:
        if dish['dishId'] == dishId:
            removed_dish = dish
            break
    
    # If dish not found, raise Http404
    if removed_dish is None:
        raise Http404("Dish not found")
    
    updated_menu_data = [dish for dish in menu_data if dish['dishId'] != dishId]
    
    with open('menu.json', 'w') as menu_file:
        json.dump(updated_menu_data, menu_file, indent=4)
    
    return render(request, 'removed.html', {'dishId': dishId})

def update_dish(request, dishId):
    with open('menu.json') as menu_file:
        menu_data = json.load(menu_file)
    
    # Find the dish with the specified dishId
    removed_dish = None
    for dish in menu_data:
        if dish['dishId'] == dishId:
            removed_dish = dish
            break
    
    # If dish not found, raise Http404
    if removed_dish is None:
        raise Http404("Dish not found")
    
    for dish in menu_data:
        if dish['dishId'] == dishId:
            if dish['dishAvailability'] == "yes":
                dish['dishAvailability'] = "no"
            else:
                dish['dishAvailability'] = "yes"
    
    
    with open('menu.json', 'w') as menu_file:
        json.dump(menu_data, menu_file, indent=4)
    
    return render(request, 'dishupdate.html', {'dishId': dishId})


def order_list(request):
    with open('order.json') as order_file:
        order_data = json.load(order_file)
    
    return render(request, 'order_list.html', {'order_data': order_data})

def take_order(request):
    if request.method == 'POST':
        CustomerName = request.POST['CustomerName']
        dishId = request.POST.getlist('dishId')
        
        # Check if dishes are available
        with open('menu.json') as menu_file:
            menu_data = json.load(menu_file)
        
        unavailable_dishes = [dish for dish in menu_data if dish['dishId'] in dishId and dish['dishAvailability'] == 'no']
        
        if unavailable_dishes:
            return render(request, 'order_unavailable.html', {'unavailable_dishes': unavailable_dishes})
        
        # Process the order
        with open('order.json') as order_file:
            order_data = json.load(order_file)
  
        item1 = None
        for item in menu_data:
         if item["dishId"] in dishId:
           item1 = item
           break
     
        order_id = str(len(order_data) + 1)
        new_order = {
            'OrderId': order_id,
            'CustomerName': CustomerName,
            'dishName': item1['dishName'],
            'Price':item1["dishPrice"],
            'Status': 'Preparing'
        }
        order_data.append(new_order)
        
        with open('order.json', 'w') as order_file:
            json.dump(order_data, order_file, indent=4)

    return render(request, 'take_order.html')

def update_order_status(request, OrderId):
    if request.method == 'POST':
        new_status = request.POST.get('status')
        
        with open('order.json') as order_file:
            order_data = json.load(order_file)
        
        order_found = False
        for order in order_data:
            if order['OrderId'] == OrderId:
                order['Status'] = new_status
                order_found = True
                break
        
        if not order_found:
            return render(request, 'order_not_found.html', {'OrderId': OrderId})
        
        with open('order.json', 'w') as order_file:
            json.dump(order_data, order_file, indent=4)
    
        return redirect('order_list')
    return render(request, 'updateStatus.html')


def filter(request, status):
    with open('order.json') as order_file:
        order_data = json.load(order_file)

    updated_order_data = [order for order in order_data if order['Status'] == status]

    return render(request, "filter_data.html", {'updated_order_data': updated_order_data})