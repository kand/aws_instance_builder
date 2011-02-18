var activeRequest = null;

/* Set up update timer depending on tab */
var updateTimer = null;
var activeTab;
function setTimer(){
    if(activeTab.attr("id") === "nav_tab_console"){
        getStatus();
        updateTimer = setInterval("getStatus()",5000);
    } else {
    	getFiles();
    	updateTimer = setInterval("getFiles()",60000);
    }
}

/* Replace any characters from output with html tags for formatting */
function charReplace(server_output){
	return server_output.replace(/\\n/g,"<br/>")
						.replace(/\\'/g,"'");
}

/* Set update time text at bottom of window, clear timer and request */
function setUpdateTime(clearTimer){
	activeRequest = null;
	
	var date = new Date();
    $("#last_update_time").html(date.getHours() + ":"
            + date.getMinutes() + ":" + date.getSeconds());
    
    if(clearTimer){
        clearTimeout(updateTimer);
        updateTimer = null;
        $("#stop_button").hide();
        $("#start_button").show();
    }
}
        
/* Gets the current status of the server, writes to server status to window */
var lastLine = 0;
function getStatus(){
	if(activeRequest){
		return false;
	}
	
    activeRequest = $.ajax({
        url:"getstatus",
        type:"POST",
        data:({lastLine:lastLine}),
        dataType:"json",
        success: function(data){
            lastLine = data.lastLine;
            var clearTime = false;
            
            var consoleOutput = "<span class='";
            if(data.error.length > 0){
            	consoleOutput += "error'>Error: " + charReplace(data.error);
            	clearTime = true;
            } else {
            	consoleOutput += "content_block'>" + charReplace(data.lines);
            }
            consoleOutput += "</span>"
            $("#console_section").append(consoleOutput);

            setUpdateTime(clearTime);
        },
        error: function(){
            var date = new Date();
            
            consoleOutput = "<span class='error'>Error: AJAX request failed. Stopping...</span><br/>";
            $("#console_section").append(consoleOutput);
            $("#last_update_time").html(date.getHours() + ":"
                + date.getMinutes() + ":" + date.getSeconds());
            
            setUpdateTime(true);
        }
    });
}

/* Gets all files added after lastFileId, only one of these requests can be made at a time */
var lastFileId = 0;
function getFiles(){
	if(activeRequest){
		return false;
	}
	
	activeRequest = $.ajax({
		url:"getfiles",
		type:"POST",
		data:({lastFileId:lastFileId}),
		dataType:"json",
		success: function(data){
			var l = data.files.length;
			for(var i = 0;i < l;i++){
				lastFileId = data.files[i].id;
				
				var fId = "file_" + data.files[i].id
				var fileOutput = "<li id='" + fId + "'>\n";
				fileOutput += "\t<a id='" + fId + "_link' class='file_link' target='_blank' href='" + data.files[i].path + "'>";
				fileOutput += data.files[i].name + "</a>\n";
				fileOutput += "\t<div id='" + fId + "_desc' class='file_description'>" + data.files[i].desc + "</div>\n";
				fileOutput += "</li>\n";
				
				$("#fileOutput").append(fileOutput);
	            
				setUpdateTime(false);				
			}
		},
		error: function(){
			setUpdateTime(true);
		}
	});
}

/* Turn on tab with active class when page is first loaded */
var navBarTabs = $("#nav_bar .tab");
var contentSections = $("div.content_section");
function getActiveTab(){
	var l = navBarTabs.length;
	for(var i = 0;i < l;i++){
		var t = $(navBarTabs[i]); 
		if(t.hasClass("active")){
			contentSections.css("display","none");
			$("#" + t.attr("id").split("_")[2] + "_section")
				.css("display","block");
			
			return t;
		}	
	}
}

/* Turn on/off updater. 'start' true to start updating, false to stop updating */
function toggleUpdate(start){
	if(start && updateTimer === null){
        setTimer();
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
	activeTab = getActiveTab();
	setTimer();

    $("#start_button").click(function(){toggleUpdate(true);});       
    $("#stop_button").click(function(){toggleUpdate(false);});
    $("#files_refresh").click(getFiles);
});
