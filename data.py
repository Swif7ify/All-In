import os
import shelve
import pickle
import shutil
from cryptography.fernet import Fernet
class Data:
    def __init__(self, Balance, amountLines, amountBet, protect):
        self.Balance = Balance
        self.amountLines = amountLines
        self.amountBet = amountBet
        self.protect = protect

    def delete_game(self):
        folder = 'gameData'
        shutil.rmtree(folder)

    def generate_key(self):
        folder = 'gameData'
        if not os.path.exists(folder):
            os.makedirs(folder)
        key = Fernet.generate_key()
        with open(os.path.join(folder, 'secret.key'), 'wb') as key_file:
            key_file.write(key)

    def load_key(self):
        folder = 'gameData'
        return open(os.path.join(folder, 'secret.key'), 'rb').read()

    def save_game(self):
        folder = 'gameData'
        if not os.path.exists(folder):
            os.makedirs(folder)
        file_path = os.path.join(folder, 'game_state')
        key_path = os.path.join(folder, 'secret.key')

        if not os.path.exists(key_path):
            self.generate_key()

        # Load the key
        key = self.load_key()
        fernet = Fernet(key)

        # Create a dictionary of the game state
        game_state = {
            'balance': self.Balance,
            'amountLines': self.amountLines,
            'amountBet': self.amountBet,
            'protect': self.protect
        }

        # Serialize and encrypt the game state
        serialized_data = pickle.dumps(game_state)
        encrypted_data = fernet.encrypt(serialized_data)

        # Save the encrypted data
        with shelve.open(file_path, 'c') as db:
            db['game_state'] = encrypted_data

    def load_game(self):
        try:
            folder = 'gameData'
            file_path = os.path.join(folder, 'game_state')

            # Load the key
            key = self.load_key()
            fernet = Fernet(key)

            # Load and decrypt the game state
            with shelve.open(file_path, 'r') as db:
                encrypted_data = db['game_state']
                decrypted_data = fernet.decrypt(encrypted_data)
                game_state = pickle.loads(decrypted_data)

            # Restore the game state
            self.Balance = game_state.get('balance', 0)
            self.amountLines = game_state.get('amountLines', 0)
            self.amountBet = game_state.get('amountBet', 0)
            self.protect = game_state.get('protect', "")
        except FileNotFoundError:
            pass
