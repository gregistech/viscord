# Viscord
**WARNING: USING 3RD-PARTY DISCORD CLIENTS IS A BANNABLE OFFENSE BY THE TOS, AND I CAN'T GUARANTEE THAT YOUR ACCOUNT WILL NOT BE BANNED IF YOU USE THIS!**

## FAQ

### What is the goal of this project?
To create an ncurses based Discord client with vim-like keybindings in Python.

### What is the progress?
In short words, not usable.

### When will we get a usable release?
I hope soon.

### How can I get my token?

1. Open the default discord client.
2. Press Ctrl+Shift+i
3. Go to the networking tab.
4. Type in the search bar: "/api"
5. Click on one of the options that you got.
6. Search for a property called authorization.
7. Profit!

## Development

### Setting your token

See [the FAQ section](#how-can-i-get-my-token) to get your token.
```bash
export VISCORD_TOKEN="token"
```
You can run the above snippet in your shell to set your token temporarily.
You can also create a file like `set_token.sh` to save your token. You will need to run `source set_token.sh` so it will apply to your current shell.
Be sure not to commit your token.

### Using a virtual environment

To create a virtual environment and install dependencies:
```bash
$ python3 -m venv ./virtenv # create the virtual env
$ source ./virtenv/bin/activate # use the right variant for your shell {,.fish,.csh}
$ pip3 install -r requirements.txt # install dependencies
```
to deactivate the virtual environment use the `deactivate` function like so:
```bash
$ deactivate
```
You can always use `$ source ./virtenv/bin/activate` to activate your virtual environment.
