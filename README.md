Pointsbot
=======
Pointsbot is a [Matrix](https://matrix.org) bot written using [python-matrix-bot-api](https://github.com/shawnanastasio/python-matrix-bot-api) for the [Giveth](https://giveth.io/) community in order to keep track of points for the [reward dao](https://medium.com/giveth/how-rewarddao-works-aka-what-are-points-7388f70269a)

Requirements
------------
* Python 3
* python-matrix-bot-api (matrix-bot-api on pip)
* gspread
* oauth2client


Usage
-----
Copy `config.ini.example` to `config.ini` and fill in your bot's Matrix credentials.

Then simply invite your bot to a room and use the format `!dish [#of points] [type of points] points to [handle] for [reason explaining why].`
See `!pointshelp` for more information

Pull requests welcome!
