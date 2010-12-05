var dateTimer = null;
var lastLine = -1;

/* Replace any characters from output with html tags for formatting */
function charReplace(server_output){
	return server_output.replace(/\\n/g,"<br/>");
}
        
/* Gets the current status of the server, writes to server status to window */
function getStatus(){
    $.ajax({
        url:"getstatus",
        type:"POST",
        data:({lastLine:lastLine}),
        dataType:"json",
        success: function(data){
            var date = new Date();
            lastLine = data.lastLine;
            
            consoleOutput = "<span class='";
            if(data.error.length > 0){
            	consoleOutput += "error'>Error: " + charReplace(data.error);
            } else {
            	consoleOutput += "content_block'>" + charReplace(data.lines);
            }
            consoleOutput += "</span>"
            $("#console_body").append(consoleOutput);
            $("#last_update_time").html(date.getHours() + ":"
                + date.getMinutes() + ":" + date.getSeconds());
        }
    });
}

$(document).ready(function(){
    getStatus();
    updateTimer = setInterval("getStatus()",5000);

    $("#start_button").click(function(){
        if( updateTimer === null ){
            getStatus();
            updateTimer = setInterval("getStatus()",5000);
            $(this).hide();
            $("#stop_button").show()
        }
    });
            
    $("#stop_button").click(function(){
        if( updateTimer !== null ){
            clearTimeout(updateTimer);
            updateTimer = null;
            $(this).hide();
            $("#start_button").show();
        }
     });
});
