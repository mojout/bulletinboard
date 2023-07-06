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
By registering, he can post ads and respond to active ads of other users. At the time of creating an ad, all registered users receive an email notification that a new ad in a particular category has appeared on the site, the frequency of sending depends on the settings of the asynchronous job queue. Also on the main page it is possible to sort ads into categories.
The main page of the site with ads looks like this:

![Screenshot](https://github.com/mojout/bulletinboard/blob/master/media/images/2023/07/02/mainpage.jpg)

:arrow_forward: On the page of detailed information about the announcement, editing and sending a response to the author of the announcement is available:

![Screenshot](https://github.com/mojout/bulletinboard/blob/master/media/images/2023/07/detail.jpg)

:arrow_forward: At the moment when the user submits a response, the author of this announcement receives an e-mail notification with information about this.
The author can go to a private page with all responses to their ads and either accept the response or reject it.

![Screenshot](https://github.com/mojout/bulletinboard/blob/master/media/images/2023/07/02/reply_list.jpg)

:arrow_forward: All user actions on the site are accompanied by a messaging framework built into Django. 
After the author of the ad has accepted the response, an email notification is sent to the user who left this response.

![Screenshot](https://github.com/mojout/bulletinboard/blob/master/media/images/2023/07/02/replymessages.jpg)

:arrow_forward: At the end of this functionality, the ad to which the response was accepted has its display below the ad. If the author decides that he needs to disable the display of some responses, he can click on the "Dismiss" button on his private page and they will disappear.

![Screenshot](https://github.com/mojout/bulletinboard/blob/master/media/images/2023/07/02/comments.jpg)





