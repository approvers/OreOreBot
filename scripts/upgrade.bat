@echo off

set argv1 = %1
set argv2 = %2

%argv2%
cd %argv1%

git pull origin master

exit 0