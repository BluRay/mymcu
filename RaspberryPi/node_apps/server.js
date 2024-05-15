/** 
  读取 写入 配置文件【pi.conf】
  读取 写入 MysqlDB
  接收 设备 POST请求 保存数据到数据库
  TODO 循环读取 传感器 数据
**/

var http = require('http');
var fs = require('fs');
var url = require('url');
var querystring = require('querystring');

// cnpm install mysql
var mysql      = require('mysql');
function getMysqlConnection() {
  var connection = mysql.createConnection({
    host     : '1.94.26.149',
    user     : 'root',
    password : 'XXXXXX',
    database : 'gravity'
  }); 
  connection.connect(); 
  return connection
}

function getVinfo(keyword) {
  console.log('-->getVinfo');
  var connection = getMysqlConnection()
  var sql = 'SELECT * FROM tb_fit';
  connection.query(sql,function (err, result) {
    if(err){
      console.log('[SELECT ERROR] - ',err.message);
      return;
    }
    console.log(result);
  })
  connection.end();
}

// 15S循环刷新数据
setInterval(function() {
  console.log('---->intervalFunc');
}, 30000);

// 创建服务器
http.createServer( function (request, response) {
  // 解析请求，包括文件名
  var pathname = url.parse(request.url).pathname;
  // 输出请求的文件名
  console.log("Request for " + pathname + " received.")
  // 从文件系统中读取请求的文件内容
  if (pathname === '/config') {
    // 解析GET方法参数
    var urlObj = url.parse(request.url)
    var query = urlObj.query
    var queryObj = querystring.parse(query)
    console.log('-->request:' + JSON.stringify(queryObj))
    
    let conf_json = {}
    fs.readFile("pi.conf",function (err, data) {
      if(err){
        return console.log(err)
      }else {
        console.log('-->readFile:' + data.toString())
        conf_json = JSON.parse(data.toString())
      }
      Object.keys(queryObj).forEach( c => {
        if (queryObj[c] === '') {
          delete conf_json[c]
        } else {
          conf_json[c] = queryObj[c]
        }
      })
      fs.writeFile('pi.conf', JSON.stringify(conf_json), function(error) {
        if (error) {
          return console.error(error)
        }
        console.log('update success')
        response.writeHead(200, {'Content-Type': 'text/json'})
        response.write(JSON.stringify(conf_json))
        response.end();
      })
    })
  }
  //解析POST方法参数
  if (pathname === '/post') {
    let body = ''
    request.on('data', function (chunk) {
      body += chunk
    });

    request.on('end', function () {
      var insert_Sql = 'INSERT INTO HOME_LAB(device_id,device_name,json_data,rec_time) VALUES(?,?,?,now())'
      body = JSON.parse(body)
      var insert_Params = [body.device_id, body.device_name, JSON.stringify(body.json_data)]
      
      var connection = getMysqlConnection()
      connection.query(insert_Sql,insert_Params,function (err, result) {
        if(err){
           console.log('[INSERT ERROR] - ',err.message);
           body.code = -1
           body.msg = err.message
        } else {
          console.log('-------INSERT OK-------');
          console.log('INSERT ID:',result);
          console.log('#######################');
          connection.end();
          console.log('-------CONN END--------');
          body.code = 0
          body.msg = 'success'
        }
        
        console.log(JSON.stringify(body))
        response.writeHead(200, {'Content-Type': 'text/json'})
        response.write(JSON.stringify(body))
        response.end()
      });
    });
  }
  if (pathname === '/hello') {
    let str = ''
    fs.readFile("pi.conf",function (err,data) {
      if(err){
        return console.log(err)
      }else {
        str = data.toString()
        console.log(data.toString()) //toString() 将buffer格式转化为中文
      }
      response.writeHead(200, {'Content-Type': 'text/html'})
      response.write('pi.conf:' + str)
      response.end()
    })
  }
  if (pathname === '/'){
    // getVinfo()
    pathname = '/index.html'
  }
  // HTML文件显示
  if (pathname.indexOf('.html') > 0){
    fs.readFile(pathname.substr(1), function (err, data) {
      if (err) {
        console.log(err)
        // HTTP 状态码: 404 : NOT FOUND / Content Type: text/html
        response.writeHead(404, {'Content-Type': 'text/html'})
      }else{
        // HTTP 状态码: 200 : OK / Content Type: text/html
        response.writeHead(200, {'Content-Type': 'text/html'})
        // 响应文件内容
        response.write(data.toString())
      }
      // 发送响应数据
      response.end()
    });
  }
  // 字体或其他类型文件
  if (pathname.indexOf('.ttf') > 0){
    fs.readFile(pathname.substr(1), function (err, data) {
      if (err) {
        console.log(err)
        // HTTP 状态码: 404 : NOT FOUND / Content Type: text/html
        response.writeHead(404, {'Content-Type': 'text/html'})
      }else{
        // HTTP 状态码: 200 : OK / Content Type: text/html
        response.writeHead(200, {'Content-Type': 'text/html'})
        // 响应文件内容
        response.write(data,'binary'); 
      }
      // 发送响应数据
      response.end()
    });
  }
}).listen(8080)

// 控制台会输出以下信息
console.log('Server running at http://127.0.0.1:8080/')