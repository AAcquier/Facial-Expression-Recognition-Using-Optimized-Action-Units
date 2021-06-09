
$(function(){
	var file;
	//Allows to import the picture selected
	$('#getPicture').change(function(e){
		file=e.target.files[0], imageType=/image.*/;
		
		  if (!file.type.match(imageType))
            return;

        var reader = new FileReader();
        reader.onload = fileOnload;
        reader.readAsDataURL(file);
		return file;
    });
	
	function fileOnload(e) {
        var $img = $('<img>', { src: e.target.result });
        var canvas = $('#canvas')[0];
        var context = canvas.getContext('2d');
		
        $img.on('load', function() {
            context.drawImage(this, 0, 0);
        });
    }
		
	var imageWidth=$('#canvas').width();
	var imageHeight=$('#canvas').height();
	var zoomCnt=1;
	
	//Allow to zoom in and zoom out
	$('.zoomout').on('click', function(){
		if(zoomCnt>1){
			imageWidth = imageWidth - 480;
			imageHeight = imageHeight - 640;
			$('canvas').width(imageWidth);
			$('canvas').height(imageHeight);
			zoomCnt--;
		}
	});
    
	$('.zoomin').on('click', function(){
		imageWidth = imageWidth + 480;
		imageHeight = imageHeight + 640;
		$('canvas').width(imageWidth);
		$('canvas').height(imageHeight);
		zoomCnt++;
	});
		
		
	var canvas = document.getElementById('canvas');
	var context = canvas.getContext("2d");
	var Markers = new Array(); 		//Stores the datato draw thw landmarks on the pictures
	var ldmkDone = new Array();		//Stores the landmarks numbers already used 
	var ldmkCoord = new Array(); 	//Stores landmark number and coordinates
	var emptyAll = 0;
		
	$('.landmark').on('click', function() {
				
		var ldmkNumber= prompt("Please enter a landmark number:")
		if (ldmkNumber== null || ldmkNumber == "" || parseInt(ldmkNumber) == NaN){
			alert("Invalid input!!! Please try again.");
		}else if (ldmkDone.includes(parseInt(ldmkNumber))){
			alert("Landmark number " + ldmkNumber + " has already been annotated. Please either try another landmark number or erase landmark number " + ldmkNumber + " and try again")
		}else{
			var check = 0;
			var Marker= function() {
				this.mark = new Image();
				this.mark.src = "http://www.clker.com/cliparts/9/1/5/2/119498475589498995button-red_benji_park_01.svg.thumb.png";
				this.Width = 4;
				this.Height = 4;
				this.XPos = 0;
				this.YPos = 0;
				this.ldmkNum = 0;
			}
			
			
			
			var setLdmk = function(mouse){
								
				if (check === 0){
					ldmkDone.push(parseInt(ldmkNumber))
					// Get current mouse coords
					var rect = canvas.getBoundingClientRect();
					
					var mouseXPos = (mouse.x - rect.left);
					var mouseYPos = (mouse.y - rect.top);
					
					// Move the marker when placed to a better location
					var marker = new Marker();
					var coord= new Array();
					var coord2Save = new Array();
					
					marker.XPos = (mouseXPos - (2.15*marker.Width))/zoomCnt;
					marker.YPos = (mouseYPos - (2.15*marker.Height))/zoomCnt;
					marker.ldmkNum = parseInt(ldmkNumber);
					Markers.push(marker);
					coord.push(marker.XPos);
					coord.push(marker.YPos);
					coord2Save.push(parseInt(ldmkNumber));
					coord2Save.push(coord);
					ldmkCoord.push(coord2Save);
					drawLdmk();
					check = 1;	
					ldmkDone.toString();
					var comment= "Landmark already added: ";
					document.getElementById("ldmkDone").innerHTML= comment+ldmkDone;
				}
			}
		}
		
		// Add mouse click event listener to img
		canvas.addEventListener("mousedown", setLdmk, false);
	});		
		
	$('.removeLdmk').on('click', function() {
		
		
		var remLdmkNum = prompt("Please input the landmark number that you would like to remove:")
		
		if (remLdmkNum== null || remLdmkNum == "" || parseInt(remLdmkNum) == NaN){
			alert("Invalid input!!! Please try again.");
		}else if (ldmkDone.includes(parseInt(remLdmkNum))== false){
			alert("Landmark "+ remLdmkNum + " is not part of the landmarks already annotated");
		}else{
			// Remove the landmark from the lists
			for(i=0;i<ldmkCoord.length;i++){
				if(ldmkCoord[i][0] === parseInt(remLdmkNum)){
					ldmkCoord.splice(i,1);
					Markers.splice(i,1);
				}
			}
			ldmkDone.splice(ldmkDone.indexOf(parseInt(remLdmkNum)),1); 
			
			//Remove everything from the canvas
			context.fillStyle = "#ff000";
			context.fillRect(0, 0, canvas.width, canvas.height);
			
			//Repopulate the canvas with the previously selected picture
			  if (!file.type.match(imageType))
				return;
			
			var reader = new FileReader();
			reader.onload = fileOnload;
			reader.readAsDataURL(file);
			drawLdmk();		//Redraw the landmarks
		}
	});
	
	var drawLdmk = function() {
		for(var i=0; i<Markers.length; i++){
			var tempMarker=Markers[i];
			// Draw marker
			context.drawImage(tempMarker.mark, tempMarker.XPos, tempMarker.YPos, tempMarker.Width, tempMarker.Height);	
				
			// Calculate postion text
			var markerText = tempMarker.ldmkNum;
			// Draw position above
			context.fillStyle = "#ff000";
			context.fillText(markerText, tempMarker.XPos, tempMarker.YPos);
		}
	}	
	
	$('#download').on('click', function() {
		
		var text =JSON.stringify(ldmkCoord);
		var filename = 'landmark.txt';
		var pom = document.createElement('a');
		pom.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
		pom.setAttribute('download', filename);

		if (document.createEvent) {
			var event = document.createEvent('MouseEvents');
			event.initEvent('click', true, true);
			pom.dispatchEvent(event);
		}
		else {
			pom.click();
		}
		return emptyAll = 1;
	});
});

