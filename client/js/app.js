var ViewModel = function() {
  var self = this;

  self.tasksURI = "http://localhost:5000/ondeck/api/v1.0/tasks";
  self.username = "geordypaul";
  self.password = "Appl3B3ar";
  self.allTasks = ko.observableArray();

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
                             "Basic " + btoa(self.username + ":" + self.password));
      },
      error: function(jqXHR) {
        console.log("ajax error " + jqXHR.status);
      }
    };
    return $.ajax(request);
  }

  self.ajax(self.tasksURI, "GET").done(function(data) {
    for (var i = 0; i < data.tasks.length; i++) {
      self.allTasks.push({
        uri: ko.observable(self.tasksURI + "/" + data.tasks[i].id),
        name: ko.observable(data.tasks[i].name),
        commitment: ko.observable(data.tasks[i].commitment),
        dueDate: ko.observable(data.tasks[i].due_date),
        daysLeft: ko.observable(data.tasks[i].days_left),
        headsUp: ko.observable(data.tasks[i].heads_up),
        createdDate: ko.observable(data.tasks[i].created_date),
        done: ko.observable(data.tasks[i].done)
      });
    }
  });
}

ko.applyBindings(new ViewModel());
