$(function () {
    var month_olympic = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
    var month_normal = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
    var month_name = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];


    var holder = document.getElementById("days");

// console.log(cyear.innerHTML)


    var my_date = new Date();
    var my_year = my_date.getFullYear();
    var my_month = my_date.getMonth();
    // var my_day = my_date.getDate();

// console.log(my_year,my_month,my_day)

//获取某年某月第一天是星期几
    function dayStart(month, year) {
        var tmpDate = new Date(year, month, 1);
        // console.log(tmpDate)
        return (tmpDate.getDay());
    }

//计算某年是不是闰年，通过求年份除以4的余数即可
    function daysMonth(month, year) {
        var tmp = year % 4;
        if (tmp == 0) {
            return (month_olympic[month]);
        } else {
            return (month_normal[month]);
        }
    }

});



