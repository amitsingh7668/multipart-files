traces
| where message contains "GCDS Response"  // Filter for messages with "GCDS Response"
| where message contains "A" or message contains "B"  // Further filter for messages with "A" or "B"
| order by timestamp desc  // Order by timestamp
| summarize 
    MessagesWithA = countif(message contains "A"),
    MessagesWithB = countif(message contains "B")
  by operation_Id  // Group by operation_Id
