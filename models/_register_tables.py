from .emails import Email, EmailHistory, UserRecipient

# register your table here
register_tables = {
    "UserRecipient": UserRecipient,
    "Email": Email,
    "EmailHistory": EmailHistory,
}
