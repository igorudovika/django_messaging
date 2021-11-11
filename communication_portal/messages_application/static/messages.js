(function () {
    'use strict';

    var alertPlaceholder = document.getElementById('liveAlertPlaceholder');
    var alertTrigger = document.getElementById('liveAlertBtn');

    function alert(message, type) {
        var wrapper = document.createElement('div');
        wrapper.innerHTML = '<div class="alert alert-' + type + ' alert-dismissible" role="alert">' + message + '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>';
        alertPlaceholder.append(wrapper);
    }
   angular.module('messages', [])
     .controller('MessagesController', ['$scope', '$http', MessagesController]);

     function MessagesController ($scope, $http) {
      $scope.messages = [];
      $scope.box = 'inbox';
      $scope.users_dict = {};

      $http.get('/api/users/').then(
        function(response) {
            $http.get('/api/inbox/').then(
                function(response) {
                    $scope.messages = response.data
                },
                function(response) {
                    alert(response.status +' ' + response.statusText, 'danger')
                }
            );

            $scope.users = response.data
            response.data.forEach(function(user) {
                $scope.users_dict[user.id] = user.username
            });
        },
        function(response) {
            alert(response.status +' ' + response.statusText, 'danger')
        }
      );

      // switch between inbox and sent one
      $scope.selectBox = function() {
        $scope.messages = [];
        $http.get('/api/' + $scope.box + "/").then(
            function(response){
                $scope.messages = response.data
            },
            function(response) {
                alert(response.status +' ' + response.statusText, 'danger')
            }
        );
      }

      // save new message
      $scope.sendMessage = function() {
        if ($scope.send_user != null && $scope.send_title != null && $scope.send_body) {
            $http.post('/api/sent/', {'recipient': $scope.send_user, 'title': $scope.send_title, 'body': $scope.send_body}).then(
                function() {
                    $scope.send_user = null;
                    $scope.send_title=null;
                    $scope.send_body=null;
                },
                function(response) {
                    alert(response.status +' ' + response.statusText, 'danger')});
                }
        else {
            alert('Not all fields where set', 'danger');
        }
      }

      // delete Message
      $scope.deleteMessage = function(id) {
        $http.delete('/api/' + $scope.box + '/' + id + '/');
      }

    // client connection to websocket
    var socket = new WebSocket('ws://' + window.location.host + '/ws/messages-monitor');
    socket.onmessage = function(event) {
      var message = JSON.parse(event.data);
      console.log(message);
      $scope.selectBox();
    }

    socket.onopen = function open() {
      console.log('WebSockets connection created.');
    };

    if (socket.readyState == WebSocket.OPEN) {
      socket.onopen();
    }
  }
  }());