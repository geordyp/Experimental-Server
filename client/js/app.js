function TasksViewModel() {
  var self = this;
  self.tasksURI = "http://localhost:5000/ondeck/api/v1.0/tasks/1/all";
  self.loginURI = "http://localhost:5000/ondeck/api/v1.0/user/login";
  self.registerUserURI = "http://localhost:5000/ondeck/api/v1.0/user";
  self.serverLogin = {
    username: "geordypaul",
    password: "Appl3B3ar"
  };

  self.user = ko.observable(null);
  self.tasks = ko.observableArray([]);

  self.ajax = function(uri, method, data) {
    var request = {
      url: uri,
      type: method,
      contentType: "application/json",
      accepts: "application/json",
      cache: false,
      dataType: "json",
      data: JSON.stringify(data),
      beforeSend: function (xhr) {
        xhr.setRequestHeader("Authorization",
                             "Basic " + btoa(self.serverLogin.username + ":" + self.serverLogin.password));
      },
      error: function(jqXHR) {
        console.log("ajax error: " + jqXHR.responseText);
      }
    };
    return $.ajax(request);
  }

  self.openLogin = function() {
    $('#login').modal('show');
  }

  self.login = function(user) {
    self.ajax(self.loginURI, 'POST', user).done(function(data) {
      $('#login').modal('hide');
      self.user(data.user[0])
      self.getActiveTasks()
    }).fail(function(jqXHR) {
      $("#loginErrorMessage").html("Incorrect username or password.");
    });
  }

  self.logout = function() {
    self.user(null);
    self.tasks([]);
  }

  self.openUserRegistration = function() {
    $('#createUser').modal('show');
  }

  self.registerUser = function(user) {
    self.ajax(self.registerUserURI, 'POST', user).done(function(data) {
      $('#createUser').modal('hide');
      self.user(data.user[0])
      self.getActiveTasks()
    }).fail(function(jqXHR) {
      console.log(jqXHR);
      if (jqXHR.responseText.includes("This username is taken")) {
        $("#createUserErrorMessage").html("The username is taken.");
      }
      else {
        $("#createUserErrorMessage").html("We couldn't create the account.");
      }
    });
  }

  self.openSettings = function() {
    $('#settings').modal('show');
  }

  self.getActiveTasks = function() {
    self.getTasks(self.user().activeTasksURI)
  }

  self.getOnDeckTasks = function() {
    self.getTasks(self.user().onDeckTasksURI)
  }

  self.getDoneTasks = function() {
    self.getTasks(self.user().doneTasksURI)
  }

  self.getTasks = function(taskURI) {
    self.ajax(taskURI, "GET").done(function(data) {
      self.tasks([])
      for (var i = 0; i < data.tasks.length; i++) {
        self.tasks.push({
          name: ko.observable(data.tasks[i].name),
          commitment: ko.observable(data.tasks[i].commitment),
          notes: ko.observable(data.tasks[i].notes),
          dueDate: ko.observable(data.tasks[i].due_date),
          daysLeft: ko.observable(data.tasks[i].days_left),
          headsUp: ko.observable(data.tasks[i].heads_up),
          done: ko.observable(data.tasks[i].done),
          completionDate: ko.observable(data.tasks[i].completion_date),
          uri: ko.observable(data.tasks[i].uri)
        });
      }
    });
  }

  self.openAdd = function() {
    $('#addTask').modal('show');
  }

  self.addTask = function(task) {
    self.ajax(self.user().createTaskURI, 'POST', task).done(function(data) {
      $('#addTask').modal('hide');

      self.tasks.push({
        name: ko.observable(data.task.name),
        commitment: ko.observable(data.task.commitment),
        notes: ko.observable(data.task.notes),
        dueDate: ko.observable(data.task.due_date),
        daysLeft: ko.observable(data.task.days_left),
        headsUp: ko.observable(data.task.heads_up),
        done: ko.observable(data.task.done),
        completionDate: ko.observable(data.task.completion_date),
        uri: ko.observable(data.task.uri)
      });
    });
  }

  self.beginEdit = function(task) {
    editTaskViewModel.setTask(task);
    $('#edit').modal('show');
  }

  self.edit = function(task, data) {
    self.ajax(task.uri(), 'PUT', data).done(function(res) {
      self.updateTask(task, res.task);
    });
  }

  self.updateTask = function(task, newTask) {
    var i = self.tasks.indexOf(task);
    self.tasks()[i].uri(newTask.uri);
    self.tasks()[i].title(newTask.title);
    self.tasks()[i].description(newTask.description);
    self.tasks()[i].done(newTask.done);
  }

  self.remove = function(task) {
    self.ajax(task.uri(), 'DELETE').done(function() {
      self.tasks.remove(task);
    });
  }

  self.markDone = function(task) {
    self.ajax(task.uri(), 'PUT', { done: true }).done(function(res) {
      self.updateTask(task, res.task);
    });
  }

  self.openLogin();
}

function LoginViewModel() {
  var self = this;
  self.username = ko.observable("");
  self.password = ko.observable("");

  self.login = function() {
    tasksViewModel.login({
      name: self.username(),
      password: self.password()
    });

    self.username("");
    self.password("");
  }

  self.createUser = function() {
    tasksViewModel.openUserRegistration();
  }
}

function CreateUserViewModel() {
  var self = this;
  self.username = ko.observable("");
  self.password = ko.observable("");
  self.verifyPassword = ko.observable("");

  self.createUser = function() {
    var reUsername = /^[a-zA-Z0-9]+$/;
    var rePassword = /^.{3,20}$/;

    // validate username
    if (!reUsername.test(self.username())) {
      $("#createUserErrorMessage").html("Invalid username.");
      self.username("");
    }
    // validate password
    else if (!rePassword.test(self.password())) {
      $("#createUserErrorMessage").html("Invalid password.");
      self.password("");
      self.verifyPassword("");
    }
    // check if passwords match
    else if (self.password() !== self.verifyPassword()) {
      $("#createUserErrorMessage").html("The passwords don't match.");
      self.password("");
      self.verifyPassword("");
    }
    // check if all fields are filled
    else if (self.username() === "" || self.password() === "" || self.verifyPassword() === "") {
      $("#createUserErrorMessage").html("All inputs need to be filled.");
    }
    else {
      tasksViewModel.registerUser({
        name: self.username(),
        password: self.password()
      });

      self.username("");
      self.password("");
      self.verifyPassword("");
      $("#createUserErrorMessage").html("");
    }
  }
}

function AddTaskViewModel() {
  var self = this;
  self.name = ko.observable("");
  self.commitment = ko.observable("");
  self.dueDate = ko.observable("");
  self.headsUp = ko.observable("");
  self.notes = ko.observable("");

  self.addTask = function() {
    // check if the needed fields are filled
    if (self.name() === "" || self.commitment() === "" || self.dueDate() === "") {
      $("#addTaskErrorMessage").html("Please fill in Task, Commitment, and Due Date.");
    }
    else {
      tasksViewModel.addTask({
        name: self.name(),
        commitment: self.commitment(),
        due_date: self.dueDate(),
        heads_up: self.headsUp(),
        notes: self.notes()
      });

      self.name("");
      self.commitment("");
      self.dueDate("");
      self.headsUp("");
      self.notes("");
      $("#addTaskErrorMessage").html("");
    }
  }
}

function EditTaskViewModel() {
  var self = this;
  self.title = ko.observable();
  self.description = ko.observable();
  self.done = ko.observable();

  self.setTask = function(task) {
    self.task = task;
    self.title(task.title());
    self.description(task.description());
    self.done(task.done());
    $('edit').modal('show');
  }

  self.editTask = function() {
    $('#edit').modal('hide');
    tasksViewModel.edit(self.task, {
      title: self.title(),
      description: self.description() ,
      done: self.done()
    });
  }
}

var tasksViewModel = new TasksViewModel();
var loginViewModel = new LoginViewModel();
var createUserViewModel = new CreateUserViewModel();
var addTaskViewModel = new AddTaskViewModel();
ko.applyBindings(tasksViewModel, $('#main')[0]);
ko.applyBindings(loginViewModel, $('#login')[0]);
ko.applyBindings(createUserViewModel, $('#createUser')[0]);
ko.applyBindings(addTaskViewModel, $('#addTask')[0]);

$(document).ready(function(){
    $('[data-toggle="popover"]').popover();
});
