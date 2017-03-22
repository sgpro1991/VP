/*
    $( ".control .prev", page ).on( "click", function() {
               $.mobile.changePage( prev + ".html", { transition: "slide", reverse: true } );
           });
*/
var deportament,alias_dep,datepicker,title,topic;
    $('#list_dep').empty()
function CHECK_AUTH(){
  var dep;

  $.ajax({
    url:'check_auth/',
    dataType:'json',
    async:false,
    success:function(data){
      dep = data

    $('#list_dep').empty()
      $.each(dep,function(k,v){

      $('#list_dep').append('<li  class="ui-first-child ui-last-child "><a href="#date" init="'+v['cn']+'" data-transition="slide" class="ui-btn ui-btn-icon-right ui-icon-carat-r deportament">'+v['ru']+'</a></li>')
      })


      $('.deportament').click(function(){
          deportament = $(this).text()
          alias_dep = $(this).attr('init')

      })

  //$.mobile.changePage( "#main_page", { transition: "pop", reverse: false } )
    },statusCode: {
      404: function(xhr) {
      ENTER()
    }
  }
  })

    return dep;
}






function ENTER(){
  $.mobile.changePage( "#auth", { transition: "pop", reverse: false } )

      $('#enter').off('click')
      $('#enter').on('click',function(e){
        VHOD()
      })




}



function VHOD(){
  var login = $('#login').val(),password = $('#password').val()

  $.ajax({
    url:'auth/?login='+login+'&password='+password,
    async:false,
    success:function(data){
    //$.mobile.changePage( "#main_page", { transition: "pop", reverse: false } );
    location.reload()
    },statusCode: {
      403: function(xhr) {
      alert('Неверный логин/пароль')
      $(document).bind("pagebeforechange",function(e){
        e.preventDefault();
        e.stopPropagation();
      })
    // $.mobile.changePage( "#auth", { transition: "pop", reverse: false } );
    }
  }
})
}







//READY DOCUMENT
$(document).ready(function(){


  $.datepicker.regional['ru'] = {
  closeText: 'Закрыть',
  prevText: '&#x3c;Пред',
  nextText: 'След&#x3e;',
  currentText: 'Сегодня',
  monthNames: ['Январь','Февраль','Март','Апрель','Май','Июнь',
  'Июль','Август','Сентябрь','Октябрь','Ноябрь','Декабрь'],
  monthNamesShort: ['Янв','Фев','Мар','Апр','Май','Июн',
  'Июл','Авг','Сен','Окт','Ноя','Дек'],
  dayNames: ['воскресенье','понедельник','вторник','среда','четверг','пятница','суббота'],
  dayNamesShort: ['вск','пнд','втр','срд','чтв','птн','сбт'],
  dayNamesMin: ['Вс','Пн','Вт','Ср','Чт','Пт','Сб'],
  dateFormat: 'dd.mm.yy',
  firstDay: 1,
  isRTL: false
  };


  $.datepicker.setDefaults($.datepicker.regional['ru']);




$(document).off("ready pageshow")
$(document).on("ready pageshow",function(){ // When entering pagetwo
CHECK_AUTH()

});







$('.return_plan').click(function(){
  window.location = '/number/'
})




$(document).on("pageshow",'#topic', function(){ // When entering pagetwo
$('#description_task').focus()
});

$(document).on("pageshow",'#title', function(){ // When entering pagetwo
$('#title_field').focus()
});




//===============================================================================



$('#send').click(function(){

SEND_DATA()

})


$('#count_chars').keyup(function(e){

  if(e.keyCode==13){
    SEND_DATA()
  }

})





$(document).on("pagebeforeshow", "#auth",function(){ // When entering pagetwo
CHECK_AUTH()
});



$('#password').keyup(function(e){

  if(e.keyCode==13){
    VHOD()
    CHECK_AUTH()
    $.mobile.changePage( "#main_page", { transition: "pop", reverse: false } );
  }

})













function SEND_DATA(){
  $('#undefined_list').empty()

    if($('#description_task').val()!=''){
    topic = $('#description_task').val()
    }else{
    topic = undefined
    }


    if($('#title_field').val()!=''){
      title = $('#title_field').val()
    }else{
      title = undefined
    }

  console.log(deportament,datepicker,title,topic)
  var count = $('#count_chars').val()

  if(deportament==undefined || datepicker == undefined || title==undefined || topic==undefined ){


    if(deportament == undefined){
      $('#undefined_list').append('<li class="ui-first-child ui-last-child "><a href="#main_page" data-transition="pop" class="ui-btn ui-btn-icon-right ui-icon-carat-r">Отдел</a></li>')
    }


    if(datepicker == undefined){
      $('#undefined_list').append('<li class="ui-first-child ui-last-child "><a href="#date" data-transition="pop" class="ui-btn ui-btn-icon-right ui-icon-carat-r">Дата</a></li>')
    }

    if(title == undefined){
      $('#undefined_list').append('<li class="ui-first-child ui-last-child "><a href="#title" data-transition="pop" class="ui-btn ui-btn-icon-right ui-icon-carat-r">Заголовок</a></li>')
    }

    if(topic == undefined){
      $('#undefined_list').append('<li class="ui-first-child ui-last-child "><a href="#topic" data-transition="pop" class="ui-btn ui-btn-icon-right ui-icon-carat-r">Описание</a></li>')
    }

    $.mobile.changePage( "#check", { transition: "pop", reverse: false } );



  }else{
      $.ajax({
        url:'create_task/',
        type:'POST',
        data:{
          'deportament':deportament,
          'alias_dep':alias_dep,
          'date':datepicker,
          'title':title,
          'topic':topic,
          'count':count,
        },success:function(data){

          $.mobile.changePage( "#main_page", { transition: "slide", reverse: false } );
          setTimeout(function(){
          $( "#popupBasicTrue" ).popup('open');
          },300)

          setTimeout(function(){
          $( "#popupBasicTrue" ).popup('close');
          },4300)

          deportament = undefined,alias_dep = undefined,datepicker = undefined,title = undefined,topic = undefined;
           $('#title_field,#description_task,#count_chars').val('')
        },statusCode: {
          405: function(xhr) {
          $.mobile.changePage( "#main_page", { transition: "slide", reverse: false } );
            setTimeout(function(){
            $( "#popupBasicFalse" ).popup('open');
            },500)

            setTimeout(function(){
            $( "#popupBasicFalse" ).popup('close');
            },3300)
          }
        }

      })
  }

}


//===============================================================================












$('.exit').click(function(){
if(confirm('Вы хотите выйти?')==true){
$.ajax({
    url:'exit/',
    success:function(data){
      CHECK_AUTH()
      location.reload()
    }
})
}
})



$('#title').on('keyup',function(e){

if($('#title_field').val()!=''){
  title = $('#title_field').val()
}else{
  title = undefined
}

  if(e.keyCode == 13){
      $.mobile.changePage( "#topic", { transition: "slide", reverse: false } );

  }
})





//=====================================================

$('#my_task').on('click',function(){
$.mobile.changePage( "#mytask", { transition: "slide", reverse: false } );
})

$('#about_tasks').off('click')
$('#about_tasks').on('click',function(){
  var col = $('#setttings-tasks').val()

  var item = $('.task_item').length

  LOAD_MY_TASKS(item,(parseInt(col))+(parseInt(item)))
})






$(window).on('load', function(){ // When entering pagetwo
setTimeout(function(){
$('#list_dep').listview('refresh');
},300)

CHECK_BITRIX_ACCOUNT()

});



function CHECK_BITRIX_ACCOUNT(){
$.ajax({
  url:'check_bitrix_account/',
  success:function(data){

  },statusCode: {
    404: function(xhr) {
      $.mobile.changePage( "#bitrix", { transition: "pop", reverse: false } );
  }
}
})



$('#bitrix_btn').on('click',function(){
  if($('#bitrix_account').val()!=''){
    $.ajax({
      url:'create_bitrix_account/?ac='+$('#bitrix_account').val(),
      success:function(data){
          $.mobile.changePage( "#main_page", { transition: "pop", reverse: false } );
      },statusCode: {
        400: function(xhr) {
          //alert('Письмо не отправлено проверьте правильность данных')
          alert('Что-то пошло не так :(')
      }
    }
    })
  }else{
    alert("Заполните поле")
  }
})


}





$(document).on("pagebeforeshow",'#mytask', function(){ // When entering pagetwo

var col = $('#setttings-tasks').val()
var item = $('.task_item').length

LOADING()
$('#tasks_box').empty()
  LOAD_MY_TASKS(0,col)
});


function LOADING(){
  $('.loading').html('<div class="loader" style="text-align:center;width:100%;height:100%; background:#f9f9f9;position:absolute;top:0;left:0;z-index:99;">'+
          '<img style="width:100px;margin:20% 0;" src="https://hsto.org/getpro/habr/post_images/451/5dc/843/4515dc843bbdc21e00d96d4db2a42d87.gif"/></div>')
}




function LOAD_MY_TASKS(item,col){
//alert(item+'||||'+col)

  $.ajax({
    url:'my_task/?item='+item+'&col='+col,
    //async:false,
    dataType:'json',
    success:function(data){
    console.log(data.length,parseInt(item-1))
    if(data.length > 9){
      //  alert(1)
        $('#about_tasks').css({'display':''})
    }else{
        $('#about_tasks').css({'display':'none'})
    }

      $.each(data,function(k,v){

        var status,buttons ='';
        if(v['status']==0){
          status =''
          buttons = '<div init="'+v['id']+'" style="padding: 20px;margin:7px 10px;display: inline-block;" data-role="button" data-corners="true" data-inline="true" data-shadow="true" data-iconshadow="true" data-wrapperels="span" data-theme="e" data-icon="delete" class="delete_task ui-icon-delete ui-btn-icon-left ui-btn ui-shadow ui-btn-corner-all btn-danger"></div><div init="'+v['id']+'" style="padding: 20px;display: inline-block;"  data-role="button" data-corners="true" data-inline="true" data-shadow="true" data-iconshadow="true" data-wrapperels="span" data-theme="e" class="edit_task ui-icon-edit ui-btn-icon-left ui-btn ui-shadow ui-btn-corner-all"></div>'

        }else if(v['status']==10){
          status = 'darksalmon'
          buttons = ''

        }else if(v['status']==20){
          status = 'aquamarine'
          buttons = ''
          //docflow = ''
        }

        //alert(v.id)

        $('#tasks_box').append('<div style="background:'+status+'" data-role="collapsible" class="task_item">'+
                    '<h3><!--<span>'+v['date']+'</span>--> '+v['title']+'</h3>'+
                    '<p>'+v['description']+'<br/>'+buttons+
                    '<br><div data-init="'+v.id+'" class="btn btn-success docflow" >Документооборот</div>'+
                    '<a href="/number/number_view/?id='+v['id_number']+'&resolutions=100">'+v['id_page']+'</a></p>'+
                    '</div>')
      })

    $('#tasks_box').collapsibleset( "refresh" );

    $('.delete_task').off('click')
    $('.delete_task').on('click',function(){
        if(confirm('Удалить ?')==true){
          DELETE_TASK($(this),$(this).attr('init'))
        }
    })

    $('.edit_task').off('click')
    $('.edit_task').on('click',function(){
        EDIT_TASK($(this).attr('init'))
    })


    $('.docflow').click(function(){
        DOCFLOW($(this).attr('data-init'))
    })

    $('.loader').fadeOut(600)//.remove()


    },statusCode: {
      403: function(xhr) {
      ENTER()
    }
  }
  })


}










function DOCFLOW(id){
//  alert(id)

  $.ajax({
    url:'/doc/create_doc/?id='+id,
    //async:false,
    success:function(data){
      alert(data)
    }
  })

}





















function EDIT_TASK(id){

$(".date_change2").datepicker("destroy");
$.ajax({
  url:'get_param_task/?id='+id,
  success:function(data){
      console.log(data[0]['date'])




      $('.date_change2').datepicker({
         dateFormat: 'yy-mm-dd',
         defaultDate: data[0]['date'],
         onSelect: function(dateText){

            if(confirm('Поменять дату на '+dateText+' ?')==true){
              $.ajax({
                url:'change_date/?id='+id+'&date='+dateText,
                success:function(data){
                  //alert(data)
                },statusCode: {
                  406: function(xhr) {
                    alert("вы не можете менять дату у этой задачи она добавлена в планирование")
                }
                }
                })
              }

        }
      })

    $('#edit_task_count').val(data[0]['count'])
    $('#edit_task_description').val(data[0]['description'])
    $('#edit_task_title').val(data[0]['title'])
    CHANGE_PARAM_TASK(id)

    $.mobile.changePage( "#edittask", { transition: "pop", reverse: false } );

  }
})

}







function CHANGE_PARAM_TASK(id){
$('#edit_task_title,#edit_task_description,#edit_task_count').off('input')
$('#edit_task_title,#edit_task_description,#edit_task_count').on('input',function(){

//alert(id)

  $.ajax({
    url:'edit_param_task/',
    type:'POST',
    data:{
        'id':id,
        'title':$('#edit_task_title').val(),
        'description':$('#edit_task_description').val(),
        'count':$('#edit_task_count').val(),
    },success:function(data){
        console.log(data)
    },statusCode: {
      406: function(xhr) {
        alert("вы не можете редактировать эту задачу она добавлена в планирование")
    }
    }



})
})


}









function DELETE_TASK(elem,id){
console.log(elem)
    $.ajax({
      url:'delete_task/?id='+id,
      success:function(data){
      elem.parent().parent().css({'margin-left':'105%','transition':'all 1s','width': '100%'})
      setTimeout(function(){
        elem.parent().parent().remove()
      },1000)

      },statusCode: {
        406: function(xhr) {
          alert("вы не можете удалить эту задачу она добавлена в планирование")
      }
    }
    })
}


//=====================================================




    // $.mobile.changePage( "#auth", { transition: "pop", reverse: false } );


  			$( ".date_change" ).datepicker({
           defaultDate: null,
           dateFormat: 'yy-mm-dd',
           onSelect: function(dateText){
                var prevDate = $(this).data("prev")
                var curDate = dateText;
                datepicker = curDate;
                console.log(datepicker)

                $.mobile.changePage( "#title", { transition: "slide", reverse: false } );

          }
        }).find(".ui-state-active").removeClass("ui-state-active");

  		})
