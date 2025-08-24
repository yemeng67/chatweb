async function http(obj){
    // 作用是将fetch的发送提前处理好，后面直接使用该函数，就不需要再次处理和判断数据

    //结构赋值
    let { method, url, params, data } = obj

    //有请求，即params，就获取并拼接到url上
    if(params){
        let str = new URLSearchParams(params).toString()
        url += '?' + str
    }

     //提前定义好res
    let res

    //判断有没有数据，即是get请求，还是其他，如post
    if(data) {
        res = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)  //转换为json格式
        })
    }else{
        res = await fetch(url)
    }

    //将数据处理后的最终结果返回出去,并且转换为json格式
    return res.json()
}



