var dateTime = new Date();
var todayDate = dateTime.getFullYear() + '-' + (dateTime.getMonth() + 1) + '-' + dateTime.getDate();
var main = new Vue({
  el: '.content_div',
  data: {
    date: '',
    inputDate: todayDate,
    selected_mod: 1,
    select_depart: '',
    selected_class: null,
    selected_dormtory: null,
    user_name: null,
    user_id: null,
    classData: [],
    dormtoryData: [],
    data: [],
    table_type: 1,
    show_class: true,
    show_date: true,
    show_dormitory: false,
    employList: [],
    visitList: [],
    departList: [],
    select_on_state: '',
    //select_off_state: '',
    select_diff_state: '',
    filterParameters: {'depart_id': '', 'attend_state': '-1', 'attend_date': todayDate},
    warn_temp_list: []
  },
  beforeMount:function() {
    let _self = this;
    let state = Number(location.href.split('=')[1]);
    if (state) {
      _self.select_on_state = '';
      _self.filterParameters['attend_state'] = '';
    } else {
      _self.select_on_state = '';
      _self.filterParameters['attend_state'] = '';
    }
  },
  mounted:function() {
    //if (this.$refs.later_click) {
    //    this.getworkerattendlist(1)
    //} else if (this.$refs.lose_click) {
    //    this.getworkerattendlist(0)
    //}

    // 获取访客列表
    // this.getvisitorlist();
    // 获取部门列表
    this.getDepartList();
    //默认获取所有人员的考勤状况
    // this.getALLPeopleAttendSate();
    //获取体温异常人员信息
    this.getWarnTmpList();
  },
  watch: {
    'filterParameters': {
      handler: function(val, old) {
        $.ajax({
          type: 'GET',
          url: '/databoard/getworkerattendlist/',
          data: {'filterParameters': JSON.stringify(val)},
          success: function (data) {
            main.employList = data;
          }
        });
      },
      deep: true
    },
    inputDate: function (val) {
      let _self = this;
      _self.filterParameters['attend_date'] = this.inputDate;
      _self.getWarnTmpList()


    },
    select_diff_state: function (val) {
      let _self = this;
      _self.filterParameters['attend_state'] = val;
    }
  },
  methods: {
    getALLPeopleAttendSate:function() {
      let _self = this;
      $.ajax({
        type: 'GET',
        url: '/databoard/getalluserattendstate/',
        success: function (resp) {
          _self.employList = resp;
        }
      })
    },

    filter_diff_state:function(diff_state) {
      let _self = this;
      _self.filterParameters['attend_state'] = diff_state;
    },
    filter_off_state:function(off_state) {
      let _self = this;
      _self.filterParameters['attend_state'] = off_state;
    },
    filter_on_state:function(on_state) {
      let _self = this;
      _self.filterParameters['attend_state'] = on_state;
    },
    filter_depart:function(depart_id) {
      let _self = this;
      _self.filterParameters['depart_id'] = depart_id;
    },
    getDepartList:function() {
      _self = this
      $.ajax({
        type: 'GET',
        url: '/databoard/get_depart_list/',
        success: function (data) {
          _self.departList = data;
        }
      });
    },
    getworkerattendlist:function(para) {
      let _self = this
      $.ajax({
        type: 'GET',
        url: '/databoard/getworkerattendlist/',
        data: {'filter_type': para},
        success: function (data) {
          _self.employList = data;
        }
      });
    },
    getWarnTmpList:function() {
      let _self = this;
      $.ajax({
        type: 'GET',
        url: '/databoard/getwarntemplist/',
        data: {date: _self.inputDate},
        success: function (resp) {
          _self.warn_temp_list = resp.lists;
        }
      })
    },
    GotoPersondetail: function (id, datea) {
      var frameSrc = "/databoard/userdetailshowpage/?user_id=" + id + "&" + "date=" + datea;
      $("#NoPermissioniframe").attr("src", frameSrc);
      $('#NoPermissionModal').modal({show: true, backdrop: 'static'});
    },
  }
});
