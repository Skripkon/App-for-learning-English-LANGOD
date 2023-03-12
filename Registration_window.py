def get_login_for_registration(new_login : str):
    if len(new_login) < 6:
        print("Your login should has at least 6 symbols")
    else:
        #Открыть окно для создания пароля???? Dodik
        pass

def get_password_for_registration(new_password: str):
    if correct_password(new_password):
        pass
    else:
        pass

def correct_password(password: str):
    if (len(password) >= 8):
        is_correct_len = True
    for elem in password:
        if chr(elem) >= 65 and chr(elem) <= 90:
            is_big_letter = True
        if chr(elem) >= 97 and chr(elem) <= 122:
            is_small_letter = True
        if chr(elem) >= 48 and chr(elem) <= 57:
            is_digit = True
    if (not is_correct_len):
        pass
    if (not is_big_letter):
        pass
    if (not is_digit):
        pass
    if (not is_small_letter):
        pass

def get_login_for_sing_in(user_login : str):
    if sql[user_login] != None:
        pass
    #Вызвать функцию считывания пароля????
    else:
        print("This login doesn't exist")



def get_password_for_sing_in(user_login : str, user_password : str):
    if (sql[user_login] == user_password):
        pass
        #Открыть пользовательское окно????
    else:
        print("Incorrect password")
