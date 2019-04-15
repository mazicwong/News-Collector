function Vector(x, y, z) {
    this.x = x;
    this.y = y;
    this.z = z;

    this.addX = function(x) {
        this.x += x;
    };

    this.addY = function(y) {
        this.y += y;
    };

    this.addZ = function(z) {
        this.z += z;
    };

    this.set = function(x, y, z) {
        this.x = x;
        this.y = y;
        this.z = z;
    };
}

function PointCollection() {
    this.mousePos = new Vector(0, 0);
    this.pointCollectionX = 0;
    this.pointCollectionY = 0;
    this.points = []

    this.newPoint = function (x, y, z) {
        var point = new Point(x, y, z);
        this.points.push(point);
        return point;
    };

    this.update = function () {
        for(var i=0; i<this.points.length; i++) {
            var point = this.points[i];

            if (point === null) {
                continue;
            }

            var dx = this.mousePos.x - point.curPos.x;
            var dy = this.mousePos.y - point.curPos.y;
            var dd = (dx * dx) + (dy * dy);
            var d = Math.sqrt(dd);

            if (d < 150) {
                point.targetPos.x = (this.mousePos.x < point.curPos.x) ? point.curPos.x - dx : point.curPos.x - dx;
                point.targetPos.y = (this.mousePos.y < point.curPos.y) ? point.curPos.y - dy : point.curPos.y - dy;
            }
            else {
                point.targetPos.x = point.originalPos.x;
                point.targetPos.y = point.originalPos.y;
            }

            point.update();
        }
    }

    this.shake = function() {
        var randomNum = Math.floor(Math.random() * 5) - 2;

        for(var i=0; i<this.points.length; i++) {
            var point = this.points[i];

            if(point === null) {
                continue;
            }

            var dx = this.mousePos.x - point.curPos.x;
            var dy = this.mousePos.y - point.curPos.y;
            var dd = (dx * dx) + (dy * dy);
            var d = Math.sqrt(dd);
            if(d < 50) {
                //point.curPos.x = point.originalPos.x + randomNum;
                //point.curPos.y = point.originalPos.y + randomNum;
                this.pointCollectionX = Math.floor(Math.random() * 5) - 2;
                this.pointCollectionY = Math.floor(Math.random() * 5) - 2;
            }
            point.draw(bubbleShape, this.pointCollectionX, this.pointCollectionY);
        }
    }

    this.draw = function (bubbleShape, reset) {
        for (var i = 0; i < this.points.length; i++) {
            var point = this.points[i];

            if (point === null)
                continue;
            
            if (window.reset) {
                this.pointCollectionX = 0
                this.pointCollectionY = 0
                this.mousePos = new Vector(0, 0);
            }

            point.draw(bubbleShape, this.pointCollectionX, this.pointCollectionY, reset);
            //point.draw(bubbleShape);
        }
    }

    this.reset = function(bubbleShape) {

    }
}

function Point(x, y, z, size, color) {
    this.curPos = new Vector(x, y, z);
    this.color = color;

    this.friction = document.Friction;
    this.rotationForce = document.rotationForce;
    this.springStrength = 0.1;

    this.originalPos = new Vector(x, y, z);
    this.radius = size;
    this.size = size;
    this.targetPos = new Vector(x, y, z);
    this.velocity = new Vector(0.0, 0.0, 0.0);

    this.update = function () {
        var dx = this.targetPos.x - this.curPos.x;
        var dy = this.targetPos.y - this.curPos.y;
        // Orthogonal vector is [-dy,dx]
        var ax = dx * this.springStrength - this.rotationForce * dy;
        var ay = dy * this.springStrength + this.rotationForce * dx;

        this.velocity.x += ax;
        this.velocity.x *= this.friction;
        this.curPos.x += this.velocity.x;

        this.velocity.y += ay;
        this.velocity.y *= this.friction;
        this.curPos.y += this.velocity.y;

        var dox = this.originalPos.x - this.curPos.x;
        var doy = this.originalPos.y - this.curPos.y;
        var dd = (dox * dox) + (doy * doy);
        var d = Math.sqrt(dd);

        this.targetPos.z = d / 100 + 1;
        var dz = this.targetPos.z - this.curPos.z;
        var az = dz * this.springStrength;
        this.velocity.z += az;
        this.velocity.z *= this.friction;
        this.curPos.z += this.velocity.z;

        this.radius = this.size * this.curPos.z;
        if (this.radius < 1) this.radius = 1;
    }

    this.draw = function(bubbleShape, dx, dy) {
        ctx.fillStyle = this.color;
        if(bubbleShape == "square") {
            ctx.beginPath();
            ctx.fillRect(this.curPos.x+dx, this.curPos.y+dy, this.radius*1.5, this.radius*1.5);
        }
        else {
            ctx.beginPath();
            ctx.arc(this.curPos.x+dx, this.curPos.y+dy, this.radius, 0, Math.PI * 2, true);
            ctx.fill();
        }
    }
}

var canvas = $("#myCanvas");
var canvasHeight = 500;
var canvasWidth = 1000;
var screenWidth = canvasWidth;
var ctx;
var dt = 0.1;

var pointCollection;

document.rotationForce = 0.0;
document.Friction = 0.85;

/*
// RGB
var white = [255, 255, 255];
var black = [68, 68, 68];
var red = [255, 68, 68];
var orange = [255, 187, 51];
var green = [153, 204, 0];
var blue = [51, 181, 229];
var purple = [170, 102, 204];
*/

// HSL
var white = [0, 0, 100];
var black = [0, 0, 27];
var red = [0, 100, 63];
var orange = [40, 100, 60];
var green = [75, 100, 40];
var blue = [196, 77, 55];
var purple = [280, 50, 60];

var offset = 0;

var mouseX = 0;

function makeColor(hslList, fade) {
    var hue = hslList[0] /*- 17.0 * fade / 1000.0*/;
    var sat = hslList[1] /*+ 81.0 * fade / 1000.0*/;
    var lgt = hslList[2] /*+ 58.0 * fade / 1000.0*/;
    return "hsl("+hue+","+sat+"%,"+lgt+"%)";
}

function phraseToHex(phrase) {
    var hexphrase = "";
    for(var i=0; i<phrase.length; i++) {
        hexphrase += phrase.charCodeAt(i).toString(16);
    }
    return hexphrase;
}

function initEventListeners() {
    $(window).bind('resize', updateCanvasDimensions).bind('mousemove', onMove);

    canvas.ontouchmove = function(e) {
        e.preventDefault();
        onTouchMove(e);
    }

    canvas.ontouchstart = function(e) {
        e.preventDefault();
    }
}

function updateCanvasDimensions() {
    canvas.attr({height: 500, width: 1000});
    canvasWidth = canvas.width();
    canvasHeight = canvas.height();

    draw();
}

function onMove(e) {
    if (pointCollection) {
        pointCollection.mousePos.set(e.pageX, e.pageY);
    }
}

function onTouchMove(e) {
    if (pointCollection) {
        pointCollection.mousePos.set(e.targetTouches[0].pageX, e.targetTouches[0].pageY);
    }
}

function bounceName() {
    shake();
    //update();

    setTimeout(function() { bounceName() }, 30);
}

function stopName() {
    // pass
}

function bounceBubbles() {
    draw();
    update();

    setTimeout(function() { bounceBubbles() }, 30);
}

function stopBubbles() {
    // pass
}

function draw(reset) {
    var tmpCanvas = canvas.get(0);

    if (tmpCanvas.getContext === null) {
        return;
    }

    ctx = tmpCanvas.getContext('2d');
    ctx.clearRect(0, 0, canvasWidth, canvasHeight);

    bubbleShape = typeof bubbleShape !== 'undefined' ? bubbleShape : "circle";

    if (pointCollection) {
        pointCollection.draw(bubbleShape, reset);
    }
}

function shake() {
    var tmpCanvas = canvas.get(0);

    if (tmpCanvas.getContext === null) {
        return;
    }

    ctx = tmpCanvas.getContext('2d');
    ctx.clearRect(0, 0, canvasWidth, canvasHeight);

    bubbleShape = typeof bubbleShape !== 'undefined' ? bubbleShape : "circle";

    if (pointCollection) {
        pointCollection.shake(bubbleShape);
    }
}

function update() {
    if (pointCollection)
        pointCollection.update();
}

$("#myCanvas").keypress(function(event) {
    console.log(e);
});

function drawName(name, letterColors) {
    updateCanvasDimensions();

    var g = []
    var offset = 0;

    function addLetter(cc_hex, ix, letterCols) {
        if(typeof letterCols !== 'undefined') {
            /* letterColors = [red, white, blue] */
            if(Object.prototype.toString.call(letterCols) === '[object Array]' && Object.prototype.toString.call(letterCols[0]) === '[object Array]') {
                letterColors = letterCols;
            }
            /* letterColors = red */
            if(Object.prototype.toString.call(letterCols) === '[object Array]' && typeof letterCols[0] === "number") {
                letterColors = [letterCols];
            }
        }
        else {
            letterColors = [black];
        }

        if (document.alphabet.hasOwnProperty(cc_hex)) {
            var chr_data = document.alphabet[cc_hex].P;
            var bc = letterColors[ix % letterColors.length];

            for (var i=0; i<chr_data.length; ++i) {
                point = chr_data[i];

                g.push(new Point(point[0]+offset,
                point[1],
                0.0,
                point[2],
                makeColor(bc,point[3])));
            }
            offset += document.alphabet[cc_hex].W;
        }
    }

    var hexphrase = phraseToHex(name);

    var col_ix = -1;
    for(var i=0; i<hexphrase.length; i+=2) {
        var cc_hex = "A" + hexphrase.charAt(i) + hexphrase.charAt(i+1);
        if(cc_hex != "A20") {
            col_ix++;
        }
        addLetter(cc_hex, col_ix, letterColors);
    }

    for (var j=0; j<g.length; j++) {
        g[j].curPos.x = (canvasWidth/2 - offset/2) + g[j].curPos.x;
        g[j].curPos.y = (canvasHeight/2 - 180) + g[j].curPos.y;
        g[j].originalPos.x = (canvasWidth/2 - offset/2) + g[j].originalPos.x;
        g[j].originalPos.y = (canvasHeight/2 - 180) + g[j].originalPos.y;
    }

    pointCollection = new PointCollection();
    pointCollection.points = g;
    initEventListeners();
    //timeout();
}

setTimeout(function () {
  updateCanvasDimensions();
}, 30);

window.reset = false;

$(window).mouseleave(function() {
    window.reset = true;
});     
$(window).mouseenter(function() {
    window.reset = false;
}); 