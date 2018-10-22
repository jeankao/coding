$(function () {
  const CS_VAR = 'btn-warning', 
        CS_ARR = 'btn-danger', 
        CS_CONST = 'btn-success',
        CS_SYMBOL = 'btn-default',
        CS_OP = 'btn-info';

  const BCLASS = {
    'var': CS_VAR, 
    'arr': CS_ARR, 
    'str-const': CS_CONST, 
    'num-const': CS_CONST,
    'op': CS_OP,
    'symbol': CS_SYMBOL,
  };

  const TYPELIST = {
    'vars': 'var', 
    'strs': 'str-const',
    'nums': 'num-const',
    'ops': 'op',
  };

  var $modal_literal_value = $('#modal-literal-value'), 
      $modal_new_array = $('#modal-new-array'),
      $modal_new_element = $('#modal-new-element');

  $('th', $modal_new_array).each(function(index, item) {
    $(item).html('<span class="badge badge-dark">'+$(item).text()+'</span>');
  });

  function getType(token) {
    console.log(token);
    if (token.match(/[\w\d]+(\[\d+\]){1,2}/))
      return 'arr';
    if (token.includes("'"))
      return 'str-const';
    if (token.match(/^\d+$/))
      return 'num-const';
    if (token.match(/[\(\)+\-*\/^]/))
      return 'op';
    if (token.match(/[\[\],]/))
      return 'symbol';
    return 'var';
  }

  function newBlock(type, item, target) {
    var element = $('<li class="expr-item '+type+' '+BCLASS[type]+'">' + item + '</li>');
    if (type !== 'symbol')
      element.addClass('btn btn-sm');
    element.appendTo($(target));
    return element;
  }

  function newExprBlock(setEventHandler = false) {
    var expr = $('<div class="expr"><ul class="expr-lhs expr-item-list"></ul> <ul class="d-inline-block pl-0"><li class="btn btn-dark btn-sm">=</li></ul> <ul class="expr-rhs expr-item-list"></ul></div>');

    if (setEventHandler) {
      $('.expr-lhs', expr).sortable({
        receive: function (event, ui) {
          $(this).empty().append($(ui.helper).clone());
        },
      }).disableSelection();
  
      $('.expr-rhs', expr).sortable({
        connectWith: '.expr-trash',
        receive: _expr_rhs_receive,
      }).disableSelection();  
    }
    expr.appendTo('#expr-list');
    return expr;
  }

  function newArrBlock(name, cols, is2d = false, rows = 1) {
    var wrapper = $('<ul class="expr-item-list" data-name="'+name+'" data-rows="'+rows+'" data-cols="'+cols+'" data-is2d="'+is2d+'"></ul>');
    if (!is2d) {
      for (var i = 0; i < cols; i++) {
        newBlock('arr', '['+i+']', wrapper);
      }  
    } else {
      for (var i = 0; i < cols; i++) {
        newBlock('arr', '['+0+']['+i+']', wrapper);
      }
      for (var r = 1; r < rows; r++) {
        $('<br>').appendTo(wrapper);
        for (var i = 0; i < cols; i++) {
          newBlock('arr', '['+r+']['+i+']', wrapper);
        }
      }
    }
    wrapper.appendTo($('<li class="arr-wrapper"><span class="btn btn-sm btn-danger">'+name+'</span></li>').appendTo($('#arr-list')));
    return wrapper;
  }

  function _expr_rhs_receive(event, ui) {
    var item = $(ui.helper);
    if (item.hasClass('expr-item arr')) {
      var name = item.parent().data('name');
      item.prepend(name);
    } else if (item.hasClass('expr-item literal')) {
      $modal_literal_value.data('literal-item', item);
      $('#modal-literal-value').modal('show');
    }
  }

  function _create_literal() {
    var item = $modal_literal_value.data('literal-item');
    var value = $('#literal-value').val().trim();
    if (item.hasClass('str')) {
      value = "'"+value+"'";
    }
    if (value) {
      item.text(value).attr('style', '');
    }
    $modal_literal_value.modal('hide');
  }

  $('#literal-value').on('keypress', function (event) {
    if (event.which === 13) {
      event.preventDefault();
      _create_literal();
    }
  });

  $('#literal-value-ok').click(function(event) {
    _create_literal();
  });

  $modal_literal_value.on('shown.bs.modal', function(event) {
    $('#literal-value').val('').focus();
  });

  $modal_literal_value.on('hide.bs.modal', function(event) {
    var item = $modal_literal_value.data('literal-item');
    if (item.html() === '&nbsp;')
      item.detach();
  });

  $modal_new_array.on('shown.bs.modal', function(event) {
    $('#div-arr-rows').addClass('d-none');
    $('table input:text', $modal_new_array).val('0');
    $('#arr-2d').prop('checked', false).change();
    $('#arr-rows').val('1').change();
    $('#arr-cols').change();
    $('#arr-name').val('').focus();
  });

  $('#arr-rows').change(function(event) {
    var arr_rows = parseInt($(this).val());
    for (var i = 1; i < 10; i++) {
      if (i < arr_rows)
        $('#modal-new-array tr:nth-child('+(i+2)+')').removeClass('d-none');
      else
        $('#modal-new-array tr:nth-child('+(i+2)+')').addClass('d-none');
    }
  });

  $('#arr-cols').change(function(event) {
    var arr_cols = parseInt($(this).val());
    for (var i = 1; i < 10; i++) {
      if (i < arr_cols)
        $('#modal-new-array tr :nth-child('+(i+2)+')').removeClass('d-none');
      else
        $('#modal-new-array tr :nth-child('+(i+2)+')').addClass('d-none');
    }
  });

  $('#arr-2d').change(function(event) {
    if ($(this).prop('checked')) {
      $('#div-arr-rows').removeClass('d-none');
      $('#modal-new-array tr th:nth-child(1)').removeClass('d-none');
    } else {
      $('#div-arr-rows').addClass('d-none');
      $('#modal-new-array tr th:nth-child(1)').addClass('d-none');
      $('#arr-rows').val('1').change();
    }
  });

  $('#literal-value-ok').click(function(event) {
    $modal_literal_value.modal('hide');
  });

  function newArrRowBlocks(row, cols, parent) {
    newBlock('symbol', '[', parent);
    var row_items = $('input', '#modal-new-array tr:nth-child('+(row+2)+')');
    newBlock('num-const', $(row_items[0]).val().trim(), parent);
    for (var i = 1; i < cols; i++) {
      newBlock('symbol', ',', parent);
      newBlock('num-const', $(row_items[i]).val().trim(), parent);
    }
    newBlock('symbol', ']', parent);
  }

  $('#new-arr-ok').click(function(event) {
    var arr_name = $('#arr-name').val().trim(),
        arr_rows = parseInt($('#arr-rows').val()), 
        arr_cols = parseInt($('#arr-cols').val()),
        arr_is2d = $('#arr-2d').prop('checked');
    var expr = $('<div class="expr"><ul class="expr-lhs expr-item-list"></ul> <ul class="d-inline-block pl-0"><li class="btn btn-dark btn-sm">=</li></ul> <ul class="expr-rhs expr-item-list"></ul></div>');
    var expr_lhs = $('.expr-lhs', expr), 
        expr_rhs = $('.expr-rhs', expr);

    newBlock('arr', arr_name, expr_lhs);

    if (arr_is2d) {
      newBlock('symbol', '[', expr_rhs);
      $('<br>').appendTo(expr_rhs);
    }
    newArrRowBlocks(0, arr_cols, expr_rhs);
    for (var r = 1; r < arr_rows; r++) {
      newBlock('symbol', ',', expr_rhs);
      $('<br>').appendTo(expr_rhs);
      newArrRowBlocks(r, arr_cols, expr_rhs);
    }
    if (arr_is2d) {
      $('<br>').appendTo(expr_rhs);
      newBlock('symbol', ']', expr_rhs);
    }

    newArrBlock(arr_name, arr_cols, arr_is2d, arr_rows);
/*
    if (setEventHandler) {
      $('.expr-lhs', expr).sortable({
        receive: function (event, ui) {
          $(this).empty().append($(ui.item).clone());
        },
      }).disableSelection();
  
      $('.sortable', expr).sortable({
        connectWith: '.expr-trash',
      }).disableSelection();  
    }
    */
    expr.appendTo('#expr-list');
    $modal_new_array.modal('hide');
    return expr;
  });


  function _var_arr_helper() {
    var name = $(this).parent().data('name');
    if ($(this).hasClass('expr-item arr'))
      return $(this).clone().prepend(name);
    else if ($(this).hasClass('expr-item literal'))
      return $(this).clone().html('&nbsp;');
    return $(this).clone();
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
      newArrBlock(arr.name, arr.cols, arr.is2d, arr.rows);
    }
    // init expression
    for (id in exprjson['exprs']) {
      var expr = exprjson['exprs'][id];
      var tokens = expr.match(/('[^']+'|[\w\d]+(\[\d+\]){0,2}|[\(\)+\-*\/]|\[|\]|,)/g);
      if (tokens) {
        expr = newExprBlock();
        if (tokens[1] === '[')
          newBlock('arr', tokens[0], $('.expr-lhs', expr));
        else
          newBlock(getType(tokens[0]), tokens[0], $('.expr-lhs', expr));
        for (var i = 1; i < tokens.length; i++) {
          token = tokens[i];
          newBlock(getType(token), token, $('.expr-rhs', expr));
        }
      }
    }
  }

  initExprElements();

  $modal_new_element.on('shown.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var title = button.text();
    var modal = $(this);

    $('#elementName').attr('pattern', button.data('pattern')).val('');
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
      var type = $modal_new_element.data('type');
      var bclass = $modal_new_element.data('class');
      var list_id = '#' + type + '-list';
      var connectTo = ".expr-rhs, .expr-trash";
      if (type === "var" || type == "arr") {
        connectTo += ", .expr-lhs";
      }
      if (type === "arr" && $('#elementNumber').val().trim()) {
        var capacity = parseInt($('#elementNumber').val().trim());
        var wrapper = newArrBlock(input, capacity);
        $('.expr-item', wrapper).draggable({
          connectToSortable: connectTo,
          revert: "invalid",
          helper: _var_arr_helper,
        });
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

  $('#new-exp').click(function() {
    newExprBlock(true);
  });

  $('.card-header .expr-item').draggable({
    connectToSortable: '.expr-rhs',
    helper: "clone",
    revert: "invalid",
  });

  $('.card-header .expr-item.str-const, .card-header .expr-item.num-const').draggable({
    connectToSortable: '.expr-rhs, .expr-trash',
    helper: "clone",
    revert: "invalid",
  });

  $('.card-header .expr-item.var, .card-header .expr-item.arr, .card-header .expr-item.literal').draggable({
    connectToSortable: '.expr-rhs, .expr-lhs, .expr-trash',
    revert: "invalid",
    helper: _var_arr_helper, 
  });

  $('.expr-lhs').sortable({
    receive: function (event, ui) {
      console.log(ui.helper);
      $(this).empty().append($(ui.helper).clone());
    },
  }).disableSelection();

  $('.expr-rhs').sortable({
    receive: _expr_rhs_receive,
  }).disableSelection();

  $('.expr-trash').sortable({
    receive: function (event, ui) {
      console.log(ui);      
      $(ui.item).detach();
      $(ui.helper).detach();
    }
  });

  $('.expr-lhs, .expr-rhs, .expr-list').sortable({
    connectWith: '.expr-trash',
  }).disableSelection();

  $('.expr-arr-list').sortable({
    connectWith: '.expr-trash',
  }).disableSelection();
  //-------------------------------------------------------------------------
  // 送出答案
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
      var size = $('.expr-item', $(obj)).length;
      data['arrs'].push({name: $(obj).data('name'), cols: $(obj).data('cols'), is2d: $(obj).data('is2d'), rows: $(obj).data('rows')});
    });

    $('.expr', '#expr-list').each(function(index, obj) {
      var tokens = [];
      $('li', $(obj)).each(function(index, item) {
        tokens.push($(item).text());
      });
      data['exprs'].push(tokens.join(' '));
    });
    console.log(data);
    $('#jsonstr').val(JSON.stringify(data));
    $('#expr-form').submit();
  });
});