$(function () {
	$('#loading').fadeOut(
	    function() {
	        $('#main').fadeIn();
	    }
	);

    $("#accordion").accordion({
        collapsible: true,
        active: false,
        autoHeight: false,
        clearStyle: true
    });

	$.jqplot.config.enablePlugins = true;

	line1 = [["Java", 8.5], ["Web", 8.8], ["Python", 7.2], ["C", 4.0]];
	plot3 = $.jqplot('languagesChart', [line1], {
		seriesDefaults : {
			renderer : $.jqplot.BarRenderer ,
			label:'Mi afinidad con distintos lenguajes de programación'
		},
		height : 320,
		width : 600,
//		series : [{
//			pointLabels : {
//				labels : ['fourteen', 'thirty two', 'fourty one', 'fourty four', 'fourty']
//			}
//			//,color: '#ff0000'
//		}],
		axes : {
			xaxis : {
				renderer : $.jqplot.CategoryAxisRenderer
			},
			yaxis : {
				min : 0,
				max : 10,
				padMax : 1.3
			}
		},
		legend: {
			show : true,
			location : 'ne'
		},
		grid: {
			background: '#36332D'
		},
		highlighter : {
			show : true,
            showMarker : false,
            showTooltip : true,
            tooltipAxes : 'both',
            useAxesFormatters : true,
            sizeAdjust: 7.5
      },
      cursor: {
        show: false,
         style : 'crosshair'
      }
   });

   line1 = [
		[2011, 24], [2012, 25], [2013, 26], [2014, 27]
   ];
	line2=[
		[1987,  0], [1988,  1], [1989,  2], [1990,  3], [1991,  4], [1992,  5], [1993,  6],
		[1994,  7], [1995,  8], [1996,  9], [1997, 10], [1998, 11], [1999, 12], [2000, 13],
		[2001, 14], [2002, 15], [2003, 16], [2004, 17], [2005, 18], [2006, 19], [2007, 20],
		[2008, 21], [2009, 22], [2010, 23], [2011, 24]
	];

	plot1 = $.jqplot('ageChart', [line1, line2], {
		series: [
			{label:'Valores Inferidos'},
			{label:'Mediciones Reales'}
		],
		seriesColors: [
			"#EAA228", "#4BB2C5"
		],
		height : 320,
		width : 600,
		axes:{
			xaxis:{
				renderer:$.jqplot.LinearAxisRenderer,
				min: 1987,
				max: 2014,
				tickOptions:{ formatString:'%4.0f' }
			},
			yaxis : {
				min : 0,
				max : 27,
				padMax : 1.3,
				tickOptions:{ formatString:'%2.0f' }
			}
		},
		legend: {
			show : true,
			location : 'se'
		},
		grid: {
			background: '#36332D'
		},
		highlighter: {
			show: true,
			sizeAdjust: 7.5
		},
		cursor: {show: false}
	});

	$('#accordion').bind('accordionchange', function (event, ui) {
		ui.newContent.css('overflow' , 'auto');
		var index = $(this).find("h2").index ( ui.newHeader[0] );
		if (index == 1)
			plot1.replot();
		if (index == 3)
			plot3.replot();
		if (index == 6)
			$('#cc').fadeIn();
	});

	$('.ui-accordion').bind('accordionchangestart', function(event, ui) {
		ui.newContent.css('overflow' , 'hidden');
		var index = $(this).find("h2").index ( ui.oldHeader[0] );
		if (index == 6)
			$('#cc').fadeOut('fast');
	});

});
