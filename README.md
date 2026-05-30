# Personal Assistant Bot

A command-line based personal assistant that helps you manage your contacts and text notes. It features a colorful interface and neatly formatted table outputs!

## Environment Configuration

Before running the application, make sure you have Python 3 installed. 
It is recommended to use a virtual environment.

1. **Navigate to the project directory**:
   ```bash
   cd project-group-8
   ```

2. **Create and activate a virtual environment (optional but recommended)**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   *(This installs `tabulate` for table rendering and `colorama` for the colored console output).*

4. **Run the application**:
   ```bash
   cd assistant
   python3 main.py
   ```

## Available Commands

### General
- `hello`: Prints a greeting message.
- `close` / `exit`: Saves all data and gracefully stops the bot.

### Contacts Management
- `add <name> <phone>`: Adds a new contact or adds a phone number to an existing contact. (Phone must be exactly 10 digits).
- `change <name> <old_phone> <new_phone>`: Updates an existing phone number for a contact.
- `phone <name>`: Shows all phone numbers for a specific contact.
- `add-email <name> <email>`: Adds an email address to a specific contact. The email format is validated.
- `add-address <name> <address>`: Adds a physical address to a contact. Must end with a valid 5-digit US ZIP code.
- `all`: Displays a beautifully formatted table of all saved contacts (including Emails and Addresses).
- `delete <name>`: Deletes a contact from the address book.
- `search <query>`: Searches for contacts by partial name or phone number and displays matching results in a table.

### Birthdays
- `add-birthday <name> <DD.MM.YYYY>`: Adds a date of birth to a specific contact.
- `show-birthday <name>`: Shows the date of birth for the specified contact.
- `birthdays`: Displays a table of all contacts who have birthdays occurring within the next 7 days, including the exact recommended congratulation date.

### Notes Management
- `add-note <text>`: Creates a new text note.
- `change-note <id> <new_text>`: Overwrites the text of an existing note by its numeric ID.
- `delete-note <id>`: Deletes a note by its numeric ID.
- `search-note <query>`: Searches for a specific keyword in all notes and displays the matching ones in a table.
- `notes`: Displays a table with all saved notes and their IDs.

## Examples

### Managing Contacts
```text
Enter a command: add Alice 1234567890
Contact added.

Enter a command: add-email Alice alice@example.com
Email added.

Enter a command: add-address Alice 123 Main St, New York, NY 10001
Address added.

Enter a command: search ali
+--------+------------+------------+-------------------+-----------------------------------+
| Name   | Phones     | Birthday   | Email             | Address                           |
+========+============+============+===================+===================================+
| Alice  | 1234567890 |            | alice@example.com | 123 Main St, New York, NY 10001   |
+--------+------------+------------+-------------------+-----------------------------------+
```

### Managing Notes
```text
Enter a command: add-note Buy milk and bread
Note added.

Enter a command: notes
+----+--------------------+
| ID | Note Text          |
+====+====================+
|  1 | Buy milk and bread |
+----+--------------------+

Enter a command: change-note 1 Buy only milk
Note updated.
```

## Data Persistence
All your contacts and notes are automatically saved into `addressbook.pkl` and `notes.pkl` when you gracefully exit the bot using the `exit` or `close` commands. Next time you launch `main.py`, your data will be safely loaded back!
