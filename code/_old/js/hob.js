var $hob = {
    sectionSemaphor : true
}

function centerMain() {

   if ($(window).width() < 640 || $(window).height() < 580)
      $.fancybox({
         href : '#win-size-error',
         modal: true
      });
   else
      $.fancybox.close();

   $('#main').position({
					of : window,
					my: 'center',
					at: 'center',
   });
}

$(function () {
   
   centerMain();
   $(window).resize(function() {
		centerMain();
	});
	
	
	
	$('#content > div').not(":first").each(function() {
		$(this).hide();
	});
	
	$('#content > div').each(function() {
		$(this).addClass('section');
	});
	
   $('#main').fadeIn(1000);
    
   $.reject({
        reject : {
            msie : true
        },
        display : ['firefox', 'opera', 'safari', 'chrome', 'gcf'],  
        imagePath : 'art/browsers/',
        header : 'Sabía que su navegador está obsoleto',
        paragraph1 : 'Está usando un navegador desactualizado u obsoleto.', 
        paragraph2 : 'El navegador que está usando no soporta los estándares web de los últimos años, y está aproximadamente cinco años atrasado.  Se recomienda lo cambie, he aquí unas sugerencias:', 
        closeLink : 'Ignorar este mensaje',
        closeMessage : 'Puede ignorar este mensaje, he tomado horas y horas de trabajo para <del>garantizar</del> intentar que este sitio pueda verse con su navegador.'
    });

    $('#cv').click(function (event) {
        $.fancybox({
            href : 'http://curriculumdehugo.com.ar',
            width : '85%',
            height : '98%',
            type : 'iframe' 
        });
        event.preventDefault();
    });

    $('#pgp').click(function (event) {
        $.fancybox({
            href : 'gpg/hugoosvaldobarrera.asc',
            type : 'iframe' 
        });
        event.preventDefault();
    });
    
    $('.menuLink').click(function (event) {
        var ref = $($(this).attr('href'));
        if (!(ref.is(":visible"))) {
            ref.show('blind');
            $('.section:visible').not(ref).hide('blind');
        }
        event.preventDefault();
    });
});
