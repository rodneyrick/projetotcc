$(function () {
	if(navigator.getlocation){
		navigator.getlocation.getCurrentPosition(getCoors, getError);
	} else{
		initialize(13.30272, -87.194107);
	}

	function getCoords(position){
		var lat = position.coords.latitude;
		var lng = position.coords.longitude;

		initialize(lat,lng);
	}

	function getError(err){
		// alert(err.message);
		initialize(13.30272, -87.194107);
	}

	function initialize(lat, lng){
		var latlng = new google.maps.LatLng(lat,lng);
		var mapSetting = {
			center: latlng,
			zoom: 15,
			mapTypeId: google.maps.MapTypeId.ROADMAP
		}
		map = new google.maps.Map($('#mapa').get(0), mapSetting);

		var marker = new google.maps.Marker({
			position: latlng,
			map: map,
			draggable: true,
			title: 'Drag'
		});

		google.maps.event.addListener(
			marker,
			'position_changed', 
			function(){
				getMarkerCoods(marker);
			}
		);
	}

	function getMarkerCoods(marker){
		var markerCoords = marker.getPosition();
		// console.log(markerCoords.lat()+ ' ' + markerCoords.lng());
		$('#id_lat').val( markerCoords.lat() );
		$('#id_lng').val( markerCoords.lng() );
	}

	$('#form_coords').submit(function(e){
		e.preventDefault();

		$.post('/coords/save', $(this).serialize, function(data){
			if(data.ok){
				$('#data').html(data.msg);
				$('#form_coords').each(function(){ this.reset; });
			} else {
				alert(data.msg);
			}
		}, 'json');
	});
});