angular.module('graderApp', [])
  .controller('GraderController', ['$scope', function($scope) {
    $scope.assignments = [
      'This is a student\'s assignment'.split(' '),
      'This is another student\'s assignment'.split(' ')
    ]

    $scope.wordClicked = function() {
      console.log('word clicked');
    }
  }])
