var initial_left = '-100px';
var initial_top = '100px';


//var cell_width = {{ canvas.cell_width }}
//var cell_height = {{ canvas.cell_height }}
//var strip = {{ canvas.strip_count }}
//var row = {{ canvas.row_count }}

function DRAW_DIVS(){


  for(var i=0;i<strip*row;i++){
    if(i>=80){
     $('.news_papper').append('<div class="draw_div draw_white ui-widget-header" style="width:'+cell_width+'px;height:'+cell_height+'px"></div>')
    }else{
     $('.news_papper').append('<div class="draw_div draw_dark ui-widget-header" style="width:'+cell_width+'px;height:'+cell_height+'px"></div>')
    }
  }
}







function DRAG(){

$('.draggable').draggable({
  snap: ".ui-widget-header",
  //revert: 'invalid',
  scroll: false,
  revert: "valid",
  start:function(event,ui){
  //  console.log(ui)
  $(this).css({'z-index':'999'})
  },


});

}








function CHANGE_ORDER(){

$('#order_init').on('change',function(){

    if(confirm('Поменять порядок?')==true){
        $.ajax({
          url:'change_order/?id_page='+$(this).attr('init')+'&value='+$(this).val(),
          type:'GET',
          success:function(data){
            //alert(data)
          },statusCode: {
          500: function(xhr) {
            alert('У вас недостаточно прав')
            location.reload()
          }
        }
        })
    }

})

}











function ADD_TEXT(){
  $('.draggable2').off('dblclick')
  $('.draggable2').on('dblclick',function(){



    var id = $(this).attr('id')
    $('#scheduler_id_block').val(id)

    var editor = $('#ckeditor').ckeditorGet();

      $.ajax({
        url:'set_data/',
        type:'POST',
        data:{
          param:'put',
          id:id,
        },
        success:function(data){

          editor.setData(data);

          $('.save_content').attr('init',id)
          //editor.insertText(data);

            $('.hidden_block').fadeIn(600)
        },statusCode: {
        403: function(xhr) {
          alert('Выможете редактировать только свои блоки')
          //location.reload()
        }
        }
      })


    $('.save_content').off('click')
    $('.save_content').on('click',function(){

    content = editor.getData();
    id = $(this).attr('init');


      $.ajax({
        url:'set_data/',
        type:'POST',
        data:{
          param:'insert',
          id:id,
          content:content,
        },
        success:function(data){
          alert("Успешно сохранено");
        }

      })

    })


    GET_BLOCK_PARAMS(id)
    GET_TASKS_FROM_PLAN(id)



  })
}



function rgb2hex(rgb){
 rgb = rgb.match(/^rgba?[\s+]?\([\s+]?(\d+)[\s+]?,[\s+]?(\d+)[\s+]?,[\s+]?(\d+)[\s+]?/i);
 return (rgb && rgb.length === 4) ? "#" +
  ("0" + parseInt(rgb[1],10).toString(16)).slice(-2) +
  ("0" + parseInt(rgb[2],10).toString(16)).slice(-2) +
  ("0" + parseInt(rgb[3],10).toString(16)).slice(-2) : '';
}








function GET_BLOCK_PARAMS(id){
  $.ajax({
    url:'get_block_param/?id='+id,
    type:'GET',
    dataType:'json',
    success:function(data){
      console.log(data)

      $('.block_param').empty()

      $.each(data,function(k,v){
            $('.block_param').append('<lable>Название</lable>'+
          '<input id="block_param_title" class="form-control" type="text" value="'+v['title']+'"/>'+
          '<lable>Ширина</lable><input id="block_param_width" class="form-control" type="number" value="'+(v['width']/cell_width)+'"/>'+
          '<lable>Высота</lable><input  id="block_param_height"  class="form-control" type="number" value="'+(v['height']/cell_height)+'"/>'+
          '<lable>Цвет</lable><input  id="block_param_color" class="form-control" type="color" value="'+(v['color'])+'"/>')
      })

        EDIT_BLOCK_PARAMS(id)
    }
  })
}












function EDIT_BLOCK_PARAMS(id) {

    $('#block_param_title,#block_param_width,#block_param_height,#block_param_color').change(function() {

        var title = $('#block_param_title').val()
        var width = $('#block_param_width').val()
        var height = $('#block_param_height').val()
        var color = $('#block_param_color').val()
        var w = (width*cell_width)
        var h = (height*cell_height)

        $.ajax({
            url: 'edit_block_param/',
            type: 'POST',
            data: {
            'id': id,
            'title': title,
            'width': w,
            'height': h,
            'color': color
            },
            success: function(data) {

                $('.draggable2').each(function() {
                    var a = $(this).attr('id')
                    //alert(a)
                    if(a==id) {
                        $(this).css({'max-width':w,'min-width':w,'max-height':h,'min-height':h,'background':color})
                    }
                })

            },
            statusCode: {
                404: function(xhr) {
                    alert('Что то не работает =(')
                    location.reload()
                }
            }
        })

    })


}












function GET_TASKS_FROM_PLAN(block_id) {

    $.ajax({
        url: 'http://plan.oblgazeta.ru/api/1.0/list_task/' + date_number + ',' + date_number,
        type: 'GET',
        dataType: 'json',
        success: function(data) {

            var task = CHECK_TASK(block_id)
            if (!task) {
                $('.plan_task_box').empty()

                $.each(data[date_number],function(k,v) {
                    $('.plan_task_box').append('<div plan_task_id="' + v['id'] + '" class="task"><div id="aut_' + v['id'] + '" class="author_topic"></div><br/></br><b class="topic">' + v['topic'] + '</b><br/><div class="description">' + v['description'] + '</div></div>')
                    $.each(v['author'], function(key,val) {
                        $('#aut_'+v['id']).append(val+'; ')
                    })
                })

                ADD_TASK(block_id)

            } else {
                $('.plan_task_box').empty()

                // GET_ONE_TASK(task)
                $.ajax({
                    url: 'get_one_task/?id=' + task,
                    type: 'GET',
                    dataType: 'json',
                    success: function(data) {
                        $('.plan_task_box').append('<lable>Есть задача</lable>'+
                        '<br/><br/><div id="' + task + '" class="task task_one">' +
                        '<div class="author_topic">' + data[0]['task_author'] + '</div>' +
                        '<br><br><b class="topic">' + data[0]['task_topic'] + '</b><br><div class="description">' + data[0]['task_description'] + '</div></div>')

                        DELETE_ONE_TASK(block_id)

                    }
                })

            }
        }
    })

}






/*
function GET_ONE_TASK(id) {
    $.ajax({
        url: 'get_one_task/?id=' + id,
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            $('.plan_task_box').append('<lable>Есть задача</lable>'+
            '<br/><br/><div id="' + id + '" class="task task_one">' +
            '<div class="author_topic">' + data[0]['task_author'] + '</div>' +
            '<br><br><b class="topic">' + data[0]['task_topic'] + '</b><br><div class="description">' + data[0]['task_description'] + '</div></div>')

            DELETE_ONE_TASK()
        }
    })
}
*/

function DELETE_ONE_TASK(block_id) {
    $('.task_one').click(function() {

        var id = $(this).attr('id')
        //var init = $(this).attr('init_block')

        if (confirm('Удалить задачу?') == true) {
            $.ajax({
                url: 'delete_one_task/?id=' + block_id+'&id_task='+ id,
                type: 'GET',
                success: function(data) {
                    $('#snaptarget > div[id=' + block_id + '] .task2').empty() // clear info in block
                    GET_TASKS_FROM_PLAN(block_id)
                }
            })
        }
    })
}





function CHECK_TASK(id) {
    var check = false;
    $.ajax({
        url: 'check_task/?id='+id,
        type: 'GET',
        async: false,
        success: function(data) {
            if (data) {
                check = data;
            }

        }

    })

    return check;
}












function ADD_TASK(id){

//  alert(id)

$('.task').click(function() {

    var author = $(this).children('.author_topic').text()
    var topic = $(this).children('.topic').text()
    var description = $(this).children('.description').text()

    $.ajax({
        url: 'add_task/',
        type: 'POST',
        data: {
            'id':id,
            'author':author,
            'topic':topic,
            'description':description,
        },
        success: function(data) {
            //alert(data)
            //each=============================
            $('.draggable2').each(function() {
                if($(this).attr('id') == id) {
                    $(this).children('.task2').empty()
                    $(this).children('.task2').append(data)
                }
            })
            //each=============================

            GET_TASKS_FROM_PLAN(id)
            //alert(data)
        },
        statusCode: {
            502: function(xhr) {
                alert('Уже есть задача')
                //location.reload()
            }
        }

    })

})

}











function DRAG_IN(){
    $('.draggable2').draggable({
        snap: ".ui-widget-header",
        //revert: 'invalid',
        scroll: false,
        stop: function(event,ui) {
            //$(this).css({'background':''})
            $(this).css({'z-index':''})

            var width = $(this).css('min-width')
            var height = $(this).css('min-height')
            var left = $(this).css('left')
            var top = $(this).css('top')
            //var id = $(this).attr('id')
            var color = getHexColor($(this).css('background-color'))
            var title = $(this).attr('title')
            var id = $(this).attr('id')

            var block = $(this) // for 'success' function

            $.ajax({
                url: 'create_blocks/',
                type: 'POST',
                data: {
                    width: width,
                    height: height,
                    left: left,
                    top: top,
                    color: color,
                    title: title,
                    id: id,
                },
                success: function(data) {
                    block.attr('id', data) // set 'id' from backend
                    block.find('.remove').html('<span class="glyphicon glyphicon-trash remove_block"></span>') // draw icon for block removal
                    block.find('.remove_block').off('click').on('click', function() {
                        if ( confirm('Удалить этот блок?') ) {
                            DELETE_BLOCKS(data)
                        }
                    })

                    ADD_TEXT()
                },
                statusCode: {
                    403: function(xhr) {
                        alert('Вы не можете двигать этот блок')
                        location.reload()
                    }
                }

            })

            //  console.log(top+'//'+left+'//'+id)

        }
    })
}



function guid() {
  function s4() {
    return Math.floor((1 + Math.random()) * 0x10000)
      .toString(16)
      .substring(1);
  }
  return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
    s4() + '-' + s4() + s4();
}




function DROP(){
$('.news_papper').droppable({

    drop: function( event, ui ) {

        var str = ui.draggable['context']['outerHTML']
        result = str.match(/background:.*[a-z]+;/)

        var width = ui.draggable['context']['offsetWidth']
        var height = ui.draggable['context']['offsetHeight']
        //var id = guid()
        var color = '#f00'
        var title = ui.draggable['context']['innerText']

        if (ui.draggable['context']['classList'][0] == "draggable") {
            //$('#snaptarget').append('<div class="draggable2 ui-widget-content ui-widget-header about" id="'+(id)+'" style="position:absolute;max-width:'+width+'px;min-width:'+width+'px; max-height:'+height+'px;min-height:'+height+'px;'+result+';left:'+initial_left+';top:'+initial_top+'">'+title+'<div class="remove"></div></div>')
            $('#snaptarget').append('<div class="draggable2 ui-widget-content ui-widget-header about" id="" style="position:absolute;max-width:'+width+'px;min-width:'+width+'px; max-height:'+height+'px;min-height:'+height+'px;'+result+';left:'+initial_left+';top:'+initial_top+'">'+title+'<div class="remove"></div></div>')
            DRAG_IN()
        }

        DROP()

        console.log(ui.draggable)

        console.log(ui.draggable['context']['offsetHeight'])
        ui.draggable.addClass('droped')

        //mass.push({"id":ui.draggable['context']['id']})
        //console.log(mass)

        var a = ui.draggable.offset()
}

});

}



function getHexColor( color ){
    //if color is already in hex, just return it...
    if( color.indexOf('#') != -1 ) return color;

    //leave only "R,G,B" :
    color = color
                .replace("rgba", "") //must go BEFORE rgb replace
                .replace("rgb", "")
                .replace("(", "")
                .replace(")", "");
    color = color.split(","); // get Array["R","G","B"]

    // 0) add leading #
    // 1) add leading zero, so we get 0XY or 0X
    // 2) append leading zero with parsed out int value of R/G/B
    //    converted to HEX string representation
    // 3) slice out 2 last chars (get last 2 chars) =>
    //    => we get XY from 0XY and 0X stays the same
    return  "#"
            + ( '0' + parseInt(color[0], 10).toString(16) ).slice(-2)
            + ( '0' + parseInt(color[1], 10).toString(16) ).slice(-2)
            + ( '0' + parseInt(color[2], 10).toString(16) ).slice(-2);
}








function DBCLICK(){

$('.dbclick').dblclick(function(){

    //var width = $(this).css('width')
    //var height = $(this).css('height')

    var width = $(this).attr('init_width')
    var height = $(this).attr('init_height')

    //var id = guid()
    var color = getHexColor($(this).css('background'))
    var title = $(this).text()

    //$('#snaptarget').append('<div title="'+title+'" class="draggable2 ui-widget-content ui-widget-header about" id="'+(id)+'" style="position:absolute;max-width:'+width+';min-width:'+width+'; max-height:'+height+';min-height:'+height+';background:'+color+';left:'+initial_left+';top:'+initial_top+'">'+title+'<div class="task2"></div><div class="remove"></div></div>')
    $('#snaptarget').append('<div title="'+title+'" class="draggable2 ui-widget-content ui-widget-header about" id="" style="position:absolute;max-width:'+width+'px;min-width:'+width+'px; max-height:'+height+'px;min-height:'+height+'px;background:'+color+';left:'+initial_left+';top:'+initial_top+'">'+title+'<div class="task2"></div><div class="remove"></div></div>')

    DRAG_IN()

    //DRAG()
    DROP()
  })
}







function CREATE_BLOCK(){
  $('#create_block_width').off('change')
  $('#create_block_width').on('change',function(){

        var width = $(this).val()
        var height = $('#create_block_height').val()
        var color =  $('#create_block_color').val()



      if(width<=strip){
        $('#different_block').css({'width':(width*cell_width),'height':(height*cell_height),'background':color})
      }else{
        alert('Превышен лимит макс.'+strip)
      }

  })




    $('#create_block_height').off('change')
    $('#create_block_height').on('change',function(){

      var width = $('#create_block_width').val()
      var height = $(this).val()
      var color =  $('#create_block_color').val()

      if(height<=row){
        $('#different_block').css({'width':(width*cell_width),'height':(height*cell_height),'background':color})
      }else{
        alert('Превышен лимит макс.'+row)
      }


    })

    $('#create_block_color').change(function(){
      var color = $(this).val()

      $('#different_block').css({'background':color})
    })


}









function ADD_NEW_BLOCK(){

  $('.init_canvas').css({'width':cell_width*strip,'height':cell_height*row,'float':'left'})




  CREATE_BLOCK()


  $('.add_new_block').on('click',function(){

      var dialog = $( "#dialog3" ).dialog({
          width: 950,
          modal: true,
          buttons: {
            "Создать блок": ADD_BLOCK_AJAX,
            "Отмена": function() {
              dialog.dialog( "close" );
            }
          },
        });
  })


}








function ADD_BLOCK_AJAX(){
  var title = $('#create_block_title').val()
  var width = $('#create_block_width').val()
  var height = $('#create_block_height').val()
  var color =  $('#create_block_color').val()

    alert(color)
  var str = 'add_block/?title='+title+'&w='+width+'&h='+height+'&c="'+color+'"'



  if(title!='' && width!='' && height!='' && color !=''){
      $.ajax({
        url:'add_block/',
        type:'POST',
        data:{
          'title':title,
          'w':width,
          'h':height,
          'c':color
        },
        success:function(data){
          if(data == 1){
            location.reload()
          }
        }
      })
  }else {
    alert('Заполните поля!')
  }


}

















//function DELETE_BLOCKS(block, param){
//function DELETE_BLOCKS(block) {
function DELETE_BLOCKS(block_id) {
    $.ajax({
        //url: 'remove_block/?id=' + block.attr('id'),
        url: 'remove_block/?id=' + block_id,
        type: 'GET',
        success: function(data) {
            if(data == 'ok') {

                $('#snaptarget > div[id=' + block_id + ']').remove()

                //block.remove()
            }
        },
        statusCode: {
            403: function(xhr) {
                alert('У вас недостаточно прав')
                //location.reload()
            }
        }
    })
}

function SET_SCALE(cart_blocks) {
    res = $('#scale_cart').val()

    $('.draggable').each(function(k,v){

        width = parseInt(cart_blocks[k]['width'])
        height = parseInt(cart_blocks[k]['height'])
        //alert(width)
       $(this).css({'max-width':(width*res/100),'max-height':(height*res/100),'min-width':(width*res/100),'min-height':(height*res/100),'font-size':res+'%'})

    })
  }

function SCALE_CART(){

var cart_blocks = []
$('.draggable').each(function(k,v){
    var h = $(this).css('max-height')
    var w = $(this).css('max-width')
    cart_blocks.push({'id':k,'width':w,'height':h})
})


  //console.log(cart_blocks)

  //$('#scale_cart').change(function(){



  $('#scale_cart').on("input change", function(){
    SET_SCALE(cart_blocks)
  })

  SET_SCALE(cart_blocks)
}






//START DOCUMENT--------------------------------------------------------------->

$( function() {

SCALE_CART()

DRAW_DIVS()



    $('.option_sel').each(function(){
        if($(this).val()==rubric){
        $(this).attr('selected','selected')
        }
    })

    $('#option_rubric').off('change')
    $('#option_rubric').on('change',function(){
        var conf = confirm('Поменять рубрику у этой странице?')
        if(conf == true){
          $.ajax({
            url:'change_rubric/?id_page='+$(this).attr('init')+'&value='+$(this).val(),
            type:'GET',
            success:function(data){
                //alert(data)
            },statusCode: {
            500: function(xhr) {
              alert('У вас недостаточно прав')
              location.reload()
              }
            }
          })
        }
    })



    $( "#accordion" ).accordion({
      heightStyle: "content",
      active: true,
      collapsible: true,
      beforeActivate: function(event, ui) {
               // The accordion believes a panel is being opened
              if (ui.newHeader[0]) {
                  var currHeader  = ui.newHeader;
                  var currContent = currHeader.next('.ui-accordion-content');
               // The accordion believes a panel is being closed
              } else {
                  var currHeader  = ui.oldHeader;
                  var currContent = currHeader.next('.ui-accordion-content');
              }
               // Since we've changed the default behavior, this detects the actual status
              var isPanelSelected = currHeader.attr('aria-selected') == 'true';

               // Toggle the panel's header
              currHeader.toggleClass('ui-corner-all',isPanelSelected).toggleClass('accordion-header-active ui-state-active ui-corner-top',!isPanelSelected).attr('aria-selected',((!isPanelSelected).toString()));

              // Toggle the panel's icon
              currHeader.children('.ui-icon').toggleClass('ui-icon-triangle-1-e',isPanelSelected).toggleClass('ui-icon-triangle-1-s',!isPanelSelected);

               // Toggle the panel's content
              currContent.toggleClass('accordion-content-active',!isPanelSelected)
              if (isPanelSelected) { currContent.slideUp(); }  else { currContent.slideDown(); }

              return false; // Cancel the default action
          }
    });




     DRAG_IN()
     DROP()
     DBCLICK()
     ADD_NEW_BLOCK()
     CHANGE_ORDER()


    $('.news_papper').css({'width':(cell_width*strip),'height':(cell_height*row)})




    $('.remove_block').click(function(){
        //var init = $(this).attr('init');
        var block = $(this).parent().parent()

        if( confirm('Удалить этот блок?') ) {
            //DELETE_BLOCKS(block,init)
            DELETE_BLOCKS(block.attr('id'))
        }
    })

    $('#ckeditor').ckeditor()




    $('.delete_page').off('click')
    $('.delete_page').on('click',function(){

        var a = $(this).attr('init')
        if(confirm("Удалить страницу") == true){
            $.ajax({
              url:'/number/delete_page/?id='+a,
              type:'GET',
              success:function(data){

                    location.href="/number/?id="+data

              }
            })
        }
    })






    ADD_TEXT()







    $(window).keyup(function(e){
      if(e.keyCode==27){
        $('.hidden_block').fadeOut(600)
      }
    })


});
