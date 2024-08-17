var i = 0;
function move(prog) {
  if (i == 0) {
    i = 1;
    var elem = document.getElementById(prog);
    var width = 10;
    var id = setInterval(frame, 10);
    function frame() {
      if (width >= 100) {
        clearInterval(id);
        i = 0;
      } else {
        width++;
        elem.style.width = width + "%";
        elem.innerHTML = width  + "%";
      }
    }
  }
}