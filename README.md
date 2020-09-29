# mc-serverbot

A Discord bot that acts as a front end, allowing discord server members to interact with an AWS EC2 instance that is hosting a minecraft servers.

The contents of the "bot" folder should be used to create a seperate repo and hosted on Heroku.

The contents of the "aws" folder contain the backend lambda and the ec2 userData contents

<b>commands</b>

<i>!start</i>      ....... starts the ec2 instance <br>
<i>!stop</i>       ........ stops the ec2 instance<br>
<i>!ip</i>         ............. returns the ip address<br>
<i>!ping</i>       ........ returns the bots ping<br>
<i>!state</i>      ....... returns the ec2 instance state<br>
