def regole_base(password: str):
    """
    Metodo Base: controlla se la password ha più di 8 caratteri e varietà di caratteri 
    (almeno una lettera maiuscola, una minuscola, un numero e un simbolo).
    """
    if len(password) < 8:
        return False, "Password troppo corta (minimo 8 caratteri)."
    
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(not c.isalnum() for c in password)
    
    if not (has_lower and has_upper and has_digit and has_symbol):
        return False, "La password deve contenere almeno una lettera minuscola, una maiuscola, un numero e un simbolo."
    
    return True, "Password conforme alle regole di base."

def verifica_avanzata(password: str, pwd_vietate: set):
    """
    Metodo Avanzato: esegue i controlli di base e verifica se la password è presente nella lista di credenziali vietate.
    """
    base_check, base_reason = regole_base(password)
    if not base_check:
        return False, base_reason
    if password.lower() in pwd_vietate:
        return False, "Password presente nella lista di credenziali compromesse."
    return True, "Password conforme alle regole avanzate."

def suggerimenti_avanzati(password: str, esito: bool, messaggio: str, in_lista_vietate: bool):
    """
    Fornisce suggerimenti per migliorare la password se risultata debole.
    """
    if esito:
        return ["Password robusta."]
    
    suggerimenti_list = []
    if len(password) < 8:
        suggerimenti_list.append("Allunga la password (minimo 8 caratteri)")
    if not any(c.isupper() for c in password):
        suggerimenti_list.append("Includi almeno una lettera maiuscola")
    if not any(c.islower() for c in password):
        suggerimenti_list.append("Includi almeno una lettera minuscola")
    if not any(c.isdigit() for c in password):
        suggerimenti_list.append("Includi almeno un numero")
    if not any(not c.isalnum() for c in password):
        suggerimenti_list.append("Includi almeno un simbolo speciale")
    
    if in_lista_vietate:
        suggerimenti_list.append("Attenzione! La password provata è presente nella lista di password compromesse")
    
    return suggerimenti_list

def analizza_password_avanzata(password: str):
    """
    Analizza la password applicando il metodo avanzato.
    Restituisce l'esito, il messaggio e i suggerimenti.
    """
    # Set dinamico di password vietate
    pwd_vietate = {"qwerty", "admin", "123456", "password", "abc123"}
    
    # Gestione dei casi limite: password vuote, solo spazi o troppo lunghe
    if not password.strip():
        esito = False
        messaggio = "Password vuota o composta solo da spazi."
        in_lista_vietate = False
    elif len(password) > 100:  # Gestione di password troppo lunghe
        esito = False
        messaggio = "Password troppo lunga. Considera di accorciarla."
        in_lista_vietate = False
    else:
        # Metodo Avanzato
        esito, messaggio = verifica_avanzata(password, pwd_vietate)
        in_lista_vietate = password.lower() in pwd_vietate
    
    # Genera suggerimenti
    suggerimenti = suggerimenti_avanzati(password, esito, messaggio, in_lista_vietate)
    
    return esito, messaggio, suggerimenti

if __name__ == "__main__":
    # Elenco di password da analizzare 
    test_passwords = [
        "Password123!", "qwerty", "SecurePass!2024",
        "admin", "Test1234", "", "aaaaaaa", "     ", "LongPassword123456789!@#"
    ]
    
    print("Test del metodo avanzato di verifica password:")
    print("-" * 50)
    
    for password in test_passwords:
        esito, messaggio, suggerimenti = analizza_password_avanzata(password)
        print(f"Password: {repr(password)}")
        print(f"Esito: {'Sicura' if esito else 'Debole'}")
        print(f"Messaggio: {messaggio}")
        print(f"Suggerimenti:")
        for suggerimento in suggerimenti:
            print(f"  - {suggerimento}")
        print("-" * 50)
    
    # Interazione con l'utente
    print("\nVerifica la tua password:")
    password_input = input("Inserisci una password: ")
    esito, messaggio, suggerimenti = analizza_password_avanzata(password_input)
    print(f"Esito: {'Sicura' if esito else 'Debole'}")
    print(f"Messaggio: {messaggio}")
    print(f"Suggerimenti:")
    for suggerimento in suggerimenti:
        print(f"  - {suggerimento}") 