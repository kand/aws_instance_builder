var dateTimer = null;
var lastLine = 0;

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
        },
        error: function(){
            var date = new Date();
            
            consoleOutput = "<span class='error'>Error: AJAX request failed. Stopping...</span><br/>";
            $("#console_body").append(consoleOutput);
            $("#last_update_time").html(date.getHours() + ":"
                + date.getMinutes() + ":" + date.getSeconds());
            
            clearTimeout(updateTimer);
            updateTimer = null;
            $("#stop_button").hide();
            $("#start_button").show();   
        }
    });
}

$(document).ready(function(){
    getStatus();
    updateTimer = setInterval("getStatus()",5000);
    
    $("#console_tab_console").click(function(){
    	$(this).addClass("active");
    	$("#console_tab_monitor").removeClass("active");
    	
    	//show console
    });
    
    $("#console_tab_monitor").click(function(){
    	$(this).addClass("active");
    	$("#console_tab_console").removeClass("active");
    	
    	//show monitor
    });

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
