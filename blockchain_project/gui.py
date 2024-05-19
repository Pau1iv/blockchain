import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests
import json

class BlockchainGUI:
    """Class representing the graphical user interface for interacting with the blockchain."""

    def __init__(self, root):
        """
        Initializes the GUI.

        :param root: The root Tkinter window.
        """
        self.root = root
        self.root.title("Blockchain GUI")

        self.create_widgets()

    def create_widgets(self):
        """Creates and configures the widgets for the GUI."""

        self.chain_frame = ttk.LabelFrame(self.root, text="Blockchain Info")
        self.chain_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.chain_text = tk.Text(self.chain_frame, height=15, width=50)
        self.chain_text.grid(row=0, column=0, padx=5, pady=5)
        self.refresh_chain_button = ttk.Button(self.chain_frame, text="Refresh Chain", command=self.get_chain)
        self.refresh_chain_button.grid(row=1, column=0, padx=5, pady= 5)


        self.tx_frame = ttk.LabelFrame(self.root, text="New Transaction")
        self.tx_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.data_label = ttk.Label(self.tx_frame, text="Data:")
        self.data_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.data_entry = ttk.Entry(self.tx_frame)
        self.data_entry.grid(row=0, column=1, padx=5, pady=5)

        self.sender_label = ttk.Label(self.tx_frame, text="Sender:")
        self.sender_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.sender_entry = ttk.Entry(self.tx_frame)
        self.sender_entry.grid(row=1, column=1, padx=5, pady=5)

        self.receiver_label = ttk.Label(self.tx_frame, text="Receiver:")
        self.receiver_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.receiver_entry = ttk.Entry(self.tx_frame)
        self.receiver_entry.grid(row=2, column=1, padx=5, pady=5)

        self.number_label = ttk.Label(self.tx_frame, text="Balance for Receiver:")
        self.number_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.number_entry = ttk.Entry(self.tx_frame)
        self.number_entry.grid(row=3, column=1, padx=5, pady=5)

        self.submit_tx_button = ttk.Button(self.tx_frame, text="Submit Transaction", command=self.submit_transaction)
        self.submit_tx_button.grid(row=4, column=0, columnspan=2, pady=5)


        self.mine_button = ttk.Button(self.root, text="Mine Block", command=self.mine_block)
        self.mine_button.grid(row=2, column=0, padx=10, pady=10)


        self.wallet_frame = ttk.LabelFrame(self.root, text="Wallet Balance")
        self.wallet_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        self.address_label = ttk.Label(self.wallet_frame, text="Address:")
        self.address_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.address_entry = ttk.Entry(self.wallet_frame)
        self.address_entry.grid(row=0, column=1, padx=5, pady=5)

        self.check_balance_button = ttk.Button(self.wallet_frame, text="Check Balance", command=self.check_balance)
        self.check_balance_button.grid(row=1, column=0, columnspan=2, pady=5)

        self.balance_label = ttk.Label(self.wallet_frame, text="Balance: 0")
        self.balance_label.grid(row=2, column=0, columnspan=2, pady=5)

    def get_chain(self):
        """Retrieves and displays the current blockchain."""
        response = requests.get('http://127.0.0.1:5000/chain')
        if response.status_code == 200:
            chain_data = response.json()["chain"]
            self.chain_text.delete(1.0, tk.END)
            self.chain_text.insert(tk.END, json.dumps(chain_data, indent=4))
        else:
            messagebox.showerror("Error", "Unable to fetch chain data.")

    def submit_transaction(self):
        """Submits a new transaction to the blockchain."""
        data = self.data_entry.get()
        sender = self.sender_entry.get()
        receiver = self.receiver_entry.get()
        balance = self.number_entry.get()

        if not data or not sender or not receiver or not balance:
            messagebox.showerror("Error", "All fields are required.")
            return

        tx_data = {
            "data": data,
            "sender": sender,
            "receiver": receiver,
            "balance": balance
        }

        response = requests.post('http://127.0.0.1:5000/transactions/new', json=tx_data)
        if response.status_code == 201:
            messagebox.showinfo("Success", "Transaction submitted successfully.")
        else:
            messagebox.showerror("Error", "Failed to submit transaction.")

    def mine_block(self):
        """Triggers the mining of a new block in the blockchain."""
        response = requests.get('http://127.0.0.1:5000/mine')
        if response.status_code == 200:
            messagebox.showinfo("Success", response.json()["message"])
        else:
            messagebox.showerror("Error", "No transactions to mine.")

    def check_balance(self):
        """Checks the balance of a given wallet address."""
        address = self.address_entry.get()
        if not address:
            messagebox.showerror("Error", "Address is required.")
            return

        response = requests.get(f'http://127.0.0.1:5000/wallet/{address}')
        if response.status_code == 200:
            balance = response.json()["balance"]
            self.balance_label.config(text=f"Balance: {balance}")
        else:
            messagebox.showerror("Error", "Failed to fetch wallet balance.")

if __name__ == "__main__":
    root = tk.Tk()
    app = BlockchainGUI(root)
    root.mainloop()

