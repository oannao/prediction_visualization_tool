

var ids = [];
var debug=false;

var form, id;
var url_si, param_si;

var chart;
var timestamp;

var siIndex = 0;
var city = "tokyo";
var traintime = "30";
var timeseries = "1";


$(document).ready(function() {

	// textbox
	$("#testtest").val(traintime);

	Highcharts.setOptions({
		global: {
			useUTC: false
		}
	});

	chart = new Highcharts.Chart({
		chart: {
			renderTo: 'chart',
			type: 'area',
			events: {
				load: requestData
			}
		},
		title: {
			text: 'Solar Radiation Prediction Data'
		},
		xAxis: {
			type: 'datetime',
			dateTimeLabelFormats: { // don't display the dummy year
				month: '%e. %b',
				year: '%b'
			}
		},
		yAxis: {
			title: {
				text: 'Value'
			},
			plotLines: [{
				value: 0,
				width: 1,
				color: '#808080'
			}]
		},
		legend: {
			enabled: false
		},
		exporting: {
			enabled: false
		},
		series: [{
				name: 'Real data',
				data: []
			},{
				name: 'Lasso Prediction',
				type: 'spline',
				data: []
		}]
	});
});

/**
 * Request data from the server, add it to the graph and set a timeout 
 * to request again
 */
function requestData() {
	param_si = '?siIndex=' + siIndex; // + "&callback=?";
	url_si = "./get/all"+param_si;
		$.ajax({
			type: 'GET',
			url: url_si,
			dataType: 'json',
			success: function(point) {
				var series = chart.series,
				shift = series[0].data.length > 50; // shift if the series is longer than 50
				if (point.length>0) {
					for (var i = 0; i < point.length; i++) {
						// add the point
						timestamp = new Date(point[i]["timestamp"]).getTime()
						chart.series[0].addPoint([timestamp, point[i]["real"]], false, shift);
						chart.series[1].addPoint([timestamp, Math.max(point[i]["lasso"],0)], true, shift);
					};
				};

				// update siIndex
				siIndex = siIndex + 1;
				
				// call it again after two seconds
				setTimeout(requestData, 2000);    
			},
			cache: false
		});
}

$(function () {
	$("#set").click(function () {
		city = $("input:radio[name='city']:checked").val();
		//traintime = $("input:radio[name='traintime']:checked").val();
		traintime = $("#testtest").val();
		timeseries = $("input:radio[name='timeseries']:checked").val();
		param_si = '?city=' + city + '&traintime=' + traintime + '&timeseries=' + timeseries;
		url_si = "./set/param" + param_si;
			$.ajax({
				type: 'GET',
				url: url_si,
				dataType: 'json',
				success: function(json) {
					siIndex = 0;
					chart.series[0].update({data: []});
					chart.series[1].update({data: []});
				},
				cache: false
			});
	});

	$(".reset").click(function () {
		$.getJSON("./restart", function (json) {
			location.reload();
		});
	});
});