Todos:
- make it so there is a record of which threads/messages are already being responded to and ignore subsequent requests
- per channel configuration table
    - model
    - whether it listens to all messages
- add slash commands
    - comms mode for channel: mute/mention/respond
- handle timeouts nicer
- metrics table
    - record per org per day
        - mentions
        - channels active
        - proactive responses
        - positive/negative reactions
- QA table
    - when a response gets a negative reaction, write the request/response/reaction into table

- is it possible to make 


Things needed if this was to be used by multiple orgs
- Tables need to be dynamically created? Use table groups to group all tables for an org (https://stackoverflow.com/questions/58657217/how-can-i-create-this-dynamodb-table-group-with-cloudformation)
- Some way of differentiating an install 
