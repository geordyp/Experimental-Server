#!/bin/bash
#todooli_tests.sh

RED='\033[0;31m'
GREEN='\033[0;32m'
#no color
NC='\033[0m'

echo "create user, missing password"
response=`curl -u me:password -H "Content-Type: application/json" -X POST -d '{"name":"sydney"}' http://localhost:5000/ondeck/api/v1.0/user 2> /dev/null`
r="$response"
userID1="${r#*id\":\ \"}"
userID1="${userID1%%\"*}"
if [[ $response == *"Bad request"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "create user, name wrong format"
response=`curl -u me:password -H "Content-Type: application/json" -X POST -d '{"name":false, "password":"goodpassword"}' http://localhost:5000/ondeck/api/v1.0/user 2> /dev/null`
r="$response"
userID1="${r#*id\":\ \"}"
userID1="${userID1%%\"*}"
if [[ $response == *"Bad request"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "create user1"
response=`curl -u me:password -H "Content-Type: application/json" -X POST -d '{"name":"sydney", "password":"goodpassword"}' http://localhost:5000/ondeck/api/v1.0/user 2> /dev/null`
r="$response"
userID1="${r#*id\":\ \"}"
userID1="${userID1%%\"*}"
if [[ $response == *"\"user\":"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "create user2"
response=`curl -u me:password -H "Content-Type: application/json" -X POST -d '{"name":"tim", "password":"goodpassword"}' http://localhost:5000/ondeck/api/v1.0/user 2> /dev/null`
r="$response"
userID2="${r#*id\":\ \"}"
userID2="${userID2%%\"*}"
if [[ $response == *"\"user\":"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "invalid username, too long"
response=`curl -u me:password -H "Content-Type: application/json" -X POST -d '{"name":"aaaaaaaaaaaaaaaaaaaaa", "password":"goodpassword"}' http://localhost:5000/ondeck/api/v1.0/user 2> /dev/null`
if [[ $response == *"Invalid username"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "invalid username, no special characters"
response=`curl -u me:password -H "Content-Type: application/json" -X POST -d '{"name":"sydney!", "password":"goodpassword"}' http://localhost:5000/ondeck/api/v1.0/user 2> /dev/null`
if [[ $response == *"Invalid username"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "invalid username, empty"
response=`curl -u me:password -H "Content-Type: application/json" -X POST -d '{"name":"", "password":"goodpassword"}' http://localhost:5000/ondeck/api/v1.0/user 2> /dev/null`
if [[ $response == *"Invalid username"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "invalid username, it's taken"
response=`curl -u me:password -H "Content-Type: application/json" -X POST -d '{"name":"sydney", "password":"goodpassword"}' http://localhost:5000/ondeck/api/v1.0/user 2> /dev/null`
if [[ $response == *"Username is taken"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "invalid password, too short"
response=`curl -u me:password -H "Content-Type: application/json" -X POST -d '{"name":"jeremy", "password":"p"}' http://localhost:5000/ondeck/api/v1.0/user 2> /dev/null`
if [[ $response == *"Invalid password"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "invalid password, too long"
response=`curl -u me:password -H "Content-Type: application/json" -X POST -d '{"name":"jeremy", "password":"ppppppppppppppppppppp"}' http://localhost:5000/ondeck/api/v1.0/user 2> /dev/null`
if [[ $response == *"Invalid password"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "invalid password, empty"
response=`curl -u me:password -H "Content-Type: application/json" -X POST -d '{"name":"jeremy", "password":""}' http://localhost:5000/ondeck/api/v1.0/user 2> /dev/null`
if [[ $response == *"Invalid password"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "login, bad request"
response=`curl -u me:password -H "Content-Type: application/json" -X POST -d '{"name":"sydney"}' http://localhost:5000/ondeck/api/v1.0/user/login 2> /dev/null`
if [[ $response == *"Bad request"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "invalid login"
response=`curl -u me:password -H "Content-Type: application/json" -X POST -d '{"name":"sydney", "password":"wrongpassword"}' http://localhost:5000/ondeck/api/v1.0/user/login 2> /dev/null`
if [[ $response == *"Invalid login"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "valid login"
response=`curl -u me:password -H "Content-Type: application/json" -X POST -d '{"name":"sydney", "password":"goodpassword"}' http://localhost:5000/ondeck/api/v1.0/user/login 2> /dev/null`
if [[ $response == *"\"user\":"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "update user, name wrong format"
response=`curl -u me:password -H "Content-Type: application/json" -X PUT -d '{"name":false}' http://localhost:5000/ondeck/api/v1.0/user/$userID1 2> /dev/null`
if [[ $response == *"Bad request"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "update user, invalid username"
response=`curl -u me:password -H "Content-Type: application/json" -X PUT -d '{"name":"aaaaaaaaaaaaaaaaaaaaa"}' http://localhost:5000/ondeck/api/v1.0/user/$userID1 2> /dev/null`
if [[ $response == *"Invalid username"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "update user, invalid username"
response=`curl -u me:password -H "Content-Type: application/json" -X PUT -d '{"name":"tim"}' http://localhost:5000/ondeck/api/v1.0/user/$userID1 2> /dev/null`
if [[ $response == *"Username is taken"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "update user, password wrong format"
response=`curl -u me:password -H "Content-Type: application/json" -X PUT -d '{"password":false}' http://localhost:5000/ondeck/api/v1.0/user/$userID1 2> /dev/null`
if [[ $response == *"Bad request"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "update user, invalid password"
response=`curl -u me:password -H "Content-Type: application/json" -X PUT -d '{"password":"p"}' http://localhost:5000/ondeck/api/v1.0/user/$userID1 2> /dev/null`
if [[ $response == *"Invalid password"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "update user, vision wrong format"
response=`curl -u me:password -H "Content-Type: application/json" -X PUT -d '{"vision":"foo"}' http://localhost:5000/ondeck/api/v1.0/user/$userID1 2> /dev/null`
if [[ $response == *"Bad request"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "update user, invalid vision too low"
response=`curl -u me:password -H "Content-Type: application/json" -X PUT -d '{"vision":-1}' http://localhost:5000/ondeck/api/v1.0/user/$userID1 2> /dev/null`
if [[ $response == *"Invalid on deck setting"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "update user, invalid vision too high"
response=`curl -u me:password -H "Content-Type: application/json" -X PUT -d '{"vision":61}' http://localhost:5000/ondeck/api/v1.0/user/$userID1 2> /dev/null`
if [[ $response == *"Invalid on deck setting"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "update user, username"
response=`curl -u me:password -H "Content-Type: application/json" -X PUT -d '{"name":"syd"}' http://localhost:5000/ondeck/api/v1.0/user/$userID1 2> /dev/null`
if [[ $response == *"\"user\":"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "update user, password"
response=`curl -u me:password -H "Content-Type: application/json" -X PUT -d '{"password":"evenbetterpassword"}' http://localhost:5000/ondeck/api/v1.0/user/$userID1 2> /dev/null`
if [[ $response == *"\"user\":"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "update user, vision"
response=`curl -u me:password -H "Content-Type: application/json" -X PUT -d '{"vision":10}' http://localhost:5000/ondeck/api/v1.0/user/$userID1 2> /dev/null`
if [[ $response == *"\"user\":"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "create task, missing fields"
response=`curl -u me:password -H "Content-Type: application/json" -X POST -d '{"due_date":"1-23-17", "heads_up":"", "notes":""}' http://localhost:5000/ondeck/api/v1.0/tasks/new/$userID1 2> /dev/null`
if [[ $response == *"Bad request"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "create task, missing fields"
response=`curl -u me:password -H "Content-Type: application/json" -X POST -d '{"name":"do something", "task_group":"personal", "due_date":"1-23-17"}' http://localhost:5000/ondeck/api/v1.0/tasks/new/$userID1 2> /dev/null`
if [[ $response == *"Bad request"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "create task, name wrong format"
response=`curl -u me:password -H "Content-Type: application/json" -X POST -d '{"name":false, "task_group":"personal", "due_date":"1-23-17", "heads_up":"", "notes":""}' http://localhost:5000/ondeck/api/v1.0/tasks/new/$userID1 2> /dev/null`
if [[ $response == *"Bad request"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "create task, name is too long"
response=`curl -u me:password -H "Content-Type: application/json" -X POST -d '{"name":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "task_group":"personal", "due_date":"1-23-17", "heads_up":"", "notes":""}' http://localhost:5000/ondeck/api/v1.0/tasks/new/$userID1 2> /dev/null`
if [[ $response == *"Invalid task name"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "create task, task group empty"
response=`curl -u me:password -H "Content-Type: application/json" -X POST -d '{"name":"do something", "task_group":"", "due_date":"1-23-17", "heads_up":"", "notes":""}' http://localhost:5000/ondeck/api/v1.0/tasks/new/$userID1 2> /dev/null`
if [[ $response == *"Invalid task group"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "create task, due date wrong format"
response=`curl -u me:password -H "Content-Type: application/json" -X POST -d '{"name":"do something", "task_group":"personal", "due_date":"asdf", "heads_up":"", "notes":""}' http://localhost:5000/ondeck/api/v1.0/tasks/new/$userID1 2> /dev/null`
if [[ $response == *"Invalid due date"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "create task, heads up wrong format"
response=`curl -u me:password -H "Content-Type: application/json" -X POST -d '{"name":"do something", "task_group":"personal", "due_date":"1-23-17", "heads_up":"asdf", "notes":""}' http://localhost:5000/ondeck/api/v1.0/tasks/new/$userID1 2> /dev/null`
if [[ $response == *"Invalid heads up"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "create task1"
response=`curl -u me:password -H "Content-Type: application/json" -X POST -d '{"name":"do something", "task_group":"personal", "due_date":"1-23-17", "heads_up":"", "notes":""}' http://localhost:5000/ondeck/api/v1.0/tasks/new/$userID1 2> /dev/null`
r="$response"
taskURI1="${r#*uri\":\ \"}"
taskURI1="${taskURI1%%\"*}"
if [[ $response == *"task"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "create task2"
response=`curl -u me:password -H "Content-Type: application/json" -X POST -d '{"name":"do something", "task_group":"personal", "due_date":"01-23-17", "heads_up":"05/04/2017", "notes":""}' http://localhost:5000/ondeck/api/v1.0/tasks/new/$userID1 2> /dev/null`
r="$response"
taskURI2="${r#*uri\":\ \"}"
taskURI2="${taskURI2%%\"*}"
if [[ $response == *"task"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "create task3"
response=`curl -u me:password -H "Content-Type: application/json" -X POST -d '{"name":"do something", "task_group":"personal", "due_date":"1-23-2017", "heads_up":"", "notes":"do a good job"}' http://localhost:5000/ondeck/api/v1.0/tasks/new/$userID1 2> /dev/null`
r="$response"
taskURI3="${r#*uri\":\ \"}"
taskURI3="${taskURI3%%\"*}"
if [[ $response == *"task"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "get active tasks"
response=`curl -u me:password -H "Content-Type: application/json" -X GET http://localhost:5000/ondeck/api/v1.0/tasks/$userID1/active 2> /dev/null`
if [[ $response == *"tasks"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "get done tasks"
response=`curl -u me:password -H "Content-Type: application/json" -X GET http://localhost:5000/ondeck/api/v1.0/tasks/$userID1/done 2> /dev/null`
if [[ $response == *"tasks"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "get on deck tasks"
response=`curl -u me:password -H "Content-Type: application/json" -X GET http://localhost:5000/ondeck/api/v1.0/tasks/$userID1/on-deck 2> /dev/null`
if [[ $response == *"tasks"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "get task1"
response=`curl -u me:password -H "Content-Type: application/json" -X GET $taskURI1 2> /dev/null`
if [[ $response == *"task"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "update task1, name wrong format"
response=`curl -u me:password -H "Content-Type: application/json" -X PUT -d '{"name":false}' $taskURI1 2> /dev/null`
if [[ $response == *"Bad request"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "update task1, name empty"
response=`curl -u me:password -H "Content-Type: application/json" -X PUT -d '{"name":""}' $taskURI1 2> /dev/null`
if [[ $response == *"Invalid task name"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "update task1, task group too long"
response=`curl -u me:password -H "Content-Type: application/json" -X PUT -d '{"task_group":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}' $taskURI1 2> /dev/null`
if [[ $response == *"Invalid task group"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "update task1, due date wrong format"
response=`curl -u me:password -H "Content-Type: application/json" -X PUT -d '{"due_date":"asdf"}' $taskURI1 2> /dev/null`
if [[ $response == *"Invalid due date"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "update task1, name, heads up, notes"
response=`curl -u me:password -H "Content-Type: application/json" -X PUT -d '{"name":"do something else", "heads_up":"1-19-17", "notes":"stay calm"}' $taskURI1 2> /dev/null`
if [[ $response == *"task"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "update task1, done, completion date"
response=`curl -u me:password -H "Content-Type: application/json" -X PUT -d '{"done":true, "completion_date":"1-19-17"}' $taskURI1 2> /dev/null`
if [[ $response == *"task"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "update task1, notes, heads up, name"
response=`curl -u me:password -H "Content-Type: application/json" -X PUT -d '{"notes":"", "heads_up":"", "name":"another name"}' $taskURI1 2> /dev/null`
if [[ $response == *"task"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "delete task1"
response=`curl -u me:password -H "Content-Type: application/json" -X DELETE $taskURI1 2> /dev/null`
if [[ $response == *"true"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "delete user1"
response=`curl -u me:password -H "Content-Type: application/json" -X DELETE http://localhost:5000/ondeck/api/v1.0/user/$userID1 2> /dev/null`
if [[ $response == *"true"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "delete user1 deleted task2"
response=`curl -u me:password -H "Content-Type: application/json" -X DELETE $taskURI2 2> /dev/null`
if [[ $response == *"No items found"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "delete user1 deleted task3"
response=`curl -u me:password -H "Content-Type: application/json" -X DELETE $taskURI3 2> /dev/null`
if [[ $response == *"No items found"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

echo "delete user2"
response=`curl -u me:password -H "Content-Type: application/json" -X DELETE http://localhost:5000/ondeck/api/v1.0/user/$userID2 2> /dev/null`
if [[ $response == *"true"* ]]; then
  echo -e "${GREEN}PASS${NC}"
else
  echo -e "${RED}FAIL${NC}"
fi

exit 0
