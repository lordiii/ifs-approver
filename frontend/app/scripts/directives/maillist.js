'use strict';

/**
 * @ngdoc directive
 * @name frontendApp.directive:MailList
 * @description
 * # MailList
 */
angular.module('frontendApp').directive('mailList', function (Imageservice, Config) {

  var MAIL_RE = /([\w\.]+@[\w\.]+)/;

  function patchEmail(image) {
    var short = MAIL_RE.exec(image.sender);
    if (short) {
      image.senderShort = short[1];
    } else {
      image.senderShort = image.sender;
    }
  }

  function addStatus(image) {
    image.approved = image.status === Imageservice.STATUS.APPROVED;
    image.rejected = image.status === Imageservice.STATUS.REJECTED;
  }

  return {
    scope: {
      filter: '@',
      onReject: '&',
      onApprove: '&',
      onError: '&',
      off: '=disableActions'
    },
    templateUrl: 'views/maillist.tpl.html',
    restrict: 'E',
    link: function postLink(scope, element, attrs) {
      scope.filter = scope.filter || 'ALL';

      var filterVal = Imageservice.FILTER[scope.filter];
      if (angular.isUndefined(filterVal)) {
        throw new Error('Invalid filter name: ' + scope.filter);
      }

      scope.showThumbnails = filterVal !== Imageservice.FILTER.MISSING;
      scope.enableActions = filterVal === Imageservice.FILTER.ALL;

      Imageservice.getImages(filterVal).then(
        function ok(data) {
          scope.images = data;
          scope.images.forEach(function (image) {
            patchEmail(image);
            image.previewUrl = Config.baseUrl + '/previews/preview_' + image.filename;
            addStatus(image);
          });
        }, function error(errData) {
          scope.onError({
            $error: errData
          });
        });
    }
  };
});
