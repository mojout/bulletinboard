# Final Django project at the 'Skillfactory' course.
### Terms of reference for the project:
>We need to develop an Internet resource for a fan server of a well-known MMORPG - something like a bulletin board. Users of our resource should be able to register in it by e-mail, having received a letter with a registration confirmation code. After registration, they can create and edit ads.Ads consist of a title and text that can include images, embedded videos, and other content. Users can submit responses to other users' ads in plain text. When sending a response, the user should receive an e-mail with a notification about it. The user should also have access to a private page with responses to his ads, inside which he can filter responses by ads, delete them and accept (when a response is accepted, the user who left the response should also receive a notification).In addition, the user must necessarily define an ad in one of the following categories: Tanks, Heals, DDs, Merchants, Guildmasters, Questgivers, Blacksmiths, Leatherworkers, Potions Masters, Spellmasters.

>We would also like to be able to send newsletters to users.

>Thank you in advance!

### For test use of the project, use these hints when setting up:

    pip install -r requirements.txt
    docker pull rabbitmq
    docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management

### The above technical task is implemented by the following functionality:
:arrow_forward: The user can access the placement of ads only after registration, which must be confirmed by the code sent by e-mail.
By registering, he can post ads and respond to active ads of other users.
The main page of the site with ads looks like this:

![Screenshot](https://github.com/mojout/bulletinboard/blob/master/media/images/2023/07/02/mainpage.jpg)

