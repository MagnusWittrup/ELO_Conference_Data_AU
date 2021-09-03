$(function () {
  $('.card-header').click(function (elem) {
    let icon = $(elem.currentTarget).find('i.fas');
    if (icon.hasClass('fa-angle-down')) {
      icon.removeClass('fa-angle-down');
      icon.addClass('fa-angle-right');
    } else {
      icon.removeClass('fa-angle-right');
      icon.addClass('fa-angle-down');
    }
    $(elem.currentTarget).next().toggle();
  });
  $('.card[data-trigger-word]').each((index, elem) => $(elem).find('.card-header').click());

  $('.dropdown-trigger').click(function (elem) {
    let icon = $(elem.currentTarget).find('i.fas');
    if (icon.hasClass('fa-angle-down')) {
      icon.removeClass('fa-angle-down');
      icon.addClass('fa-angle-right');
    } else {
      icon.removeClass('fa-angle-right');
      icon.addClass('fa-angle-down');
    }
    $(elem.currentTarget).next().toggle();
  });

  $('.trigger-word-checkbox').click(function (target) {
    let triggerWord = $(target.currentTarget).data().triggerWordToggle;
    $('[data-trigger-word="' + triggerWord + '"]').each((index, elem) => $(elem).toggle());
  });
});
