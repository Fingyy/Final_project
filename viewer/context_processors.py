def stock_admin_context(request):
    stock_admin = request.user.groups.filter(name='stock_admin').exists()
    return {
        'stock_admin': stock_admin,
    }