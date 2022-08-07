var fs = require('fs');
var babel = require('@babel/core');

if(process.argv.length != 4 && process.argv.length != 3) {
    console.log('Usage: node get_ast.js <input.js> [output_file]');
    return;
}

var code_file = process.argv[2];
var out_file = process.argv[3];


function removeASTLocation(b) {
    if (Array.isArray(b)) {
        b.forEach(a => removeASTLocation(a));
    } else if (typeof b === 'object' && b != null) {
        delete b['loc'];
        delete b['start'];
        delete b['end'];
        const values = Object.values(b).filter(v => Array.isArray(v) || typeof v === 'object');
        removeASTLocation(values);
    }
};
    

let ast;

if (process.argv.length == 3) {
    ast = babel.transformFileSync(code_file, {ast: true, babelrc: false, sourceType: 'script'}).ast.program;
    removeASTLocation(ast); // for prettier printing
    console.log(JSON.stringify(ast, null, 2));
} else {
    babel.transformFile(code_file, {ast: true, babelrc: false, sourceType: 'script'}, function(err, result) {
        var ast = result.ast.program;
        let ast_string = JSON.stringify(ast);
        fs.writeFileSync(out_file, ast_string, 'utf-8');
    });
}
