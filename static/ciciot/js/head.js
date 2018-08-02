$(function () {
    $(".select_box").click(function (event) {
        event.stopPropagation();
        $(this).find(".option").toggle();
        $(this).parent().siblings().find(".option").hide();
    });
    $(document).click(function (event) {
        var eo = $(event.target);
        if ($(".select_box").is(":visible") && eo.attr("class") != "option" && !eo.parent(".option").length)
            $('.option').hide();
    });
    $(".option li").click(function () {
        var check_value = $(this).text();
        var zlValue = $('.option li:eq(1)').html();
        var bqValue = $('.option li:eq(2)').html();
        $(this).parent().siblings(".select_txt").text(check_value);
        $("#select_value").val(check_value);
    });
})
