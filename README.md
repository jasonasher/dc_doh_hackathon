# DC DOH Hackathon
Repository for the DC DOH Hackathon on September 23rd, 2017 (National Day of Civic Hacking)

This repository is for the Rat Riddance and Food Safety/Restaurant Inspections projects.

[Add notes about how the goals of the project and how this hackathon is a kickoff event]

## Join the project

Add your name to our [sign up sheet](https://docs.google.com/spreadsheets/d/1dp82BlwxMHGIiNPjfspWBkp_K1SZox0PXug8J8aOssU/edit?usp=sharing) in the "Sign up sheet" tab.

We are recruiting individuals for the following tasks:

* **Data cleaning:** Help us convert raw data frames into clean feature datasets that are ready to integrate into models!
* **Data visualization:** Look at the available datasets (See the "Dataset summary" tab in our [sign up sheet](https://docs.google.com/spreadsheets/d/1dp82BlwxMHGIiNPjfspWBkp_K1SZox0PXug8J8aOssU/edit?usp=sharing), chat with DC DOH agency representatives about maps and visualizations of interest, and create the visualizations!
* **User interface/experience (UI/UX):** 1) Build out features for our current 311 data portal (http://dc311portal.codefordc.org/) OR 2) Design and start to develop an application to view and report restaurant violations.
* **Project management:** Interested in helping us manage the project? Chat with one of the project leads!

Find a task to tackle in Github issues!

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
Now instead of plain `git push` and `git fetch`, use these:

```
$ git push origin <branch-name>       #pushes to your forked repo
$ git fetch dohhackathon <branch-name>   #fetches from the dohhackathon repo
```
Here’s [more information](https://github.com/blog/2042-git-2-5-including-multiple-worktrees-and-triangular-workflows#improved-support-for-triangular-workflows) on setting up triangular workflows (scroll to “Improved support…”).

Never worked with a triangular workflow before? Ask a project lead for help.

Please push your code to the folder labeled with your task!

## After the Hackathon
[tell people how to remain involved with the project]

## Contact

**Rat Riddance:** Jason Asher (jason.m.asher [AT] gmail [DOT] com) and Elizabeth Lee (eclee25 [AT] gmail [DOT] com)

**Food Safety/Restaurant Inspections:** Mohammad Kemal (mohakemal9@gmail.com)
