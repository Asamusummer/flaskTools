function chooseorg1(org1_code) {
        $.get('/checkattend/getnextorg/',{'org1_code':org1_code},function (data_list) {
            var org2_info = $('#org2').empty().append('<option value>' + ' ' + '</option>');
            var org3_info = $('#org3').empty().append('<option value>' + ' ' + '</option>');
            $.each(data_list.orglist,function (i,org) {
                org2_info.append('<option value="' + org.p_code + '">' + org.p_name + '</option>')
            })

        })
    }
    //选择二级组织
function chooseorg2(org2_code) {
      console.log(org2_code)
        let org1_code = $('#org1').val();
        $.get('/checkattend/getnextorg/',{'org1_code':org1_code,'org2_code':org2_code},function (data_list) {
            var org3_info = $('#org3').empty().append('<option value>' + ' ' + '</option>');
            $.each(data_list.orglist,function (i,org) {
                org3_info.append('<option value="' + org.org_code + '">' + org.org_name + '</option>')
            })
        })
    }



