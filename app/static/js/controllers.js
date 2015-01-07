app.controller('GraderController', ['$scope', 'server', function($scope, server) {
    server.getAssignments().then(function(assignments) {
      console.log(assignments);
      $scope.assignments = assignments;
    });
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
