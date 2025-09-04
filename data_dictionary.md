
# Data Dictionary - sample tables

## customers
customer_id: primary key, string
name: string
signup_date: ISO date YYYY-MM-DD

## orders
order_id: primary key, string
customer_id: FK -> customers.customer_id
order_date: ISO date YYYY-MM-DD (parsed by pandas)
amount: numeric, expected >= 0
status: enum [Placed, Delivered, Cancelled]
