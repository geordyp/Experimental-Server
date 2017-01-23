function TasksViewModel() {
  var self = this;
  self.tasksURI = "http://localhost:5000/ondeck/api/v1.0/tasks/1/all";
  self.loginURI = "http://localhost:5000/ondeck/api/v1.0/user/login";
  self.registerUserURI = "http://localhost:5000/ondeck/api/v1.0/user";
  self.serverLogin = {
    username: "geordypaul",
    password: "Appl3B3ar"
  };

  self.user = ko.observable();
  self.tasks = ko.observableArray();

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

  self.beginAdd = function() {
    $('#add').modal('show');
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

  self.add = function(task) {
    self.ajax(self.tasksURI, 'POST', task).done(function(data) {
      self.tasks.push({
        uri: ko.observable(data.task.uri),
        title: ko.observable(data.task.title),
        description: ko.observable(data.task.description),
        done: ko.observable(data.task.done)
      });
    });
  }

  self.beginLogin = function() {
    $('#login').modal('show');
  }

  self.beginUserRegistration = function() {
    $('#createUser').modal('show');
  }

  self.login = function(user) {
    self.ajax(self.loginURI, 'POST', user).done(function(data) {
      $('#login').modal('hide');
      self.user(data.user[0])
      self.getTasks(self.user().activeTasksURI)
    }).fail(function(jqXHR) {
      $("#loginErrorMessage").html("Incorrect username or password.");
    });
  }

  self.registerUser = function(user) {
    self.ajax(self.registerUserURI, 'POST', user).done(function(data) {
      $('#createUser').modal('hide');
      self.user(data.user[0])
      self.getTasks(self.user().activeTasksURI)
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

  self.getTasks = function(taskURI) {
    self.ajax(taskURI, "GET").done(function(data) {
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

  self.beginLogin();
}

function AddTaskViewModel() {
  var self = this;
  self.title = ko.observable();
  self.description = ko.observable();

  self.addTask = function() {
    $('#add').modal('hide');
    tasksViewModel.add({
      title: self.title(),
      description: self.description()
    });
    self.title("");
    self.description("");
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

function LoginViewModel() {
  var self = this;
  self.username = ko.observable();
  self.password = ko.observable();

  self.login = function() {
    tasksViewModel.login({
      name: self.username(),
      password: self.password()
    });
  }

  self.createUser = function() {
    tasksViewModel.beginUserRegistration();
  }
}

function CreateUserViewModel() {
  var self = this;
  self.username = ko.observable();
  self.password = ko.observable();
  self.verifyPassword = ko.observable();
  self.vision = ko.observable();

  self.createUser = function() {
    var reUsername = /^[a-zA-Z0-9]+$/;
    var rePassword = /^.{3,20}$/;

    // validate username
    if (!reUsername.test(self.username())) {
      $("#createUserErrorMessage").html("Invalid username.");
      $("#inputNewUsername").val("");
    }
    // validate password
    else if (!rePassword.test(self.password())) {
      $("#createUserErrorMessage").html("Invalid password.");
      $("#inputNewPassword").val("");
      $("#inputVerifyPassword").val("");
    }
    // check if passwords match
    else if (self.password() !== self.verifyPassword()) {
      $("#createUserErrorMessage").html("The passwords don't match.");
      $("#inputNewPassword").val("");
      $("#inputVerifyPassword").val("");
    }
    // validate vision
    else if (self.vision() > 30 || self.vision() < 1 || !Number.isInteger(parseInt(self.vision()))) {
      $("#createUserErrorMessage").html("Days should be an integer between 1 and 30.");
      $("#inputVision").val("");
    }
    // check if all fields are filled
    else if (self.username() === "" || self.password() === "" || self.verifyPassword() === "" || self.vision() === "") {
      $("#createUserErrorMessage").html("All inputs need to be filled.");
    }
    else {
      tasksViewModel.registerUser({
        name: self.username(),
        password: self.password(),
        vision: parseInt(self.vision())
      });
    }
  }
}

var tasksViewModel = new TasksViewModel();
var loginViewModel = new LoginViewModel();
var createUserViewModel = new CreateUserViewModel();
var addTaskViewModel = new AddTaskViewModel();
ko.applyBindings(tasksViewModel, $('#main')[0]);
ko.applyBindings(loginViewModel, $('#login')[0]);
ko.applyBindings(createUserViewModel, $('#createUser')[0]);
ko.applyBindings(addTaskViewModel, $('#add')[0]);

$(document).ready(function(){
    $('[data-toggle="popover"]').popover();
});
