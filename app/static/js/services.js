app.factory('server', function($http) {
  return {
    getAssignments: function() {
      return $http.post('/assignments')
              .then(function(result) {
                return result.data;
              });
    }
  }
});
