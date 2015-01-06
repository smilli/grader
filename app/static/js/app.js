var app = angular.module('graderApp', [])
  .controller('GraderController', ['$scope', function($scope) {
    $scope.assignments = [
      'This is a student\'s assignment'.split(' '),
      'This is another student\'s assignment'.split(' ')
    ];
    
    $scope.focusGradeBox = false;
    $scope.word = '';

    $scope.wordClicked = function(word) {
      console.log(word + ' clicked');
      $scope.word = word;
      $scope.focusGradeBox = true;
    }
  }])
