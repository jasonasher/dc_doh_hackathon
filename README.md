# DC DOH Hackathon
Repository for the DC DOH Hackathon on September 23rd, 2017

This repository is for the Rat Riddance and Food Safety/Restaurant Inspections projects.

Contact:
Rat Riddance - Jason Asher and Elizabeth Lee
Food Safety/Restaurant Inspections - Mohammad Kemal

## Join the project

Sign in [here](https://docs.google.com/spreadsheets/d/1dp82BlwxMHGIiNPjfspWBkp_K1SZox0PXug8J8aOssU/edit?usp=sharing)

## Contribute your code

Start by forking the repository, and then cloning the forked version of the repository to your computer. We use a triangular workflow - you should push to your fork, but fetch/pull from this repository. Setting this up is easy. Use these commands:
```
$ git clone <url-of-your-fork>
$ cd dc-doh-hackathon
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
