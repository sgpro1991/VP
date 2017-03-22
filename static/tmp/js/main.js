var initial_left = '-100px';
var initial_top = '100px';



//var cell_width = {{ canvas.cell_width }}
//var cell_height = {{ canvas.cell_height }}
//var strip = {{ canvas.strip_count }}
//var row = {{ canvas.row_count }}

function DRAW_DIVS(){


  for(var i=0;i<strip*row;i++){
    if(i>=80){
     $('.news_papper,.papper').append('<div class="draw_div draw_white ui-widget-header" style="width:'+cell_width+'px;height:'+cell_height+'px"></div>')
    }else{
     $('.news_papper,.papper').append('<div class="draw_div draw_dark ui-widget-header" style="width:'+cell_width+'px;height:'+cell_height+'px"></div>')
    }
  }
}



function GET_CM(){
$('.draggable2').on('mouseover',function(){
  $(this).find('.badge_main').addClass('active_panel')
})

$('.draggable2').on('mouseout',function(){
  $(this).find('.badge_main').removeClass('active_panel')
})
}




function DRAG(){

$('.draggable').draggable({
  snap: ".ui-widget-header",
  //revert: 'invalid',
  scroll: false,
  revert: "valid",
  start:function(event,ui){

  $(this).css({'z-index':'999'})
  },


});

}




function RESIZABLE(block){
  block.resizable({
    grid: [ cell_width, cell_height ],
    //ghost: true,
    //animate: true,
    disabled: false,
  //  minWidth: cell_width,
    maxWidth: (cell_width*strip),
    maxHeight:(cell_height*row),

    resize:function(event,ui){

          $(this).css({"padding":"0"})
          var w = parseInt($(this).css('width'))
          var h = parseInt($(this).css('height'))
          var hr = Math.ceil(h/cell_height)
          var wr = Math.ceil(w/cell_width)
          //alert(hr)

          $(this).css({'height':(hr*cell_height),'width':(wr*cell_width)})
        },


    create:function(event,ui){
          $(this).css({"padding":"0"})

        },

    start:function(event,ui){



          event.stopPropagation();
          $(this).addClass('imp_show_content')
        },

    stop:function(event,ui){

        var id = $(this).attr('id')

        var w = parseInt($(this).css('width'))
        var h = parseInt($(this).css('height'))
        var hr = Math.ceil(h/cell_height)
        var wr = Math.ceil(w/cell_width)
        //alert(hr)

        $(this).css({'height':(hr*cell_height),'width':(wr*cell_width)})
        $(this).attr('b_width',(wr*cell_width))
        $(this).attr('b_height',(hr*cell_height))
        $.ajax({
          url:'/block/change_parametrs/?id='+id+'&width='+(wr*cell_width)+'&height='+(hr*cell_height),
          type:'GET',
          success:function(data){
            //alert(data)
          },statusCode: {
          403: function(xhr) {
            alert('У вас недостаточно прав')
            location.reload()
          }
        }
        })
        setTimeout(function(){
          $('.droped').removeClass('imp_show_content')
        },100)
    }
    //animate: true
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

//alert(device.mobile())

  var clk

  if (device.mobile() == true){


    clk = 'click'
  }else{
    clk = 'dblclick'
  }

//alert(clk)

  $('.draggable2').off(clk)
  $('.draggable2').on(clk,function(){


    var id = $(this).attr('id')
    $('#scheduler_id_block').val(id)

    var editor = $('#ckeditor').ckeditorGet();

      $.ajax({
        url:'/block/set_data/',
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
          alert('Не достаточно прав')
          //location.reload()
        }
        }
      })


    $('.save_content').off('click')
    $('.save_content').on('click',function(){

    content = editor.getData();
    id = $(this).attr('init');
    //alert(id)
      //if(content!=''){
        $.ajax({
          url:'/block/set_data/',
          type:'POST',
          data:{
            param:'insert',
            id:id,
            content:content,
          },
          success:function(data){


              $('.draggable2').each(function(){
                  if($(this).attr('id') == id){

                  //alert(parseInt($(this).css('width')))

                    $(this).find('.panel_block').find('.content_block').remove()
                    $(this).find('.panel_block').append('<div class="content_block"><span init="'+id+'"  title="Контент" class="glyphicon glyphicon-file show_content" b_width="'+parseInt($(this).css('width'))+'" b_height="'+parseInt($(this).css('height'))+'"></span></div>')
                    SHOW_CONTENT()
                  }
              })
            alert("Успешно сохранено");
          }

        })
      //}else{
        //alert('Пусто напишите хоть что-нибудь')
      //}
    })


    GET_BLOCK_PARAMS(id)
    GET_TASKS_FROM_PLAN(id,date_number,date_number)
    CHANGE_DEB_CHECKS(id,date_number,date_number)

    $('.super-calendar__show').off('click')
    $('.super-calendar__show').on('click',function(){


      if(!$('.plan_task_box').hasClass('isset_task')){

        var from1 = $('.super-calendar__from').val();
        var to2 = $('.super-calendar__to').val();
        GET_TASKS_FROM_PLAN(id,from1,to2)
        CHANGE_DEB_CHECKS(id,from1,to2)

      }else{
          alert('Уже есть задача')
      }
      //  alert(1)
    })

  })
}



function rgb2hex(rgb){
 rgb = rgb.match(/^rgba?[\s+]?\([\s+]?(\d+)[\s+]?,[\s+]?(\d+)[\s+]?,[\s+]?(\d+)[\s+]?/i);
 return (rgb && rgb.length === 4) ? "#" +
  ("0" + parseInt(rgb[1],10).toString(16)).slice(-2) +
  ("0" + parseInt(rgb[2],10).toString(16)).slice(-2) +
  ("0" + parseInt(rgb[3],10).toString(16)).slice(-2) : '';
}










function END_PAGE(){
  $('.end_plan').change(function(){

    if($(this).is(':checked')){
      var value = '1'
    }else{
      var value = '0'
    }

    var init = $(this).attr('init')
    //alert(init)
    $.ajax({
      url:'/block/end_page/?id='+init+'&value='+value,
      success:function(data){
        //alert(data)
      }
    })
  })
}
















function GET_BLOCK_PARAMS(id){
  $.ajax({
    url:'/block/get_block_param/?id='+id,
    type:'GET',
    dataType:'json',
    success:function(data){
      console.log(data)

      $('.block_param').empty()

      $.each(data,function(k,v){

      //console.log(k,v)
        if(v['role']>3){
          var block_param_title = '<lable>Название</lable><input id="block_param_title" class="form-control" type="text" value="'+v['title']+'"/>'
        }else{
          var block_param_title = ''
        }


          $('.block_param').html(block_param_title+
          //'<input id="block_param_title" class="form-control" type="text" value="'+v['title']+'"/>'+
          '<lable><span class="badge about_width">'+(v['width']/cell_width)+'</span> Ширина</lable><div><input id="block_param_width" class="range" type="range" max="'+strip+'" min="1" value="'+(v['width']/cell_width)+'"/></div>'+
          '<lable><span class="badge about_height">'+(v['height']/cell_height)+'</span> Высота</lable><div><input  id="block_param_height"  class="range" type="range" max="'+row+'" min="1" value="'+(v['height']/cell_height)+'"/></div>'+
          '<lable>Цвет</lable><div><input  id="block_param_color" class="form-control" type="color" value="'+(v['color'])+'"/></div>'+
          '<br/>'+
          '<button id="remove_block_panel" init="'+id+'" class="form-control btn btn-danger remove_block">Удалить блок</button>'+
          '<div class="indicator_box"></div>')

      })

        $('#block_param_width').on('input',function(){
          $('.about_width').html($(this).val())
        })

        $('#block_param_height').on('input',function(){
          $('.about_height').html($(this).val())
        })

        EDIT_BLOCK_PARAMS(id)
    }
  })
}












function EDIT_BLOCK_PARAMS(id) {

  $('#remove_block_panel').on('click',function(){
    if ( confirm('Удалить этот блок?') ) {
        DELETE_BLOCKS(id)
        $('.hidden_block').fadeOut(500)
    }
  })




    $('#block_param_title,#block_param_width,#block_param_height,#block_param_color').on('input change',function() {

        $('.indicator_box').html('<span class="indicator glyphicon glyphicon-download"></span> Сохранение...')

        var timerId = setInterval(function() {
          $('.indicator').toggleClass('active_indicator')
        }, 500);

        //alert(id)


        var title = $('#block_param_title').val()
        var width = $('#block_param_width').val()
        var height = $('#block_param_height').val()
        var color = $('#block_param_color').val()
        var w = (width*cell_width)
        var h = (height*cell_height)


        //alert(title)
        $.ajax({
            url: '/block/edit_block_param/',
            type: 'POST',
            data: {
            'id': id,
            'title': title,
            'width': w,
            'height': h,
            'color': color
            },
            success: function(data) {

            setTimeout(function() {
              $('.indicator_box').empty();
              clearInterval(timerId);
            },1000)


                $('.draggable2').each(function() {
                    var a = $(this).attr('id')
                    //alert(a)
                    if(a==id) {
                        $('#title_'+id).text(title)

                        GET_SQUARE(w,h,$('#ad_square'+id));

                        $(this).css({'width':w,'height':h,'background':color})
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





function CHANGE_DEB_CHECKS(block_id,from,to){
  $('.deb_check').off('change')
  $('.deb_check').on('change',function(){
    GET_TASKS_FROM_PLAN(block_id,from,to)
  })

  $('#allocation_rubric').off('change')
  $('#allocation_rubric').on('change',function(){

    if($(this).prop('checked')){
      $('.deb_check').each(function(){
        $(this).prop('checked',false)
      })
      GET_TASKS_FROM_PLAN(block_id,from,to)
    }else{
      $('.deb_check').each(function(){
        $(this).prop('checked',true)
      })
      GET_TASKS_FROM_PLAN(block_id,from,to)
    }
  })

}




function GET_TASKS_FROM_PLAN(block_id,from,to) {
    $.ajax({
        //url: 'http://plan.oblgazeta.ru/api/1.0/list_task/'+from+','+to,
        url: '/api/list_task/?from='+from+'&to='+to,
        type: 'GET',
        async:false,
        dataType: 'json',
        success: function(data) {

            var task = CHECK_TASK(block_id)
            if (!task) {
                $('.plan_task_box').empty()


                  var checks = []

                  $('.deb_check').each(function(){
                    if($(this).prop( "checked" )){
                      checks.push($(this).val())
                    }
                  })





                  $.each(data,function(k,v) {
                          var mas = []
                          data[k].filter(function(item){
                                mas.push(item)
                          })



                            $('.plan_task_box').append('<hr></hr><span class="badge badge_strong">'+k+'</span>'+
                            ' Всего задач <span class="badge">'+data[k].length+'</span><br/>')


                        $.each(mas,function(k,v) {
                          if(checks.indexOf(v.deportament) != -1){

                            $('.plan_task_box').append('<div plan_task_id="' + v['id'] + '"  class="task">'+
                                '<span class="metka '+v['alias_dep']+'">'+v['deportament']+'</span>'+
                                '<div id="aut_' + v['id'] + '" class="author_topic">'+v['name']+'</div>'+
                                '<b class="topic">' + v['title'] + '</b><br/>'+
                                '<div class="description">' + v['description'] + '</div>'+
                                '</div>')
                            }
                        })
                  })




                  $('.deb_check').each(function(){
                      var dis = $(this).attr('init')
                      if($(this).is(':checked')){
                          $('.'+dis).css({'display':''})
                      }else{
                         $('.'+dis).css({'display':'none'})
                      }
                  })

                //  $.each(data[date_number],function(k,v) {
                    //$('.plan_task_box').append('<div plan_task_id="' + v['id'] + '" class="task"><div id="aut_' + v['id'] + '" class="author_topic"></div><br/></br><b class="topic">' + v['topic'] + '</b><br/><div class="description">' + v['description'] + '</div></div>')
                    //$.each(v['author'], function(key,val) {
                    //    $('#aut_'+v['id']).append(val+'; ')
                  //  })
              //  })

                ADD_TASK(block_id)
                $('.plan_task_box').removeClass('isset_task')

            } else {

                $('.plan_task_box').empty()
                // GET_ONE_TASK(task)
                $.ajax({
                    url: '/block/get_one_task/?id=' + task,
                    type: 'GET',
                    dataType: 'json',
                    success: function(data) {
                        $('.plan_task_box').append('<lable>Есть задача</lable>'+
                        '<br/><br/><div id="' + task + '" class="task task_one">' +
                        '<div class="author_topic">' + data[0]['task_author'] + '</div>' +
                        '<br><br><b class="topic">' + data[0]['task_topic'] + '</b><br><div class="description">' + data[0]['task_description'] + '</div></div>')

                        DELETE_ONE_TASK(block_id)

                      $('.plan_task_box').addClass('isset_task')

                    }
                })

            }
        }
    })



}








function DELETE_ONE_TASK(block_id) {
    $('.task_one').click(function() {

        var id = $(this).attr('id')
        //var init = $(this).attr('init_block')

        if (confirm('Удалить задачу?') == true) {
            $.ajax({
                url: '/block/delete_one_task/?id='+block_id+'&id_task='+ id,
                type: 'GET',
                success: function(data) {

                    $('#snaptarget > div[id=' + block_id + '] .task2').empty() // clear info in block
                    GET_TASKS_FROM_PLAN(block_id,date_number,date_number)
                    $('#task_all_view'+block_id).remove()
                }
            })
        }
    })
}





function CHECK_TASK(id) {
    var check = false;
    $.ajax({
        url: '/block/check_task/?id='+id,
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
    var task_id = $(this).attr('plan_task_id')


    $.ajax({
        url: '/block/add_task/',
        type: 'POST',
        data: {
            'id':id,
            'task_id':task_id,
            /*'author':author,
            'topic':topic,
            'description':description,*/
        },
        success: function(data) {
            //alert(data)
            //each=============================
            $('.draggable2').each(function() {
                if($(this).attr('id') == id) {

                    $(this).append('<div class="task_main" id="task_all_view'+id+'">'+
                    '<span class="author_task">'+author+'</span>'+
                    '<div class="task2">'+description+'</div>'+
                    '</div>')
                  //  $(this).children('.task2').empty()
                  //  $(this).children('.task2').append(data)
                }
            })
            //each=============================

            GET_TASKS_FROM_PLAN(id,date_number,date_number)
            //alert(data)
        },
        statusCode: {
            502: function(xhr) {
                alert('Уже есть задача')
                //location.reload()
            }
        },statusCode: {
            403: function(xhr) {

                if(confirm('Эта задача уже закреплена за другим блоком прикрепить ее к этому блоку?')==true){
                  REDIRECT_TASK(xhr.responseText,id,author,description)
                }
                  //location.reload()
            }
          }

    })

})

}



function REDIRECT_TASK(task_id,id,author,description){
  $.ajax({
      url: '/block/redirect_task/',
      type: 'POST',
      data: {
          'id':id,
          'task_id':task_id,
      },success:function(data){
            location.reload()
      }
    })
}



function GET_SQUARE(width,height,block){
  var strip = parseInt(width)/cell_width;
  var row = parseInt(height)/cell_height;
  var main;

  $.ajax({
    url:'/api/get_block_stats/?columns='+strip+'&rows='+row,
    async:false,
    success:function(data){
        main = data;
    }
  })
    block.html('<span class="badge">'+main['square']+' см<sup>2</sup></span> <span class="badge">'+main['maxchars']+'</span>');
}










function SHOW_CONTENT(){


  function get_params(col,row){
    var param;
    $.ajax({
      url:'/api/get_block_stats/?columns='+col+'&rows='+row,
      async:false,
      success:function(data){
        param = data
      }
    })

    return param;
  }



  $('.show_content').on('click',function(){


    var col = parseInt($(this).attr('b_width'))/cell_width
    var row = parseInt($(this).attr('b_height'))/cell_height
    var param = get_params(Math.ceil(col),Math.ceil(row))

    //alert(col)






    $('.content_box_append').empty()

      $.ajax({
        url:'/api/get_content/?id='+$(this).attr('init'),
        success:function(data){

            //console.log(param['square'])
            //alert(param['maxchars'])
            try{
              $('.content_box_append').html('<div style="text-align:center" class="panel panel-default">'+
              '<div class="panel-heading">'+
              '<span class="badge">'+param['square']+' см<sup>2</sup></span>'+
              ' <span title="Количество знаков" class="badge">'+param['maxchars']+'</span>'+
              '</div>'+
              ''+
              '<br/>'+data+'</div>')
            }catch(e){
              $('.content_box_append').html('<div style="text-align:center" class="panel panel-default">'+
              '<br/>'+data+'</div>')
            }

        },
        statusCode: {
            404: function(xhr) {


              $('.content_box_append').html('<div style="text-align:center" class="panel panel-default">'+
              '<div class="panel-heading">'+
              '<span class="badge">'+param['square']+' см<sup>2</sup></span>'+
              ' <span title="Количество знаков" class="badge">'+param['maxchars']+'</span>'+
              '</div>'+
              ''+
              '<br/>'+
              '<span class="glyphicon glyphicon-ban-circle"></span></div>')

            }
        }
      })

    if($(this).hasClass('draggable2')==false){
          $('.content_box').addClass('content_box_active')
    }

  })


  $('.close_content_box').on('click',function(){
    $('.content_box').removeClass('content_box_active')
  })



  $(window).keyup(function(e){
    if(e.keyCode == 27){
      $('.content_box').removeClass('content_box_active')
    }
  })



}





function DRAG_IN(){
    $('.draggable2').draggable({
        snap: ".ui-widget-header",
        //revert: 'invalid'
        zIndex: 99,
        scroll: false,
        stop: function(event,ui) {
            //$(this).css({'background':''})
            $(this).css({'z-index':''})

            var width = $(this).css('width')
            var height = $(this).css('height')
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
                    //alert(data)

                    block.find('.ad_square').attr('id','ad_square'+data)
                    block.find('.ad_square').html(GET_SQUARE(width,height,$('#ad_square'+data)))

                    block.find('.title').attr('id','title_'+data)
                    block.find('.remove').html('<span class="glyphicon glyphicon-trash remove_block"></span>') // draw icon for block removal
                    block.find('.remove_block').off('click').on('click', function() {
                        if ( confirm('Удалить этот блок?') ) {
                            DELETE_BLOCKS(data)
                        }
                    })

                    ADD_TEXT()
                    GET_CM()
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
            $('#snaptarget').append('<div class="draggable2 ui-widget-content ui-widget-header about" id="" style="width:'+width+'px;height:'+height+'px;'+result+';left:'+initial_left+';top:'+initial_top+'"><div  class="title">'+title+'</div> <div class="ad_square badge_main"></div> <div class="remove"></div></div>')
            DRAG_IN()
            RESIZABLE($('.draggable2'))
        }

        DROP()




        ui.draggable.addClass('droped')

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

$('.dbclick').on('click',function(){

  //  alert(1)

    //var width = $(this).css('width')
    //var height = $(this).css('height')check

    var width = $(this).attr('init_width')
    var height = $(this).attr('init_height')

    //var id = guid()
    //var color = getHexColor($(this).css('background'))
    var color = $(this).attr('color')

    var color2 = $(this).css('background')
    //alert(color2)
    var title = $(this).text()

    //$('#snaptarget').append('<div title="'+title+'" class="draggable2 ui-widget-content ui-widget-header about" id="'+(id)+'" style="position:absolute;max-width:'+width+';min-width:'+width+'; max-height:'+height+';min-height:'+height+';background:'+color+';left:'+initial_left+';top:'+initial_top+'">'+title+'<div class="task2"></div><div class="remove"></div></div>')
    $('#snaptarget').append('<div title="'+title+'" class="draggable2 ui-widget-content ui-widget-header about" id="" style="position:absolute;width:'+width+'px;height:'+height+'px;background:#'+color+';left:'+initial_left+';top:'+initial_top+'">'+
    '<div class="title">'+title+'</div>'+
    //'<div class="task_main">'+
    '<div class="task2"></div>'+
    //'</div>'+
    '<div class="ad_square badge_main"></div>'+
    //'<div class="remove"></div>'+
    '<div class="label label-default panel_block">'+
    '<div class="remove" title="Удалить блок">'+
    //'<span init="" class="glyphicon glyphicon-trash remove_block"></span>'+
    '</div>'+
    '<div class="content_block">'+
    '</div>'+
    '</div>'+
    '</div>')



    DRAG_IN()
    RESIZABLE($('.draggable2'))
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


















function DELETE_BLOCKS(block_id) {
    $.ajax({
        //url: 'remove_block/?id=' + block.attr('id'),
        url: '/block/remove_block/?id=' + block_id,
        type: 'GET',
        success: function(data) {
            if(data == 'ok') {

                $('#snaptarget > div[id=' + block_id + ']').remove()
                $('.droped').each(function(){
                  if($(this).attr('id') == block_id){
                      $(this).remove()
                  }
                })
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
       $(this).css({'width':(width*res/100),'height':(height*res/100),'font-size':res+'%'})

    })
  }

function SCALE_CART(){

var cart_blocks = []
$('.draggable').each(function(k,v){
    var h = $(this).css('height')
    var w = $(this).css('width')
    cart_blocks.push({'id':k,'width':w,'height':h})
})



  //$('#scale_cart').change(function(){



  $('#scale_cart').on("input change", function(){
    SET_SCALE(cart_blocks)
  })

  SET_SCALE(cart_blocks)
}





function CHECK_RULE() {
/*
  $.ajax({
    url:'check_rule/',
    success:function(data){
      if(data==5){
        //alert('a')
      }else{
        $('.shwduller_box').remove()
      }
    }
  })
*/
}




//START DOCUMENT--------------------------------------------------------------->

$( function() {



//var cal_from = $('.super-calendar__from').val()
//alert(cal_from)



$('.navbar-toggle').click(function(){
$('.collapse').slideToggle(500)
$('.collapse').toggleClass('active_menu')
})



//sort deportament ====================
$('.deb_check').change(function(){

  $('.deb_check').each(function(){
      var dis = $(this).attr('init')
      if($(this).is(':checked')){

      //alert(dis)
          $('.'+dis).css({'display':''})
      }else{
        $('.'+dis).css({'display':'none'})
      }
  })
})
//sort deportament ====================


END_PAGE()
SHOW_CONTENT()
CHECK_RULE()
SCALE_CART()
DRAW_DIVS()





//выдвигашка под ховер


GET_CM()





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

                if(ui.newHeader.context.id=='ui-id-5'){
                  setTimeout(function(){
                      document.getElementById('iframe_a').src ='/claim/';
                  },100)
                }

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
     RESIZABLE($('.draggable2'))
     DROP()
     DBCLICK()
     ADD_NEW_BLOCK()
     CHANGE_ORDER()


    $('.news_papper').css({'width':(cell_width*strip),'height':(cell_height*row)})




    $('.remove_block').click(function(){
        //var init = $(this).attr('init');
        var block = $(this).parent().parent()

          //alert(block.attr('id'))

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


$('.hidden_block').click(function(){
        $('.hidden_block').fadeOut(600)
})

$('#accordion').click(function(e){
  //alert(1)
  e.stopPropagation();

})


    $(window).keyup(function(e){
      if(e.keyCode==27){
        $('.hidden_block').fadeOut(600)
      }
    })



    function OPACITY(val){
      if(val!=10){
      $('.droped').css({'opacity':'0.'+val})
      }else{
      $('.droped').css({'opacity':1})
      }
    }







    $('#transperent_block').on('input change',function(){
    var val = $(this).val()
    OPACITY(val)
    })


$('.about_rubrics_btn').on('click',function(){
  $('.about_rubrics').toggleClass('active_about_rubric')

})



});
