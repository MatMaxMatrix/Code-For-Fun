from common import test_passwords, pwd_vietate, suggerimenti
from basic_check import analizza_password_base
from advanced_check import analizza_password_avanzata
from heuristic_check import analizza_password_euristica

def main():
    """
    Funzione principale che testa i tre metodi di verifica password.
    """
    try:
        print("Sistema di verifica password")
        print("=" * 50)
        print("1. Metodo Base")
        print("2. Metodo Avanzato")
        print("3. Metodo Euristico")
        print("=" * 50)
        
        livello_input = int(input("Seleziona il livello di sicurezza (1, 2 o 3): "))
        if livello_input not in [1, 2, 3]:
            print("Livello di sicurezza non valido!")
            return
        
        # Chiedi all'utente se vuole usare le password di test o inserire una propria password
        use_test = input("Vuoi usare le password di test? (s/n): ").lower() == 's'
        
        if use_test:
            passwords = test_passwords
        else:
            password = input("Inserisci la password da verificare: ")
            passwords = [password]
        
        for password in passwords:
            print("\n" + "=" * 50)
            print(f"Analisi per {repr(password)}:")
            
            if livello_input == 1:
                risultato = analizza_password_base(password)
            elif livello_input == 2:
                risultato = analizza_password_avanzata(password)
            else:  # livello_input == 3
                risultato = analizza_password_euristica(password)
            
            for metodo, (esito, messaggio) in risultato.items():
                print(f"  {metodo}: {'Sicura' if esito else 'Debole'} - {messaggio}")
            
            print("\nSuggerimenti:")
            for suggerimento in suggerimenti(password, risultato):
                print(f"  - {suggerimento}")
            
            print("=" * 50)
    
    except ValueError:
        print("Input non valido. Per favore, inserisci un numero intero.")

if __name__ == "__main__":
    main() 