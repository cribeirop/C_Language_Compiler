import re
#valida email
# kevin-lee@fakesub..mail.com incorrecly accepted

pattern = r'[A-Za-z0-9-_]+([.]\w+)*[@][A-Za-z0-9-]+([.]\w+)+'

