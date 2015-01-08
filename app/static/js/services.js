app.factory('server', function($http) {
  return {
    getAssignments: function(id) {
      return $http.post('/assignments/' + id)
              .then(function(result) {
                return result.data;
              });
    },
    gradeAssignment: function(id, assignment) {
      console.log(assignment)
      return $http.post('/grade/' + id, 
        {assignment: assignment})
    }
  }
});
