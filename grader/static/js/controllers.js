app.controller('GraderController', ['$scope', 'server', function($scope, server) {
    $scope.assignmentId = 0
    $scope.graded = {} // dict with ids that have been graded already
    server.getAssignment($scope.assignmentId).then(function(assignment) {
      $scope.assignment = assignment;
    });
    server.getNumAssignments().then(function(resp) {
      $scope.numAssignments = parseInt(resp.data, 10);
    });

    $scope.getNumber = function(num) {
      return new Array(num);
    }

    $scope.focusGradeBox = false;
    $scope.word = null;
    $scope.correctTo = '';

    $scope.wordClicked = function(word) {
      if (!word.correct) {
        word.correct = true;
        word.teacherCorrection = '';
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
        $scope.word.teacherCorrection = $scope.correctTo;
        $scope.word.selected = false;
        $scope.correctTo = '';
      }
    }

    $scope.gradeAssignment = function() {
      if (!($scope.assignmentId in $scope.graded)) {
        $scope.graded[$scope.assignmentId] = true;
        server.gradeAssignment($scope.assignmentId, $scope.assignment);
        $scope.updateAssignment($scope.assignmentId + 1);
      } else {
        // TODO(smilli): show error dialog
      }
    }

    $scope.updateAssignment = function(id) {
      if (id >= 0 && id < $scope.numAssignments) {
        $scope.assignmentId = id;
        server.getAssignment(id).then(function(assignment) {
          // TODO(smilli): make sure you get an assignment back
          // actually just add len of assignments to scope
          $scope.assignment = assignment;
        });
        $scope.focusGradeBox = false;
        $scope.word = null;
        $scope.correctTo = '';
        console.log($scope.assignmentGraded);
      }
    }

    $scope.reset = function() {
      server.reset();
      $scope.updateAssignment(0);
    }
  }])
