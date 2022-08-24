# Discord BOT for Jenshin Impact Mabar

### Brief
This BOT are build using python 3.9, and run using worker at Heroku, if you are developers and like to run this bot locally you can run it using `python3 main.py`. For dependency it just use `pandas numpy discord.py` and for installing all the dependency you can run `pip3 install -r requirements.txt`.

### Usage
For you who want to fork this bot or run it for your own, you need:
1. Github account
2. Heroku account (Optional, but better if you have it)
3. Discord account
4. Discord Developer mode activated

After you already create all the necessary account, you need to create bot in discord developer dashboard, and get the bot API Code (I don't post my API, and discord can detect if I post my API code to public). For running the bot you have 2 method:

1. **Bare metal**
&nbsp;&nbsp; - First thing first, you need install all dependency tools `python3.9 pip3 discord`, after tools already downloaded you need to install all neccessary library to order bot can run properly use `pip3 install -r requirements.txt`
&nbsp;&nbsp; - After that you need make a `.env` file in your discord bot folder, in there you need to declare:
&nbsp;&nbsp;&nbsp;`DISCORD_TOKEN=[DISCORD_BOT_TOKEN_YOU_GET_WHEN_CREATING_BOT]`
&nbsp;&nbsp; - Finally you just run your python script from command line (CMD), terminal or powershell as long as your CLI can call `python3` globally

## To-Do
- [x] Generate redeem link.
- [ ] Generate redeem link using UID in #UID channel text.
- [ ] Pull release patch note.
- [ ] Pull account stats using Hoyoverse public API.
- [ ] Pull battle Chronicle using Hoyoverse public API -> JPEG or PNG.
- [x] Hosted bot on PaaS (Heroku).