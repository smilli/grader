var assignments = [
      'This is a student\'s assignment',
      'This is another student\'s assignment'
];


var getAssignments = function(data) {
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
}


var app = angular.module('graderApp', [])
  .controller('GraderController', ['$scope', function($scope) {
    $scope.assignments = getAssignments(assignments);
    $scope.focusGradeBox = false;
    $scope.word = null;
    $scope.correctTo = '';

    $scope.wordClicked = function(word) {
      if ($scope.word) {
        $scope.word.selected = false;
      }
      $scope.word = word;
      $scope.word.selected = true;
      $scope.focusGradeBox = true;
    }

    $scope.submit = function() {
      if ($scope.word) {
        $scope.word.correct = false;
        $scope.word.correction = $scope.correctTo;
        $scope.word.selected = false;
        $scope.correctTo = '';
      }
    }
  }])
