/**
 * Created with PyCharm.
 * User: Administrator
 * Date: 16-5-26
 * Time: 下午6:10
 * To change this template use File | Settings | File Templates.
 */
document.write("<script language='javascript' src='static/js/jquery-3.1.0.min.js'></script>");
var res = '';
function loadm()
{
	var url = '/module_list';
	var myAjax = new Ajax.Request(
	url,
	{
		method: 'get',
		onComplete: showResponse
	});
	function showResponse(originalRequest)
	{
        res = originalRequest.responseJSON
	console.info(res)
        for (i in res){
            $("#modulelist").append(
            "<div class='panel panel-default' id='"+i+"'><div class='panel-heading'><h4 class='panel-title'><a data-toggle='collapse' data-parent='#modulelist' href='#body"+i+"'>"+i+"</a></h4></div>")
            $("#"+i).append("<div id='body"+i+"' class='panel-collapse collapse'>")
            for (var j=0; j<res[i].length;j++){
                $("#body"+i).append("<div class='panel-body'><p  id='"+res[i][j].id+"' onclick='moduleleave2(this.id);create(this.id);'>"+i+""+res[i][j].modname+"</a></div>")
            }
        }
	}
}
function moduleleave2(currvalue) {
    if (currvalue==-1){return false;}
    var download =  document.getElementById("download")
    download.options.length=0;
	var url = '/module_list?id='+currvalue;
	var myAjax = new Ajax.Request(
	url,
	{
		method: 'get',
		onComplete: showResponse
	});
	function showResponse(originalRequest)
	{
		eval("var resultString='"+originalRequest.responseText+"'");
		var objarray=resultString.split("|");
        var a=0;
	    for ( var i=0;i<objarray.length;i++){
            a += 1;
            download.options.add(new Option(objarray[i],a));
		}
	}
}
function create(currentid){
    var url = '/server_list?sid='+currentid;
    var myAjax = new Ajax.Request(
        url,
        {
            method: 'get',
            onComplete: showResponse
        });
    function  showResponse(originalRequest) {
        var tabObj = document.getElementById("viewTabs")
        var str = "";
        //if (res.length == 0) {
        res = originalRequest.responseJSON.serverlist
        var rowNum=tabObj.rows.length;
        for (i=rowNum-1;i>0;i--)
         {
             tabObj.deleteRow(i);
             //rowNum=rowNum-1;
             //i=i-1;
         }
        for(var i=0; i<res.length; i++){
            var newTr = tabObj.insertRow();
            newTr.id = "tab"+i;
            var newTd0 = newTr.insertCell();
            newTd0.innerHTML="<input type='checkbox' name='chkArr' id='chkArr"+i+"' value="+res[i].sid+" />";
            var newTd1 = newTr.insertCell();
            newTd1.innerText=res[i].addr;
            var newTd2 = newTr.insertCell();
            newTd2.innerText=res[i].appname;
            var newTd3 = newTr.insertCell();
            newTd3.innerText=res[i].work_dir;
            var newTd4 = newTr.insertCell();
            newTd4.innerText=res[i].user;
    }
  }
}
function removeTr(trNum){
  $("#"+trNum).remove();
}
function commit(){
    var id_array=new Array();
        $("#submit").attr("disabled",true);
        $('input[type="checkbox"]:checked').each(function(){
            id_array.push($(this).val());
            $('input[type="checkbox"]').attr("checked",false);
        })
    var war=$("#download").find("option:selected").text();
        $.ajax({
            traditional:true,
            type: 'get',
            url: '/commit/',
            data: {
                'sid': id_array,
                'war': war
            },
            success: function(ret){
                console.info(ret)
                $('#result').html(ret.replace(/\n/g, '<br>'));
                $("#submit").attr("disabled",false);
            },
            error: function(){
                $('#result').html("请选择正确选项");
                $("#submit").attr("disabled",false);
            },
        });
}
function rollback(){
    var id_array=new Array();
        $("#rollback").attr("disabled",true);
        $('input[type="checkbox"]:checked').each(function(){
            id_array.push($(this).val());
            $('input[type="checkbox"]').attr("checked",false);
        })
        $.ajax({
            traditional:true,
            type: 'get',
            url: '/rollback/',
            data: {
                'sid': id_array,
            },
            success: function(ret){
                $('#result').html(ret.replace(/\n/g, '<br>'));
                $("#rollback").attr("disabled",false);
            },
            error: function(){
                $('#result').html("请选择正确选项");
                $("#rollback").attr("disabled",false);
            },
        });
}

