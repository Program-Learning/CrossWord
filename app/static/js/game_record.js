$(document).ready(function() {
    $("#finishPaperButton").click(function() {
        $.ajax({
            url: finishPaperUrl, // 替换为你的路由或 API 地址
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
    $("#restartButton").click(function() {
        event.preventDefault();
        location.href = restartUrl;
    });
    $('#saveButton').click(function() {
        // 使用 html2canvas 截取网页内容
        html2canvas(document.body).then(function(canvas) {
            // 将 canvas 转换为图片
            var imgData = canvas.toDataURL('image/png');

            // 创建一个链接元素
            var link = document.createElement('a');
            link.download = 'screenshot.png'; // 设置下载文件名
            link.href = imgData; // 设置图片数据

            // 模拟点击链接以触发下载
            link.click();
        });
    });
});
