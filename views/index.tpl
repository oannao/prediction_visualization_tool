<!DOCTYPE html>
<head>
<meta http-equiv="content-type" content="text/html; charset=utf-8"/>
<title>　{{ title }} </title>
<link rel="stylesheet" type="text/css" href="/css/bootstrap.min.css">
<link rel="stylesheet" type="text/css" href="/css/bootstrap-responsive.min.css">
<link rel="stylesheet" type="text/css" href="/css/style.css">
<!--[if lt IE 9]>
<script type="text/javascript">
alert("Your browser does not support the canvas tag.");
</script>
<![endif]-->
<script src="/js/jquery.min.js" type="text/javascript"></script>
<script src="/js/jquery.leanModal.min.js" type="text/javascript"></script>
<script src="/js/main.js" type="text/javascript"></script>
</head>
<body>

<div class="navbar">
  <div class="navbar-inner">
    <div class="container">
 
      <!-- .btn-navbar is used as the toggle for collapsed navbar content -->
      <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </a>
 
      <!-- Be sure to leave the brand out there if you want it shown -->
      <a class="brand" href="#">Solar Radiation Predictor</a>
 
      <!-- Everything you want hidden at 940px or less, place within here -->
      <div class="nav-collapse collapse">
        <!-- .nav, .navbar-search, .navbar-form, etc -->
      </div>
 
    </div>
  </div>
</div>

<div class="container">
	<div class="options row">
		<div class="cities span4">
			<p><strong>都市</strong><br>
				<div class="row">
					<div class="span1">
						<label class="radio"><input type="radio" name="city" id="city1" value="sapporo">札幌</label>
						<label class="radio"><input type="radio" name="city" id="city3" value="tokyo" checked>東京</label>
						<label class="radio"><input type="radio" name="city" id="city5" value="toyama">富山</label>
						<label class="radio"><input type="radio" name="city" id="city7" value="hiroshima">広島</label>
						<label class="radio"><input type="radio" name="city" id="city9" value="fukuoka">福岡</label>
					</div>
					<div class="span1">
						<label class="radio"><input type="radio" name="city" id="city2" value="sendai">仙台</label>
						<label class="radio"><input type="radio" name="city" id="city4" value="nagoya">名古屋</label>
						<label class="radio"><input type="radio" name="city" id="city6" value="osaka">大阪</label>
						<label class="radio"><input type="radio" name="city" id="city8" value="matsuyama">松山</label>
					</div>
				</div>
			</p>
		</div>

		<div class="times span6">
			<div class="row">
				<div class="span2">
					<p><strong>学習期間</strong><br>
						<input class="input-mini" type="text" id="testtest" placeholder="Type training time…">days
					</p>
				</div>
				<div class="span2">
					<p><strong>時系列の取り扱い</strong><br>
						<label class="radio"><input type="radio" name="timeseries" id="timeseries0" value="0">なし</label>
						<label class="radio"><input type="radio" name="timeseries" id="timeseries1" value="1" checked>1時間</label>
						<label class="radio"><input type="radio" name="timeseries" id="timeseries2" value="2">1,2時間</label>
						<label class="radio"><input type="radio" name="timeseries" id="timeseries3" value="3">1,2,3時間</label>
					</p>
				</div>
				<div class="span2">
					<p><strong>予測領域</strong><br>
						<label class="radio"><input type="radio" name="field" id="field0" value="0">地点</label>
						<label class="radio"><input type="radio" name="field" id="field1" value="5">5km x 5km</label>
						<label class="radio"><input type="radio" name="field" id="field1" value="20" checked>20km x 20km</label>
						<label class="radio"><input type="radio" name="field" id="field1" value="40">40km x 40km</label>
					</p>
				</div>
			</div>
		</div>

		<button class="btn btn-primary span2" id="set" type="button">Set Parameter</button>
	</div>

	<div id="chart"></div>

</div>
<script src="/js/highstock.js" type="text/javascript"></script>
<script src="/js/exporting.js" type="text/javascript"></script>
</body>
</html>
