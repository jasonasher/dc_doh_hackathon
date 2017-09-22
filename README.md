# DC Government Health and Human Services Hackathon
![a](https://user-images.githubusercontent.com/23619819/30629730-7a274c62-9dab-11e7-860b-921895f6e839.PNG)

National Day of Civic Hacking, September 23rd, 2017

This repository is for hackathon projects supporting the DC Department of Health.

***
## Project descriptions
***
### Rat Riddance
Orkin Pest Control recently named Washington DC the third "rattiest" city in America, and long-time DC residents know that rodent populations have been on the rise. Mayor Bowser announced a "Rat Riddance" initiative last year, which aims to reduce rodent populations through changes in commercial practice and community awareness campaigns. In support of these efforts, the DC Office of the Chief Technology Officer (OCTO) has been analyzing 311 service request data related to rodent abatement requests and developing models to predict upticks in rat-related complaints in space and time.

The goals for our project are 2-fold:
  1. Develop models that can predict long-term trends in rodent complaints. These models will be complementary to ongoing OCTO efforts.
  2. Build out features on a public-facing 311 data portal that allows users to examine trends in service complaints over time and in their neighborhoods. This data portal will encompass all nuisance-related service complains, not just those related to rodents.
***
### Food Safety/Restaurant Inspections
Food establishments that sell or serve food to the public must apply for a health permit and be inspected for compliance with the DC Department of Health. These establishments include restaurants, school cafeterias, bakeries, mobile food vendors, and markets. The majority of the permitted food service establishments in Washington, DC receive two routine unannounced food safety inspections per year. DOH follows the federal food code and only closes an establishment for critical violations that cannot be corrected while an inspector is onsite (for several hours) and poses immediate harm to residents and visitors to the District. The purpose of a food safety inspection is to ensure the food is being handled properly from preparation through serving. DOH seeks understanding as to whether or not there are common factors of establishments that can guide future training efforts for business owners and staff or that may help the department allocate staff resources in a more efficient and effective manner. Note that the number of times annually that a food retail location is inspected is based on its risk category.Any problems observed are recorded on the inspection report and the manager is taught the correct procedure or method immediately

The goals for our project
  1. Data analysis/visualizations of the DOH restaurant inspection data report
  2. Develop a model featuring relationships between location, risk category, serious food-safety violations, closure etc.
  3. Develop an application for DOH staff that tracks upcoming  inspections, displays information on expiring licenses, and aids in the efficient prioritization of follow-up inspections.


***
## Join the projects

1. Add your name to our [sign up sheet](https://docs.google.com/spreadsheets/d/1dp82BlwxMHGIiNPjfspWBkp_K1SZox0PXug8J8aOssU/edit?usp=sharing) in the "Sign up sheet" tab
2. Find an available task under Github Issues, assign yourself or your group to the task, and get hacking!

We are recruiting individuals for the following types of tasks:

* **Data cleaning:** Help us convert raw data frames into clean feature datasets that are ready to integrate into models!
* **Data visualization:** Look at the available datasets (See the "Dataset summary" tab in our [sign up sheet](https://docs.google.com/spreadsheets/d/1dp82BlwxMHGIiNPjfspWBkp_K1SZox0PXug8J8aOssU/edit?usp=sharing), chat with DC DOH agency representatives about maps and visualizations of interest, and create the visualizations!
* **User interface/experience (UI/UX):**
  1. Build out features for our existing 311 data portal in R Shiny (http://dc311portal.codefordc.org/)
  2. Design and start to develop a web application for the public to view DOH inspection reports for food retail establishments  
  3. Design and start to develop an application for DOH staff that tracks upcoming inspections, displays information on expiring licenses, and aids in the efficient prioritization of follow-up inspections.
* **Project management:** Interested in helping us manage the project? Chat with one of the project leads!

***
## Contribute your code

Start by forking this repository to your Github account (click "Fork" in the top right).
Then clone the forked version of the repository to your computer using the URL listed under "Clone or Download".
```
$ git clone <url-of-your-fork>
```
We use a triangular workflow - you should push to your Github account's fork, but fetch/pull from this master repository. Setting this up requires adding a remote to this repository account. "Git clone" will have created your repository in a new folder called "dc_doh_hackathon". Use these commands to add the remote to that new folder:
```
$ cd dc_doh_hackathon
$ git remote add dohhackathon https://github.com/jasonasher/dc_doh_hackathon.git
$ git remote -v
  #you should see this:
  dohhackathon       https://github.com/jasonasher/dc_doh_hackathon.git (fetch)
  dohhackathon       https://github.com/jasonasher/dc_doh_hackathon.git (push)
  origin          <your/forked/url> (push)
  origin          <your/forked/url> (fetch)
```
Now instead of plain `git push` and `git pull`, use these:

```
$ git push origin <branch-name>         #pushes to your forked repo
$ git pull dohhackathon <branch-name>   #fetches and merges from the dohhackathon repo
```
Here’s [more information](https://github.com/blog/2042-git-2-5-including-multiple-worktrees-and-triangular-workflows#improved-support-for-triangular-workflows) on setting up triangular workflows (scroll to “Improved support…”).

Never worked with a triangular workflow before? Ask a project lead for help.
***
## After the Hackathon

**Rat Riddance:**

The Rat Hack meets regularly at Code for DC meetup events. To stay involved after the hackathon:
  1. Join the Code for DC group on [Meetup](https://www.meetup.com/)
  2. Join the [Code for DC Slack](https://codefordc.org/joinslack) and hop on to the #rats channel
  3. Check out our [primary project page](https://eclee25.github.io/the-rat-hack/)
  4. Make sure your name and contact information are on our [hackathon sign up sheet](https://docs.google.com/spreadsheets/d/1dp82BlwxMHGIiNPjfspWBkp_K1SZox0PXug8J8aOssU/edit?usp=sharing)!


**Food Safety/Restaurant Inspections:**

  The restaurant insepction Hack meets regularly at Code for DC meetup events. To stay involved after the hackathon:

  1. Join the Code for DC group on [Meetup](https://www.meetup.com/) and
  3. Subscribe for [#restaurant_inspection channel](https://codefordc.slack.com/messages/C221SGTKJ/search/in:%23restaurant_inspection/)
  3. Make sure your name and contact information are on our [hackathon sign up sheet](https://docs.google.com/spreadsheets/d/1dp82BlwxMHGIiNPjfspWBkp_K1SZox0PXug8J8aOssU/edit?usp=sharing)!


***
## Contact

**Rat Riddance:** Jason Asher (jason.m.asher@gmail.com) and Elizabeth Lee (eclee25@gmail.com)

**Restaurant Inspections:** Mohammed Kemal (mohakemal9@gmail.com) and Astrid Atienza (atienza211@gmail.com)
