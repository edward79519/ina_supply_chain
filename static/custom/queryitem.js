$(document).ready(function() {
    $(document).on('click', '#dbsearch', function () {
        let sn = $('#searchitemsn').val();
        if (sn === ""){
            $('#searchmsg').text("請輸入庫存系統料號。")
        } else {
            $.ajax({
                url: '/quotation/ajax/itemdetail/',
                method: "GET",
                data: {
                    sn: sn,
                },
                success: function (res) {
                    if (res.status) {
                        $('#searchmsg').text("查詢成功！");
                        let data = res.result;
                        let cate_name = data.cate_name;
                        let cate_en = data.cate_ed;
                        $('#id_name').val(data.item_name);
                        $('#id_sn').val(data.item_sn);
                        $('#id_specmain').val(data.item_specmain);
                        $('#id_specsub').val(data.item_specsub);
                        $('#id_cate').prop('disabled', false);
                        $('#id_cate').find("option:contains("+ cate_name +")").prop('selected', true);
                        $('#id_name, #id_sn, #id_specmain, #id_specsub, #id_cate').prop('disabled', true);
                    } else {
                        $('#searchmsg').text(res.result);
                        $('#id_name, #id_sn, #id_specmain, #id_specsub, #id_cate').val("");
                    }
                },
            });
        }
    });
    $(document).on('click', '#submit', function () {
        $('input, select').prop('disabled', false);
    });
});