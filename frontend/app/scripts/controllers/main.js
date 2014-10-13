'use strict';

/**
 * @ngdoc function
 * @name frontendApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the frontendApp
 */
angular.module('frontendApp').controller('MainCtrl', function ($scope, Imageservice, Config) {

  $scope.ui = {
    error: false
  };

  $scope.disable = false;

  $scope.approve = function (image) {
    $scope.disable = true;
    Imageservice.approveImage(image.id).then(
      function ok() {
        image.approved = true;
        image.showImage = false;
      }, function error(errData) {
        $scope.ui.error = errData;
        $scope.disable = false;
      }
    ).finally(function () {
        $scope.disable = false;
      });
  };

  $scope.reject = function (image) {
    Imageservice.rejectImage(image.id).then(
      function ok() {
        image.rejected = true;
        image.showImage = false;
      }, function error(errData) {
        $scope.ui.error = errData;
      }
    ).finally(function () {
        $scope.disable = false;
      });
  };

});
