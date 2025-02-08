$(document).ready(function() {
    $("#logout").click(function() {
        event.preventDefault();
        $.ajax({
            url: logoutUrl, // 替换为你的路由或 API 地址
            type: "POST", // 根据你的 API 要求的 HTTP 方法
            success: function(response) {
                // 请求成功时的处理
                if (response.status == "success") {
                    location.reload();
                } else {
                    alert(response.message);
                    window.location.href = loginWebUrl;
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
})
