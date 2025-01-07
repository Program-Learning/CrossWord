function logoutAdmin() {
    window.location.href = logoutAdminUrl; // 由服务器动态注入
}

function upload_csv_web() {
    window.location.href = uploadCsvUrl; // 由服务器动态注入
}

function show_web() {
    window.location.href = showUrl; // 由服务器动态注入
}

function new_poem_web() {
    window.location.href = newPoemUrl; // 由服务器动态注入
}

function deleteAdmin(adminId) {
    fetch(deleteAdminUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id: adminId })
    })
        .then(response => response.json())
        .then(data => {
            if (data.code === 0) {
                showMessage('success', "Successfully deleted admin", 'message', 3000);
                queryAdmin();
            } else {
                showMessage('error', "Failed to delete admin: " + data.message, 'message', 3000);
            }
        })
        .catch(error => {
            showMessage('error', "Error deleting admin:" + error, 'message', 3000);
        });
}

function queryAdmin() {
    fetch(queryAdminUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
    })
        .then(response => response.json())
        .then(data => {
            if (data.code === 0) {
                const admins = data.data;
                const table = document.createElement("table");
                table.innerHTML = `<tr>
                    <th>管理员编号</th>
                    <th>用户名</th>
                    <th>密码</th>
                    <th>操作</th>
                </tr>`;
                admins.forEach(admin => {
                    const row = table.insertRow(-1);
                    row.innerHTML = `<td>${admin.id}</td>
                        <td>${admin.username}</td>
                        <td>******</td>
                        <td><button onclick="deleteAdmin(${admin.id})">删除</button></td>`;
                });
                const row = table.insertRow(-1);
                row.innerHTML = `<td>未插入</td>
                    <td>username:<input type="text" id="new_admin_username" name="username" required></td>
                    <td>password:<input type="password" id="new_admin_password" name="password" required></td>
                    <td><button onclick="addAdmin()">插入</button></td>`;
                const adminTable = document.getElementById("adminTable");
                adminTable.innerHTML = '';
                adminTable.appendChild(table);
            } else {
                showMessage('error', "Failed to query admins: " + data.message, 'message', 3000);
            }
        })
        .catch(error => {
            showMessage('error', "Error querying admins:" + error, 'message', 3000);
        });
}

function addAdmin() {
    const username = document.getElementById("new_admin_username").value;
    const password = document.getElementById("new_admin_password").value;
    fetch(addAdminUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    })
        .then(response => response.json())
        .then(data => {
            if (data.code === 0) {
                showMessage('success', "Successfully added admin", 'message', 3000);
                queryAdmin();
            } else {
                showMessage('error', "Failed to add admin: " + data.message, 'message', 3000);
            }
        })
        .catch(error => {
            showMessage('error', "Error adding admin:" + error, 'message', 3000);
        });
}
