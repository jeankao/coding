$(function () {
  const CS_VAR = 'btn-warning',
        CS_ARR = 'btn-danger',
        CS_CONST = 'btn-success',
        CS_SYMBOL = 'btn-default',
        CS_OP = 'btn-info';

  const TYPEMAP = {
    'arr': {c: CS_ARR, reg: /[\w]+(\[[^\[\]]+\])+/},
    'str-const': {c: CS_CONST, reg: /^'[^\']*'$/},
    'num-const': {c: CS_CONST, reg: /^\d+$/},
    'op': {c: CS_OP, reg: /[\(\)+\-*\/^]/},
    'symbol': {c: CS_SYMBOL, reg: /[\[\],]/},
    'var': {c: CS_VAR, reg: /.+/},
  };

  var $modal_literal_value = $('#modal-literal-value'),
      $modal_new_array = $('#modal-new-array'),
      $modal_new_var = $('#modal-new-var');

  $('th', $modal_new_array).each(function(index, item) {
    $(item).html('<span class="badge badge-dark">'+$(item).text()+'</span>');
  });

  function getType(token) {
    if (Number.isInteger(token))
      return 'num-const';
    for (type in TYPEMAP) {
      if (token.match(TYPEMAP[type].reg))
        return type;
    }
    return 'var';
  }

  function _new_arr_expr_block(item_str, parent) {
    //console.log('_arr_expr_block', item_str);
    var container = $('<ul class="expr-rhs expr-item-list"></ul>');
    var tokens = item_str.match(/\w+|[\(\)+\-*\/^]/g);
    for (var i = 0; i < tokens.length; i++) 
      newBlock(getType(tokens[i].trim()), tokens[i].trim(), container);
    container.appendTo(parent);
  }

  function newBlock(type, item, target, add_container = false) {
    var element = $('<li class="expr-item '+type+' '+TYPEMAP[type].c+'"></li>');
    if (type !== 'symbol')
      element.addClass('btn btn-sm');
    if (type === 'arr' && add_container) {
      var name = item.match(/[^\[\]]+/g);
      //console.log('name = ', name);
      if (name && name.length > 1) {
        element.append(name[0]);
        for (var i = 1; i < name.length; i++) {
          element.append('[');
          _new_arr_expr_block(name[i], element);
          element.append(']');
        }
      }
    } else {
      element.append(item);
    }
    element.appendTo($(target));
    return element;
  }

  function _expr_arr_item_receive(item) {
    var label = item.text();
    var name = label.match(/[^\[\]]+/g);
    item.text('');
    if (name && name.length > 1) {
      item.append(name[0]);
      for (var i = 1; i < name.length; i++) {
        var container = $('<ul class="expr-rhs expr-item-list"></ul>');
        newBlock(getType(name[i]), name[i], container);
        item.append('[').append(container).append(']');
      }
    }
    $('.expr-rhs', item).sortable({
      connectWith: '.expr-trash',
      receive: _expr_rhs_receive,
    }).disableSelection();
    item.attr('style', '');
    return item;
  }

  function _expr_lhs_receive(event, ui) {
    var item = $(ui.helper);
    if (item.hasClass('expr-item arr')) {
      _expr_arr_item_receive(item);
    }
    $(this).empty().append(item);
    $('.expr-rhs', item).sortable({
      connectWith: '.expr-trash',
      receive: _expr_rhs_receive,
    }).disableSelection();
  }

  function newExpr(setEventHandler = false) {
    var expr = $('<div class="expr"><ul class="expr-lhs expr-item-list"></ul> <ul class="d-inline-block pl-0"><li class="btn btn-sm">=</li></ul> <ul class="expr-rhs expr-item-list"></ul></div>');

    if (setEventHandler) {
      $('.expr-lhs', expr).sortable({
       receive: _expr_lhs_receive,
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
    $('.expr-item.arr', wrapper).draggable({
      connectToSortable: '.expr-rhs, .expr-lhs',
      revert: "invalid",
      helper: _var_arr_helper,
    });
    return wrapper;
  }

  function _expr_rhs_receive(event, ui) {
    var item = $(ui.helper);
    if (item.hasClass('expr-item arr')) {
      _expr_arr_item_receive(item);
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

  function _new_arr_row(items, parent) {
    newBlock('symbol', '[', parent);
    _new_arr_expr_block(items[0], parent);
    for (var i = 1; i < items.length; i++) {
      newBlock('symbol', ',', parent);
      _new_arr_expr_block(items[i], parent);
    }
    newBlock('symbol', ']', parent);
  }

  function _new_arr_expr(name, is2d, data, expr) {
    var expr_lhs = $('.expr-lhs', expr),
        expr_rhs = $('.expr-rhs', expr);

    expr_rhs.removeClass('expr-rhs');
    newBlock('arr', name, expr_lhs);
    if (is2d) {
      newBlock('symbol', '[', expr_rhs);
      $('<br>').appendTo(expr_rhs);
      _new_arr_row(data[0], expr_rhs);
      for (var r = 1; r < data.length; r++) {
        newBlock('symbol', ',', expr_rhs);
        $('<br>').appendTo(expr_rhs);
        _new_arr_row(data[r], expr_rhs);
      }
      $('<br>').appendTo(expr_rhs);
      newBlock('symbol', ']', expr_rhs);
    } else {
      _new_arr_row(data, expr_rhs);
    }
    $('.expr-rhs', expr).sortable({
      connectWith: '.expr-trash',
      receive: _expr_rhs_receive,
    }).disableSelection();
  }

  $('#new-arr-ok').click(function(event) {
    var arr_name = $('#arr-name').val().trim(),
        arr_rows = parseInt($('#arr-rows').val()),
        arr_cols = parseInt($('#arr-cols').val()),
        arr_is2d = $('#arr-2d').prop('checked');
    var expr = newExpr();
    var data = [];
    for (var row = 0; row < arr_rows; row++) {
      var row_items = $('input', '#modal-new-array tr:nth-child('+(row+2)+')');
      var arr = [];
      for (var col = 0; col < arr_cols; col++) {
        arr.push($(row_items[col]).val().trim());
      }
      data.push(arr);
    }
    _new_arr_expr(arr_name, arr_is2d, arr_is2d ? data : data[0], expr);
    newArrBlock(arr_name, arr_cols, arr_is2d, arr_rows);
    expr.appendTo('#expr-list');
    $modal_new_array.modal('hide');
    return expr;
  });


  function _var_arr_helper() {
    var name = $(this).parent().data('name');
    if ($(this).hasClass('expr-item arr')) {
      var helper = $(this).clone();
      helper.prepend(name);
      return helper;
    }
    if ($(this).hasClass('expr-item literal'))
      return $(this).clone().html('&nbsp;');
    return $(this).clone();
  }


  $modal_new_var.on('shown.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var title = button.text();
    var modal = $(this);

    $('#varName').attr('pattern', button.data('pattern')).val('');
    if (button.data('type') === 'num-const') {
      $('#varName').attr('type', 'number');
    } else {
      $('#varName').attr('type', '');
    }
    if (button.data('type') === 'arr') {
      $('#form-group-elementNumber').css('display', 'block');
    } else {
      $('#form-group-elementNumber').css('display', 'none');
    }

    modal.data('type', button.data('type'));
    modal.data('class', button.data('class'));
    modal.find('.modal-title').text(title);
    $('#varName').val('').focus();
  });

  function createNewVar() {
    var input = $('#varName').val().trim();
    if (input !== "") {
      newBlock('var', input, '#var-list').draggable({
        connectToSortable: '.expr-lhs, .expr-rhs, .expr-trash',
        helper: "clone",
        revert: "invalid",
      });
      $('#varName').val('').focus();
    }
  }

  $('#new-var-ok').click(createNewVar);

  $('#varName').on('keypress', function (event) {
    if (event.which === 13) {
      event.preventDefault();
      createNewVar();
      $('#varName').val('').focus();
    }
  });

  $('#new-exp').click(function() {
    newExpr(true);
  });

  $('.card-header .expr-item').draggable({
    connectToSortable: '.expr-rhs',
    helper: "clone",
    revert: "invalid",
  });

  $('.expr-trash').sortable({
    receive: function (event, ui) {
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
  // 初始化先前送出的舊運算式
  function initExprElements() {
    //console.log(exprjson);
    // init vars
    var items = exprjson['vars'];
    for (id in items) {
      item = items[id];
      newBlock('var', item, '#var-list').draggable({
        connectToSortable: '.expr-rhs, .expr-lhs, .expr-trash',
        revert: "invalid",
        helper: "clone",
      });
    }
    // init arrs
    for (id in exprjson['arrs']) {
      var arr = exprjson['arrs'][id];
      newArrBlock(arr.name, arr.cols, arr.is2d, arr.rows);
    }
    // init expression
    for (id in exprjson['exprs']) {
      var exprstr = exprjson['exprs'][id];
      var tokens = exprstr.match(/('[^']+'|\w+(\[[^\[\]]+\])*|[\(\)+\-*\/]|\[|\]|,)/g);
      if (tokens) {
        if (tokens[1] === '[') {
          var expr = newExpr();
          expr_rhs = exprstr.split(' = ');
          arrdef = expr_rhs[1].match(/\[[^\[\]]*\]/g);
          data = [];
          for (var i = 0; i < arrdef.length; i++) {
            data.push(arrdef[i].match(/[^\[\],]+/g));
          }
          if (tokens[2] === '[')
            _new_arr_expr(tokens[0], true, data, expr);
          else
            _new_arr_expr(tokens[0], false, data[0], expr);
        } else {
          var expr = newExpr(true);
          var expr_rhs = $('.expr-rhs', expr),
              expr_lhs = $('.expr-lhs', expr);

          newBlock(getType(tokens[0]), tokens[0], expr_lhs, true);
          for (var i = 1; i < tokens.length; i++) {
            token = tokens[i];
            newBlock(getType(token), token, expr_rhs, true);
          }
          $('.expr-item>.expr-rhs', expr).sortable({
            connectWith: '.expr-trash',
            receive: _expr_rhs_receive,
          }).disableSelection();

        }
      }
    }
  }

  initExprElements();

  //-------------------------------------------------------------------------
  // 送出答案
  $('#expr-submit').click(function() {
    var data = {
      vars: [],
      arrs: [],
      exprs: [],
    };

    $('.expr-item', '#var-list').each(function(index, obj) {
      data['vars'].push($(obj).text());
    });

    $('.expr-item-list', '#arr-list').each(function(index, obj) {
      var size = $('.expr-item', $(obj)).length;
      data['arrs'].push({name: $(obj).data('name'), cols: $(obj).data('cols'), is2d: $(obj).data('is2d'), rows: $(obj).data('rows')});
    });

    $('.expr', '#expr-list').each(function(index, obj) {
      var tokens = [];
      $('li', $(obj)).each(function(index, item) {
        if ($(item).parent().parent().hasClass('expr') || $(item).parent().parent().parent().hasClass('expr')) {
          tokens.push($(item).text());
        }
      });
      data['exprs'].push(tokens.join(' '));
    });
    $('#jsonstr').val(JSON.stringify(data));
    $('#expr-form').submit();
  });
});