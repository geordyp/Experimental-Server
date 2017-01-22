function TasksViewModel() {
  var self = this;
  self.tasksURI = "http://localhost:5000/ondeck/api/v1.0/tasks/1/all";
  self.loginURI = "http://localhost:5000/ondeck/api/v1.0/user/login";
  self.serverLogin = {
    username: "geordypaul",
    password: "Appl3B3ar"
  };

  self.user = ko.observable();
  self.tasks = ko.observableArray();

  self.error

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
        console.log("ajax error: " + jqXHR.responseText + " " + jqXHR.status);
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

  self.login = function(user) {
    self.ajax(self.loginURI, 'POST', user).done(function(data) {
      self.user(data.user[0])
      self.getTasks();
    }).fail(function(jqXHR) {
      if (jqXHR.status == 403)
        setTimeout(self.beginLogin, 500);
    });
  }

  self.login = function(user) {
    self.ajax(self.loginURI, 'POST', user).done(function(data) {
      $('#login').modal('hide');
      self.user(data.user[0])
      self.getActiveTasks()
    }).fail(function(jqXHR) {
      if (jqXHR.status == 403)
        setTimeout(self.beginLogin, 500);
    });
  }

  self.getActiveTasks = function() {
    self.ajax(self.user().activeTasksURI, "GET").done(function(data) {
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
}

var tasksViewModel = new TasksViewModel();
var addTaskViewModel = new AddTaskViewModel();
var loginViewModel = new LoginViewModel();
ko.applyBindings(tasksViewModel, $('#main')[0]);
ko.applyBindings(loginViewModel, $('#login')[0]);
ko.applyBindings(addTaskViewModel, $('#add')[0]);
