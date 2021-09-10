# Setup
Currently, we use **PIPENV**, a thrid party package to help manage the virtual enviroment. In order to setup all you have to do run a simple script

1. Run "source setup.sh". The shell script helps you download pipenv to your home directory and creates a new python virtual enviroment with all the dependencies required installed
   
# Version Control
In order to make things managable, some preliminary rules are established with regards to version control. Please fell free to add or comment to these rules!

1. Main branch will only have stable releases (aka when we reach certain milestones, we will merge dev into main)
2. Dev branch will be our active developing branch
3. When building new features, branch out from dev and merge back when complete. **DO NOT WORK ON A FEATURE THAT THE BRANCH IS NOT CREATED FOR**
4. **COMMIT OFTEN, PULL BEFORE PUSH, DON'T FORCE PUSH, AND PUSH OFTEN**