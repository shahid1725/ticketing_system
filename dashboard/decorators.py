from django.shortcuts import redirect

def admin_permission_required(fun):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_superuser:
            return redirect("adminlogin")
        else:
            return fun(request,*args,**kwargs)
    return wrapper