# Set dinamico di password vietate
pwd_vietate = {"qwerty", "admin", "123456", "password", "abc123"}

# Elenco di password da analizzare 
test_passwords = [
    "Password123!", "qwerty", "SecurePass!2024",
    "admin", "Test1234", "", "aaaaaaa", "     ", "LongPassword123456789!@#"
]

def suggerimenti(password: str, risultati_metodo: dict):
    """
    Fornisce suggerimenti per migliorare la password se risultata debole in uno qualsiasi dei metodi applicati.
    """
    suggerimenti_list = []
    if not risultati_metodo.get("Metodo Base", (True, ""))[0]:
        if len(password) < 8:
            suggerimenti_list.append("allunga la password (minimo 8 caratteri)")
        if not any(c.isupper() for c in password):
            suggerimenti_list.append("includi almeno una lettera maiuscola")
        if not any(c.islower() for c in password):
            suggerimenti_list.append("includi almeno una lettera minuscola")
        if not any(c.isdigit() for c in password):
            suggerimenti_list.append("includi almeno un numero")
        if not any(not c.isalnum() for c in password):
            suggerimenti_list.append("includi almeno un simbolo speciale")
    
    if "Metodo Avanzato" in risultati_metodo and not risultati_metodo["Metodo Avanzato"][0]:
        suggerimenti_list.append("Attenzione! La password provata è presente nella lista di password compromesse")
    if "Metodo Euristico" in risultati_metodo and not risultati_metodo["Metodo Euristico"][0]:
        suggerimenti_list.append("Attenzione! Evita password comuni")
    
    return suggerimenti_list if suggerimenti_list else ["Password robusta."] 