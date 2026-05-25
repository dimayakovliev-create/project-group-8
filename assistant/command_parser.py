#    Розбирає введений рядок на команду та аргументи. Повертає команду в нижньому регістрі та список аргументів.
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    
    return cmd, *args