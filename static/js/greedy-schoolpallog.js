(function (window, undefined) {
    var $ = jQuery;
    function greedySchoolPalLog() {
        this.operationType.apply(this, arguments);
    }
    function greedySchoolPalLog1() {
        this.operationType1.apply(this, arguments);
    }
    greedySchoolPalLog.prototype = {
        operationType: function (type, operationName, orgId, userRole, userName, url,eventId) {
            if (typeof (operationName) != 'undefined') {
                this.PageId = type.substring(7);
                this.ControlId = operationName.substring(3);
                this.operationLogsUrl = url;
                this.OrgId = orgId;
                this.UserRole = userRole;
                this.UserName = userName;
                if (typeof (eventId) != 'undefined')
                {
                    this.EventId = eventId;
                }
                else
                {
                  this.EventId = '5';
                }              
                this.operationLogsAdd();
            }
        },
        operationLogsUrl: "http://localhost:10364/SchoolPal/OperationLogsAdd",
        operationLogsAdd: function () {
            var data = {};
            data.OrgId = this.OrgId;
            data.UserRole = this.UserRole;
            data.UserName = this.UserName;
            data.PageId = this.PageId;
            data.ControlId = this.ControlId;
            data.EventId = this.EventId;
            $.ajax({
                url: this.operationLogsUrl,
                data: data,
                type: "GET",
                dataType: 'jsonp'
            });
        }
    }
    greedySchoolPalLog1.prototype = {
        operationLogsUrl: "http://localhost:10364/SchoolPal/OperationLogsAdd",
        operationType1: function (type, operationName, orgId, userRole, userName, userTel, url, eventId) {
            if (typeof (operationName) != 'undefined') {
                this.PageId = type.substring(7);
                this.ControlId = operationName.substring(3);
                this.operationLogsUrl = url;
                this.OrgId = orgId;
                this.UserRole = userRole;
                this.UserName = userName;
                this.UserTel = userTel;
                if (typeof (eventId) != 'undefined') {
                    this.EventId = eventId;
                }
                else {
                    this.EventId = '5';
                }
                this.operationLogsAdd1();
            }
        },
        operationLogsAdd1: function () {
            var data = {};
            data.OrgId = this.OrgId;
            data.UserRole = this.UserRole;
            data.UserName = this.UserName;
            data.UserTel = this.UserTel;
            data.PageId = this.PageId;
            data.ControlId = this.ControlId;
            data.EventId = this.EventId;
            $.ajax({
                url: this.operationLogsUrl,
                data: data,
                type: "GET",
                dataType: 'jsonp'
            });
        }
    }
    window.greedySchoolPalLog = greedySchoolPalLog;
    window.greedySchoolPalLog1 = greedySchoolPalLog1;
})(window);