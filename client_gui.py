import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

def receive_messages(client_socket, text_area):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                text_area.config(state=tk.NORMAL)
                text_area.insert(tk.END, message + "\n")
                text_area.config(state=tk.DISABLED)
                text_area.yview(tk.END)
        except:
            print("Error receiving message from server.")
            client_socket.close()
            break

def send_message(client_socket, message_input, text_area):
    message = message_input.get()
    message_input.delete(0, tk.END)
    if message:
        try:
            client_socket.send(message.encode('utf-8'))
            text_area.config(state=tk.NORMAL)
            text_area.insert(tk.END, "You: " + message + "\n")
            text_area.config(state=tk.DISABLED)
            text_area.yview(tk.END)
        except:
            print("Error sending message.")
            client_socket.close()

def start_client():
    server_ip = "127.0.0.1"  # localhost
    server_port = 5555

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    # Create GUI window
    window = tk.Tk()
    window.title("WhatsApp-like Chat")

    # Create text area for chat messages
    text_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, state=tk.DISABLED, width=50, height=20)
    text_area.grid(column=0, row=0, padx=10, pady=10)

    # Create entry widget for typing messages
    message_input = tk.Entry(window, width=40)
    message_input.grid(column=0, row=1, padx=10, pady=10)

    # Create send button
    send_button = tk.Button(window, text="Send", width=10, command=lambda: send_message(client_socket, message_input, text_area))
    send_button.grid(column=1, row=1)

    # Start thread to receive messages from server
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, text_area))
    receive_thread.start()

    # Start the tkinter main loop
    window.mainloop()

if __name__ == "__main__":
    start_client()
