from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required(login_url='employee_signin')
def employee_meallist(request):
    meals_list = MealPlans.objects.all().order_by('-id')

    paginator=Paginator(meals_list, 10)
    page_number=request.GET.get('page')
    try:
        meal=paginator.page(page_number)
    except PageNotAnInteger:
        meal=paginator.page(1)
    except EmptyPage:
        meal=paginator.page(paginator.num_pages)

    has_meal= paginator.count > 0
    return render(request,'EmpSales/EmpMeal_Plans/employee_Meal_List.html',{'meal':meal, 'has_meal':has_meal})


@login_required(login_url='employee_signin')
def employee_mealadd(request):
    if request.method == 'POST':
        meals = request.POST.get('meals')

        if MealPlans.objects.filter(meals=meals).exists():
            messages.error(request,'An Meal already exists')
            return render(request,'EmpSales/EmpMeal_Plans/employee_Meal_Add.html')

        MealPlans.objects.create(
            meals=meals,

        )
        messages.success(request,'Meals added successfully')
        return redirect('employee_meallist')
    return render(request,'EmpSales/EmpMeal_Plans/employee_Meal_Add.html')


@login_required(login_url='employee_signin')
def employee_mealedit(request,id):
    meal = get_object_or_404(MealPlans, id=id)

    if request.method == 'POST':
        meals = request.POST.get('meals')

        if MealPlans.objects.filter(meals=meal.meals).exclude(id=meal.id).exists():
            messages.error(request,'An Meal already exists')
            return render(request,'EmpSales/EmpMeal_Plans/employee_Meal_Edit.html',{'meal':meal})

        meal.meals = meals
        meal.save()
        messages.success(request,'Meals edited successfully')

        return redirect('employee_meallist')

    return render(request,'EmpSales/EmpMeal_Plans/employee_Meal_Edit.html', {'meal': meal})



@login_required(login_url='employee_signin')
def employee_mealdelete(request, meal_id):
    meal = get_object_or_404(MealPlans, id=meal_id)
    meal.delete()
    return redirect('employee_meallist')