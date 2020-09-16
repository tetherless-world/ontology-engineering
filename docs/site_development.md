---
---

# Site Development Instructions

This page contains technical documentation useful for developing your project site.

The site is built using Jekyll, which primarily uses Markdown along with the Liquid template language.
Helpful documentation on Jekyll development can be found [here](https://jekyllrb.com).

If you have questions or are experiencing difficulties, please contact Sam:
stoufs2 at rpi dot edu or Shruthi: chari at rpi dot edu

## Project Repo Maintenance and Site Setup Instructions

When you are trying to add to the website template that you have setup for your individual projects, please follow these steps:

1. Each project has a dedicated github branch, which is titled . Note, the is a placeholder that you need to replace with your actual project name.
2. Please only checkout this branch onto your machine using "git checkout "
3. All your project files are under the oe2020/ folder. This will be your project repository, a folder that you will upload all your artefacts, and use for website rendering as well.
4. We have setup website templates for each of your projects, that are accessible at project specific URLS of the form: http://--rpi-ontology-engineering.netlify.app/
5. When you are editing the website for your assignments, you can edit the .md files that we have created for you in your project repositories.
6. Images can be added to the images/ folder in your project repository.
7. Files can be added to the files/ folder in your project repository.
8. We have examples on how you can embed files and images for preview on your project website. Please try and use these templates we have provided for you.

Also, the navigation bar of your project page is filled out by us, and if you want to edit this (e.g.:, to add options), please consult with course TA, Shruthi: charis@rpi.edu or Sam Stouffer, stoufs2@rpi.edu
Finally, should you have any questions: please check the course instructions page at: https://master--rpi-ontology-engineering.netlify.app/.

We have further instructions, on the technical implementation of this infrastructure below. Please read through for your understanding.

## Preview a branch site on Netlify

The primary course site is hosted on GitHub Pages and is automatically built from the master branch.
The projects, however, cannot be hosted on GitHub Pages, which only allows hosting of a single branch.
Because of this, we will be hosting the branches using Netlify, a free cloud hosting service.

All branches of the GitHub repository will be built and hosted on Netlify at a url dependent upon the branch name.

The url for your branch will be https://*branch-name*--rpi-ontology-engineering.netlify.app/
where *branch-name* is the name of your branch.

Netlify will rebuild the site from your branch whenever you push new commits to the GitHub repo.
Allow several minutes for Netlify to rebuild the site from your changes.

## Preview a branch site on your own machine

Optionally, you can preview changes to your branch site without the hassle of pushing up a commit and waiting for Netlify
by building and serving the site on your own machine.

Follow the instructions [here](https://jekyllrb.com/docs/).
Skip the steps where you create a new site and change directory (just make sure you are in the `ontology-engineering` root directory when executing commands.)
