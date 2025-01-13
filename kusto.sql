traces
| where message contains "GCDS Response"  // Filter for messages with "GCDS Response"
| where message contains "A" or message contains "B"  // Further filter for messages with "A" or "B"
| order by timestamp desc  // Order by timestamp
| summarize 
    MessagesWithA = countif(message contains "A"),
    MessagesWithB = countif(message contains "B")
  by operation_Id  // Group by operation_Id


traces
| where message contains "GCDS Response"  // Filter for messages with "GCDS Response"
| where message contains "A" or message contains "B"  // Further filter for messages with "A" or "B"
| extend MessageType = case(
    message contains "A", "A",
    message contains "B", "B",
    "Other"  // Default case if needed
)
| summarize 
    MessagesWithA = make_list(message, MessageType == "A"),
    MessagesWithB = make_list(message, MessageType == "B")
  by operation_Id


traces
| where message contains "GCDS Response"  // Filter for messages with "GCDS Response"
| where message contains "A" or message contains "B"  // Further filter for messages with "A" or "B"
| order by timestamp desc  // Order by timestamp
| summarize 
    MessagesWithA = make_list_if(message, message contains "A"),  // Group messages containing "A"
    MessagesWithB = make_list_if(message, message contains "B")   // Group messages containing "B"
  by operation_Id  // Group by operation_Id


