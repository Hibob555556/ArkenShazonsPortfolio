import hashlib
import os

RED = '\033[31m'
GREEN = '\033[32m'
RESET = '\033[0m'

class FileNotSpecified(Exception):
    pass

class Hasher:
    def __init__(self):
        self.file_path = ""
        self.expected = ""

    def get_sha1(self):
        """Description: Calculate and return the SHA-1 hash.
        Args:
            - None

        Returns:
            - String: the SHA-1 hash of the specified file

        Raises: 
            - Exceptions: 
                - FileNotFoundError | Raises FileNotFound error when file path is invalid.
                - FileNotSpecified | Raises custom FileNotSpecified error when the function is called before a file is specified.

        """
        if not self.file_path:
            raise FileNotSpecified("No file path specified.")
        sha1 = hashlib.sha1()
        with open(self.file_path, "rb") as file:
            for bytes_blk in iter(lambda: file.read(4069), b""):
                sha1.update(bytes_blk)
        return sha1.hexdigest()


    def get_sha256(self):
        """Description: Calculate and return the SHA-256 hash.
        Args:
            - None

        Returns:
            - String: the SHA-256 hash of the specified file

        Raises: 
            - Exceptions: 
                - FileNotFoundError | Raises FileNotFound error when file path is invalid.
                - FileNotSpecified | Raises custom FileNotSpecified error when the function is called before a file is specified.

        """
        if not self.file_path:
            raise FileNotSpecified("No file path specified.")
        sha256 = hashlib.sha256()
        with open(self.file_path, "rb") as file:
            for bytes_blk in iter(lambda: file.read(4069), b""):
                sha256.update(bytes_blk)
        return sha256.hexdigest()
    
    def get_sha512(self):
        """Description: Calculate and return the SHA-512 hash.
        Args:
            - None

        Returns:
            - String: the SHA-512 hash of the specified file

        Raises: 
            - Exceptions: 
                - FileNotFoundError | Raises FileNotFound error when file path is invalid.
                - FileNotSpecified | Raises custom FileNotSpecified error when the function is called before a file is specified.

        """
        if not self.file_path:
            raise FileNotSpecified("No file path specified.")
        sha512 = hashlib.sha512()
        with open(self.file_path, "rb") as file:
            for bytes_blk in iter(lambda: file.read(4096), b""):
                sha512.update(bytes_blk)
        return sha512.hexdigest()
    

    def get_md5(self):
        """Description: Calculate and return MD5 hash.
        Args:
            - None

        Returns:
            - String: the MD5 hash of the specified file

        Raises: 
            - Exceptions: 
                - FileNotFoundError | Raises FileNotFound error when file path is invalid.
                - FileNotSpecified | Raises custom FileNotSpecified error when the function is called before a file is specified.

        """
        if not self.file_path:
            raise FileNotSpecified("No file path specified.")
        md5 = hashlib.md5()
        with open(self.file_path, "rb") as file:
            for bytes_blk in iter(lambda: file.read(4096), b""):
                md5.update(bytes_blk)
        return md5.hexdigest()


# clear the console to make it look pretty
def clear_console():
    if os.name == 'nt':  # name for windows
        _ = os.system('cls')
    else:  # if not windows it is usually mac or linux and clear should work
        _ = os.system('clear')


def print_header():
    logo = '''
            ___    _  _     ___     ___    _                        _                     
    o O O  / __|  | || |   /   \   / __|  | |_      ___     __     | |__    ___      _ _  
   o       \__ \  | __ |   | - |  | (__   | ' \    / -_)   / _|    | / /   / -_)    | '_| 
  TS__[O]  |___/  |_||_|   |_|_|   \___|  |_||_|   \___|   \__|_   |_\_\   \___|   _|_|_  
 {======|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""| 
./o--000'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-' 
'''
    spacer = '''|===========================================================================================|
|                                                                                           |
|===========================================================================================|
'''
    print(logo)
    print(spacer)


def print_main_menu(warn = False, custom_message = ""):
    clear_console()
    print_header()
    print("1) Sha")
    print("2) MD")
    try:
        if warn:
            if custom_message != "":
                print(f"{custom_message}. Please enter a valid choice...")
            else:
                print("Please enter a valid choice...")
            choice = int(input ("What algorithm would you like to use (1, 2)? ").strip().lower())
        else:
            choice = int(input ("What algorithm would you like to use (1, 2)? ").strip().lower())

    except TypeError:
        return print_main_menu(True, "Please enter a number")

    except Exception:
        return print_main_menu(True)
    
    if choice < 3 and choice > 0:
        return choice
    else:
        return print_main_menu(True, "Please select 1 or 2")
    

def print_sha_menu(warn = False, custom_message = ""):
    clear_console()
    print_header()
    print("1) SHA-1")
    print("2) SHA-256")
    print("3) SHA-512")
    try:
        if warn:
            if custom_message != "":
                print(f"{custom_message}. Please enter a valid choice...")
            else:
                print("Please enter a valid choice...")
            choice = int(input ("What algorithm would you like to use (1, 2, 3)? ").strip().lower())
        else:
            choice = int(input ("What algorithm would you like to use (1, 2, 3)? ").strip().lower())

    except TypeError:
        return print_main_menu(True, "Please enter a number")

    except Exception:
        return print_main_menu(True)
    
    if choice < 4 and choice > 0:
        return choice
    else:
        return print_main_menu(True, "Please select a number from 1 to 3")

# main prog loop
def main():
    running = True
    while running: 
        menu_id = print_main_menu()
        use_md5 = False
        use_sha = False
        method = -1

        match menu_id:
            case 1:
                method = print_sha_menu()
                use_sha = True
            case 2:
                use_md5 = True


        if use_sha:
            # SHA
            request = Hasher()
            request.file_path = input("Please input the full file path for the file you would like to get the hash of: ").strip('"')
            request.expected = input("Please input the hash you are expecting: ").strip('"').lower()

            hash = ""
            if method == 1:
                hash = request.get_sha1()
            elif method == 2:
                hash = request.get_sha256()
            else:
                hash = request.get_sha512()

            print(f"Provided hashes. Expected: {request.expected}. Calculated: {hash}.")
            if (request.expected == hash):
                print(f"{GREEN}The provided hash matches the calculated hash.{RESET}")
            else:
                print(f"{RED}The provided hash does NOT match the expected hash.{RESET}")
        
        if use_md5:
            # AES
            request = Hasher()
            request.file_path = input("Please input the full file path for the file you would like to get the hash of: ").strip('"')
            request.expected = input("Please input the hash you are expecting: ").strip('"').lower()

            hash = request.get_md5()

            print(f"Provided hashes. Expected: {request.expected}. Calculated: {hash}.")
            if (request.expected == hash):
                print(f"{GREEN}The provided hash matches the calculated hash.{RESET}")
            else:
                print(f"{RED}The provided hash does NOT match the expected hash.{RESET}")

        running = input("Would you like to check another file (yes, no)? ").strip().lower()
        if running != "yes":
            running = False


if __name__ == "__main__":
    main()
