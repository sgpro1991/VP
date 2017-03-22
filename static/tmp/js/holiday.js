function CLEAR_CANVAS(){

  //$('.droped').fadeOut(600)
  //$('.papper').fadeOut(600)
  var sec = 3;
  setTimeout(function(){

  $('.droped').each(function(){
      //$(this).css({'margin-top':(Math.random()*(1 - 1000) + 200)+'px','position':'relative','margin-left':(Math.random()*(1 - 1000) + 200) +'px','transform':'rotateZ('+(Math.random()*(1 - 1000) + 200)+'deg)','transition':'all '+sec+'s'})
    })
    $('.pashal_text').css({'transition':'all 0.3s'})
  },800)

  setInterval(function(){
        var a_color = ['red','green','coral','thistle','yellowgreen','turquoise','sienna','pink']
        $('.pashal_text').css({'color':a_color[Math.floor(Math.random() * a_color.length)]})
  },300)


$('.btn-pashal').click(function(){


  $('.btn-pashal2').fadeIn()
  var b_color = ['lightblue','violet','gold','yellowgreen','turquoise','lightcyan','pink','plum','aliceblue']

  $('.draw_div').each(function(){
    $(this).css({'margin-top':(Math.random()*(1 - 1000) + 200)+'px','background':b_color[Math.floor(Math.random() * b_color.length)],'margin-left':(Math.random()*(1 - 500) + 200) +'px','transition':'all '+sec+'s'})

  })

  $('.droped').each(function(){
    $(this).css({'margin-top':(Math.random()*(1 - 1000) + 200)+'px','margin-left':(Math.random()*(1 - 1000) + 200) +'px','transform':'rotateZ('+(Math.random()*(1 - 1000) + 200)+'deg)','transition':'all '+sec+'s'})
  })

})



// reset
$('.btn-pashal2').click(function(){

  $('.pashal_box').remove()

  $('.draw_div').each(function(){
    $(this).css({'margin-top':'','margin-left':'','transform':'','background':''})
  })

  $('.droped').each(function(){
    $(this).css({'margin-top':'','position':'absolute','margin-left':'','transform':''})
  })


    setTimeout(function(){
      $('.draw_div').each(function(){
        $(this).css({'transition':''})
      })
      $('.droped').each(function(){
        $(this).css({'transition':''})
      })
    },3000)
  })

}
CLEAR_CANVAS()
