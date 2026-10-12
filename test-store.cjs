const {test}=require('node:test');
const assert=require('node:assert/strict');
const {prepare,filterProducts,sanitizeCart,subtotal}=require('./dist/store-core.js');
const data=[
 {id:'a',name:'Glicinato de Magnesio | Swanson',description:'Contiene: 100 cápsulas\nMarca: Swanson',url:'https://vitashop.com.ar/productos/magnesio/',price:40500,compare:'$0,00',available:true,categories:['Suplementos','Magnesio']},
 {id:'b',name:'Probiótico | Horbaach',description:'Contiene: 60 caps\nMarca: Horbaach',url:'https://vitashop.com.ar/productos/probiotico/',price:38999,compare:'$47.800,00',available:false},
 {id:'c',name:'Vitamina B12 | Now Foods',description:'Marca: Now Foods',url:'https://vitashop.com.ar/productos/vitamina-b12/',price:32000.5,compare:'$40.000,00',available:true}
].map(prepare);
test('precio de comparación cero no crea descuentos; conserva el descuento real',()=>{assert.equal(data[0].oldPrice,null);assert.equal(data[1].oldPrice,47800);assert.equal(data[2].oldPrice,40000);});
test('búsqueda tolera acentos y combina disponibilidad y precio',()=>{assert.deepEqual(filterProducts(data,{query:'probiotico'}).map(p=>p.id),['b']);assert.equal(filterProducts(data,{query:'probiótico',available:true}).length,0);assert.deepEqual(filterProducts(data,{maxPrice:39000,available:true}).map(p=>p.id),['c']);assert.equal(filterProducts(data,{query:'magnesio swanson'})[0].id,'a');});
test('ordenar por precio no altera el orden del catálogo original',()=>{assert.deepEqual(filterProducts(data,{sort:'asc'}).map(p=>p.id),['c','b','a']);assert.deepEqual(data.map(p=>p.id),['a','b','c']);});
test('carrito recuperado elimina productos sin stock, IDs inexistentes y cantidades inválidas',()=>{assert.deepEqual(sanitizeCart({a:2,b:4,unknown:1,c:-3},data),{a:2});assert.deepEqual(sanitizeCart({a:'2.9',c:1000},data),{a:2,c:99});assert.deepEqual(sanitizeCart({a:'NaN'},data),{});assert.deepEqual(sanitizeCart(null,data),{});});
test('subtotal exacto en centavos no incluye productos sin stock ni envíos desconocidos',()=>{assert.equal(subtotal({a:2,c:3,b:7,unknown:1},data),177001.5);assert.equal(subtotal({},data),0);});
