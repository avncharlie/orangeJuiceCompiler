// testing 'this'
var obj = {
    outside() {
        return foo();
    },
    insideProp: function() {
        return this;
    },
    insideMember() {
        return this;
    }
}
function foo () {
	return this;
}

console.log(obj.outside() == globalThis);
console.log(obj.insideProp() == obj);
console.log(obj.insideMember() == obj);


