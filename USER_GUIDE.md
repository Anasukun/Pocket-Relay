# How to Set Up PocketRelay

Welcome! Follow these simple steps to get PocketRelay running on your phone.

1. **Create your Telegram Bot**
   1. Open the Telegram app on your phone.
   2. Search for the user "@BotFather".
   3. Send a message saying "/newbot".
   4. BotFather will ask you to choose a name for your bot.
   5. Choose a username that ends in "bot" (for example, "myhelper123_bot").
   6. BotFather will give you a long password called an API Token. Copy that token.

2. **Install PocketRelay**
   
   **Option A: 🚀 Quick Tool Install (No repo download required)**
   Run this single command in your terminal to install `pocketrelay` globally:
   ```bash
   uv tool install git+https://github.com/Anasukun/Pocket-Relay.git
   ```
   *(Or using `pipx`: `pipx install git+https://github.com/Anasukun/Pocket-Relay.git`)*

   Once installed, run the setup wizard from any terminal:
   ```bash
   pocketrelay init
   ```
   *Follow the on-screen instructions to paste your Telegram API Token and receive your 6-digit pairing code.*

   ---

   **Option B: 🛠️ Manual Clone & Setup (Developers)**
   1. Open terminal and navigate into the cloned `PocketRelay` folder:
      ```bash
      cd PocketRelay
      ```
   2. Sync dependencies:
      ```bash
      uv sync
      ```
   3. Launch setup wizard:
      ```bash
      uv run pocketrelay init
      ```

3. **Pair your Phone**
   1. Go back to the Telegram app on your phone.
   2. Search for the bot username you created in step 1 and open a chat with it.
   3. Send a message starting with "/pair" followed by a space and your 6-digit code (For example: `/pair 123456`).
   4. Your phone is now securely connected to your computer!

4. **Start PocketRelay**
   1. In your computer's terminal, type:
      ```bash
      pocketrelay run
      ```
      *(Or `uv run pocketrelay run` if you built from source)*
   2. That's it! You can now send messages to your bot on Telegram, and it will help you with your project.

### Safety Features
We want to make sure your files are safe. Here is what PocketRelay does automatically:
1. It works on a separate copy of your files first. It will never change your original work unless you tap "Approve" on your phone.
2. It hides passwords and secret keys so they are never sent to your phone.
3. It stays inside your project folder and cannot peek at other personal files on your computer.

### Things you can say to your Bot on Telegram
- Send **/start** to see if the bot is awake.
- Send **/projects** to see what you are working on.
- Send **/doctor** to check if everything is running correctly.
