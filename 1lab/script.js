function cost() {
	var result = 0;
	console.log(result);
	if (document.getElementById("1").checked == true) {
		result = result + 17500;
	}
	if (document.getElementById("2").checked == true) {
		result = result + 19000;
	}
	if (document.getElementById("3").checked == true) {
		result = result + 30500;
	}
	if (document.getElementById("4").checked == true) {
		result = result + 4000;
	}
	document.getElementById("result").innerHTML = "Оплата за улуги:"+result;
	console.log(document.getElementById("4").checked, document.getElementById("2").value);
}