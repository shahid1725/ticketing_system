from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages

from django.contrib.auth.decorators import login_required


@login_required(login_url='admin_loginview')
def accountdetails(request):
    account_list = BankAccount.objects.all().order_by('-id')

    paginator=Paginator(account_list, 10)
    page_number= request.GET.get('page')
    try:
        account = paginator.page(page_number)
    except PageNotAnInteger:
        account =paginator.page(1)
    except EmptyPage:
        account = paginator.page(paginator.num_pages)

    has_account = paginator.count > 0
    
    return render(request,'Sales/Account_Details/Account_Details_list.html',{'account':account, 'has_account': has_account})


@login_required(login_url='admin_loginview')
def accountdetailsadd(request):
    if request.method == 'POST':
        account_name = request.POST.get('account_name')
        account_number = request.POST.get('account_number')
        ifsc_code = request.POST.get('ifsc_code')

        if BankAccount.objects.filter(account_number=account_number).exists():
            messages.error(request,'An account with this account number already exists')
            return render(request,'Sales/Account_Details/Account_Details_Add.html')

        BankAccount.objects.create(
            account_name=account_name,
            account_number=account_number,
            ifsc_code=ifsc_code



        )
        messages.success(request,'Account details added successfully')
        return redirect('accountdetails')
    return render(request,'Sales/Account_Details/Account_Details_Add.html')

@login_required(login_url='admin_loginview')
def accountdetailsedit(request,id):
    account = get_object_or_404(BankAccount, id=id)
    if request.method == 'POST':
        account_name = request.POST.get('account_name')
        account_number = request.POST.get('account_number')
        ifsc_code = request.POST.get('ifsc_code')

        if BankAccount.objects.filter(account_number=account.account_number).exclude(id=account.id).exists():
            messages.error(request,'An account with this account number already exists')
            return render(request,'Sales/Account_Details/Account_Details_Edit.html',{'account':account})
        
        account.account_name = account_name
        account.account_number = account_number
        account.ifsc_code = ifsc_code
        account.save()
        messages.success(request,'Account details updated successfully')
        return redirect('accountdetails')
    
    return render(request,'Sales/Account_Details/Account_Details_Edit.html', {'account':account})


@login_required(login_url='admin_loginview')
def accountdetailsdelete(request, account_id):
    account = get_object_or_404(BankAccount, id=account_id)
    account.delete()
    messages.success(request,'Account deleted successfully')
    return redirect('accountdetails')