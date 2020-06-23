var dateTime = new Date();
var todayDate = dateTime.getFullYear() + '-' + (dateTime.getMonth() + 1) + '-' + dateTime.getDate();
var nowweektype = 0;
var swiper = new Swiper('.swiper-container', {
    autoplay: {
        delay: 5000,
    },
    pagination: {
        el: '.swiper-pagination',
        clickable: true,
    },
});

var content_div = new Vue({
    el: '#content_div',
    data: {
        classList: [],
        studentList: [],
        currentIndex: null,
        page_code: null,
        pieData: [],
        illegalList: [],
        list: [],
        todayAttendList: [],
        departAttendDetailList: [],
        visitList: [],
        slideList: [],
        employList: [],
        filterDate: todayDate,
        indexImg: {'flag': null},

        // 考勤圈
        clist: [],
        losslist: [],
        rightlist: [],
        laterlist: [],
        nowdate: todayDate,
        blueoption: null,
        right_attend_chart: null,
        yellowoption: null,
        wrong_attend_chart: null,
        redoption: null,
        loss_attend_chart: null,
        start: 0,
        end: 5,
        warningrecordsLists: [],
        focus_depart_id:''
    },
    beforeDestroy: function() {
        clearInterval(this.timer);
    },
    watch: {
        filterDate: function (newVal, oldVal) {
            this.slideList = []

            _self.getSlideList()

            if (newVal != todayDate) {
                clearInterval(this.freshVist)
                clearInterval(this.freshAttend)
                clearInterval(this.frshPie)
                clearInterval(this.slide)
            } else {
            }
        }
    },
    computed: {
        newSlideList: function() {
            return this.slideList.slice(this.start, this.end)
        }
    },
    mounted: function () {
        // 定时刷新访客列表
        this.freshVist = setInterval(this.getVisitList, 1000 * 3);
        this.freshAttend = setInterval(this.getAttendList, 1000 * 3);
        this.frshPie = setInterval(this.getallattendData, 1000 * 3);    // 15 秒钟刷新一次饼状图
        this.slide = setInterval(this.getSlideList, 1000 * 3);
        this.warning = setInterval(this.getWarningRecords, 1000 * 3);
        this.newdata = setInterval(this.getnewdata, 1000 * 3);
        this.attendetails = setInterval(this.getAttendDetail(this.focus_depart_id ), 1000 * 3);
        setInterval("window.location.reload()", 1000 * 60 * 60);  // 每小时刷新一次页面，缓解页面压力

        this.getallcalData();
        this.getallattendData();    // 饼状图


        // 获取今日考勤信息列表
        this.getAttendList();

        // // 获取某个部门考勤详情
        // this.getAttendDetail();

        // 获取访客列表
        this.getVisitList();

        // 获取滑动列表
        this.getSlideList();
        //获取异常人员警示
        this.getWarningRecords();
        this.getnewdata();

        var _self = this;

    },
    methods: {

        previousData: function () {
            if (this.start <= 0) {
                return
            }
            this.start = this.start - 1
            this.end = this.end - 1
        },

        nextData: function () {
            if (this.end >= this.slideList.length) {
                return
            }
            this.start = this.start + 1
            this.end = this.end + 1
        },

        // 获取当月每一天的日历
        getallcalData: function () {
            var _self = this;
            $.ajax({
                type: 'GET',
                url: '/databoard/get_calendar_list/',
                success: function (data) {
                    _self.clist = data.list.lastlist;
                    $('#calendar').calendar({
                        width: document.body.clientWidth * 0.25 - 80,
                        height: '70%',
                        data: _self.clist,
                        onSelected: function (view, date, data) {
                            _self.nowdate = date.getFullYear() + '-' + (date.getMonth() + 1) + '-' + date.getDate()
                            _self.filterDate = _self.nowdate
                            _self.getAttendList(_self.filterDate)
                            _self.getVisitList(_self.filterDate)
                            _self.getWarningRecords(_self.filterDate)
                            _self.getallattendData()

                        }
                    });
                }
            });
        },

        get_employ_list: function(id,datea){
            var frameSrc = "/databoard/userdetailshowpage/?user_id=" + id +"&date="+datea;
            $("#NoPermissioniframe").attr("src", frameSrc);
            $('#NoPermissionModal').modal({ show: true, backdrop: 'static' });

        },
        getworkerattendlist: function() {
            _self = this
            $.ajax({
                type: 'GET',
                url: '/databoard/getworkerattendlist/',
                success: function (data) {
                    _self.employList = data;
                }
            });
        },

        fullUrl: function(value) {
            if (!value) {
                return value
            }
            return value
        },
        getSlideList: function() {
            _self = this
            $.ajax({
                type: 'GET',
                url: '/databoard/get_slide_info/',
                data: {'filter_date': _self.filterDate},
                success: function (data) {
                    _self.slideList = data;
                }
            });
        },
        getAttendList: function() {
            _self = this
            $.ajax({
                type: 'GET',
                url: '/databoard/get_attend_list/',
                data: {'filter_date': _self.filterDate},
                success: function (data) {
                    _self.todayAttendList = data;
                    if((_self.focus_depart_id==''||_self.focus_depart_id=='undefined')&&data.length>0){
                        _self.focus_depart_id=data[0].depart_id;
                        _self.getAttendDetail(_self.focus_depart_id);
                    }

                }
            });
        },
        getAttendDetail: function(depart_id) {

            _self = this;
            _self.focus_depart_id =depart_id;
            $.ajax({
                type: 'GET',
                url: '/databoard/get_depart_attend_detail/',
                data: {'depart_id': depart_id, 'filter_date': _self.filterDate},
                dataType: "json",
                success: function (data) {
                    if (data.status) {
                        _self.departAttendDetailList = data.result;
                    }
                }
            });
        },
        getVisitList: function() {
            _self = this;
            $.ajax({
                type: 'GET',
                url: '/databoard/get_visit_list/',
                data: {'filter_date': _self.filterDate},
                dataType: "json",
                success: function (data) {
                    if (data.status) {
                        _self.visitList = data.result;
                    }
                }
            });
        },
        getWarningRecords: function(){
            _self = this;
            $.ajax({
                type:'GET',
                url:'/databoard/getwarningrecords/',
                data: {'filter_date': _self.filterDate},
                success:function (resp) {
                    _self.warningrecordsLists = resp.lists;
                }
            })
        },
        getnewdata: function(){
            _self = this;
            $.ajax({
                type:'GET',
                url:'/databoard/getnewdata/',
                success:function (resp) {
                    document.getElementById('now_num').innerText= resp.all_count + '人次'
                    document.getElementById('todayattend').innerText = resp.attendcord + '/'+resp.all_num+'人';
                    document.getElementById('todaytem').innerText = resp.possen_count + '例'
                }
            })
        },
        replaceIp: function (value) {
            if (!value) {
                return value
            }
            if (/((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d))))/.test(value)) {
                return value.replace(/192.168.10.10/, '192.168.10.10')
            }
            return '/static/images/placeholder/' + Math.ceil(Math.random() * 9).toString() + '.jpg';
        },
        gettodaydate: function () {
            day = new Date();
            month = day.getMonth() + 1;
            days = day.getDate();
            if (month >= 10) {
                currentDate = month + "-";
            } else {
                currentDate = '0' + month + "-";
            }
            if (days >= 10) {
                currentDate += days
            } else {
                currentDate += "0" + days;
            }
            return currentDate
        },


        // 考勤圈的饼状图
        getallattendData: function () {
            var _self = this;
            $.ajax({
                type: 'GET',
                url: '/databoard/get_all_attend_data/',
                data: {nowdate: _self.nowdate},
                success: function (data) {
                    _self.losslist = data;
                    _self.laterlist = data;
                    _self.rightlist = data;
                    if (_self.losslist.length > 0) {
                        _self.right_attend_chart = echarts.init(document.getElementById('right_attend_chart'));
                        _self.wrong_attend_chart = echarts.init(document.getElementById('wrong_attend_chart'));
                        _self.loss_attend_chart = echarts.init(document.getElementById('loss_attend_chart'));
                        _self.blueoption = {
                            title: {
                                text: '体温正常\n\n' + _self.rightlist[0] + '%',
                                x: 'center',
                                y: 'center',
                                textStyle: {
                                    fontWeight: 'normal',
                                    color: '#ffffff',
                                    fontSize: '14'
                                }
                            },
                            color: ['rgba(176, 212, 251, 1)'],

                            series: [{
                                name: 'Line 1',
                                type: 'pie',
                                clockWise: true,
                                radius: ['70%', '78%'],
                                itemStyle: {
                                    normal: {
                                        label: {
                                            show: false
                                        },
                                        labelLine: {
                                            show: false
                                        }
                                    }
                                },
                                hoverAnimation: false,
                                data: [{
                                    value: _self.rightlist[0],
                                    name: '01',
                                    itemStyle: {
                                        normal: {
                                            color: 'rgba(9,210,5,0.81)',
                                            label: {
                                                show: false
                                            },
                                            labelLine: {
                                                show: false
                                            }
                                        }
                                    }
                                }, {
                                    name: '02',
                                    value: _self.rightlist[1] + _self.rightlist[2],
                                    itemStyle: {
                                        normal: {
                                            color: { // 完成的圆环的颜色
                                                colorStops: [{
                                                    offset: 1,
                                                    color: 'rgba(255,255,255,0.8)' // 100% 处的颜色
                                                }]
                                            },
                                        }
                                    }
                                }]
                            }]
                        }
                        _self.yellowoption = {
                            title: {
                                text: '体温异常\n\n' + _self.losslist[2] + '%',
                                x: 'center',
                                y: 'center',
                                textStyle: {
                                    fontWeight: 'normal',
                                    color: '#ffffff',
                                    fontSize: '14'
                                }
                            },
                            color: ['rgba(176, 212, 251, 1)'],

                            series: [{
                                name: 'Line 1',
                                type: 'pie',
                                clockWise: true,
                                radius: ['70%', '78%'],
                                itemStyle: {
                                    normal: {
                                        label: {
                                            show: false
                                        },
                                        labelLine: {
                                            show: false
                                        }
                                    }
                                },
                                hoverAnimation: false,
                                data: [{
                                    value: _self.losslist[2],
                                    name: '01',
                                    itemStyle: {
                                        normal: {
                                            color: 'rgba(255,178,12,0.8)',
                                            label: {
                                                show: false
                                            },
                                            labelLine: {
                                                show: false
                                            }
                                        }
                                    }
                                }, {
                                    name: '02',
                                    value: _self.losslist[0] + _self.losslist[1],
                                    itemStyle: {
                                        normal: {
                                            color: { // 完成的圆环的颜色
                                                colorStops: [{
                                                    offset: 1,
                                                    color: 'rgba(255,255,255,0.8)' // 100% 处的颜色
                                                }]
                                            },
                                        }
                                    }
                                }]
                            }]
                        }
                        _self.redoption = {
                            title: {
                                text: '未筛查\n\n' + _self.laterlist[1] + '%',
                                x: 'center',
                                y: 'center',
                                textStyle: {
                                    fontWeight: 'normal',
                                    color: '#ffffff',
                                    fontSize: '14'
                                }
                            },
                            color: ['rgba(176, 212, 251, 1)'],

                            series: [{
                                name: 'Line 1',
                                type: 'pie',
                                clockWise: true,
                                radius: ['70%', '78%'],
                                itemStyle: {
                                    normal: {
                                        label: {
                                            show: false
                                        },
                                        labelLine: {
                                            show: false
                                        }
                                    }
                                },
                                hoverAnimation: false,
                                data: [{
                                    value: _self.laterlist[1],
                                    name: '01',
                                    itemStyle: {
                                        normal: {
                                            color: 'rgba(255,35,12,0.8)',
                                            label: {
                                                show: false
                                            },
                                            labelLine: {
                                                show: false
                                            }
                                        }
                                    }
                                }, {
                                    name: '02',
                                    value: _self.laterlist[0] + _self.laterlist[2],
                                    itemStyle: {
                                        normal: {
                                            color: { // 完成的圆环的颜色
                                                colorStops: [{
                                                    offset: 1,
                                                    color: 'rgba(255,255,255,0.8)' // 100% 处的颜色
                                                }]
                                            },
                                        }
                                    }
                                }]
                            }]
                        };
                        _self.$nextTick(function () {
                            _self.wrong_attend_chart.dispose();
                            _self.loss_attend_chart.dispose();
                            _self.wrong_attend_chart = echarts.init(document.getElementById('wrong_attend_chart'));
                            _self.loss_attend_chart = echarts.init(document.getElementById('loss_attend_chart'));
                            _self.right_attend_chart.setOption(_self.blueoption);
                            _self.wrong_attend_chart.setOption(_self.yellowoption);
                            _self.loss_attend_chart.setOption(_self.redoption);
                            _self.wrong_attend_chart.getZr().on('click', function (params) {
                                 var frameSrc = "/databoard/get_employ_list/?filter_type=1";
                                $("#NoPermissioniframe").attr("src", frameSrc);
                                $('#NoPermissionModal').modal({ show: true, backdrop: 'static' });
                                $("#NoPermissionModalLabel").html("体温筛查详情")
                            });
                            _self.loss_attend_chart.getZr().on('click', function (params) {
                               var frameSrc = "/databoard/get_employ_list/?filter_type=1";
                                $("#NoPermissioniframe").attr("src", frameSrc);
                                $('#NoPermissionModal').modal({ show: true, backdrop: 'static' });
                                $("#NoPermissionModalLabel").html("体温筛查详情")
                            })
                        });
                    }
                }
            });
        },

        // 点击饼状图跳转详情列表页面
        getAttendInfo: function (attend_state) {
            // 查看考勤详情
            window.location.href = '/databoard/getattendinfo/?attend_state=' + attend_state
        }
    },
});

// icon hover 效果
function hoverIcon(tag) {
    tag.style.opacity = '0.5'
    tag.style.cursor = 'pointer'
    tag.style.border = '1px solid gold'
}

function outIcon(tag) {
    tag.style.opacity = '1'
    tag.style.border = ''
}

function hoverIndexImg(tag) {
    tag.style.cursor = 'pointer'
}

function outIndexImg(tag) {
    tag.style.opacity = '1'
}

function get_visit_list() {
    this.location.href = "/get_visit_page"
}

// icon 模态框
function Buttonclick(e) {
    var flag = true

    var blockid = e.id
    var thefloor = blockid.split('-')[0]
    var dev_type = blockid.split('-')[1]
    $.ajax({
        type: 'GET',
        url: '/databoard/getbuildingdevicesta/',
        data: {
            floor: thefloor,
            type: dev_type
        },
        success: function (resp) {
            var newside = document.getElementById('newside')
            // {#var brotherleft = $('#')#}
            newside.innerHTML = ''
            newside.style.left = "1600px"
            newside.style.top = "420px"
            if (newside.style.display == "block") {
                newside.style.display = "none";
            } else {
                newside.style.display = "block";
            }
            if (resp.length == 0) {
                newside.style.display = "none";
            }
            for (var i = 0; i < resp.length; i++) {
                var a_obj = document.createElement('table')
                a_obj.innerHTML = ' <tr> <td> <a href="/monitor_detail" style="color: white;">' + resp[i].name + '</a></td><td> <a href="/monitor_detail" style="color: white;">' + resp[i].status + '</a></td>  </tr> '
                newside.appendChild(a_obj)
            }
        }
    })
}

// 天气
$(function () {
    $('#air_select').change(function () {
        vm_air_vue_check.area_code = $(this).children('option:selected').val();
        if (vm_air_vue_check.nowweektype == 0) {
            vm_air_vue_check.getairhourData()
        } else {
            vm_air_vue_check.getairweekData()
        }
    })

    $(document).on('click', '.days-div', function () {
        $('.days-div').removeClass('checked')
        $('.days-div').removeClass('selected')
        $(this).addClass('selected')
    })

    function fullUrl(value) {
        if (!value) {
            return value
        }
        return 'http://192.168.10.10:8888/media/' + value
    }
});


function gettodaydate() {
    day = new Date();
    month = day.getMonth() + 1;
    days = day.getDate()
    if (month >= 10) {
        currentDate = month + "-";
    } else {
        currentDate = '0' + month + "-";
    }
    if (days >= 10) {
        currentDate += days
    } else {
        currentDate += "0" + days;
    }
    return currentDate
}

function changedevicetype(btn, devicetype) {
    $('.all_device_txt span').css('color', 'rgba(255,255,255,0.3)')
    $('.high_power_txt span').css('color', 'rgba(255,255,255,0.3)')
    $('.all_device_txt').children('i').css('display', 'none')
    $('.all_device_txt').children('span').css('margin-left', '24px')
    $('.high_power_txt').children('i').css('display', 'none')
    $('.high_power_txt').children('span').css('margin-left', '24px')
    $(btn).css({
        'color': 'rgba(255,255,255,1)',
        'margin-left': 0
    })
    $(btn).prev('i').css({
        'display': 'block'
    })
}

function changedatetype(btn, datetype) {
    $('.date-span').css('color', 'rgba(255,255,255,0.3)')
    $(btn).css('color', '#ffffff')
}
