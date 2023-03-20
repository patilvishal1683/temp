import win32com.client


outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
# inbox = outlook.GetDefaultFolder(6)
inbox_folder = outlook.GetDefaultFolder(6)
inbox = inbox_folder.Folders
AWS = inbox['AWS']
messages = AWS.Items
for message in messages:
    emaiL_data = {'subject': message.Subject, 'body': message.Subject}
    print(emaiL_data)


#



