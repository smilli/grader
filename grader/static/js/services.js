app.factory('server', function($http) {
  return {
    getAssignment: function(id) {
      return $http.post('/assignments/' + id)
              .then(function(result) {
                return result.data;
              });
    },
    gradeAssignment: function(id, assignment) {
      return $http.post('/grade/' + id,
        {assignment: assignment});
    },
    reset: function() {
      return $http.post('/reset/');
    },
    getNumAssignments: function() {
      return $http.post('/num-assignments/');
    }
  }
});
