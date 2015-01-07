var assignments = [
      'This is a student\'s assignment',
      'This is another student\'s assignment'
];


var getAssignments = function($http) {
    $http.post('/assignments').
      success(function(data, status, headers, config) {
        console.log(data);
        assignments = []
        for (var i = 0; i < data.length; i++) {
          assignment = []
          words = data[i].split(' ');
          for (var j = 0; j < words.length; j++) {
            word = {'correct': true, 'correction':'', 'selected': false};
            word.text = words[j];
            assignment.push(word);
          }
          assignments.push(assignment);
        }
        return assignments;
      });
}


var app = angular.module('graderApp', [])
