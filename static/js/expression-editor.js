$(function () {
  
  function initExprElements() {
    var type_list = {
      'vars': {type: 'var', bclass: 'btn-warning'}, 
      'strs': {type: 'str-const', bclass: 'btn-success'},
      'nums': {type: 'num-const', bclass: 'btn-success'},
    };
    for (type in type_list) {
      for (id in exprjson[type]) {
        item = exprjson[type][id];
        var element = $('<li class="btn btn-sm expr-item '+type_list[type].type+' '+type_list[type].bclass+'">' + item + '</li>');
        element.appendTo($('#'+type_list[type].type+'-list'));
      }  
    }
    for (id in exprjson['arrs']) {
      var arr = exprjson['arrs'][id];
      var capacity = arr.size;
      var item = $("<li></li>");
      var wrapper = $('<ul class="expr-item-list" data-name="'+arr.name+'" data-size="'+capacity+'"></ul>');
      for (var i = 0; i < capacity; i++) {
        var element = $('<li class="btn btn-sm expr-item arr btn-danger">' + arr.name + '[' + i + ']</li>');
        element.appendTo(wrapper);
      }
      wrapper.appendTo(item);
      item.appendTo($('#arr-list'));
    }
    // init expression
  }

  initExprElements();



  $('#new-element').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var title = button.text();
    var modal = $(this);

    $('#elementName').attr('pattern', button.data('pattern'));
    $('#elementName').val('');
    if (button.data('type') === 'num-const') {
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
      var connectTo = ".expr-rhs";
      if (type === "var" || type == "arr") {
        connectTo += ", .expr-lhs";
      }
      if (type === "arr" && $('#elementNumber').val().trim()) {
        var capacity = parseInt($('#elementNumber').val().trim());
        var item = $("<li></li>");
        var wrapper = $('<ul class="expr-item-list" data-name="'+input+'" data-size="'+capacity+'"></ul>');
        for (var i = 0; i < capacity; i++) {
          var element = $('<li class="btn btn-sm expr-item ' + type + ' ' + bclass + '">' + input + '[' + i + ']</li>');
          element.draggable({
            connectToSortable: connectTo,
            helper: "clone",
            revert: "invalid",
          }).appendTo(wrapper);
        }
        wrapper.appendTo(item);
        item.appendTo($(list_id));
      } else {
        if (type==="str-const")
          input = "'" + input + "'";
        var element = $('<li class="btn btn-sm expr-item ' + type + ' ' + bclass + '">' + input + '</li>');
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

  // Create New Expression
  function createNewExpr() {
    var expr_str = '<div class="expr"><ul class="expr-lhs expr-item-list"><li class="btn btn-warning btn-sm">?</li></ul> <ul class="d-inline-block pl-0"><li class="btn btn-dark btn-sm">=</li></ul> <ul class="expr-rhs expr-item-list sortable"></ul></div>';
    var expr = $(expr_str);
    $('.expr-lhs', expr).sortable({
      receive: function (event, ui) {
        $(this).empty().append($(ui.item).clone());
      },
    }).disableSelection();
    $('.sortable', expr).sortable({
      connectWith: '.expr-trash',
    }).disableSelection();
    expr.appendTo('#expr-list');  
  }

  $('#new-exp').click(createNewExpr);

  $('.expr-item').draggable({
    connectToSortable: '.expr-rhs',
    helper: "clone",
    revert: "invalid",
  });

  $('.expr-item.var, .expr-item.arr').draggable({
    connectToSortable: '.expr-rhs, .expr-lhs',
    helper: "clone",
    revert: "invalid",
  });

  $('.expr-lhs').sortable({
    receive: function (event, ui) {
      $(this).empty().append($(ui.item).clone());
    },
  }).disableSelection();

  $('.expr-trash').sortable({
    receive: function (event, ui) {
      $(ui.item).detach();
    }
  });

  $('.sortable').sortable({
    connectWith: '.expr-trash',
  }).disableSelection();

  //
  $('#expr-submit').click(function() {
    var data = {
      vars: [], 
      arrs: [],
      strs: [],
      nums: [],
      exprs: [],
    };

    $('.expr-item', '#var-list').each(function(index, obj) {
      data.vars.push($(obj).text());
    });

    $('.expr-item', '#str-const-list').each(function(index, obj) {
      data.strs.push($(obj).text());
    });

    $('.expr-item', '#num-const-list').each(function(index, obj) {
      data.nums.push($(obj).text());
    });

    $('.expr-item-list', '#arr-list').each(function(index, obj) {
      data.arrs.push({name: $(obj).data('name'), size: $(obj).data('size')});
    });

    $('.expr', '#expr-list').each(function(index, obj) {
      var tokens = [];
      $('li', $(obj)).each(function(index, item) {
        tokens.push($(item).text());
      });
      data.exprs.push(tokens.join(' '));
    });
    console.log(data);
    console.log(JSON.stringify(data));
    $('#jsonstr').val(JSON.stringify(data));
    $('#expr-form').submit();
  });
});