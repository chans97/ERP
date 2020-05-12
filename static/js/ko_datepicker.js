(function (factory) {
    if (typeof define === "function" && define.amd) {
        define(["../widgets/datepicker"], factory);
    } else {
        factory(jQuery.datepicker);
    }
}(function (datepicker) {
    datepicker.regional.ko = {
        closeText: "닫기",
        prevText: "이전달",
        nextText: "다음달",
        currentText: "오늘",
        monthNames: ["1월", "2월", "3월", "4월", "5월", "6월",
            "7월", "8월", "9월", "10월", "11월", "12월"],
        monthNamesShort: ["1월", "2월", "3월", "4월", "5월", "6월",
            "7월", "8월", "9월", "10월", "11월", "12월"],
        dayNames: ["일요일", "월요일", "화요일", "수요일", "목요일", "금요일", "토요일"],
        dayNamesShort: ["일", "월", "화", "수", "목", "금", "토"],
        dayNamesMin: ["일", "월", "화", "수", "목", "금", "토"],
        weekHeader: "주",
        dateFormat: "yy-m-d",
        firstDay: 0,
        isRTL: false,
        showMonthAfterYear: false,
        yearSuffix: "년"
    };
    datepicker.setDefaults(datepicker.regional.ko);
    return datepicker.regional.ko;
}));

$(function () {
    $("#date2").datepicker({
        showOn: "button",
        buttonImage: "{% static 'img/btn_date.png'%}",
        buttonImageOnly: true,
    }); $.datepicker.setDefaults($.datepicker.regional['ko']);         //default셋팅
    $("#txt_prodStart").datepicker();
    $('img.ui-datepicker-trigger').css({ 'margin-right': '5px', 'height': '18px' });  //아이콘(icon) 위치
    $('img.ui-datepicker-trigger').attr('align', 'absmiddle');
    $('#date2').datepicker('setDate', 'today');
});
$(function () {
    $("#date3").datepicker({
        showOn: "button",
        buttonImage: "{% static 'img/btn_date.png'%}",
        buttonImageOnly: true,
    }); $.datepicker.setDefaults($.datepicker.regional['ko']);         //default셋팅
    $("#txt_prodStart").datepicker();
    $('img.ui-datepicker-trigger').css({ 'margin-right': '5px', 'height': '18px' });  //아이콘(icon) 위치
    $('img.ui-datepicker-trigger').attr('align', 'absmiddle');
});
$(function () {
    $("#date4").datepicker({
        showOn: "button",
        buttonImage: "{% static 'img/btn_date.png'%}",
        buttonImageOnly: true,
    }); $.datepicker.setDefaults($.datepicker.regional['ko']);         //default셋팅
    $("#txt_prodStart").datepicker();
    $('img.ui-datepicker-trigger').css({ 'margin-right': '5px', 'height': '18px' });  //아이콘(icon) 위치
    $('img.ui-datepicker-trigger').attr('align', 'absmiddle');
});
