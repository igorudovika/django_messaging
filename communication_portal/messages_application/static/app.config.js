//add CSRFToken to each request from Frontend
(function () {
   'use strict';
   angular.module('messages').run(['$http', run])
   function run($http) {
    $http.defaults.xsrfHeaderName = 'X-CSRFToken';
    $http.defaults.xsrfCookieName = 'csrftoken'
   }
})();