var map;
var CentroCiudad = new google.maps.LatLng(-24.774662,-65.415064);
var ciudad = ' ,Provincia de Salta, Argentina'
var marcador;
var coordenadas;
var directionsDisplay;
var directionsService = new google.maps.DirectionsService();

function initialize() {
	directionsDisplay = new google.maps.DirectionsRenderer();
	var mapProp = {
		center:CentroCiudad,
		zoom:13,
		mapTypeId:google.maps.MapTypeId.ROADMAP
	};
	map=new google.maps.Map(document.getElementById("googleMap"),mapProp);
}
function AgregarMarcador(latitud,longitud,Direccion){

	if(marcador != undefined && marcador != ''){
		marcador.setMap(null);
		marcador = '';
	}
	if (latitud != ''){
	coordenadas = new google.maps.LatLng(latitud,longitud);
        marcador=new google.maps.Marker({
            map:map,
            position: coordenadas,
            draggable:true,
            animation: google.maps.Animation.DROP
        });
        $("#latitud").val(latitud);
        $("#longitud").val(longitud);
        marcador.addListener('dragend', function()
        {
            $("#latitud").val(marcador.getPosition().lat());
            $("#longitud").val(marcador.getPosition().lng());
        });
	}else{
	    BuscarDireccion(Direccion);
	}
	/*var infowindow = new google.maps.InfoWindow({
		content:"Aca va la cantidad de productos"
	});
	google.maps.event.addListener(marcador, 'click', function() {
		infowindow.open(map,marcador);
	});*/
}
/*
function geocodePosition(pos)
{
   geocoder = new google.maps.Geocoder();
   geocoder.geocode({latLng: pos}, function(results, status){
            if (status == google.maps.GeocoderStatus.OK)
            {
                $("#coordenadas").val(results[0].formatted_address);
                //$("#mapErrorMsg").hide(100);
            }
            else
            {
                //$("#mapErrorMsg").html('Cannot determine address at this location.'+status).show(100);
                $("#coordenadas").val('error');
            }
        }
    );
}*/

function BuscarDireccion(Direccion){

	//var Direccion=document.getElementById('EntradaDireccion').value;
	var geocoder = new google.maps.Geocoder();
    var dir = Direccion + ciudad;
	geocoder.geocode({address: dir}, function(result, status) {
      if (status == google.maps.GeocoderStatus.OK) {
         var CoordenadaRecibida = result[0].geometry.location;
         AgregarMarcador(CoordenadaRecibida.lat(),CoordenadaRecibida.lng(),dir);
         //calcRoute(CoordenadaRecibida);
         //map.setCenter(CoordenadaRecibida);
         //map.setZoom(17);
      } else {
          alert("Error");
      }
	});
}
/*
function calcRoute(Coordenadas) {
  var request = {
      origin: CentroCiudad,
      destination: Coordenadas,
      travelMode: google.maps.TravelMode['DRIVING']
      };
  directionsService.route(request, function(response, status) {
    if (status == google.maps.DirectionsStatus.OK) {directionsDisplay.setMap(map)
      directionsDisplay.setDirections(response);

    }
  });
}*/

google.maps.event.addDomListener(window, 'load', initialize);
