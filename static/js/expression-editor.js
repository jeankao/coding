$(function () {
  console.log(exprjson);
  const CS_VAR = 'btn-warning', 
        CS_ARR = 'btn-danger', 
        CS_CONST = 'btn-success',
        CS_OP = 'btn-info';

  const BCLASS = {
    'var': CS_VAR, 
    'arr': CS_ARR, 
    'str-const': CS_CONST, 
    'num-const': CS_CONST,
    'op': CS_OP,
  };

  const TYPELIST = {
    'vars': 'var', 
    'strs': 'str-const',
    'nums': 'num-const',
  };

  function newBlock(type, item, target) {
    var element = $('<li class="btn btn-sm expr-item '+type+' '+BCLASS[type]+'">' + item + '</li>');
    element.appendTo($(target));
    return element;
  }

  function getType(token) {
    if (token.includes('['))
      return 'arr';
    if (token.includes("'"))
      return 'str-const';
    if (token.match(/^\d+$/))
      return 'num-const';
    if (token.match(/[\(\)+\-*\/^]/))
      return 'op';
    return 'var';
  }

  function initExprElements() {
    // init vars, strs, nums
    for (key in TYPELIST) {
      var items = exprjson[key];
      for (id in items) {
        item = items[id];
        newBlock(TYPELIST[key], item, '#'+TYPELIST[key]+'-list');
      }  
    }
    // init arrs
    for (id in exprjson['arrs']) {
      var arr = exprjson['arrs'][id];
      var capacity = arr.size;
      var wrapper = $('<ul class="expr-item-list" data-name="'+arr.name+'" data-size="'+capacity+'"></ul>');
      for (var i = 0; i < capacity; i++) {
        newBlock('arr', arr.name+'['+i+']', wrapper);
      }
      wrapper.appendTo($("<li></li>").appendTo($('#arr-list')));
    }
    // init expression
    for (id in exprjson['exprs']) {
      var expr = exprjson['exprs'][id];
      var tokens = expr.match(/('[^']+'|[\w\d]+(\[\d+\])?|[\(\)+\-*\/])/g);
      expr = $('<div class="expr"><ul class="expr-lhs expr-item-list"></ul> <ul class="d-inline-block pl-0"><li class="btn btn-dark btn-sm">=</li></ul> <ul class="expr-rhs expr-item-list sortable"></ul></div>');
      newBlock(getType(tokens[0]), tokens[0], $('.expr-lhs', expr));
      for (var i = 1; i < tokens.length; i++) {
        token = tokens[i];
        newBlock(getType(token), token, $('.expr-rhs', expr));
      }
      expr.appendTo('#expr-list');
    }
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
        var wrapper = $('<ul class="expr-item-list" data-name="'+input+'" data-size="'+capacity+'"></ul>');
        for (var i = 0; i < capacity; i++) {
          newBlock('arr', input+'['+i+']', wrapper).draggable({
            connectToSortable: connectTo,
            helper: "clone",
            revert: "invalid",
          });
        }
        wrapper.appendTo($("<li></li>").appendTo($('#arr-list')));
      } else {
        if (type==="str-const")
          input = "'" + input + "'";
        
        newBlock(type, input, list_id).draggable({
          connectToSortable: connectTo,
          helper: "clone",
          revert: "invalid",
        });
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
      console.log(ui);
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

    for (var key in TYPELIST) {
      $('.expr-item', '#'+TYPELIST[key]+'-list').each(function(index, obj) {
        data[key].push($(obj).text());
      });  
    }

    $('.expr-item-list', '#arr-list').each(function(index, obj) {
      data['arrs'].push({name: $(obj).data('name'), size: $(obj).data('size')});
    });

    $('.expr', '#expr-list').each(function(index, obj) {
      var tokens = [];
      $('li', $(obj)).each(function(index, item) {
        tokens.push($(item).text());
      });
      data['exprs'].push(tokens.join(' '));
    });
    $('#jsonstr').val(JSON.stringify(data));
    $('#expr-form').submit();
  });
});