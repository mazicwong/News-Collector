function fillWith(str, len, c, isBack) {
    str = str.toString();
    if(str.length >= len) {
        return str;
    }
    var padding = '';
    for(var i = 0; i < len - str.length; i++) {
        padding += c;
    }
    if(isBack) {
        return str + padding;
    } else {
        return padding + str;
    }
}

function timestampToADtime(timestamp) {
    var day     = new Date(timestamp * 1000);
    var year    = fillWith(day.getFullYear(), 4, '0', false);
    var month   = fillWith(day.getMonth() + 1, 2, '0', false);
    var date    = fillWith(day.getDate(), 2, '0', false);
    var hours    = fillWith(day.getHours(), 2, '0', false);
    var minutes = fillWith(day.getMinutes(), 2, '0', false);
    var seconds = fillWith(day.getMinutes(), 2, '0', false);
    return (year+"-"+month+"-"+date+" "+hours+":"+minutes+":"+seconds);
}
