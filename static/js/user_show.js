var main = new Vue({
   el:'#left_col',
   data:function(){
       return {
           date: '',
           inputDate: '',
           userimfolist:[],
           selected_behavor:'',
           show_date:true
       }
   },
   mounted : function() {
        this.date,this.inputDate = this.gettodaydate();
        this.getUserSingleBehavor();
        this.$nextTick(function () {
            this.getUserSingleBehavor();
        })
   },
   methods : {
    getUserSingleBehavor:function() {
        let _self = this;
        $.ajax({
            type:'GET',
            url:'/databoard/usersingleproplebehaor/',
            data:{
                date: _self.inputDate,
                behavor_state:_self.selected_behavor,
                user_user_id : $("#user_id").val()
            },
            success : function(data) {
                _self.userimfolist = data.data;
            }
        })
    },
    gettodaydate: function () {
            day = new Date();
            year = day.getFullYear();
            month = day.getMonth() + 1;
            days = day.getDate();
            if (month >= 10) {
                currentDate = month + "-";
                inputDate = month + '/'
            } else {
                currentDate = '0' + month + "-";
                inputDate = '0' + month + "/";
            }
            if (days >= 10) {
                currentDate += days;
                inputDate += days;
            } else {
                currentDate += "0" + days;
                inputDate += "0" + days;
            }
            currentDate = year + '-' + currentDate;
            click_date = $("#click_date").val()

            return click_date
        },
       input_blur: function () {
            // 输入框失焦时触发
            var _self = this;
            _self.getAllFilterConditions();
        }
   },
   watch:{

       selected_behavor:function() {
           let _self = this;
           _self.getUserSingleBehavor();
       },
       date:function() {
            var _self = this;
            _self.getUserSingleBehavor();
        }
   }
});
