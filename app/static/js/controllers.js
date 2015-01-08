app.controller('GraderController', ['$scope', 'server', function($scope, server) {
    $scope.assignmentId = 0
    server.getAssignments($scope.assignmentId).then(function(assignment) {
      $scope.assignment = assignment;
    });
    $scope.focusGradeBox = false;
    $scope.word = null;
    $scope.correctTo = '';

    $scope.wordClicked = function(word) {
      if (!word.correct) {
        word.correct = true;
        word.correction = '';
        return;
      }
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

    $scope.newAssignment = function(offset) {
      if ($scope.assignmentId + offset > 0) {
        $scope.assignmentId += offset
        //server.gradeAssignment();
        server.getAssignments($scope.assignmentId).then(function(assignment) {
          // TODO(smilli): make sure you get an assignment back
          // actually just add len of assignments to scope
          $scope.assignment = assignment;
        });
        $scope.focusGradeBox = false;
        $scope.word = null;
        $scope.correctTo = '';
      }
    }
  }])
