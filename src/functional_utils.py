def filter_sales_by_category(sales, category):
    return [sale for sale in sales if sale.category == category]


def filter_sales_by_date(sales, date):
    return [sale for sale in sales if sale.date == date]