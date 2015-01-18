app.factory('server', function($http) {
  return {
    getAssignment: function(id) {
      return $http.post('/assignments/' + id)
              .then(function(result) {
                return result.data;
              });
    },
    gradeAssignment: function(id, answer) {
      return $http.post('/grade/' + id,
        {answer: answer});
    },
    reset: function() {
      return $http.post('/reset/');
    },
    getAssignmentInfo: function() {
      return $http.post('/assignment-info/');
    }
  }
});
