Step 0:
Revenue(5x12) is not tidy because it breaks rule 1 and 2. Quarter is spread across 12 headers and the revenue values is split among those headers. Each row also hold 12 observations which breaks rule 2. Shipments(35x2) is tidy because every row represents a single shipment. Orders(20x5) is tidy because each variable is represented as a column, each order is a row, and every cell has one value
Step 1: 
The raw revenue file is wide. It violates rules 1 and 2. Quarter is spread across 12 headers and the revenue values is split among those headers. Each row also hold 12 observations which breaks rule 2. To fix this I used melt to move the quarter headers into column. The values are going into revenue. 
Step 2: 
order_id is unique in orders.csv, but not in shipments.csv. The join is one to many from orders to shipments because there are 15 duplicates in shipments. 
Step 3:
The orders only mean is the correct mean. The join repeats each orders amount per shipment. This means that orders with more shipments are counted more times and drag the average. On the other hand, each order counts once. 
Step 4:
The final table has column company,quarter,revenue,n_orders,order_amount_total, and n_shipments. I used company at the quarter level becuse revenue is only there. A table with one row per observation needs every colum at each level. I summarized orders before merging because they are more compact. If i merged before, it would repeat. I only took the amounts from orders because it would repeat if i did. I counted all the shipments seperate because of the repeating amounts. I saved it as a csv so someone else could pickup and start analyzing immediately. 
Step 5:
The raw chart could only show all the revenue numbers lumped together, since the quarters were spread over 12 columns. It couldn’t tell me which company or quarter a number came from. After tidying, quarter and company are their own columns, so one lineplot with hue="company" shows revenue over time for all five companies.
