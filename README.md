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
   - On **macOS/Linux**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - On **Windows (Command Prompt)**:
     ```cmd
     python -m venv venv
     venv\Scripts\activate.bat
     ```
   - On **Windows (PowerShell)**:
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```

3. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   *(This installs `tabulate` for table rendering, `colorama` for the colored console output, and `prompt_toolkit` for smart auto-completion).*

4. **Run the application**:
   - On **macOS/Linux**:
     ```bash
     cd assistant
     python3 main.py
     ```
   - On **Windows**:
     ```cmd
     cd assistant
     python main.py
     ```

## 🌟 Smart Auto-Completion

The application features an interactive and smart command-line prompt powered by `prompt_toolkit`:
- **Command Auto-Completion**: Press `Tab` at any time to see a list of available commands or to auto-complete the command you are typing.
- **Dynamic Name Suggestions**: For commands that require a contact's name (e.g., `change`, `phone`, `add-birthday`, `delete`), pressing `Tab` will instantly suggest names that are currently saved in your address book!

## 📚 Available Commands

### General
- `hello`: Prints a greeting message.
- `help`: Shows a formatted table with all available commands and their descriptions.
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

## 🎭 Demo Scenario

To quickly test the capabilities of the application during a presentation or review, you can populate the bot with pre-configured demo data.

### 0. Generate Demo Data
Run the standalone data generator script. This will cleanly overwrite your current `addressbook.pkl` and `notes.pkl` with a set of test contacts and notes:
```bash
cd assistant
python demo_data.py
```
Now, launch the bot (`python main.py`) and try out the following flow:

### 1. View Initial Data
Start by viewing the pre-loaded data:
```text
Enter a command: all
Enter a command: notes
```
*Notice how John has a complete profile, while other contacts have missing fields.*

### 2. Birthdays
You can check a specific person's birthday, or see who has upcoming birthdays within the next 7 days. `John` is hardcoded to have a birthday soon:
```text
Enter a command: show-birthday John
Enter a command: birthdays
```

### 3. Adding & Updating Contacts
Let's add a brand new contact with multiple phone numbers, and then change one of them:
```text
Enter a command: add Mike 1111111111
Enter a command: add Mike 2222222222
Enter a command: change Mike 1111111111 3333333333
Enter a command: phone Mike
```

### 4. Add Email & Addresses
Let's add an email address to Mike, and then give him a physical address. If you make a mistake, just call the command again to overwrite the old one!
```text
Enter a command: add-email Mike mike.personal@gmail.com
Enter a command: add-address Mike 123 Old St, NY 10001
Enter a command: add-address Mike 456 New Ave, NY 10002
Enter a command: search mike
```

### 5. Deleting Contacts
The demo data includes a contact named `Dummy`. Let's get rid of them:
```text
Enter a command: delete Dummy
Enter a command: all
```

### 6. Working with Notes
You can also manage text notes with full search capability. Let's add a new note, update it, and search for it:
```text
Enter a command: add-note Buy tickets to the cinema
Enter a command: change-note 4 Buy tickets to the theatre
Enter a command: search-note theatre
Enter a command: delete-note 4
```

### 7. Smart Auto-Completion
Start typing a command that requires a contact name and press `Tab` to see the suggestions based on the demo data!
```text
Enter a command: change <Press Tab>
```

## 💾 Data Persistence
All your contacts and notes are automatically saved into `addressbook.pkl` and `notes.pkl` when you gracefully exit the bot using the `exit` or `close` commands. Next time you launch `main.py`, your data will be safely loaded back!
