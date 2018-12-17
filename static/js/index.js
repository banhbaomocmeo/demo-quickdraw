var canvas = document.querySelector( 'canvas' ),
    c = canvas.getContext( '2d' ),
    mouseX = 0,
    mouseY = 0,
    last_mouseX = 0,
    last_mouseY = 0,
    width = 256,
    height = 256,
    colour = 'black',
    mousedown = false;

// resize the canvas
canvas.width = width;
canvas.height = height;
c.beginPath();
c.rect(0,0,256,256);
c.fillStyle = "white";
c.fill();
c.lineWidth = 5;
c.lineJoin = 'round';
c.lineCap = 'round';
c.strokeStyle = 'black';

console.log("hello")

function draw() {
    if (mousedown) {
        // set the colour
        c.fillStyle = colour;
        // start a path and paint a circle of 20 pixels at the mouse position
        c.beginPath();
		c.moveTo(last_mouseX, last_mouseY);
		c.lineTo(mouseX, mouseY);
		c.closePath();
		c.stroke();
    }
}

// get the mouse position on the canvas (some browser trickery involved)
canvas.addEventListener( 'mousemove', function( event ) {
    last_mouseX = mouseX
    last_mouseY = mouseY
    if( event.offsetX ){
        mouseX = event.offsetX;
        mouseY = event.offsetY;
    } else {
        mouseX = event.pageX - event.target.offsetLeft;
        mouseY = event.pageY - event.target.offsetTop;
    }
    // call the draw function
    draw();
}, false );

canvas.addEventListener( 'mousedown', function( event ) {
    mousedown = true;
}, false );
canvas.addEventListener( 'mouseup', function( event ) {
    mousedown = false;
}, false );


$('#check').click(function(){
    data = canvas.toDataURL('image/png')
    saveImage(data)
});

$('#reset').click(function(){
    c.fillStyle = "white";
    c.fillRect(0,0,256,256);
});


function saveImage(input) {
    $.ajax({
        url: "http://localhost:5000/api/predict",
        method: 'POST',
        data:{
            imageBase64: input
        },
        success: function( data, textStatus, jQxhr ){
            console.log(data)
            CreateTableFromJSON(data)
        },
        error: function( jqXhr, textStatus, errorThrown ){
            $('#api_output').html( "There was an error" );
            console.log( errorThrown );
        }
    })
}

function CreateTableFromJSON(data) {
    // EXTRACT VALUE FOR HTML HEADER. 
    label = data['label']
    score = data['score']
    col = ['label', 'score']
    // CREATE DYNAMIC TABLE.
    var table = document.createElement("table");

    // CREATE HTML TABLE HEADER ROW USING THE EXTRACTED HEADERS ABOVE.

    var tr = table.insertRow(-1);                   // TABLE ROW.

    for (var i = 0; i < 2; i++) {
        var th = document.createElement("th");      // TABLE HEADER.
        th.innerHTML = col[i];
        tr.appendChild(th);
    }

    // ADD JSON DATA TO THE TABLE AS ROWS.
    for (var i = 0; i < label.length; i++) {

        tr = table.insertRow(-1);

        for (var j = 0; j < col.length; j++) {
            var tabCell = tr.insertCell(-1);
            tabCell.innerHTML = data[col[j]][i];
        }
    }

    // FINALLY ADD THE NEWLY CREATED TABLE WITH JSON DATA TO A CONTAINER.
    var divContainer = document.getElementById("result");
    divContainer.innerHTML = "";
    divContainer.appendChild(table);
}