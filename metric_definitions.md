
# Metric Definitions (sample)

Revenue = SUM(amount) for orders with status IN ('Delivered', 'Placed')
Order Count = COUNT(DISTINCT order_id)
AOV = Revenue / Order Count

# DQ Rules
- Primary keys must not be null
- No duplicate primary keys
- Date columns must parse to valid dates
- Numeric columns must parse to numeric (no 'abc' values)
- Domain columns must contain only allowed values
- Referential integrity: FK must exist in parent table
