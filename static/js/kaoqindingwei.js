$(function () {
    function getTodayDays() {
        let dateTime = new Date();
        let year = dateTime.getFullYear();
        let month = dateTime.getMonth() + 1;
        let day = dateTime.getDate();
        let currentMonth, currentDay;
        if (month >= 10) {
            currentMonth = month + "-";
        } else {
            currentMonth = "0" + month + "-";
        }
        if (day >= 10) {
            currentDay = day;
        } else {
            currentDay = "0" + day;
        }
        return year + "-" + currentMonth + currentDay;
    }

    $('.date').text(getTodayDays());

    function shijian() {
        let date = new Date();
        let hour = date.getHours();
        let mm = date.getMinutes();
        let ss = date.getSeconds();
        let currentMm;
        if (mm >= 10) {
            currentMm = mm;
        } else {
            currentMm = '0' + mm;
        }
        let currentSs;
        if (ss >= 10) {
            currentSs = ss;
        } else {
            currentSs = '0' + ss;
        }
        let time = hour + ':' + currentMm + ':' + currentSs;
        return time;
    }

    //初始化高德地图函数
    function setMap() {
        var map = new AMap.Map("container", {
            resizeEnable: true
        });
        map.plugin('AMap.Geolocation', function () {
            geolocation = new AMap.Geolocation({
                enableHighAccuracy: true, //是否使用高精度定位，默认:true
                timeout: 10000, //超过10秒后停止定位，默认：无穷大
                buttonOffset: new AMap.Pixel(10, 20), //定位按钮与设置的停靠位置的偏移量，默认：Pixel(10, 20)
                zoomToAccuracy: true, //定位成功后调整地图视野范围使定位位置及精度范围视野内可见，默认：false
                buttonPosition: 'RB'
            });
            map.addControl(geolocation);
            geolocation.getCurrentPosition();
            AMap.event.addListener(geolocation, 'complete', onComplete); //返回定位信息
            AMap.event.addListener(geolocation, 'error', onError); //返回定位出错信息
        });

        //解析定位结果
        function onComplete(data) {
            // console.log(data);
            // console.log(data.formattedAddress);
            $('#shangban').text(data.formattedAddress);
            // console.log('纬度：' + data.position.getLat());
            // console.log('经度：' + data.position.getLng());
        }

        // 解析定位错误信息
        function onError(data) {
         }

    }

    setMap();

    function setMap1() {
        var map = new AMap.Map("container", {
            resizeEnable: true
        });
        map.plugin('AMap.Geolocation', function () {
            geolocation = new AMap.Geolocation({
                enableHighAccuracy: true, //是否使用高精度定位，默认:true
                timeout: 10000, //超过10秒后停止定位，默认：无穷大
                buttonOffset: new AMap.Pixel(10, 20), //定位按钮与设置的停靠位置的偏移量，默认：Pixel(10, 20)
                zoomToAccuracy: true, //定位成功后调整地图视野范围使定位位置及精度范围视野内可见，默认：false
                buttonPosition: 'RB'
            });
            map.addControl(geolocation);
            geolocation.getCurrentPosition();
            AMap.event.addListener(geolocation, 'complete', onComplete); //返回定位信息
            AMap.event.addListener(geolocation, 'error', onError); //返回定位出错信息
        });

        //解析定位结果
        function onComplete(data) {
            // console.log(data);
            // console.log(data.formattedAddress);
            $('#xiaban').text(data.formattedAddress);
            // console.log('纬度：' + data.position.getLat());
            // console.log('经度：' + data.position.getLng());
        }

        // 解析定位错误信息
        function onError(data) {
         }

    }

    //上班单匡
    // var mobileSelect1 = new MobileSelect({
    //     trigger: '#dka',
    //     title: '',
    //     wheels: [
    //         {data: ['年假', '病假', '事假', '调休', '产假', '剖产假']}
    //     ],
    //     position: [2] //初始化定位
    // });
    //
    // console.log(mobileSelect1.wheelsData = {data: ['年', '月', '日', '牛', '产假', '剖产假']});

    $('#check').click(function () {

        $('.shangbantime').text(shijian());
        $('.dot')[0].style.backgroundColor = 'green';
        $('#shanbanarea').removeClass('show');
        $('#xiabanareatitle').removeClass('show');
        $(this).addClass('show');
        $('#check2').removeClass("show");
        $('#xiabanweizhi').removeClass("show");

        setMap1();

        $.ajax({
            type: 'POST',
            url: '/mobileattendwork/',
            data: {
                user_id: window.location.href.split("=")[1],
                attend_type: $('#attendtypework').text(),
                starttime: $(".shangbantime").text(),
                attend_place: $('#shangban').text()
            },
            success: function (data) {
                if (data.status === 200) {
                    alert(data.msg);
                } else {
                    alert(data.msg);
                }
            }
        })
    });

    $('#check2').click(function () {

        $('.xiabantime').text(shijian());
        $('.dot')[1].style.backgroundColor = 'green';
        $(this).text('完成打卡');

        $.ajax({
            type: 'POST',
            url: '/mobileattendworkxiaban/',
            data: {
                user_id: window.location.href.split("=")[1],
                endWorkTime: $('.xiabantime').text(),
                attendOutPlace: $('#xiaban').text()
            },
            success: function (data) {
                if (data.status === 200) {
                    alert(data.msg);
                } else {
                    alert(data.msg);
                }
            }
        })
    });


    $('#dka').click(function () {
        $('.msg__overlay').css('opacity',1).css('display','block');
        $('.msg_wrap').css('display','block');
    });

    $('.ul__style li').click(function(){
        $('.msg__overlay').css('opacity',0).css('display','none');
        $('.msg_wrap').css('display','none');
    })

});

var user_msg = new Vue({
    el: "#main_text",
    data() {
        return {
            userImg: '',
            userName: ''
        }
    },
    mounted: function () {
        this.getuserMsg();
    },
    methods: {
        getuserMsg: function () {
            let _self = this;
            $.ajax({
                type: 'GET',
                url: '/mobileclockin/',
                data: {
                    user_id: window.location.href.split("=")[1],
                },
                success: function (data) {
                    _self.userName = data.user_name;
                    _self.userImg = data.user_img;
                }
            })
        }
    }
});


