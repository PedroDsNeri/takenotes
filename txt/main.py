import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

USERS_ARCHIVE = os.path.join(BASE_DIR, "users.txt")
NOTES_ARCHIVE = os.path.join(BASE_DIR, "notes.txt")

def initialize_archives():
    if not os.path.exists(USERS_ARCHIVE):
        with open(USERS_ARCHIVE, "w", encoding="utf-8") as f:
            pass

    if not os.path.exists(NOTES_ARCHIVE):
        with open(NOTES_ARCHIVE, "w", encoding="utf-8") as f:
            pass

def register():
    print("\n\n--- REGISTER ---")
    username = input("type a username: ")
    password = input("type a password: ")
    confirm_password = input("confirm the password: ")

    if (not username) or (not password):
        print("\nUsername and password cannot be empty!\n\n")
        return

    if password != confirm_password:
        print("\npasswords doesn't match\n\n")
        return

    with open(USERS_ARCHIVE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                saved_user, _ = line.strip().split(":")
                if saved_user == username:
                    print("\nthis username is already registered!\n\n")
                    return
                
    with open(USERS_ARCHIVE, "a", encoding="utf-8") as f:
        f.write(f"{username}:{password}")
    print("\nuser registered successfully!!!\n\n")

def login():
    print("\n\n--- LOGIN ---")
    username = input("Username: ")
    password = input("Password: ")

    with open(USERS_ARCHIVE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                saved_user, saved_password = line.strip().split(":")
                if saved_user == username and saved_password == password:
                    print(f"\n\nWelcome Back, {username}\n\n")
                    menu_notes(username)
                    return
    print("\nIncorrect username or password!\n\n")


def load_user_notes(username):
    user_notes_list = []
    if os.path.exists(NOTES_ARCHIVE):
        with open(NOTES_ARCHIVE, "r", encoding="utf-8") as f:
            for line in f:
                if line.split() and "|" in line:
                    user_note, text_note = line.strip().split("|", 1)
                    if user_note == username:
                        user_notes_list.append(text_note)
    return user_notes_list


def save_deleted_state_to_file(username, current_memory_notes):
    remaining_lines = []
    with open(NOTES_ARCHIVE, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip() and "|" in line:
                    user_note, _ = line.strip().split("|", 1)
                    if user_note != username:
                        remaining_lines.append(line)

    with open(NOTES_ARCHIVE, "w", encoding="utf-8") as f:
            f.writelines(remaining_lines)
            for note in current_memory_notes:
                f.write(f"{username}|{note}\n")



def menu_notes(username):
   
    notes_list = load_user_notes(username)
    
    while True:
        print(f"\n--- NOTES FOR {username.upper()} ---")
        print("1. Create new note")
        print("2. View my notes")
        print("3. Delete a note")
        print("4. Log out to main menu")
        option = input("Choose an option: ").strip()

        if option == "1":
            note = input("What's your note?: ").strip()
            if note:
               
                notes_list.append(note)
                with open(NOTES_ARCHIVE, "a", encoding="utf-8") as f:
                    f.write(f"{username}|{note}\n")
                print("\nNote was saved!\n\n")
        
        elif option == "2":
            print(f"\n\n--- Your notes ---")
            if not notes_list:
                print("\nYou don't have any notes.\n\n")
            else:
                for idx, note in enumerate(notes_list, 1):
                    print(f"{idx}. {note}\n\n")
        
        elif option == "3":
            print(f"\n--- Delete a note ---")
            if not notes_list:
                print("You don't have any notes to delete.")
                continue
                
            for idx, note in enumerate(notes_list, 1):
                print(f"{idx}. {note}")
                
            try:
                choice = int(input("Enter the number of the note to delete: ")) - 1
                # Check validity using list boundaries
                if choice >= 0 and choice < len(notes_list):
                    notes_list.pop(choice)
                    save_deleted_state_to_file(username, notes_list)
                    print("Note deleted successfully!")
                else:
                    print("\nInvalid note number.\n\n")
            except ValueError:
                print("\nPlease enter a valid number.\n\n")
        
        elif option == "4":
            print("\nLogging out...\n\n")
            break
        else:
            print("\nInvalid Option!\n\n")


def main():
    initialize_archives()

    print("--------------------------------------------")
    print("--------------------------------------------")
    print("              TAKE NOTES SYSTEM             ")
    print("--------------------------------------------")
    print("--------------------------------------------")  
    while True:
        print("\n(To use this system you must have an account first)\n")
        print("1. Register User")
        print("2. Log In")
        print("3. Exit Program")
        option = input("Choose an option: ").strip()

        if option == "1":
            register()
        elif option == "2":
            login()
        elif option == "3":
            print("\n\nBye!\n\n")
            break
        else:
            print("\nInvalid option!\n\n")

if __name__ == "__main__":
    main()
        
    


