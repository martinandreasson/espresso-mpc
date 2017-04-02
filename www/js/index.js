var curtemp = new TimeSeries();
var settemp = new TimeSeries();
var control_signal = new TimeSeries();
var lastreqdone = 1;
var timeout;

function refreshinputs() {
  $.getJSON({
    url: "/allstats",
    timeout: 500,
    success: function ( resp ) {
      $("#inputSetTemp").val( resp.settemp );
      $("#inputSetSteamTemp").val( resp.setsteamtemp );
      $("#inputgetclienttime").val( resp.setsteamtemp );
      $("#inputTimerOnMo").val( resp.TimerOnMo );
      $("#inputTimerOffMo").val( resp.TimerOffMo );
      $("#inputTimerOnTu").val( resp.TimerOnTu );
      $("#inputTimerOffTu").val( resp.TimerOffTu );
      $("#inputTimerOnWe").val( resp.TimerOnWe );
      $("#inputTimerOffWe").val( resp.TimerOffWe );
      $("#inputTimerOnTh").val( resp.TimerOnTh );
      $("#inputTimerOffTh").val( resp.TimerOffTh );
      $("#inputTimerOnFr").val( resp.TimerOnFr );
      $("#inputTimerOffFr").val( resp.TimerOffFr );
      $("#inputTimerOnSa").val( resp.TimerOnSa );
      $("#inputTimerOffSa").val( resp.TimerOffSa );
      $("#inputTimerOnSu").val( resp.TimerOnSu );
      $("#inputTimerOffSu").val( resp.TimerOffSu );
    }
  });
}

function onresize() {
    var h;
    if ($(window).height()*.50 > 450 ) {
      h = 450;
    } else {
      h = $(window).height()*.50;
    }

    $("#chart").attr("width", $("#fullrow").width()-30);
    $("#chart").attr("height", h);
    $("#controllerchart").attr("width", $("#fullrow").width()-30);
    $("#controllerchart").attr("height", h);

    if ($(document).width() < 600) {
      $("#toggleadv").html("Adv");
    } else {
      $("#toggleadv").html("Advanced");
    }
}

function getclienttime(){
 var date = new Date();
 var timeinms = date.getTime();
  $.post(
    "/getclienttime",
    { getclienttime: timeinms }
  );
};

$(document).ready(function(){

  onresize();
  $(window).resize(onresize);

  createTimeline();

  $(".adv").hide();
  $("#toggleadv").click(function(){
    $(".adv").toggle();
  });

  $(".timer").hide();
  $("#toggletimer").click(function(){
    $(".timer").toggle();
  });

  refreshinputs();

  getclienttime();

  $("#inputSetTemp").change(function(){
    $.post(
      "/settemp",
      { settemp: $("#inputSetTemp").val() }
    );
  });

  $("#inputSetSteamTemp").change(function(){
    $.post(
      "/setsteamtemp",
      { setsteamtemp: $("#inputSetSteamTemp").val() }
    );
  });

  $("#inputTimerOnMo").change(function(){
    $.post(
      "/TimerOnMo",
      { TimerOnMo: $("#inputTimerOnMo").val() }
    );
  });

  $("#inputTimerOffMo").change(function(){
    $.post(
      "/TimerOffMo",
      { TimerOffMo: $("#inputTimerOffMo").val() }
    );
  });

  $("#inputTimerOnTu").change(function(){
    $.post(
      "/TimerOnTu",
      { TimerOnTu: $("#inputTimerOnTu").val() }
    );
  });

  $("#inputTimerOffTu").change(function(){
    $.post(
      "/TimerOffTu",
      { TimerOffTu: $("#inputTimerOffTu").val() }
    );
  });

  $("#inputTimerOnWe").change(function(){
    $.post(
      "/TimerOnWe",
      { TimerOnWe: $("#inputTimerOnWe").val() }
    );
  });

  $("#inputTimerOffWe").change(function(){
    $.post(
      "/TimerOffWe",
      { TimerOffWe: $("#inputTimerOffWe").val() }
    );
  });

  $("#inputTimerOnTh").change(function(){
    $.post(
      "/TimerOnTh",
      { TimerOnTh: $("#inputTimerOnTh").val() }
    );
  });

  $("#inputTimerOffTh").change(function(){
    $.post(
      "/TimerOffTh",
      { TimerOffTh: $("#inputTimerOffTh").val() }
    );
  });

  $("#inputTimerOnFr").change(function(){
    $.post(
      "/TimerOnFr",
      { TimerOnFr: $("#inputTimerOnFr").val() }
    );
  });

  $("#inputTimerOffFr").change(function(){
    $.post(
      "/TimerOffFr",
      { TimerOffFr: $("#inputTimerOffFr").val() }
    );
  });

  $("#inputTimerOnSa").change(function(){
    $.post(
      "/TimerOnSa",
      { TimerOnSa: $("#inputTimerOnSa").val() }
    );
  });

  $("#inputTimerOffSa").change(function(){
    $.post(
      "/TimerOffSa",
      { TimerOffSa: $("#inputTimerOffSa").val() }
    );
  });

  $("#inputTimerOnSu").change(function(){
    $.post(
      "/TimerOnSu",
      { TimerOnSu: $("#inputTimerOnSu").val() }
    );
  });

  $("#inputTimerOffSu").change(function(){
    $.post(
      "/TimerOffSu",
      { TimerOffSu: $("#inputTimerOffSu").val() }
    );
  });

});

setInterval(function() {
  if (lastreqdone == 1) {
    $.getJSON({
      url: "/allstats",
      timeout: 2000,
      success: function ( resp ) {
        curtemp.append(new Date().getTime(), resp.tempc);
        settemp.append(new Date().getTime(), resp.settemp);
        control_signal.append(new Date().getTime(), resp.control_signal);
        $("#curtemp").html(resp.tempc.toFixed(2));
        $("#control_signal").html(resp.control_signal.toFixed(2));
      },
      complete: function () {
        lastreqdone = 1;
      }
    });
    lastreqdone = 0;
  }
}, 500);

function createTimeline() {
  var chart = new SmoothieChart({millisPerPixel:500,grid:{sharpLines:true,millisPerLine:20000,verticalSections:15},maxValue:160,minValue:10});
  chart.addTimeSeries(settemp, {lineWidth:2,strokeStyle:'#ffff00'});
  chart.addTimeSeries(curtemp, {lineWidth:2,strokeStyle:'#ff0000'});
  chart.streamTo(document.getElementById("chart"), 500);

  var controllerchart = new SmoothieChart({millisPerPixel:500,grid:{sharpLines:true,millisPerLine:20000,verticalSections:10},maxValue:100,minValue:0});
  controllerchart.addTimeSeries(control_signal, {lineWidth:2,strokeStyle:'#ff00ff'});
  controllerchart.streamTo(document.getElementById("controllerchart"), 500);
}
