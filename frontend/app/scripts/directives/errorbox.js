'use strict';

/**
 * @ngdoc directive
 * @name frontendApp.directive:errorBox
 * @description
 * # errorBox
 */
angular.module('frontendApp')
  .directive('errorBox', function () {
    return {
      scope: {
        errorMsg: '='
      },
      templateUrl: 'views/errorbox.tpl.html',
      restrict: 'E',
      link: function postLink(scope, element, attrs) {
        scope.close = function () {
          scope.errorMsg = '';
        };
      }
    };
  });
