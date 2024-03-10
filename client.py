import xmlrpc.client

server_url = "http://localhost:6666/"
proxy = xmlrpc.client.ServerProxy(server_url)

def add_note_ui():
    topic = input("Enter topic: ")
    text = input("Enter note text: ")
    timestamp = input("Enter timestamp (YYYY-MM-DDTHH:MM:SS): ")
    if proxy.add_note(topic, text, timestamp):
        print("Note added successfully.")
    else:
        print("Error adding note.")

def get_notes_ui():
    topic = input("Enter topic to retrieve notes: ")
    notes = proxy.get_notes(topic)
    if notes:
        for note in notes:
            print(f"Timestamp: {note['timestamp']}, Text: {note['text']}")
    else:
        print("No notes found for this topic.")

def query_wikipedia_ui():
    topic = input("Enter topic to search on Wikipedia and update: ")
    result = proxy.query_wikipedia_and_update(topic)
    if result:
        print(f"Wikipedia link for '{topic}': {result}")
    else:
        print("Failed to find or add Wikipedia link to the topic.")

def main():
    while True:
        print("\n1. Add Note\n2. Get Notes\n3. Query Wikipedia and Update Topic\n4. Exit")
        choice = input("Choose an option:\n")
        if choice == "1":
            add_note_ui()
        elif choice == "2":
            get_notes_ui()
        elif choice == "3":
            query_wikipedia_ui()
        elif choice == "4":
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
