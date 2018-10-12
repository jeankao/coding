$(function () {
  $('#new-element').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var title = button.text();
    var modal = $(this);

    $('#elementName').attr('pattern', button.data('pattern'));
    $('#elementName').val('');
    if (button.data('type') === 'const') {
      $('#elementName').attr('type', 'number');
    } else {
      $('#elementName').attr('type', '');
    }
    if (button.data('type') === 'arr') {
      $('#form-group-elementNumber').css('display', 'block');
    } else {
      $('#form-group-elementNumber').css('display', 'none');
    }

    modal.data('type', button.data('type'));
    modal.data('class', button.data('class'));
    modal.find('.modal-title').text(title);
    $('#elementName').val('').focus();
  });

  function createNewElement() {
    var input = $('#elementName').val().trim();
    if (input !== "") {
      var type = $('#new-element').data('type');
      var bclass = $('#new-element').data('class');
      var list_id = '#' + type + '-list';
      var connectTo = ".exp-rhs";
      if (type === "var" || type == "arr") {
        connectTo += ", .exp-lhs";
      }
      if (type === "arr" && $('#elementNumber').val().trim()) {
        var capcacity = parseInt($('#elementNumber').val().trim());
        var item = $("<li></li>");
        var wrapper = $('<ul class="exp-item-list"></ul>');
        for (var i = 0; i < capcacity; i++) {
          var element = $('<li class="btn btn-sm exp-item exp-item-' + type + ' ' + bclass + '">' + input + '[' + i + ']</li>');
          element.draggable({
            connectToSortable: connectTo,
            helper: "clone",
            revert: "invalid",
          }).appendTo(wrapper);
        }
        wrapper.appendTo(item);
        item.appendTo($(list_id));
      } else {
        var element = $('<li class="btn btn-sm exp-item exp-item-' + type + ' ' + bclass + '">' + input + '</li>');
        element.draggable({
          connectToSortable: connectTo,
          helper: "clone",
          revert: "invalid",
        }).appendTo($(list_id));
        $('#elementName').val('').focus();
        }
    }
  }
  $('#new-element-ok').click(createNewElement);
  $('#elementName').on('keypress', function (event) {
    if (event.which === 13) {
      event.preventDefault();
      createNewElement();
      $('#elementName').val('').focus();
    }
  });

  $('.exp-item').draggable({
    connectToSortable: '.exp-rhs',
    helper: "clone",
    revert: "invalid",
  });

  $('.exp-item-var').draggable({
    connectToSortable: '.exp-rhs, .exp-lhs',
    helper: "clone",
    revert: "invalid",
  });

  $('.exp-lhs').sortable({
    receive: function (event, ui) {
      $(this).empty().append($(ui.item).clone());
    },
  }).disableSelection();

  $('.exp-trash').sortable({
    receive: function (event, ui) {
      $(ui.item).detach();
    }
  });

  $('.sortable').sortable({
    connectWith: '.exp-trash',
  }).disableSelection();
});