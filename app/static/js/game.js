$(document).ready(function() {
    $("#upload").click(function() {
        // 收集数据
        var poem = $("#poem").val(); // 假设这是一个文本域
        var row = parseInt($("#row").val(), 10); // 假设这是一个输入字段
        var col = parseInt($("#col").val(), 10); // 假设这是另一个输入字段
        var direction = $("#direction").val(); // 假设这是另一个输入字段
        // 创建一个包含数据的对象
        var dataToSend = {
            poem: poem,
            row: row,
            col: col,
            direction: direction,
        };

        // 转换为 JSON（jQuery 会自动处理，因为我们将数据作为对象传递）

        // 发送 AJAX 请求
        $.ajax({
            url: submitUrl, // 替换为你的路由或 API 地址
            type: "POST", // 根据你的 API 要求的 HTTP 方法
            contentType: "application/json", // 如果你明确要求 JSON 格式
            dataType: "json", // 期望从服务器返回的数据类型
            data: JSON.stringify(dataToSend), // 如果你的 API 需要 JSON 字符串，则转换为字符串
            success: function(response) {
                // 请求成功时的处理
                console.log(response);
                if (response.status == "success") {
                    location.reload();
                } else {
                    alert(response.message);
                }
                // 在这里，你可以根据响应内容更新页面或其他操作
            },
            error: function(xhr, status, error) {
                // 请求失败时的处理
                console.error("Error: " + error);
            },
        });
    });
    $("#logout").click(function() {
        $.ajax({
            url: logoutUrl, // 替换为你的路由或 API 地址
            type: "POST", // 根据你的 API 要求的 HTTP 方法
            success: function(response) {
                // 请求成功时的处理
                if (response.status == "success") {
                    location.reload();
                } else {
                    alert(response.message);
                }
                // 在这里，你可以根据响应内容更新页面或其他操作
            },
            error: function(xhr, status, error) {
                // 请求失败时的处理
                console.error("Error: " + error);
            },
        });
        // clearBrowserCookie();
    });

    $(".default , .word_back").click(function() {
        const id = $(this).attr("id");
        $(this).removeClass("default");
        $(this).addClass("click_back");

        // 移除所有具有默认class的div上的'active-class'（如果存在）
        $(".default").removeClass("click_back");
        // 给被点击的div添加'active-class'
        $(this).addClass("default");

        // 解析 id（这里假设 id 是由 i_j 形式的字符串组成）
        // 你可以使用 split 方法来分割字符串，或者使用其他方式
        var parts = id.split("_");
        var rowValue = parseInt(parts[0], 10); // 将字符串转换为整数，基数为10
        var colValue = parseInt(parts[1], 10); // 将字符串转换为整数，基数为10
        $("#row").val(rowValue + 1);
        $("#col").val(colValue + 1);
        // 现在你可以使用 i 和 j 进行其他操作了
        console.log(
            "Clicked div with id parts: i = " + rowValue + ", j = " + colValue,
        );
    });
});
