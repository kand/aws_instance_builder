/* Replace any characters from output with html tags for formatting */
function charReplace(server_output){
	return server_output.replace(/\\n/g,"<br/>").replace(/\\'/g,"'");
}
        
/* Gets the current status of the server, writes to server status to window */
var updateTimer = null;
var lastLine = 0;
function getStatus(){
	//maybe here put another ajax request for any new files
	
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
            $("#console_section").append(consoleOutput);
            $("#last_update_time").html(date.getHours() + ":"
                + date.getMinutes() + ":" + date.getSeconds());
        },
        error: function(){
            var date = new Date();
            
            consoleOutput = "<span class='error'>Error: AJAX request failed. Stopping...</span><br/>";
            $("#console_section").append(consoleOutput);
            $("#last_update_time").html(date.getHours() + ":"
                + date.getMinutes() + ":" + date.getSeconds());
            
            clearTimeout(updateTimer);
            updateTimer = null;
            $("#stop_button").hide();
            $("#start_button").show();   
        }
    });
}

/* Provides functionality to tabbed navigation */
var navBarTabs = $("#nav_bar .tab");
var contentSections = $("div.content_section");
function navTabClick(){
	navBarTabs.removeClass("active");
	contentSections.css("display","none");
	$("#" + $(this).addClass("active").attr("id").split("_")[2] + "_section")
		.css("display","block");
}

/* Turn on/off updater. 'start' true to start updating, false to stop updating */
function toggleUpdate(start){
	if(start && updateTimer === null){
        getStatus();
        updateTimer = setInterval("getStatus()",5000);
        $("#start_button").css("display","none");
        $("#stop_button").css("display","inline");
	} else if(!start && updateTimer !== null){
        clearTimeout(updateTimer);
        updateTimer = null;
        $("#stop_button").css("display","none");
        $("#start_button").css("display","inline");	
	}
}

$(document).ready(function(){
    getStatus();
    updateTimer = setInterval("getStatus()",5000);
    
    navBarTabs.click(navTabClick);

    $("#start_button").click(function(){toggleUpdate(true);});       
    $("#stop_button").click(function(){toggleUpdate(false);});
});
